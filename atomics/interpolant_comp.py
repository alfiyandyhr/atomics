import numpy as np
from openmdao.api import ExplicitComponent


class InterpolantComp(ExplicitComponent):
    """Interpolate bottom/top layers through thickness.

    Input order: all bottom-layer cells, then all top-layer cells.
    Without out_to_in, output order is layer-major. Otherwise, entry i
    of out_to_in is the layer-major index supplying global DG0 DOF i.
    """

    def initialize(self):
        self.options.declare("in_name", types=str)
        self.options.declare("out_name", types=str)
        self.options.declare("in_shape", types=int)
        self.options.declare("num_pts", types=int)
        self.options.declare("out_to_in", default=None, allow_none=True)

    def setup(self):
        n = self.options["in_shape"]
        nz = self.options["num_pts"]
        if n < 2 or n % 2 or nz < 2:
            raise ValueError("Expected two equal surfaces and num_pts >= 2")
        plane = n // 2
        out_size = nz * plane
        mapping = self.options["out_to_in"]
        if mapping is None:
            mapping = np.arange(out_size, dtype=np.int64)
        else:
            mapping = np.asarray(mapping)
            if (
                mapping.shape != (out_size,)
                or not np.issubdtype(mapping.dtype, np.integer)
                or np.any(mapping < 0) or np.any(mapping >= out_size)
                or np.unique(mapping).size != out_size
            ):
                raise ValueError("out_to_in must be a layer-major permutation")
            mapping = mapping.astype(np.int64)

        self._cell = mapping % plane
        self._alpha = (mapping // plane) / (nz - 1)
        a, b = self.options["in_name"], self.options["out_name"]
        self.add_input(a, shape=n)
        self.add_output(b, shape=out_size)
        rows = np.arange(out_size, dtype=np.int64)
        self.declare_partials(
            b, a,
            rows=np.concatenate((rows, rows)),
            cols=np.concatenate((self._cell, self._cell + plane)),
            val=np.concatenate((1.0 - self._alpha, self._alpha)),
        )

    def compute(self, inputs, outputs):
        x = inputs[self.options["in_name"]]
        plane = x.size // 2
        outputs[self.options["out_name"]] = (
            (1.0 - self._alpha) * x[self._cell]
            + self._alpha * x[plane + self._cell]
        )
