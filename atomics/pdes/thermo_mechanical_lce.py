"""Small-strain, thermally actuated LCE residual for DOLFINx."""

import ufl


def get_residual_form(u, v, rho_e, phi_angle, k, alpha, method="RAMP"):
    """Return the original LCE weak residual.

    ``u`` and ``v`` are three-component fields; ``rho_e`` and
    ``phi_angle`` are scalar coefficient Functions. The return value is
    a UFL form, not an assembled DOLFINx form.
    """
    if u.ufl_shape != (3,) or v.ufl_shape != (3,):
        raise ValueError("The LCE residual requires 3D displacement fields")

    if method == "SIMP":
        C = rho_e**3
    elif method == "RAMP":
        C = rho_e / (1.0 + 8.0 * (1.0 - rho_e))
    else:
        raise ValueError(f"Unknown density interpolation: {method}")

    nu = 0.49
    lame_lambda = k * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    mu = k / (2.0 * (1.0 + nu))
    thermal_load = 1.0

    strain_u = ufl.sym(ufl.grad(u))
    strain_v = ufl.sym(ufl.grad(v))

    S = ufl.as_matrix(((-2.0, 0.0, 0.0),
                       (0.0, 1.0, 0.0),
                       (0.0, 0.0, 1.0)))
    c = ufl.cos(phi_angle)
    s = ufl.sin(phi_angle)
    L = ufl.as_matrix(((c, s, 0.0),
                       (-s, c, 0.0),
                       (0.0, 0.0, 1.0)))
    rotated_actuation = ufl.dot(ufl.transpose(L), ufl.dot(S, L))

    effective_strain = (
        strain_u - alpha * C * thermal_load * rotated_actuation
    )

    # Deliberately preserve the legacy model: its volumetric term is
    # lambda * div(u), NOT lambda * tr(effective_strain).
    stress = (
        lame_lambda * ufl.div(u) * ufl.Identity(3)
        + 2.0 * mu * effective_strain
    )
    return ufl.inner(stress, strain_v) * ufl.dx(domain=u.function_space.mesh)
