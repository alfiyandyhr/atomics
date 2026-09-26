import numpy as np
from openmdao.api import ExplicitComponent


class SymmericRhocomp(ExplicitComponent):
    """Mirror an L-by-L quarter into a (2L)-by-(2L) density layer."""

    def initialize(self):
        self.options.declare("in_name", types=str)
        self.options.declare("out_name", types=str)
        self.options.declare("in_shape", types=int)
        self.options.declare("num_copies", types=int)

    def setup(self):
        size = self.options["in_shape"]
        L = int(np.sqrt(size))
        if L < 1 or L * L != size or self.options["num_copies"] != 4:
            raise ValueError("Expected a nonempty square quarter and 4 copies")

        row, col = np.indices((2 * L, 2 * L))
        source_row = np.minimum(row, 2 * L - 1 - row)
        source_col = np.minimum(col, 2 * L - 1 - col)
        self._source = (source_row * L + source_col).ravel()

        in_name, out_name = self.options["in_name"], self.options["out_name"]
        self.add_input(in_name, shape=size)
        self.add_output(out_name, shape=4 * size)
        self.declare_partials(
            out_name, in_name,
            rows=np.arange(4 * size, dtype=np.int64),
            cols=self._source,
            val=1.0,
        )

    def compute(self, inputs, outputs):
        outputs[self.options["out_name"]] = (
            inputs[self.options["in_name"]][self._source]
        )