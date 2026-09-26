class PDEProblem(object):
    '''
    PDEProblem is a class containing the mesh and the dictionaries of
    the boundary conditions, inputs, states, and outputs.
    '''

    def __init__(self, mesh):
        self.mesh = mesh

        self.inputs_dict = dict()
        self.states_dict = dict()
        self.scalar_outputs_dict = dict()
        self.field_outputs_dict = dict()
        self.bcs_list = list()

    def add_bc(self, bc):
        self.bcs_list.append(bc)

    def add_input(self, name, function):
        if name in self.inputs_dict:
            raise ValueError('name has already been used for an input')

        function.name = name
        self.inputs_dict[name] = dict(
            function=function,
        )

    def add_state(self, name, function, residual_form, *arguments):
        function.name = name
        self.states_dict[name] = dict(
            function=function,
            residual_form=residual_form,
            arguments=arguments,
        )

    def add_load_step_residual(self, state_name, residual_factory):
        """
        Register a load-stepping residual factory for a state.

        The callable must accept ``(load_factor, final_step)`` and return
        the UFL residual form for that load step.
        """
        if state_name not in self.states_dict:
            raise KeyError(
                "Cannot register load stepping for unknown state {!r}."
                .format(state_name)
            )
        self.states_dict[state_name][
            'load_step_residual_form'
        ] = residual_factory

    def add_scalar_output(self, name, form, *arguments):
        self.scalar_outputs_dict[name] = dict(
            form=form,
            arguments=arguments,
        )

    def add_field_output(self, name, form, *arguments):
        self.field_outputs_dict[name] = dict(
            form=form,
            arguments=arguments,
        )