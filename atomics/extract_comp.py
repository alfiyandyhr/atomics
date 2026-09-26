import numpy as np
from openmdao.core.explicitcomponent import ExplicitComponent


class ExtractComp(ExplicitComponent):
    """Extract globally indexed entries from a replicated OpenMDAO vector.

    ``partial_dof`` must contain GLOBAL scalar indices of the input, in the
    desired output order. Constructing those indices from a process-local
    DOLFINx subspace dofmap is the caller's responsibility.
    """

    def initialize(self):
        self.options.declare("in_name", types=str)
        self.options.declare("out_name", types=str)
        self.options.declare("in_shape", types=int)
        self.options.declare("partial_dof", types=np.ndarray)

    def setup(self):
        indices = self.options["partial_dof"]
        input_size = self.options["in_shape"]
        if indices.ndim != 1 or not np.issubdtype(indices.dtype, np.integer):
            raise ValueError("partial_dof must be a 1D integer array")
        if np.any(indices < 0) or np.any(indices >= input_size):
            raise ValueError("partial_dof contains an out-of-range global DOF")

        self._indices = np.asarray(indices, dtype=np.int64)
        in_name = self.options["in_name"]
        out_name = self.options["out_name"]
        self.add_input(in_name, shape=input_size)
        self.add_output(out_name, shape=self._indices.size)
        self.declare_partials(
            of=out_name,
            wrt=in_name,
            rows=np.arange(self._indices.size, dtype=np.int64),
            cols=self._indices,
            val=1.0,
        )

    def compute(self, inputs, outputs):
        outputs[self.options["out_name"]] = (
            inputs[self.options["in_name"]][self._indices]
        )
