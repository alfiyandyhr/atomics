from pathlib import Path

import gmsh
import numpy as np
import openmdao.api as om
import ufl
from basix.ufl import element, mixed_element
from dolfinx import fem, io
from dolfinx import mesh as dmesh
from dolfinx.io import gmshio
from mpi4py import MPI
from petsc4py import PETSc
from scipy.spatial import cKDTree

from atomics.api import AtomicsGroup, PDEProblem
from atomics.extract_comp import ExtractComp
from atomics.general_filter_comp import GeneralFilterComp
from atomics.ksconstraints_comp import KSConstraintsComp
from atomics.pdes.thermo_mechanical_mix_2d_stress import (
    get_residual_form,
)


comm = MPI.COMM_WORLD

# Choose "mass" or "compliance".
# objective = "compliance"
objective = "mass"

LENGTH = WIDTH = 0.20
HIGHT = 0.05
RADIUS = 0.01
# MESH_SIZE = 0.003
MESH_SIZE = 0.006
NUM_CELL_X = NUM_CELL_Y = 5

KAPPA = 235.0
K = 69.0e9
ALPHA = 13.0e-6
POWER = 90.0
T_0 = 20.0

# The old boolean difference retained only the upper-right quadrant.
# Generate that quadrant directly, subtracting its nine intersecting cells.
CELL_COORDINATES = np.linspace(-0.08, 0.08, NUM_CELL_X)
QUADRANT_CENTERS = np.array(
    [(x, y) for y in CELL_COORDINATES for x in CELL_COORDINATES
     if x >= 0.0 and y >= 0.0],
    dtype=np.float64,
)

HEAT_FULL = 5
HEAT_HALF = 6
HEAT_QUARTER = 7
RIGHT = 10
TOP = 14
MATERIAL = 20

AREA_CYLINDER = 2.0 * np.pi * RADIUS * HIGHT
q = fem.Constant if False else None  # Constants are created after the mesh.


def make_mesh():
    """Build the OCC geometry on rank zero; distribute it with DOLFINx."""
    if comm.rank == 0:
        gmsh.initialize()
        gmsh.model.add("battery_pack_quadrant")
        occ = gmsh.model.occ

        rectangle = occ.addRectangle(0.0, 0.0, 0.0, LENGTH / 2, WIDTH / 2)
        disks = [
            (2, occ.addDisk(float(x), float(y), 0.0, RADIUS, RADIUS))
            for x, y in QUADRANT_CENTERS
        ]
        material, _ = occ.cut([(2, rectangle)], disks)
        occ.synchronize()

        gmsh.model.addPhysicalGroup(
            2, [tag for dim, tag in material], MATERIAL
        )

        curves = gmsh.model.getBoundary(
            material, combined=True, oriented=False
        )
        boundary_groups = {
            HEAT_FULL: [],
            HEAT_HALF: [],
            HEAT_QUARTER: [],
            RIGHT: [],
            TOP: [],
        }

        for dim, tag in curves:
            if dim != 1:
                continue

            xmin, ymin, _, xmax, ymax, _ = gmsh.model.getBoundingBox(1, tag)
            tol = 1.0e-5  # OCC bounding boxes have a small tolerance.

            if abs(xmin - LENGTH / 2) < tol and abs(xmax - LENGTH / 2) < tol:
                boundary_groups[RIGHT].append(tag)
                continue
            if abs(ymin - WIDTH / 2) < tol and abs(ymax - WIDTH / 2) < tol:
                boundary_groups[TOP].append(tag)
                continue

            # Distinguish circular hole boundaries from the straight
            # symmetry edges by the OCC curve's center of mass.
            if abs(xmax - xmin) < tol or abs(ymax - ymin) < tol:
                continue

            cx, cy, _ = occ.getCenterOfMass(1, tag)
            distances = np.linalg.norm(
                QUADRANT_CENTERS - (cx, cy), axis=1
            )
            nearest = QUADRANT_CENTERS[np.argmin(distances)]
            if np.min(distances) > RADIUS + tol:
                raise RuntimeError(
                    f"Cannot identify circular boundary curve {tag}."
                )

            zero_coordinates = np.count_nonzero(
                np.isclose(nearest, 0.0)
            )
            marker = (
                HEAT_QUARTER if zero_coordinates == 2 else
                HEAT_HALF if zero_coordinates == 1 else HEAT_FULL
            )
            boundary_groups[marker].append(tag)

        for marker, tags in boundary_groups.items():
            if not tags:
                raise RuntimeError(f"Empty Gmsh boundary group {marker}.")
            gmsh.model.addPhysicalGroup(1, tags, marker)

        gmsh.option.setNumber("Mesh.MeshSizeMin", MESH_SIZE)
        gmsh.option.setNumber("Mesh.MeshSizeMax", MESH_SIZE)
        gmsh.model.mesh.generate(2)

    try:
        # In DOLFINx 0.9 this returns (mesh, cell_tags, facet_tags).
        msh, cell_tags, facet_tags = gmshio.model_to_mesh(
            gmsh.model if comm.rank == 0 else None,
            comm,
            rank=0,
            gdim=2,
        )
    finally:
        if comm.rank == 0:
            gmsh.finalize()

    if facet_tags is None:
        raise RuntimeError("Gmsh boundary physical groups were not imported.")
    return msh, cell_tags, facet_tags


