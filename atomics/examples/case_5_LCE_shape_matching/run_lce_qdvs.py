"""Quarter-design LCE optimization, using DOLFINx 0.9 and IPOPT."""

from pathlib import Path

import numpy as np
import ufl
from mpi4py import MPI
from petsc4py import PETSc
from dolfinx import fem, io, mesh as dmesh
import openmdao.api as om

from atomics.api import PDEProblem, AtomicsGroup
from atomics.pdes.thermo_mechanical_lce import get_residual_form
from atomics.general_filter_comp import GeneralFilterComp
from atomics.copy_comp import CopyComp
from atomics.interpolant_comp import InterpolantComp
from atomics.symmetric_angle_comp import SymmericAnglecomp
from atomics.symmetric_rho_comp import SymmericRhocomp


comm = MPI.COMM_WORLD

# Keep the physical domain and discretization of the legacy example.
LENGTH = 2.5e-3
WIDTH = 5.0e-3
THICKNESS = 5.0e-5
NX = NY = 20
NZ = 4
Y0 = -WIDTH / 2.0
X0 = -LENGTH
K = 5.0e6
ALPHA = 2.5e-3
TARGET_ANGLE = np.deg2rad(2.5)
PLANE = NX * NY
QUARTER = PLANE // 4

mesh = dmesh.create_box(
    comm,
    ((X0, Y0, 0.0), (LENGTH, WIDTH / 2.0, THICKNESS)),
    (NX, NY, NZ),
    cell_type=dmesh.CellType.hexahedron,
    dtype=np.float64,
)
Vrho = fem.functionspace(mesh, ("Discontinuous Lagrange", 0))
Vangle = fem.functionspace(mesh, ("Discontinuous Lagrange", 0))
Vu = fem.functionspace(mesh, ("Lagrange", 1, (3,)))
rho = fem.Function(Vrho, name="density")
phi = fem.Function(Vangle, name="angle")
u = fem.Function(Vu, name="displacements")
v = ufl.TestFunction(Vu)


def grid_indices(space):
    """Return (iz, iy, ix) in global scalar-DG0-DOF order."""
    imap = space.dofmap.index_map
    if space.dofmap.index_map_bs != 1:
        raise ValueError("This grid mapping requires a scalar DG0 space")
    n_owned = imap.size_local
    owned_global = imap.local_to_global(
        np.arange(n_owned, dtype=np.int32)
    )
    owned_xyz = space.tabulate_dof_coordinates()[:n_owned, :3].copy()
    gathered = comm.allgather((owned_global, owned_xyz))
    xyz = np.empty((imap.size_global, 3), dtype=np.float64)
    seen = np.zeros(imap.size_global, dtype=bool)
    for indices, coordinates in gathered:
        if np.any(seen[indices]):
            raise RuntimeError("Duplicated owned global DG0 DOF")
        xyz[indices] = coordinates
        seen[indices] = True
    if not np.all(seen):
        raise RuntimeError("Missing owned global DG0 DOF")
    if xyz.shape[0] != NX * NY * NZ:
        raise ValueError("Unexpected number of DG0 cells")

    origin = np.array((X0, Y0, 0.0))
    spacing = np.array((2 * LENGTH / NX, WIDTH / NY, THICKNESS / NZ))
    scaled = (xyz - origin) / spacing - 0.5
    ijk = np.rint(scaled).astype(np.int64)
    if not np.allclose(scaled, ijk, rtol=0.0, atol=1.0e-5):
        raise ValueError("DG0 coordinates do not match the rectangular grid")
    ix, iy, iz = ijk.T
    if (
        np.any(ix < 0) or np.any(ix >= NX)
        or np.any(iy < 0) or np.any(iy >= NY)
        or np.any(iz < 0) or np.any(iz >= NZ)
    ):
        raise ValueError("Cell coordinate outside the grid")
    flat = (iz * NY + iy) * NX + ix
    if np.unique(flat).size != flat.size:
        raise ValueError("Multiple DG0 DOFs mapped to one grid cell")
    return iz, iy, ix


