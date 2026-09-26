import ufl
from dolfinx import fem
from petsc4py import PETSc


def get_residual_form(
    u,
    v,
    rho_e,
    *,
    additive="strain",
    k=8.0,
    method="RAMP",
    c2_e=None,
):
    """
    Construct the compressible neo-Hookean residual.

    Parameters
    ----------
    u
        Displacement Function.
    v
        Displacement test function.
    rho_e
        Material-density Function.
    additive
        ``"strain"``, ``"vol"``, or ``False``/``"False"``.
    k
        Solid-material Young's-modulus scale.
    method
        ``"SIMP"`` or ``"RAMP"``.
    c2_e
        Optional DOLFINx Function or Constant used by the strain-additive
        model. If omitted, a spatially uniform value of 5e-4 is used.

    Notes
    -----
    External traction is intentionally not included here. It should be
    subtracted from the returned residual in the run file, as is done by
    the other migrated examples.
    """
    mesh = u.function_space.mesh
    dx = ufl.Measure(
        "dx",
        domain=mesh,
        metadata={"quadrature_degree": 4},
    )

    method = method.upper()
    if method == "SIMP":
        stiffness = rho_e**3
    elif method == "RAMP":
        stiffness = rho_e / (
            1.0 + 8.0 * (1.0 - rho_e)
        )
    else:
        raise ValueError(
            f"Unknown material interpolation method: {method!r}"
        )

    geometric_dimension = mesh.geometry.dim
    identity = ufl.Identity(geometric_dimension)

    # Kinematics
    deformation_gradient = identity + ufl.grad(u)
    right_cauchy_green = (
        deformation_gradient.T * deformation_gradient
    )
    ic = ufl.tr(right_cauchy_green)
    jacobian = ufl.det(deformation_gradient)

    youngs_modulus = k * stiffness
    additive_energy = 0.0

    if additive == "strain":
        c1_e = (
            k
            * 5.0e-2
            / (1.0 + 8.0 * (1.0 - 5.0e-2))
            / 6.0
        )

        if c2_e is None:
            c2_e = fem.Constant(
                mesh,
                PETSc.ScalarType(5.0e-4),
            )

        # Preserve the invariant shift used by the legacy formulation.
        ic_shift = ic - 3.0
        additive_energy = (
            (1.0 - stiffness)
            * (
                c1_e * ic_shift
                + (c2_e * ic_shift) ** 2
            )
        )

    elif additive == "vol":
        stiffen_power = 1.0
        youngs_modulus = (
            k * stiffness / jacobian**stiffen_power
        )

    elif additive in (False, None, "False"):
        pass

    else:
        raise ValueError(
            f"Unknown additive model: {additive!r}"
        )

    poisson_ratio = 0.4
    lambda_ = (
        youngs_modulus
        * poisson_ratio
        / (1.0 + poisson_ratio)
        / (1.0 - 2.0 * poisson_ratio)
    )
    mu = (
        youngs_modulus
        / (2.0 * (1.0 + poisson_ratio))
    )

    # Compressible neo-Hookean strain-energy density.
    strain_energy = (
        0.5 * mu * (ic - 3.0)
        - mu * ufl.ln(jacobian)
        + 0.5 * lambda_ * ufl.ln(jacobian) ** 2
    )

    if additive == "strain":
        strain_energy += additive_energy

    potential_energy = strain_energy * dx
    return ufl.derivative(
        potential_energy,
        u,
        v,
    )
