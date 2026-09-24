import ufl


def get_residual_form(u, v, rho_e, E=1, method='SIMP'):
    if method == 'SIMP':
        C = rho_e**3
    else:
        C = rho_e / (1.0 + 8.0 * (1.0 - rho_e))    

    # Preserve the original behavior: C is the design variable and ranges
    # from zero to one.
    E = 1.0 * C

    nu = 0.3  # Poisson's ratio

    lambda_ = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    mu = E / (2.0 * (1.0 + nu))  # Lamé's parameters

    epsilon_u = ufl.sym(ufl.grad(u))
    epsilon_v = ufl.sym(ufl.grad(v))

    dimension = u.ufl_shape[0]

    sigma = (
        lambda_ * ufl.div(u) * ufl.Identity(dimension)
        + 2.0 * mu * epsilon_u
    )

    return ufl.inner(sigma, epsilon_v) * ufl.dx