mesh, cell_tags, facet_tags = make_mesh()
facet_dim = mesh.topology.dim - 1
dx = ufl.Measure("dx", domain=mesh)
ds = ufl.Measure("ds", domain=mesh, subdomain_data=facet_tags)

q = fem.Constant(mesh, PETSc.ScalarType(POWER / AREA_CYLINDER))
f_r = fem.Constant(
    mesh, np.array((-1.0e6 / HIGHT, 0.0), dtype=PETSc.ScalarType)
)
f_t = fem.Constant(
    mesh, np.array((0.0, -1.0e6 / HIGHT), dtype=PETSc.ScalarType)
)

pde_problem = PDEProblem(mesh)

density_space = fem.functionspace(mesh, ("Discontinuous Lagrange", 0))
density = fem.Function(density_space)
density.x.array[:] = 0.65
density.x.scatter_forward()
pde_problem.add_input("density", density)

displacement_element = element(
    "Lagrange", mesh.basix_cell(), 1,
    shape=(mesh.geometry.dim,), dtype=np.float64
)
temperature_element = element(
    "Lagrange", mesh.basix_cell(), 1, dtype=np.float64
)
mixed_space = fem.functionspace(
    mesh, mixed_element([displacement_element, temperature_element])
)
mixed_state = fem.Function(mixed_space)
u, T = ufl.split(mixed_state)
v, T_hat = ufl.TestFunctions(mixed_space)

residual = get_residual_form(
    u, v, density, T, T_hat, KAPPA, K, ALPHA
)
residual -= (
    ufl.dot(f_r, v) * ds(RIGHT)
    + ufl.dot(f_t, v) * ds(TOP)
    + q * T_hat * (ds(HEAT_FULL) + ds(HEAT_HALF) + ds(HEAT_QUARTER))
)
pde_problem.add_state("mixed_states", mixed_state, residual, "density")

local_volume = fem.assemble_scalar(
    fem.form(fem.Constant(mesh, PETSc.ScalarType(1.0)) * dx)
)
volume = comm.allreduce(local_volume, op=MPI.SUM)

# RAMP interpolation: density is the filtered topology rho; C is
# its dimensionless mechanical stiffness factor, not stiffness in Pa.
C = density / (1.0 + 8.0 * (1.0 - density))
pde_problem.add_scalar_output(
    "avg_density", density / volume * dx, "density"
)
pde_problem.add_scalar_output(
    "avg_density_p", C / volume * dx, "density"
)
pde_problem.add_scalar_output(
    "compliance",
    ufl.dot(f_r, u) * ds(RIGHT) + ufl.dot(f_t, u) * ds(TOP),
    "mixed_states",
)

# Retain the stress convention of the original example.
nu = 0.3
E = K * C
mu = E / (2.0 * (1.0 + nu))
lambda_plane_stress = E * nu / (1.0 - nu**2)
I = ufl.Identity(mesh.geometry.dim)
strain = ufl.sym(ufl.grad(u)) - C * ALPHA * I * (T - T_0)
sigma = lambda_plane_stress * ufl.div(u) * I + 2.0 * mu * strain
deviator = sigma - ufl.tr(sigma) * I / 3.0
von_mises = ufl.sqrt(
    1.5 * ufl.inner(deviator / 1.0e3, deviator / 1.0e3)
    + 1.0e-12
)
test_density = ufl.TestFunction(density_space)
pde_problem.add_field_output(
    "von_Mises",
    von_mises * test_density / ufl.CellVolume(mesh) * dx,
    "mixed_states",
    "density",
)

