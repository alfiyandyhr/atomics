import ufl


def get_residual_form(
    u, v, rho_e, T, T_hat, KAPPA, k, alpha,
    mode="plane_stress", method="RAMP", T_r=20.0,
):
    """Mixed thermoelastic/heat-conduction residual for DOLFINx/UFL.

    Retains the original example's thermal-strain and stress convention.
    The applied tractions and heat fluxes are subtracted by the caller.
    """
    if method == "RAMP":
        C = rho_e / (1.0 + 8.0 * (1.0 - rho_e))
    elif method == "SIMP":
        C = rho_e**3
    else:
        raise ValueError("method must be 'RAMP' or 'SIMP'")

    E = k * C
    nu = 0.3
    mu = E / (2.0 * (1.0 + nu))

    if mode == "plane_stress":
        # Algebraically equivalent to the plane-stress Lamé conversion
        # when E > 0, but avoids a 0/0 expression at E == 0.
        lambda_ = E * nu / (1.0 - nu**2)
    elif mode == "plane_strain":
        lambda_ = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    else:
        raise ValueError("mode must be 'plane_stress' or 'plane_strain'")

    identity = ufl.Identity(u.ufl_shape[0])
    strain = ufl.sym(ufl.grad(u)) - C * alpha * identity * (T - T_r)
    stress = lambda_ * ufl.div(u) * identity + 2.0 * mu * strain

    dx = ufl.Measure("dx", domain=u.ufl_domain())
    return (
        ufl.inner(stress, ufl.sym(ufl.grad(v))) * dx
        + ufl.dot(C * KAPPA * ufl.grad(T), ufl.grad(T_hat)) * dx
    )
