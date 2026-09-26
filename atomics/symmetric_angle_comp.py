import numpy as np
from openmdao.api import ExplicitComponent


class SymmericAnglecomp(ExplicitComponent):
    """Mirror bottom/top quarter angles, applying pi-angle on each reflection."""

    def initialize(self):
        self.options.declare("in_name", types=str)
        self.options.declare("out_name", types=str)
        self.options.declare("in_shape", types=int)
        self.options.declare("num_copies", types=int)

    def setup(self):
        size = self.options["in_shape"]
        L = int(np.sqrt(size // 2))
        if (
            size < 2 or size != 2 * L * L
            or self.options["num_copies"] != 4
        ):
            raise ValueError("Expected two nonempty square quarters and 4 copies")

        surface, row, col = np.indices((2, 2 * L, 2 * L))
        source_row = np.minimum(row, 2 * L - 1 - row)
        source_col = np.minimum(col, 2 * L - 1 - col)
        self._source = (
            surface * L * L + source_row * L + source_col
        ).ravel()
        self._sign = (
            (1 - 2 * (row >= L)) * (1 - 2 * (col >= L))
        ).ravel().astype(float)
        self._offset = np.where(self._sign < 0, np.pi, 0.0)

        in_name, out_name = self.options["in_name"], self.options["out_name"]
        self.add_input(in_name, shape=size)
        self.add_output(out_name, shape=4 * size)
        self.declare_partials(
            out_name, in_name,
            rows=np.arange(4 * size, dtype=np.int64),
            cols=self._source,
            val=self._sign,
        )

    def compute(self, inputs, outputs):
        outputs[self.options["out_name"]] = (
            self._sign * inputs[self.options["in_name"]][self._source]
            + self._offset
        )