# Roller/symmetry conditions and a temperature sink on x=0.1, y=0.1.
vertical_facets = dmesh.locate_entities_boundary(
    mesh, facet_dim, lambda x: np.isclose(x[0], 0.0)
)
horizontal_facets = dmesh.locate_entities_boundary(
    mesh, facet_dim, lambda x: np.isclose(x[1], 0.0)
)
sink_facets = np.unique(np.concatenate((
    facet_tags.find(RIGHT), facet_tags.find(TOP)
))).astype(np.int32)

for subspace, facets, value in (
    (mixed_space.sub(0).sub(0), vertical_facets, 0.0),
    (mixed_space.sub(0).sub(1), horizontal_facets, 0.0),
    (mixed_space.sub(1), sink_facets, T_0),
):
    collapsed_space, _ = subspace.collapse()
    bc_value = fem.Function(collapsed_space)
    bc_value.x.array[:] = value
    bc_value.x.scatter_forward()
    dofs = fem.locate_dofs_topological(
        (subspace, collapsed_space), facet_dim, facets
    )
    pde_problem.add_bc(fem.dirichletbc(bc_value, dofs, subspace))


def global_temperature_parent_dofs():
    """Map global collapsed-temperature DOFs to global mixed-state DOFs."""
    temperature_space, local_parent_dofs = mixed_space.sub(1).collapse()
    parent_map = mixed_space.dofmap.index_map
    child_map = temperature_space.dofmap.index_map
    if mixed_space.dofmap.index_map_bs != 1 or (
        temperature_space.dofmap.index_map_bs != 1
    ):
        raise RuntimeError("Expected scalar-block mixed/temperature maps.")

    nowned = child_map.size_local
    child_globals = child_map.local_to_global(
        np.arange(nowned, dtype=np.int32)
    )
    parent_globals = parent_map.local_to_global(
        np.asarray(local_parent_dofs[:nowned], dtype=np.int32)
    )
    pairs = comm.allgather((child_globals, parent_globals))
    result = np.full(child_map.size_global, -1, dtype=np.int64)
    for child_ids, parent_ids in pairs:
        result[child_ids] = parent_ids
    if np.any(result < 0):
        raise RuntimeError("Incomplete global temperature DOF map.")
    return result


temperature_parent_dofs = global_temperature_parent_dofs()

# The original example pins filtered density around all nine quadrant cells
# and along the top/right outer perimeter.
coordinates = density_space.tabulate_dof_coordinates()[:, :2]
near_cells = cKDTree(QUADRANT_CENTERS).query(coordinates)[0] <= (
    RADIUS + 0.002
)
near_perimeter = (
    np.abs(coordinates[:, 0] - LENGTH / 2) <= 0.002
) | (
    np.abs(coordinates[:, 1] - WIDTH / 2) <= 0.002
)
owned_density = density_space.dofmap.index_map.size_local
local_fixed = np.flatnonzero(
    (near_cells | near_perimeter)[:owned_density]
).astype(np.int32)
global_fixed = density_space.dofmap.index_map.local_to_global(local_fixed)
fixed_dofs = np.unique(np.concatenate(comm.allgather(global_fixed)))


def set_function_from_global(function, values):
    """Assign owned DOLFINx DOFs from a replicated OpenMDAO vector."""
    values = np.asarray(values).reshape(-1)
    dofmap = function.function_space.dofmap
    index_map = dofmap.index_map
    bs = dofmap.index_map_bs
    owned = index_map.size_local
    global_blocks = index_map.local_to_global(
        np.arange(owned, dtype=np.int32)
    )
    global_dofs = (
        bs * global_blocks[:, None]
        + np.arange(bs, dtype=np.int64)[None, :]
    ).reshape(-1)
    function.x.array[:owned * bs] = values[global_dofs]
    function.x.scatter_forward()


