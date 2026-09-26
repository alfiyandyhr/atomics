from pathlib import Path
import numpy as np
import ufl
from scipy.sparse import csr_matrix, coo_matrix
from scipy.sparse.linalg import splu
import scipy.sparse.linalg as splinalg
from petsc4py import PETSc
from mpi4py import MPI
import openmdao.api as om
from atomics.pde_problem import PDEProblem
from dolfinx import fem, io
from dolfinx.fem import petsc as fem_petsc


class StatesComp(om.ImplicitComponent):
    """
    StatesComp is a OpenMDAO  implicit component, which wraps the FEniCS PDE solver.
    The total derivatives are also calculated in StatesComp.
    problem.
    The users do not need to modify StatesComp ideally. 
    The same settings can be modified in AtomicsGroup() 
    from the run file.
    Parameters
    ----------
    ``linear_solver_`` solver for the total derivatives
    values=['fenics_direct', 'scipy_splu', 'fenics_krylov', 'petsc_gmres_ilu', 'scipy_cg','petsc_cg_ilu']
    ``problem_type`` solver for the FEA problem
    values=['linear_problem', 'nonlinear_problem', 'nonlinear_problem_load_stepping']
    ``visualization`` whether to save the iteration histories
    values=['True', 'False'],
    Returns
    -------
    outputs['state_name'] : numpy array
        states
    """

    def initialize(self):
        self.options.declare('pde_problem', types=PDEProblem)
        self.options.declare('state_name', types=str)
        self.options.declare(
            'linear_solver_',
            default='petsc_cg_gamg',
            values=[
                'fenics_direct',
                'scipy_splu',
                'fenics_krylov',
                'petsc_gmres_ilu',
                'petsc_gmres_bjacobi',
                'scipy_cg',
                'petsc_cg_ilu',
                'petsc_cg_gamg',
            ],
        )
        self.options.declare(
            'problem_type', default='nonlinear_problem', 
            values=['linear_problem', 'nonlinear_problem', 'nonlinear_problem_load_stepping'],
        )
        self.options.declare(
            'visualization', default='True', 
            values=['True', 'False'],
        )
        self.options.declare(
            'num_load_steps', default=8, types=int,
        )
        self.options.declare(
            'fail_on_nonconvergence', default=True, types=bool,
        )

    def setup(self):
        pde_problem = self.options['pde_problem']
        state_name = self.options['state_name']

        state_function = pde_problem.states_dict[state_name]['function']
        self.comm = state_function.function_space.mesh.comm
        self._state_layout = self._build_layout(
            state_function.function_space
        )

        self.itr = 0
        self.argument_functions_dict = argument_functions_dict = dict()
        self._argument_layouts = {}
        self._derivative_sparsity = {}

        for argument_name in pde_problem.states_dict[state_name]['arguments']:
            argument_function = \
                pde_problem.inputs_dict[argument_name]['function']

            function_comm = argument_function.function_space.mesh.comm
            comm_relation = MPI.Comm.Compare(
                self.comm,
                function_comm,
            )
            if comm_relation not in (MPI.IDENT, MPI.CONGRUENT):
                raise ValueError(
                    "State {!r} and argument {!r} must use compatible "
                    "MPI communicators.".format(
                        state_name,
                        argument_name,
                    )
                )

            argument_functions_dict[argument_name] = argument_function
            self._argument_layouts[argument_name] = self._build_layout(
                argument_function.function_space
            )

        for argument_name, argument_function in self.argument_functions_dict.items():
            self.add_input(
                argument_name,
                shape=self._argument_layouts[
                    argument_name
                ]['global_size'],
            )

        self.add_output(
            state_name,
            # OpenMDAO otherwise initializes outputs to one. A zero
            # displacement is the appropriate first Newton/SNES guess for
            # mechanics problems, while subsequent evaluations retain the
            # preceding converged solution as a warm start.
            val=np.zeros(self._state_layout['global_size']),
            shape=self._state_layout['global_size'],
        )

        derivative_functions = {
            state_name: state_function,
            **self.argument_functions_dict,
        }

        for argument_name, argument_function in \
                derivative_functions.items():
            derivative_coo = self.compute_derivative(
                state_name,
                argument_function,
            )

            expected_shape = (
                self._state_layout['global_size'],
                (
                    self._state_layout['global_size']
                    if argument_name == state_name
                    else self._argument_layouts[
                        argument_name
                    ]['global_size']
                ),
            )

            if derivative_coo.shape != expected_shape:
                raise RuntimeError(
                    "Derivative of state {!r} with respect to {!r} "
                    "has shape {}, expected {}.".format(
                        state_name,
                        argument_name,
                        derivative_coo.shape,
                        expected_shape,
                    )
                )

            rows = derivative_coo.row.copy()
            cols = derivative_coo.col.copy()
            self._derivative_sparsity[argument_name] = (
                rows,
                cols,
            )

            self.declare_partials(
                state_name,
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

    @staticmethod
    def _derivative_form(residual_form, argument_function):
        """Construct a UFL Gateaux derivative with an explicit direction."""
        direction = ufl.TrialFunction(argument_function.function_space)
        return ufl.derivative(
            residual_form,
            argument_function,
            direction,
        )

    def _petsc_to_scipy(self, matrix):
        """Copy a serial PETSc AIJ matrix into a SciPy CSR matrix."""
        if self.comm.size != 1:
            raise RuntimeError(
                "SciPy linear solvers are only available in serial. "
                "Use a PETSc solver for MPI execution."
            )

        indptr, indices, data = matrix.getValuesCSR()
        return csr_matrix(
            (
                np.asarray(data).copy(),
                np.asarray(indices).copy(),
                np.asarray(indptr).copy(),
            ),
            shape=matrix.getSize(),
        )

    def _matrix_to_global_coo(self, matrix):
        """Convert distributed PETSc matrix rows to replicated global COO."""
        indptr, local_cols, local_data = matrix.getValuesCSR()
        row_start, row_end = matrix.getOwnershipRange()

        indptr = np.asarray(indptr, dtype=np.int64)
        local_cols = np.asarray(local_cols, dtype=np.int64).copy()
        local_data = np.asarray(local_data).copy()

        local_rows = np.repeat(
            np.arange(row_start, row_end, dtype=np.int64),
            np.diff(indptr),
        )

        gathered = self.comm.allgather(
            (local_rows, local_cols, local_data)
        )

        rows = np.concatenate([entry[0] for entry in gathered])
        cols = np.concatenate([entry[1] for entry in gathered])
        data = np.concatenate([entry[2] for entry in gathered])

        # Keep setup() and linearize() ordering identical.
        order = np.lexsort((cols, rows))
        rows = rows[order]
        cols = cols[order]
        data = data[order]

        return coo_matrix(
            (data, (rows, cols)),
            shape=tuple(int(size) for size in matrix.getSize()),
        )

    def _function_to_global(self, function, layout):
        """Convert a distributed DOLFINx Function to a replicated array."""
        local_values = np.zeros(
            layout['global_size'],
            dtype=function.x.array.dtype,
        )
        local_values[layout['owned_global_dofs']] = \
            function.x.array[:layout['owned_size']]

        global_values = np.zeros_like(local_values)
        self.comm.Allreduce(
            local_values,
            global_values,
            op=MPI.SUM,
        )
        return global_values

    def _global_to_petsc_vector(self, values, vector):
        """Copy a replicated global array into locally owned PETSc entries."""
        values = np.asarray(values)
        start, end = vector.getOwnershipRange()

        local_array = vector.getArray()
        local_array[:] = 0.0
        local_array[:end - start] = values[start:end]

    def _petsc_vector_to_global(self, vector):
        """Convert a distributed PETSc vector to a replicated array."""
        start, end = vector.getOwnershipRange()

        local_values = np.zeros(
            vector.getSize(),
            dtype=PETSc.ScalarType,
        )
        local_array = vector.getArray(readonly=True)
        local_values[start:end] = local_array[:end - start]

        global_values = np.zeros_like(local_values)
        self.comm.Allreduce(
            local_values,
            global_values,
            op=MPI.SUM,
        )
        return global_values

    def _boundary_conditions(self):
        pde_problem = self.options['pde_problem']
        state_name = self.options['state_name']

        # Preserve the special treatment of the variational density filter.
        if state_name == 'density':
            return []

        return list(getattr(pde_problem, 'bcs_list', []))

    def compute_derivative(self, arg_name, arg_function):
        pde_problem = self.options['pde_problem']
        state_name = self.options['state_name']

        residual_form = pde_problem.states_dict[state_name]['residual_form']

        derivative_form = self._derivative_form(
            residual_form,
            arg_function,
        )

        # Applying the state BCs zeros constrained residual rows. For
        # dR/dstate, the constrained diagonal is set to one.
        matrix = fem_petsc.assemble_matrix(
            fem.form(derivative_form),
            bcs=self._boundary_conditions(),
        )
        matrix.assemble()

        try:
            derivative_coo = self._matrix_to_global_coo(matrix)
        finally:
            matrix.destroy()

        return derivative_coo

    def _set_values(self, inputs, outputs):
        pde_problem = self.options['pde_problem']
        state_name = self.options['state_name']
        state_function = pde_problem.states_dict[state_name]['function']

        state_function.x.array[:self._state_layout['owned_size']] = (
            np.asarray(outputs[state_name])[
                self._state_layout['owned_global_dofs']
            ]
        )
        state_function.x.scatter_forward()

        for argument_name, argument_function in self.argument_functions_dict.items():
            layout = self._argument_layouts[argument_name]
            argument_function.x.array[:layout['owned_size']] = (
                np.asarray(inputs[argument_name])[
                    layout['owned_global_dofs']
                ]
            )
            argument_function.x.scatter_forward()

    def apply_nonlinear(self, inputs, outputs, residuals):
        pde_problem = self.options['pde_problem']
        state_name = self.options['state_name']

        residual_form = pde_problem.states_dict[state_name]['residual_form']
        state_function = \
            pde_problem.states_dict[state_name]['function']

        self._set_values(inputs, outputs)

        derivative_form = self._derivative_form(
            residual_form,
            state_function,
        )
        problem = fem_petsc.NonlinearProblem(
            residual_form,
            state_function,
            bcs=self._boundary_conditions(),
            J=derivative_form,
        )

        residual_vector = fem_petsc.create_vector(problem.L)

        try:
            problem.form(state_function.x.petsc_vec)
            problem.F(
                state_function.x.petsc_vec,
                residual_vector,
            )
            residuals[state_name] = \
                self._petsc_vector_to_global(residual_vector)
        finally:
            residual_vector.destroy()

    def _solve_residual(self, residual_form, state_function, options_prefix, options):
        """
        Solve a residual equation with PETSc SNES.

        DOLFINx 0.9 NonlinearProblem provides residual and Jacobian
        assembly callbacks, but it does not construct or run SNES.
        Therefore, create and configure SNES explicitly.
        """
        derivative_form = self._derivative_form(
            residual_form,
            state_function,
        )
        self.derivative_form = derivative_form

        problem = fem_petsc.NonlinearProblem(
            residual_form,
            state_function,
            bcs=self._boundary_conditions(),
            J=derivative_form,
        )

        residual_vector = fem_petsc.create_vector(problem.L)
        jacobian_matrix = fem_petsc.create_matrix(problem.a)

        # Keep the SNES solution vector separate from the DOLFINx
        # Function vector. During a line search, PETSc may evaluate the
        # residual at a temporary trial vector. The UFL forms, however,
        # evaluate state_function, so every trial vector must first be
        # copied into state_function.
        state_vector = state_function.x.petsc_vec
        solution_vector = state_vector.copy()

        snes = PETSc.SNES().create(
            state_function.function_space.mesh.comm
        )

        def update_state(x):
            """Copy the current SNES iterate into state_function."""
            # Synchronize ghost entries of the SNES trial vector.
            problem.form(x)

            # Copy the current trial values into the Function used as
            # the coefficient in the residual and Jacobian forms.
            x.copy(state_vector)
            state_function.x.scatter_forward()

        def assemble_residual(_snes, x, b):
            update_state(x)
            problem.F(x, b)

        def assemble_jacobian(_snes, x, A, P):
            update_state(x)
            problem.J(x, A)

            if P.handle != A.handle:
                problem.J(x, P)

        try:
            snes.setOptionsPrefix(options_prefix)
            snes.setFunction(
                assemble_residual,
                residual_vector,
            )
            snes.setJacobian(
                assemble_jacobian,
                jacobian_matrix,
                jacobian_matrix,
            )

            # Insert the supplied options into PETSc's options database
            # under this solve's unique prefix.
            petsc_options = PETSc.Options()
            petsc_options.prefixPush(options_prefix)
            try:
                for key, value in options.items():
                    petsc_options[key] = value
            finally:
                petsc_options.prefixPop()

            snes.setFromOptions()

            # Solve using a vector that is independent of the DOLFINx
            # Function vector. The callbacks synchronize the Function
            # for every SNES/line-search evaluation.
            snes.solve(
                None,
                solution_vector,
            )

            # Transfer the final accepted SNES solution back to the
            # DOLFINx Function.
            update_state(solution_vector)

            converged_reason = snes.getConvergedReason()
            residual_norm = snes.getFunctionNorm()
            if converged_reason < 0:
                message = (
                    "PETSc SNES did not converge for state "
                    f"'{self.options['state_name']}'. "
                    f"Converged reason: {converged_reason}; "
                    f"residual norm: {residual_norm:.6e}."
                )

                if self.options['fail_on_nonconvergence']:
                    raise RuntimeError(message)

                print("Warning: " + message)
        finally:
            snes.destroy()
            solution_vector.destroy()
            jacobian_matrix.destroy()
            residual_vector.destroy()

    @staticmethod
    def _write_function(filename, function, time):
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)

        writer = io.VTKFile(
            function.function_space.mesh.comm,
            str(filename),
            "w",
        )
        try:
            writer.write_function(function, float(time))
        finally:
            writer.close()

    def _write_visualization(self, state_function):
        output_directory = Path("solutions_iterations_40ramp")
        output_directory.mkdir(parents=True, exist_ok=True)

        for argument_name, argument_function in self.argument_functions_dict.items():
            output_function = argument_function

            if argument_name == 'density':
                V = argument_function.function_space
                output_function = fem.Function(V)
                output_function.name = argument_name

                density_expression = (
                    argument_function
                    / (1.0 + 8.0 * (1.0 - argument_function))
                )
                interpolant = fem.Expression(
                    density_expression,
                    V.element.interpolation_points(),
                )
                output_function.interpolate(interpolant)
                output_function.x.scatter_forward()

            self._write_function(
                output_directory / f"{argument_name}_{self.itr}.pvd",
                output_function,
                self.itr,
            )

        self._write_function(
            output_directory
            / f"{self.options['state_name']}_{self.itr}.pvd",
            state_function,
            self.itr,
        )

    def solve_nonlinear(self, inputs, outputs):
        pde_problem = self.options['pde_problem']
        state_name = self.options['state_name']
        problem_type = self.options['problem_type']
        visualization = self.options['visualization']

        state_data = pde_problem.states_dict[state_name]
        state_function = state_data['function']
        residual_form = state_data['residual_form']

        self.itr += 1
        self._set_values(inputs, outputs)

        options_prefix = f"atomics_{state_name}_{self.itr}_"

        if problem_type == 'linear_problem':
            if state_name == 'density':
                print('this is a variational density filter')

            # SNES KSPONLY performs one Newton step. For a linear residual,
            # this is the complete linear solve.
            self._solve_residual(
                residual_form,
                state_function,
                options_prefix,
                {
                    "snes_type": "ksponly",
                    "snes_max_it": 1,
                    "snes_error_if_not_converged": False,
                    "ksp_type": "preonly",
                    "pc_type": "lu",
                    "pc_factor_mat_solver_type": "mumps",
                    "ksp_error_if_not_converged": False,
                },
            )

        elif problem_type == 'nonlinear_problem':

            # Keep the state supplied by OpenMDAO as a warm start. During
            # optimization this is normally the preceding converged state.

            self._solve_residual(
                residual_form,
                state_function,
                options_prefix,
                {
                    "snes_type": "newtonls",
                    "snes_linesearch_type": "bt",
                    "snes_max_it": 100,
                    "snes_rtol": 1.0e-8,
                    "snes_atol": 1.0e-10,
                    "snes_stol": 1.0e-12,
                    "snes_error_if_not_converged": False,
                    "ksp_type": "preonly",
                    "pc_type": "lu",
                    "pc_factor_mat_solver_type": "mumps",
                    "ksp_error_if_not_converged": False,
                },
            )

        elif problem_type == 'nonlinear_problem_load_stepping':
            state_function.x.array[:] = 0.0
            state_function.x.scatter_forward()

            num_steps = self.options['num_load_steps']
            if num_steps < 1:
                raise ValueError(
                    "num_load_steps must be at least one."
                )

            # The original load-stepping implementation called an
            # application-specific get_residual_form function and used an
            # undefined tractionBC variable. Store a closure/factory in the
            # state entry instead:
            #
            # states_dict[state_name]["load_step_residual_form"] =
            #     lambda load_factor, final_step: ...
            residual_factory = state_data.get(
                'load_step_residual_form'
            )

            if residual_factory is None:
                raise RuntimeError(
                    "nonlinear_problem_load_stepping requires "
                    "states_dict[state_name]['load_step_residual_form']. "
                    "The callable must accept (load_factor, final_step) "
                    "and return a UFL residual form."
                )

            for step in range(num_steps):
                load_factor = float(step + 1) / float(num_steps)
                final_step = step == num_steps - 1
                step_residual = residual_factory(
                    load_factor,
                    final_step,
                )

                self._solve_residual(
                    step_residual,
                    state_function,
                    f"{options_prefix}step_{step}_",
                    {
                        "snes_type": "newtonls",
                        "snes_linesearch_type": "bt",
                        "snes_max_it": 100,
                        "snes_rtol": 1.0e-8,
                        "snes_atol": 1.0e-10,
                        "snes_stol": 1.0e-12,
                        "snes_error_if_not_converged": False,
                        "ksp_type": "preonly",
                        "pc_type": "lu",
                        "pc_factor_mat_solver_type": "mumps",
                        "ksp_error_if_not_converged": False,
                    },
                )

        if visualization == 'True' and self.itr % 50 == 0:
            self._write_visualization(state_function)

        outputs[state_name] = self._function_to_global(
            state_function,
            self._state_layout,
        )

    def linearize(self, inputs, outputs, partials):
        pde_problem = self.options['pde_problem']
        state_name = self.options['state_name']

        state_function = pde_problem.states_dict[state_name]['function']
        residual_form = pde_problem.states_dict[state_name]['residual_form']

        self._set_values(inputs, outputs)

        derivative_functions = {
            state_name: state_function,
            **self.argument_functions_dict,
        }

        for argument_name, argument_function in \
                derivative_functions.items():
            derivative_coo = self.compute_derivative(
                state_name,
                argument_function,
            )

            expected_rows, expected_cols = \
                self._derivative_sparsity[argument_name]

            if (
                not np.array_equal(
                    derivative_coo.row,
                    expected_rows,
                )
                or not np.array_equal(
                    derivative_coo.col,
                    expected_cols,
                )
            ):
                raise RuntimeError(
                    "The Jacobian sparsity pattern for state {!r} "
                    "with respect to {!r} changed after setup()."
                    .format(state_name, argument_name)
                )

            partials[state_name, argument_name] = \
                derivative_coo.data

    def _assemble_linearized_matrix(self):
        pde_problem = self.options['pde_problem']
        state_name = self.options['state_name']

        state_function = pde_problem.states_dict[state_name]['function']
        residual_form = pde_problem.states_dict[state_name]['residual_form']

        self.derivative_form = self._derivative_form(
            residual_form,
            state_function,
        )

        matrix = fem_petsc.assemble_matrix(
            fem.form(self.derivative_form),
            bcs=self._boundary_conditions(),
        )
        matrix.assemble()
        return matrix

    def solve_linear(self, d_outputs, d_residuals, mode):
        linear_solver_ = self.options['linear_solver_']
        state_name = self.options['state_name']

        if mode not in ('fwd', 'rev'):
            raise ValueError(f"Unsupported OpenMDAO derivative mode: {mode}")

        matrix = self._assemble_linearized_matrix()

        if mode == 'fwd':
            rhs = np.asarray(
                d_residuals[state_name],
                dtype=PETSc.ScalarType,
            )
        else:
            rhs = np.asarray(
                d_outputs[state_name],
                dtype=PETSc.ScalarType,
            )

        try:
            if linear_solver_ in ('scipy_splu', 'scipy_cg'):
                if self.comm.size != 1:
                    raise RuntimeError(
                        "{} is a serial solver. Use fenics_direct or "
                        "one of the PETSc solvers for MPI execution."
                        .format(linear_solver_)
                    )

                scipy_matrix = self._petsc_to_scipy(matrix)

                if mode == 'rev':
                    scipy_operator = scipy_matrix.transpose().tocsr()
                else:
                    scipy_operator = scipy_matrix

                if linear_solver_ == 'scipy_splu':
                    factorization = splu(scipy_operator.tocsc())
                    solution = factorization.solve(rhs)
                else:
                    solution, info = splinalg.cg(
                        scipy_operator,
                        rhs,
                        rtol=1.0e-8,
                        atol=0.0,
                        maxiter=1_000_000,
                    )
                    if info != 0:
                        raise RuntimeError(
                            "SciPy CG failed to converge; "
                            f"solver info={info}"
                        )

            else:
                ksp = PETSc.KSP().create(matrix.comm)

                if mode == 'fwd':
                    input_vector = matrix.createVecLeft()
                    solution_vector = matrix.createVecRight()
                else:
                    # A^T maps the residual-space vector to the
                    # state-space vector.
                    input_vector = matrix.createVecRight()
                    solution_vector = matrix.createVecLeft()

                try:
                    self._global_to_petsc_vector(
                        rhs,
                        input_vector,
                    )
                    solution_vector.set(0.0)

                    ksp.setOperators(matrix)
                    ksp.setOptionsPrefix(
                        "atomics_linear_{}_".format(state_name)
                    )
                    pc = ksp.getPC()

                    if linear_solver_ == 'fenics_direct':
                        ksp.setType('preonly')
                        pc.setType('lu')
                        pc.setFactorSolverType('mumps')

                    elif linear_solver_ in (
                        'fenics_krylov',
                        'petsc_gmres_ilu',
                        'petsc_gmres_bjacobi',
                    ):
                        ksp.setType('gmres')

                        if (
                            self.comm.size == 1
                            and linear_solver_
                            != 'petsc_gmres_bjacobi'
                        ):
                            pc.setType('ilu')
                        else:
                            # Parallel ILU is used through one block per
                            # MPI process rather than PCILU on MPIAIJ.
                            pc.setType('bjacobi')

                        ksp.setTolerances(
                            rtol=1.0e-10,
                            max_it=1_000_000,
                        )

                    elif linear_solver_ in (
                        'petsc_cg_ilu',
                        'petsc_cg_gamg',
                    ):
                        ksp.setType('cg')

                        if (
                            self.comm.size == 1
                            and linear_solver_
                            == 'petsc_cg_ilu'
                        ):
                            pc.setType('ilu')
                        else:
                            pc.setType('gamg')

                        ksp.setTolerances(
                            rtol=1.0e-10,
                            max_it=1_000_000,
                        )

                    else:
                        raise ValueError(
                            f"Unknown linear solver: {linear_solver_}"
                        )

                    ksp.setFromOptions()

                    if mode == 'fwd':
                        ksp.solve(input_vector, solution_vector)
                    else:
                        ksp.solveTranspose(
                            input_vector,
                            solution_vector,
                        )

                    converged_reason = ksp.getConvergedReason()
                    if converged_reason < 0:
                        raise RuntimeError(
                            "PETSc KSP failed to converge; "
                            f"converged reason={converged_reason}"
                        )

                    solution = self._petsc_vector_to_global(
                        solution_vector
                    )
                finally:
                    solution_vector.destroy()
                    input_vector.destroy()
                    ksp.destroy()

            if mode == 'fwd':
                d_outputs[state_name] = solution
            else:
                d_residuals[state_name] = solution
        finally:
            matrix.destroy()
