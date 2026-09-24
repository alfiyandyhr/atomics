import numpy as np
import ufl
from scipy.sparse import coo_matrix
import openmdao.api as om
from dolfinx import fem, la
import dolfinx.fem.petsc as fem_petsc
from mpi4py import MPI
from atomics.pde_problem import PDEProblem


class FieldOutputsComp(om.ExplicitComponent):
    """
    FieldOutputsComp wraps up a the field (a scalar on each element) output 
    (used as constraints/objective) from a DOLFINx/UFL linear form.

    Parameters
    ----------
    pde_problem   PDEProblem
        PDEProblem is a class containing the dictionaries of
        the boundary conditions, inputs, states, and outputs.
    field_output_name : str
        the name of the field output
    Returns
    -------
    outputs[field_output_name] numpy array
    """

    def initialize(self):
        self.options.declare('pde_problem', types=PDEProblem)
        self.options.declare('field_output_name', types=str)

    def setup(self):
        pde_problem = self.options['pde_problem']
        field_output_name = self.options['field_output_name']
        field_output = pde_problem.field_outputs_dict[field_output_name]
        ufl_form = field_output['form']

        # The field output must be represented by a rank-one UFL form.
        self._field_form = fem.form(ufl_form)
        if self._field_form.rank != 1:
            raise ValueError(
                "Field output {!r} must be defined by a rank-one UFL form; "
                "got form rank {}.".format(
                    field_output_name,
                    self._field_form.rank,
                )
            )

        self._field_space = self._field_form.function_spaces[0]
        self.comm = self._field_space.mesh.comm
        self._field_layout = self._build_layout(self._field_space)

        self.argument_functions_dict = {}
        self._argument_layouts = {}
        self._derivative_forms = {}
        self._derivative_sparsity = {}

        for argument_name in field_output['arguments']:
            if argument_name in pde_problem.inputs_dict:
                argument_function = \
                    pde_problem.inputs_dict[argument_name]['function']
            elif argument_name in pde_problem.states_dict:
                argument_function = \
                    pde_problem.states_dict[argument_name]['function']
            else:
                raise KeyError(
                    "Field output {!r} references unknown argument {!r}."
                    .format(field_output_name, argument_name)
                )

            function_comm = argument_function.function_space.mesh.comm
            comm_relation = MPI.Comm.Compare(self.comm, function_comm)
            if comm_relation not in (MPI.IDENT, MPI.CONGRUENT):
                raise ValueError(
                    "Argument {!r} and field output {!r} must use "
                    "compatible MPI communicators.".format(
                        argument_name,
                        field_output_name,
                    )
                )

            self.argument_functions_dict[argument_name] = argument_function
            self._argument_layouts[argument_name] = self._build_layout(
                argument_function.function_space
            )

            self.add_input(
                argument_name,
                shape=self._argument_layouts[argument_name]['global_size'],
            )

            trial_function = ufl.TrialFunction(
                argument_function.function_space
            )
            derivative_ufl = ufl.derivative(
                ufl_form,
                argument_function,
                trial_function,
            )
            self._derivative_forms[argument_name] = fem.form(
                derivative_ufl
            )

        # Retain a globally sized, replicated OpenMDAO output. In serial this
        # has the same size and ordering as the legacy assembled vector.
        self.add_output(
            field_output_name,
            shape=self._field_layout['global_size'],
        )

        # Determine and declare the sparse Jacobian pattern.
        for argument_name in self.argument_functions_dict:
            derivative_coo = self.compute_derivative(argument_name)

            expected_shape = (
                self._field_layout['global_size'],
                self._argument_layouts[argument_name]['global_size'],
            )
            if derivative_coo.shape != expected_shape:
                raise RuntimeError(
                    "Derivative of field output {!r} with respect to {!r} "
                    "has shape {}, expected {}.".format(
                        field_output_name,
                        argument_name,
                        derivative_coo.shape,
                        expected_shape,
                    )
                )

            rows = derivative_coo.row.copy()
            cols = derivative_coo.col.copy()
            self._derivative_sparsity[argument_name] = (rows, cols)

            self.declare_partials(
                field_output_name,
                argument_name,
                rows=rows,
                cols=cols,
            )

    @staticmethod
    def _build_layout(function_space):
        """Build global scalar-DOF indices for locally owned values."""
        index_map = function_space.dofmap.index_map
        block_size = function_space.dofmap.index_map_bs

        owned_blocks = index_map.size_local
        owned_size = owned_blocks * block_size
        global_size = index_map.size_global * block_size

        # IndexMap indices refer to blocks. Expand each block index into
        # scalar indices matching Function.x.array ordering.
        global_blocks = index_map.local_to_global(
            np.arange(owned_blocks, dtype=np.int32)
        )
        owned_global_dofs = (
            block_size * global_blocks[:, None]
            + np.arange(block_size, dtype=np.int64)[None, :]
        ).reshape(-1)

        return {
            'owned_size': owned_size,
            'global_size': global_size,
            'owned_global_dofs': owned_global_dofs,
        }

    def _matrix_to_global_coo(self, matrix):
        """Convert a distributed PETSc matrix to replicated global COO."""
        indptr, local_cols, local_data = matrix.getValuesCSR()
        row_start, row_end = matrix.getOwnershipRange()

        indptr = np.asarray(indptr, dtype=np.int64)
        local_cols = np.asarray(local_cols, dtype=np.int64).copy()
        local_data = np.asarray(local_data).copy()

        local_rows = np.repeat(
            np.arange(row_start, row_end, dtype=np.int64),
            np.diff(indptr),
        )

        # Each rank owns a unique range of matrix rows. Replicate all sparse
        # entries so each OpenMDAO process sees the same Jacobian structure
        # and values.
        gathered = self.comm.allgather(
            (local_rows, local_cols, local_data)
        )

        rows = np.concatenate([entry[0] for entry in gathered])
        cols = np.concatenate([entry[1] for entry in gathered])
        data = np.concatenate([entry[2] for entry in gathered])

        # Keep the ordering deterministic between setup() and subsequent
        # compute_partials() calls.
        order = np.lexsort((cols, rows))
        rows = rows[order]
        cols = cols[order]
        data = data[order]

        matrix_shape = tuple(int(size) for size in matrix.getSize())
        return coo_matrix(
            (data, (rows, cols)),
            shape=matrix_shape,
        )

    def compute_derivative(self, argument_name):
        """Assemble a field-output Jacobian as a replicated COO matrix."""
        derivative_matrix = fem_petsc.assemble_matrix(
            self._derivative_forms[argument_name],
        )

        try:
            # fem.petsc.assemble_matrix does not finalize the PETSc matrix.
            derivative_matrix.assemble()
            return self._matrix_to_global_coo(derivative_matrix)
        finally:
            # PETSc objects returned by DOLFINx should be destroyed
            # collectively when they are no longer needed.
            derivative_matrix.destroy()

    def _set_values(self, inputs):
        for argument_name, argument_function in \
                self.argument_functions_dict.items():
            layout = self._argument_layouts[argument_name]

            owned_size = layout['owned_size']
            owned_global_dofs = layout['owned_global_dofs']

            # OpenMDAO stores a replicated global vector, whereas DOLFINx
            # stores owned values followed by ghost values on each rank.
            argument_function.x.array[:owned_size] = (
                np.asarray(inputs[argument_name])[owned_global_dofs]
            )

            # Update ghost entries before evaluating or differentiating forms.
            argument_function.x.scatter_forward()

    def compute(self, inputs, outputs):
        field_output_name = self.options['field_output_name']

        self._set_values(inputs)

        field_vector = fem.assemble_vector(self._field_form)

        # Accumulate contributions assembled into ghost degrees of freedom
        # back to their owning MPI ranks.
        field_vector.scatter_reverse(la.InsertMode.add)

        layout = self._field_layout
        owned_size = layout['owned_size']
        owned_global_dofs = layout['owned_global_dofs']

        local_field = np.zeros(
            layout['global_size'],
            dtype=field_vector.array.dtype,
        )
        local_field[owned_global_dofs] = \
            field_vector.array[:owned_size]

        global_field = np.zeros_like(local_field)
        self.comm.Allreduce(
            local_field,
            global_field,
            op=MPI.SUM,
        )

        outputs[field_output_name] = global_field

    def compute_partials(self, inputs, partials):
        field_output_name = self.options['field_output_name']
        self._set_values(inputs)

        for argument_name in self.argument_functions_dict:
            derivative_coo = self.compute_derivative(argument_name)
            expected_rows, expected_cols = \
                self._derivative_sparsity[argument_name]

            # OpenMDAO requires the values to remain aligned with the sparse
            # row/column pattern declared during setup().
            if (
                not np.array_equal(derivative_coo.row, expected_rows)
                or not np.array_equal(derivative_coo.col, expected_cols)
            ):
                raise RuntimeError(
                    "The Jacobian sparsity pattern for field output {!r} "
                    "with respect to {!r} changed after setup().".format(
                        field_output_name,
                        argument_name,
                    )
                )

            partials[field_output_name, argument_name] = \
                derivative_coo.data