num_density = (
    density_space.dofmap.index_map.size_global
    * density_space.dofmap.index_map_bs
)
num_state = (
    mixed_space.dofmap.index_map.size_global
    * mixed_space.dofmap.index_map_bs
)

prob = om.Problem()
independent = om.IndepVarComp()
independent.add_output(
    "density_unfiltered", val=np.full(num_density, 0.65)
)
prob.model.add_subsystem("indep_var_comp", independent, promotes=["*"])
prob.model.add_subsystem(
    "general_filter_comp",
    GeneralFilterComp(density_function_space=density_space),
    promotes=["*"],
)
prob.model.add_subsystem(
    "atomics_group",
    AtomicsGroup(
        pde_problem=pde_problem,
        problem_type="linear_problem",
        linear_solver_="fenics_direct",
    ),
    promotes=["*"],
)
prob.model.add_subsystem(
    "extract_comp",
    ExtractComp(
        in_name="mixed_states",
        out_name="temperature_field",
        in_shape=num_state,
        partial_dof=temperature_parent_dofs,
    ),
    promotes=["*"],
)
prob.model.add_subsystem(
    "temperature_ks",
    KSConstraintsComp(
        in_name="temperature_field",
        out_name="t_max",
        shape=(temperature_parent_dofs.size,),
        axis=0,
        rho=20.0,
    ),
    promotes=["*"],
)
prob.model.add_subsystem(
    "stress_ks",
    KSConstraintsComp(
        in_name="von_Mises",
        out_name="von_Mises_max",
        shape=(num_density,),
        axis=0,
        rho=20.0,
    ),
    promotes=["*"],
)

prob.model.add_design_var("density_unfiltered", lower=1.0e-4, upper=1.0)
prob.model.add_constraint(
    "density", indices=fixed_dofs, lower=1.0, upper=1.0
)

if objective == "mass":
    prob.model.add_objective("avg_density")
    prob.model.add_constraint("t_max", upper=50.0)
elif objective == "compliance":
    prob.model.add_objective("compliance")
    # This is nonlinear: C(rho) is the RAMP interpolation.
    prob.model.add_constraint("avg_density_p", upper=0.51)
    prob.model.add_constraint("t_max", upper=55.0)
else:
    raise ValueError("objective must be 'mass' or 'compliance'")

prob.driver = om.pyOptSparseDriver()
prob.driver.options["optimizer"] = "IPOPT"
prob.driver.opt_settings["max_iter"] = 500
prob.driver.opt_settings["tol"] = 1.0e-6
prob.driver.opt_settings["print_level"] = 5
prob.driver.opt_settings["print_user_options"] = "yes"

prob.setup()
prob.run_driver()

set_function_from_global(density, prob.get_val("density"))
set_function_from_global(mixed_state, prob.get_val("mixed_states"))

displacements = mixed_state.sub(0).collapse()
displacements.name = "displacements"
temperature = mixed_state.sub(1).collapse()
temperature.name = "temperature"

stiffness = fem.Function(density_space)
stiffness.name = "stiffness"
stiffness.interpolate(
    fem.Expression(C, density_space.element.interpolation_points())
)
stiffness.x.scatter_forward()

stress = fem.Function(density_space)
stress.name = "von_Mises"
stress.interpolate(
    fem.Expression(von_mises, density_space.element.interpolation_points())
)
stress.x.scatter_forward()

output_dir = Path("solutions") / f"battery_pack_{objective}"
if comm.rank == 0:
    output_dir.mkdir(parents=True, exist_ok=True)
comm.barrier()

for filename, function in (
    ("displacements.xdmf", displacements),
    ("temperature.xdmf", temperature),
    ("density.xdmf", density),
    ("stiffness.xdmf", stiffness),
    ("von_Mises.xdmf", stress),
):
    with io.XDMFFile(
        comm, str(output_dir / filename), "w", encoding=io.XDMFFile.Encoding.ASCII
    ) as writer:
        writer.write_mesh(mesh)
        writer.write_function(function, 0.0)

