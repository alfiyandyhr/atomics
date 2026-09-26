import ufl


def get_residual_form(u, v, rho_e, method='RAMP'):
    """
    Return the Saint-Venant--Kirchhoff internal residual.

    Parameters
    ----------
    u
        DOLFINx displacement Function.
    v
        UFL displacement TestFunction.
    rho_e
        DOLFINx density Function.
    method : {"SIMP", "RAMP"}
        Material interpolation method.
    """
    mesh = u.function_space.mesh
    dx = ufl.Measure(
        "dx",
        domain=mesh,
        metadata={"quadrature_degree": 4},
    )

    if method == 'SIMP':
        stiffness = rho_e**3
    elif method == 'RAMP':
        stiffness = rho_e / (1 + 8. * (1. - rho_e))
    else:
        raise ValueError(
            "Unknown material interpolation method {!r}; expected "
            "'SIMP' or 'RAMP'.".format(method)
        )

    k = 3e1

    youngs_modulus = k * stiffness

    nu = 0.3

    mu = youngs_modulus / (2.0 * (1.0 + nu))
    lmbda = (
        youngs_modulus * nu
        / ((1.0 + nu) * (1.0 - 2.0 * nu))
    )

    dimension = u.ufl_shape[0]
    identity = ufl.Identity(dimension)

    # Finite-strain kinematics.
    deformation_gradient = identity + ufl.grad(u)
    right_cauchy_green = ufl.dot(
        deformation_gradient.T,
        deformation_gradient,
    )
    green_lagrange_strain = 0.5 * (
        right_cauchy_green - identity
    )

    # Saint-Venant--Kirchhoff second Piola stress.
    second_piola_stress = (
        2.0 * mu * green_lagrange_strain
        + lmbda
        * ufl.tr(green_lagrange_strain)
        * identity
    )

    strain_energy_density = 0.5 * ufl.inner(
        second_piola_stress,
        green_lagrange_strain,
    )
    internal_energy = strain_energy_density * dx

    return ufl.derivative(internal_energy, u, v)