iz, iy, ix = grid_indices(Vrho)
# Global DG0 output index -> row-major 2D cell index.
density_out_to_in = iy * NX + ix
# Global DG0 output index -> layer-major 3D cell index.
angle_out_to_in = iz * PLANE + iy * NX + ix

pde = PDEProblem(mesh)
pde.add_input("density", rho)
pde.add_input("angle", phi)
pde.add_state(
    "displacements", u,
    get_residual_form(u, v, rho, phi, K, ALPHA),
    "density", "angle",
)

dx = ufl.Measure("dx", domain=mesh)
one = fem.Constant(mesh, PETSc.ScalarType(1.0))
volume = comm.allreduce(fem.assemble_scalar(fem.form(one * dx)), op=MPI.SUM)
pde.add_scalar_output("avg_density", rho / volume * dx, "density")

x = ufl.SpatialCoordinate(mesh)
desired = ufl.as_vector((
    -(1.0 - np.cos(TARGET_ANGLE)) * x[0],
    0.0,
    abs(x[0]) * np.sin(TARGET_ANGLE),
))
error = desired - u
pde.add_scalar_output(
    "error_norm",
    (1.0e9 / volume) * ufl.inner(error, error) * dx,
    "displacements",
)

# x=0 and y=0 are INTERIOR symmetry planes; neither can be
# selected with locate_entities_boundary().
atol = 1.0e-12
for component, marker in (
    (0, lambda x: np.isclose(x[0], 0.0, rtol=0, atol=atol)),
    (1, lambda x: np.isclose(x[1], 0.0, rtol=0, atol=atol)),
    (2, lambda x: (
        np.isclose(x[0], 0.0, rtol=0, atol=atol)
        & np.isclose(x[1], 0.0, rtol=0, atol=atol)
        & np.isclose(x[2], 0.0, rtol=0, atol=atol)
    )),
):
    subspace = Vu.sub(component)
    collapsed, _ = subspace.collapse()
    dofs, _ = fem.locate_dofs_geometrical(
        (subspace, collapsed), marker
    )
    if comm.allreduce(dofs.size, op=MPI.SUM) == 0:
        raise RuntimeError(
            f"No DOFs found for displacement component {component}"
        )
    pde.add_bc(
        fem.dirichletbc(
            np.array(0.0, dtype=PETSc.ScalarType),
            dofs, subspace,
        )
    )