# Preserve the unstructured cells and circular holes in the PNGs.
# Restrict to owned cells to avoid drawing MPI partition ghosts twice.
num_owned_cells = mesh.topology.index_map(mesh.topology.dim).size_local
local_polygons = [
    mesh.geometry.x[mesh.geometry.dofmap[cell], :2].copy()
    for cell in range(num_owned_cells)
]
local_density = np.array(
    [
        density.x.array[density_space.dofmap.cell_dofs(cell)[0]]
        for cell in range(num_owned_cells)
    ],
    dtype=np.float64,
)
local_stiffness = np.array(
    [
        stiffness.x.array[density_space.dofmap.cell_dofs(cell)[0]]
        for cell in range(num_owned_cells)
    ],
    dtype=np.float64,
)
plot_data = comm.gather(
    (local_polygons, local_density, local_stiffness),
    root=0,
)

if comm.rank == 0:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    from matplotlib.colors import LinearSegmentedColormap, Normalize

    # Collect polygons and values from the top-right quadrant
    quadrant_polygons = [
        polygon
        for rank_polygons, _, _ in plot_data
        for polygon in rank_polygons
    ]
    density_values = np.concatenate([part[1] for part in plot_data])
    stiffness_values = np.concatenate([part[2] for part in plot_data])

    # Mirror the quadrant to create the full battery pack
    # Top-right (original), top-left, bottom-left, bottom-right
    def mirror_polygons(polygons, mirror_x=False, mirror_y=False):
        """Mirror polygons across x and/or y axes."""
        mirrored = []
        for poly in polygons:
            new_poly = poly.copy()
            if mirror_x:
                new_poly[:, 0] = -new_poly[:, 0]
            if mirror_y:
                new_poly[:, 1] = -new_poly[:, 1]
            mirrored.append(new_poly)
        return mirrored

    # Create all four quadrants
    polygons = []
    full_density_values = []
    full_stiffness_values = []

    # Top-right quadrant (original)
    polygons.extend(quadrant_polygons)
    full_density_values.append(density_values)
    full_stiffness_values.append(stiffness_values)

    # Top-left quadrant (mirror across x)
    polygons.extend(mirror_polygons(quadrant_polygons, mirror_x=True, mirror_y=False))
    full_density_values.append(density_values)
    full_stiffness_values.append(stiffness_values)

    # Bottom-left quadrant (mirror across both x and y)
    polygons.extend(mirror_polygons(quadrant_polygons, mirror_x=True, mirror_y=True))
    full_density_values.append(density_values)
    full_stiffness_values.append(stiffness_values)

    # Bottom-right quadrant (mirror across y)
    polygons.extend(mirror_polygons(quadrant_polygons, mirror_x=False, mirror_y=True))
    full_density_values.append(density_values)
    full_stiffness_values.append(stiffness_values)

    # Concatenate all values
    full_density_values = np.concatenate(full_density_values)
    full_stiffness_values = np.concatenate(full_stiffness_values)

    cmap = LinearSegmentedColormap.from_list(
        "battery_stiffness",
        [
            (0.00, "#ffffff"),
            (0.15, "#f5edeb"),
            (0.50, "#d4a291"),
            (1.00, "#861d26"),
        ],
    )

    for filename, values, label in (
        ("density.png", full_density_values, "filtered density ρ"),
        (
            "stiffness_factor.png",
            full_stiffness_values,
            "relative stiffness factor C(ρ)",
        ),
    ):
        fig = plt.figure(figsize=(10, 10), facecolor="white")
        ax = fig.add_axes([0.07, 0.25, 0.86, 0.72])
        image = PolyCollection(
            polygons,
            array=values,
            cmap=cmap,
            norm=Normalize(vmin=0.0, vmax=1.0),
            edgecolors="none",
        )
        ax.add_collection(image)
        ax.set_xlim(-LENGTH / 2, LENGTH / 2)
        ax.set_ylim(-WIDTH / 2, WIDTH / 2)
        ax.set_aspect("equal")
        ax.set_axis_off()

        cax = fig.add_axes([0.20, 0.08, 0.60, 0.035])
        cbar = fig.colorbar(image, cax=cax, orientation="horizontal")
        cbar.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        cbar.ax.xaxis.set_ticks_position("top")
        cbar.ax.xaxis.set_label_position("top")
        cbar.set_label(label, labelpad=8, fontsize=15)
        cbar.outline.set_visible(False)
        fig.savefig(output_dir / filename, dpi=180)
        plt.close(fig)
