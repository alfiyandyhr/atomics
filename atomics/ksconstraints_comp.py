import numpy as np
from openmdao.core.explicitcomponent import ExplicitComponent


class KSConstraintsComp(ExplicitComponent):
    """Smooth maximum along an axis of a replicated OpenMDAO input.

    A one-dimensional input reduced along axis zero has a length-one
    OpenMDAO output. ``rho`` must be strictly positive.
    """

    def initialize(self):
        self.options.declare("shape", types=tuple)
        self.options.declare("axis", types=int)
        self.options.declare("out_name", types=str)
        self.options.declare("in_name", types=str)
        self.options.declare("rho", default=50.0, types=(float, int))

    def setup(self):
        shape = self.options["shape"]
        if not shape or any(n < 1 for n in shape):
            raise ValueError("shape must contain positive dimensions")
        if self.options["rho"] <= 0:
            raise ValueError("rho must be positive")

        axis = self.options["axis"]
        if not -len(shape) <= axis < len(shape):
            raise ValueError("axis is outside input dimensions")
        self._axis = axis % len(shape)
        self._shape = shape

        reduced_shape = shape[:self._axis] + shape[self._axis + 1:]
        output_shape = reduced_shape or (1,)
        in_name = self.options["in_name"]
        out_name = self.options["out_name"]

        self.add_input(in_name, shape=shape)
        self.add_output(out_name, shape=output_shape)

        output_indices = np.arange(np.prod(output_shape)).reshape(
            output_shape
        )
        if reduced_shape:
            rows = np.broadcast_to(
                np.expand_dims(output_indices, axis=self._axis),
                shape,
            ).ravel()
        else:
            rows = np.zeros(np.prod(shape), dtype=np.int64)

        self.declare_partials(
            of=out_name,
            wrt=in_name,
            rows=rows,
            cols=np.arange(np.prod(shape)),
        )

    def _value_and_weights(self, inputs):
        values = np.asarray(
            inputs[self.options["in_name"]]
        ).reshape(self._shape)
        rho = self.options["rho"]

        # A real shift prevents overflow without discarding imaginary
        # perturbations when checking this component by complex step.
        offset = np.max(
            np.real(values), axis=self._axis, keepdims=True
        )
        exponentials = np.exp(rho * (values - offset))
        sums = np.sum(exponentials, axis=self._axis, keepdims=True)
        result = offset + np.log(sums) / rho
        weights = exponentials / sums
        return np.squeeze(result, axis=self._axis), weights

    def compute(self, inputs, outputs):
        result, _ = self._value_and_weights(inputs)
        outputs[self.options["out_name"]] = result

    def compute_partials(self, inputs, partials):
        _, weights = self._value_and_weights(inputs)
        partials[
            self.options["out_name"], self.options["in_name"]
        ] = weights.ravel()
