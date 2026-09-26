import numpy as np
from openmdao.api import ExplicitComponent


class CopyComp(ExplicitComponent):
    """Copy a layer; optionally place copies in global DG0 DOF order."""

    def initialize(self):
        self.options.declare("in_name", types=str)
        self.options.declare("out_name", types=str)
        self.options.declare("in_shape", types=int)
        self.options.declare("num_copies", types=int)
        # Entry i says which input-layer entry supplies output DOF i.
        self.options.declare("out_to_in", default=None, allow_none=True)

    def setup(self):
        n = self.options["in_shape"]
        copies = self.options["num_copies"]
        if n < 1 or copies < 1:
            raise ValueError("in_shape and num_copies must be positive")
        mapping = self.options["out_to_in"]
        if mapping is None:
            mapping = np.tile(np.arange(n, dtype=np.int64), copies)
        else:
            mapping = np.asarray(mapping)
            if (
                mapping.shape != (n * copies,)
                or not np.issubdtype(mapping.dtype, np.integer)
                or np.any(mapping < 0) or np.any(mapping >= n)
            ):
                raise ValueError("Invalid out_to_in mapping")
            mapping = mapping.astype(np.int64)
        self._source = mapping
        a, b = self.options["in_name"], self.options["out_name"]
        self.add_input(a, shape=n)
        self.add_output(b, shape=n * copies)
        self.declare_partials(
            b, a,
            rows=np.arange(n * copies, dtype=np.int64),
            cols=mapping, val=1.0,
        )

    def compute(self, inputs, outputs):
        outputs[self.options["out_name"]] = (
            inputs[self.options["in_name"]][self._source]
        )