prob = om.Problem()
design = om.IndepVarComp()
design.add_output(
    "density_unfiltered_layer_q",
    val=np.ones(QUARTER),
)
initial_angle = np.zeros(2 * QUARTER)
# Preserve the approximate initial strip from the original example.
initial_angle[:QUARTER // 4] = np.pi / 2.0
design.add_output("angle_t_b_q", val=initial_angle)
prob.model.add_subsystem("indep_var_comp", design, promotes=["*"])

prob.model.add_subsystem(
    "sym_rho_comp",
    SymmericRhocomp(
        in_name="density_unfiltered_layer_q",
        out_name="density_unfiltered_layer",
        in_shape=QUARTER, num_copies=4,
    ),
    promotes=["*"],
)
prob.model.add_subsystem(
    "sym_angle_comp",
    SymmericAnglecomp(
        in_name="angle_t_b_q", out_name="angle_t_b",
        in_shape=2 * QUARTER, num_copies=4,
    ),
    promotes=["*"],
)
prob.model.add_subsystem(
    "copy_comp",
    CopyComp(
        in_name="density_unfiltered_layer",
        out_name="density_unfiltered",
        in_shape=PLANE, num_copies=NZ,
        out_to_in=density_out_to_in,
    ),
    promotes=["*"],
)
prob.model.add_subsystem(
    "interpolant_comp",
    InterpolantComp(
        in_name="angle_t_b", out_name="angle",
        in_shape=2 * PLANE, num_pts=NZ,
        out_to_in=angle_out_to_in,
    ),
    promotes=["*"],
)
prob.model.add_subsystem(
    "general_filter_comp",
    GeneralFilterComp(density_function_space=Vrho),
    promotes=["*"],
)
prob.model.add_subsystem(
    "atomics_group",
    AtomicsGroup(
        pde_problem=pde,
        # The residual is linear in u for fixed density and angle.
        problem_type="linear_problem",
        linear_solver_="fenics_direct",
    ),
    promotes=["*"],
)

prob.model.add_design_var(
    "density_unfiltered_layer_q", lower=1.0e-4, upper=1.0
)
prob.model.add_design_var("angle_t_b_q", lower=0.0, upper=np.pi)
prob.model.add_objective("error_norm")
# Linear in the DENSITY design variable, despite the nonlinear
# displacement/angle path elsewhere in the model.
prob.model.add_constraint("avg_density", upper=0.4, linear=True)

prob.driver = om.pyOptSparseDriver()
prob.driver.options["optimizer"] = "IPOPT"
prob.driver.opt_settings["max_iter"] = 1000
prob.driver.opt_settings["tol"] = 1.0e-5
prob.driver.opt_settings["print_level"] = 5
prob.driver.opt_settings["print_user_options"] = "yes"
prob.setup()
prob.run_driver()


def set_function_from_global(function, values):
    """Synchronize a DOLFINx Function with replicated OpenMDAO output."""
    values = np.asarray(values).ravel()
    dofmap = function.function_space.dofmap
    imap = dofmap.index_map
    bs = dofmap.index_map_bs
    blocks = imap.local_to_global(
        np.arange(imap.size_local, dtype=np.int32)
    )
    owned = (
        bs * blocks[:, None] + np.arange(bs)[None, :]
    ).ravel()
    function.x.array[:owned.size] = values[owned]
    function.x.scatter_forward()


# The last driver evaluation need not have populated these Functions
# with the final OpenMDAO design; synchronize them explicitly.
set_function_from_global(rho, prob.get_val("density"))
set_function_from_global(phi, prob.get_val("angle"))
set_function_from_global(u, prob.get_val("displacements"))

stiffness = fem.Function(Vrho, name="stiffness_factor")
stiffness.x.array[:] = rho.x.array / (
    1.0 + 8.0 * (1.0 - rho.x.array)
)
stiffness.x.scatter_forward()

outdir = Path("solutions/")
if comm.rank == 0:
    outdir.mkdir(parents=True, exist_ok=True)
comm.barrier()


def save_xdmf(filename, function):
    # XDMF is collective; all MPI ranks must enter this context.
    with io.XDMFFile(comm, str(outdir / filename), "w") as writer:
        writer.write_mesh(mesh)
        writer.write_function(function, 0.0)
    # Remove the accompanying .h5 file
    import os
    h5_file = str(outdir / filename).replace(".xdmf", ".h5")
    if comm.rank == 0 and os.path.exists(h5_file):
        os.remove(h5_file)


save_xdmf("displacements.xdmf", u)
save_xdmf("density.xdmf", rho)
save_xdmf("angles.xdmf", phi)
save_xdmf("stiffness.xdmf", stiffness)

# Collect ONLY owned cells for the 2D PNG slices.
num_owned = Vrho.dofmap.index_map.size_local
local_global = Vrho.dofmap.index_map.local_to_global(
    np.arange(num_owned, dtype=np.int32)
)
plot_parts = comm.gather(
    (
        iz[local_global], iy[local_global], ix[local_global],
        rho.x.array[:num_owned].copy(),
        phi.x.array[:num_owned].copy(),
        stiffness.x.array[:num_owned].copy(),
    ),
    root=0,
)

if comm.rank == 0:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap, LinearSegmentedColormap
    from matplotlib.collections import LineCollection
    from matplotlib.patches import Rectangle, ConnectionPatch

    grids = {
        "density": np.empty((NZ, NY, NX)),
        "angle": np.empty((NZ, NY, NX)),
        "stiffness": np.empty((NZ, NY, NX)),
    }
    for z, y, xcell, densities, angles, factors in plot_parts:
        grids["density"][z, y, xcell] = densities
        grids["angle"][z, y, xcell] = angles
        grids["stiffness"][z, y, xcell] = factors

    x_edges = np.linspace(X0, LENGTH, NX + 1)
    y_edges = np.linspace(Y0, WIDTH / 2.0, NY + 1)
    dx_cell = x_edges[1] - x_edges[0]
    dy_cell = y_edges[1] - y_edges[0]
    xc, yc = np.meshgrid(
        (x_edges[:-1] + x_edges[1:]) / 2.0,
        (y_edges[:-1] + y_edges[1:]) / 2.0,
    )

    # Density is copied through the thickness in this design.
    density_2d = grids["density"].mean(axis=0)
    ACTIVE_THRESHOLD = 0.5  # Visual cutoff only; does not affect optimization.
    active = density_2d >= ACTIVE_THRESHOLD

    def draw_directors(ax, layer):
        ax.pcolormesh(
            x_edges, y_edges, active.astype(float),
            cmap=ListedColormap(["white", "#999999"]),
            vmin=0, vmax=1, shading="flat",
            edgecolors="#80b9f2", linewidth=0.55,
        )

        # A director is an unoriented line segment, not an arrow.
        angles = grids["angle"][layer][active]
        centers = np.column_stack((xc[active], yc[active]))
        half_length = 0.34 * min(dx_cell, dy_cell)
        offsets = half_length * np.column_stack((
            np.cos(angles), np.sin(angles),
        ))
        segments = np.stack((centers - offsets, centers + offsets), axis=1)
        ax.add_collection(LineCollection(
            segments, colors="#303030", linewidths=0.8,
        ))
        ax.set_xlim(x_edges[0], x_edges[-1])
        ax.set_ylim(y_edges[0], y_edges[-1])
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    fig, (ax_top, ax_bottom, ax_density) = plt.subplots(
        1, 3, figsize=(16, 5.8),
        gridspec_kw={"wspace": 0.30},
    )
    draw_directors(ax_top, NZ - 1)
    draw_directors(ax_bottom, 0)

    # Highlight and enlarge a portion of the bottom-layer directors.
    i0, i1 = 2, max(3, NX // 2)
    j0, j1 = NY - max(3, NY // 3), NY
    bounds = (
        x_edges[i0], y_edges[j0],
        x_edges[i1] - x_edges[i0],
        y_edges[j1] - y_edges[j0],
    )
    ax_bottom.add_patch(Rectangle(
        bounds[:2], bounds[2], bounds[3],
        fill=False, edgecolor="#e53935", linewidth=2.0,
    ))
    zoom = ax_bottom.inset_axes(
        (-0.37, 0.23, 0.46, 0.55), zorder=5,
    )
    draw_directors(zoom, 0)
    zoom.set_xlim(x_edges[i0], x_edges[i1])
    zoom.set_ylim(y_edges[j0], y_edges[j1])
    for spine in zoom.spines.values():
        spine.set_visible(True)
        spine.set_edgecolor("#80b9f2")
        spine.set_linewidth(1.5)
    fig.add_artist(ConnectionPatch(
        xyA=(x_edges[i1], y_edges[j0]), coordsA=zoom.transData,
        xyB=(x_edges[i0], y_edges[j0]), coordsB=ax_bottom.transData,
        arrowstyle="->", color="#e53935", linewidth=1.5,
    ))

    red_density = LinearSegmentedColormap.from_list(
        "lce_density",
        [(0.0, "white"), (0.2, "white"),
         (0.5, "#bd8174"), (1.0, "#850c18")],
    )
    ax_density.pcolormesh(
        x_edges, y_edges, density_2d,
        cmap=red_density, vmin=0, vmax=1, shading="flat",
        edgecolors="#181818", linewidth=0.55,
    )
    ax_density.set_xlim(x_edges[0], x_edges[-1])
    ax_density.set_ylim(y_edges[0], y_edges[-1])
    ax_density.set_aspect("equal")
    ax_density.set_xticks([])
    ax_density.set_yticks([])
    for spine in ax_density.spines.values():
        spine.set_visible(False)

    for ax, label in (
        (ax_top, r"$\phi^{\mathrm{top}}$  (a)"),
        (ax_bottom, r"$\phi^{\mathrm{bot}}$  (b)"),
        (ax_density, "Density  (c)"),
    ):
        ax.set_xlabel(label, fontsize=16, labelpad=12)

    fig.savefig(
        outdir / "lce_design.png", dpi=220,
        bbox_inches="tight", facecolor="white",
    )
    plt.close(fig)
