import numpy as np
import ufl
import openmdao.api as om
from dolfinx import fem, la
from mpi4py import MPI
from atomics.pde_problem import PDEProblem


class ScalarOutputsComp(om.ExplicitComponent):
    """
    ScalarOutputsComp wraps up a the scalar output (constraints/objective)
    from a DOLFINx/UFL form.
    Parameters
    ----------
    pde_problem PDEProblem
        PDEProblem is a class containing the mesh and the dictionaries of
        the boundary conditions, inputs, states, and outputs.
    scalar_output_name : str
        the name of the scalar output
    Returns
    -------
    outputs[scalar_output_name] numpy array   
        The assembled scalar output.
    """

    def initialize(self):
        self.options.declare('pde_problem', types=PDEProblem)
        self.options.declare('scalar_output_name', types=str)

    def setup(self):
        pde_problem = self.options['pde_problem']
        scalar_output_name = self.options['scalar_output_name']

        scalar_output = pde_problem.scalar_outputs_dict[scalar_output_name]
        ufl_form = scalar_output['form']

        self.argument_functions_dict = {}
        self._argument_layouts = {}
        self._derivative_forms = {}

        for argument_name in scalar_output['arguments']:
            if argument_name in pde_problem.inputs_dict:
                argument_function = \
                    pde_problem.inputs_dict[argument_name]['function']
            elif argument_name in pde_problem.states_dict:
                argument_function = \
                    pde_problem.states_dict[argument_name]['function']
            else:
                raise KeyError(
                    "Scalar output {!r} references unknown argument {!r}."
                    .format(scalar_output_name, argument_name)
                )

            self.argument_functions_dict[argument_name] = argument_function

        # Obtain the communicator from one of the coefficient functions. For
        # an argument-free functional, obtain it from the UFL integration
        # domain.
        if self.argument_functions_dict:
            first_function = next(
                iter(self.argument_functions_dict.values())
            )
            self.comm = first_function.function_space.mesh.comm
        else:
            domain = ufl_form.ufl_domain()
            mesh = domain.ufl_cargo()
            if mesh is None:
                raise RuntimeError(
                    "Cannot determine the communicator for scalar output "
                    "{!r}.".format(scalar_output_name)
                )
            self.comm = mesh.comm

        for argument_name, argument_function in \
                self.argument_functions_dict.items():
            function_space = argument_function.function_space
            index_map = function_space.dofmap.index_map
            block_size = function_space.dofmap.index_map_bs

            function_comm = function_space.mesh.comm
            comm_relation = MPI.Comm.Compare(self.comm, function_comm)
            if comm_relation not in (MPI.IDENT, MPI.CONGRUENT):
                raise ValueError(
                    "All arguments of scalar output {!r} must use compatible "
                    "MPI communicators.".format(scalar_output_name)
                )

            owned_blocks = index_map.size_local
            owned_size = owned_blocks * block_size
            global_size = index_map.size_global * block_size

            # DOLFINx IndexMap global indices refer to blocks. Expand them
            # into scalar indices so they match Function.x.array ordering.
            global_blocks = index_map.local_to_global(
                np.arange(owned_blocks, dtype=np.int32)
            )
            owned_global_dofs = (
                block_size * global_blocks[:, None]
                + np.arange(block_size, dtype=np.int64)[None, :]
            ).reshape(-1)

            self._argument_layouts[argument_name] = {
                'owned_size': owned_size,
                'global_size': global_size,
                'owned_global_dofs': owned_global_dofs,
            }

            # Retain globally sized, replicated OpenMDAO inputs. This
            # preserves the interface of the legacy FunctionSpace.dim()
            # implementation and permits dense compute_partials().
            self.add_input(argument_name, shape=global_size)

            derivative_ufl = ufl.derivative(
                ufl_form,
                argument_function,
            )
            self._derivative_forms[argument_name] = fem.form(
                derivative_ufl
            )

        self.add_output(scalar_output_name)
        self.declare_partials(scalar_output_name, '*')

        # Compile the scalar functional once rather than JIT-compiling it on
        # every call to compute().
        self._scalar_form = fem.form(ufl_form)

    def _set_values(self, inputs):
        for argument_name, argument_function in \
                self.argument_functions_dict.items():
            layout = self._argument_layouts[argument_name]
            owned_size = layout['owned_size']
            owned_global_dofs = layout['owned_global_dofs']

            # Set owned entries from the replicated global OpenMDAO vector.
            argument_function.x.array[:owned_size] = (
                np.asarray(inputs[argument_name])[owned_global_dofs]
            )

            # Populate ghost entries required during form assembly.
            argument_function.x.scatter_forward()
              
    def compute(self, inputs, outputs):
        scalar_output_name = self.options['scalar_output_name']

        self._set_values(inputs)

        # DOLFINx assemble_scalar returns the contribution from this MPI
        # rank, so explicitly sum the functional over all ranks.
        local_value = fem.assemble_scalar(self._scalar_form)
        global_value = self.comm.allreduce(local_value, op=MPI.SUM)

        outputs[scalar_output_name] = global_value

    def compute_derivative(self, argument_name):
        derivative_vector = fem.assemble_vector(
            self._derivative_forms[argument_name]
        )

        # Accumulate element contributions held on ghost degrees of freedom
        # back to the owning MPI rank.
        derivative_vector.scatter_reverse(la.InsertMode.add)

        layout = self._argument_layouts[argument_name]
        owned_size = layout['owned_size']
        global_size = layout['global_size']
        owned_global_dofs = layout['owned_global_dofs']

        # Convert the distributed DOLFINx gradient into the globally sized,
        # replicated gradient expected by the OpenMDAO input.
        local_gradient = np.zeros(
            global_size,
            dtype=derivative_vector.array.dtype,
        )
        local_gradient[owned_global_dofs] = \
            derivative_vector.array[:owned_size]

        global_gradient = np.zeros_like(local_gradient)
        self.comm.Allreduce(
            local_gradient,
            global_gradient,
            op=MPI.SUM,
        )

        return global_gradient

    def compute_partials(self, inputs, partials):
        self._set_values(inputs)

        scalar_output_name = self.options['scalar_output_name']

        for argument_name in self.argument_functions_dict:
            derivative_numpy = self.compute_derivative(argument_name)
            partials[scalar_output_name, argument_name][0, :] = \
                derivative_numpy
