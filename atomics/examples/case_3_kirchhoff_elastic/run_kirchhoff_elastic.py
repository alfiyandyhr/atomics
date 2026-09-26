from pathlib import Path
import numpy as np
import ufl
from mpi4py import MPI
from petsc4py import PETSc
from dolfinx import fem, io
from dolfinx import mesh as dmesh
import openmdao.api as om
from atomics.api import PDEProblem, AtomicsGroup
from atomics.pdes.st_kirchhoff import get_residual_form
from atomics.general_filter_comp import GeneralFilterComp


comm = MPI.COMM_WORLD

'''
1. Define the mesh
'''
NUM_ELEMENTS_X = 80
NUM_ELEMENTS_Y = 40
LENGTH_X = 160.0
LENGTH_Y = 80.0

mesh = dmesh.create_rectangle(
    comm=comm,
    points=(
        (0.0, 0.0),
        (LENGTH_X, LENGTH_Y),
    ),
    n=(NUM_ELEMENTS_X, NUM_ELEMENTS_Y),
    cell_type=dmesh.CellType.quadrilateral,
    dtype=np.float64,
)

'''
2. Define the traction boundary conditions
'''
# Apply the traction around the middle of the right edge.
TRACTION_TAG = 6
facet_dim = mesh.topology.dim - 1
traction_half_width = LENGTH_Y / NUM_ELEMENTS_Y


def traction_boundary(x):
    return np.logical_and(
        np.isclose(x[0], LENGTH_X),
        np.abs(x[1] - LENGTH_Y / 2.0)
        <= traction_half_width + 1.0e-12,
    )


traction_facets = dmesh.locate_entities_boundary(
    mesh,
    dim=facet_dim,
    marker=traction_boundary,
)
traction_facets = np.sort(traction_facets)

facet_tags = dmesh.meshtags(
    mesh,
    facet_dim,
    traction_facets,
    np.full(
        traction_facets.size,
        TRACTION_TAG,
        dtype=np.int32,
    ),
)

dss = ufl.Measure(
    "ds",
    domain=mesh,
    subdomain_data=facet_tags,
)

traction = fem.Constant(
    mesh,
    (
        PETSc.ScalarType(0.0),
        PETSc.ScalarType(-1.0 / 4.0),
    ),
)

'''
3. Setup the PDE problem
'''
pde_problem = PDEProblem(mesh)

# Cell-wise density input.
density_function_space = fem.functionspace(
    mesh,
    ("Discontinuous Lagrange", 0),
)
density_function = fem.Function(density_function_space)
density_function.name = "density"

# Give setup-time Jacobian assembly a nonzero stiffness coefficient.
density_function.x.array[:] = 1.0
density_function.x.scatter_forward()

pde_problem.add_input('density', density_function)

# Vector displacement state.
displacements_function_space = fem.functionspace(
    mesh,
    (
        "Lagrange",
        1,
        (mesh.geometry.dim,),
    ),
)
displacements_function = fem.Function(
    displacements_function_space
)
displacements_function.name = "displacements"

v = ufl.TestFunction(displacements_function_space)

method = 'SIMP'
residual_form = get_residual_form(
    displacements_function, 
    v, 
    density_function,
    method=method
)

residual_form -= (
    ufl.dot(traction, v)
    * dss(TRACTION_TAG)
)

pde_problem.add_state(
    'displacements',
    displacements_function,
    residual_form,
    'density',
)

# Average-density constraint. assemble_scalar returns a rank-local
# contribution, so explicitly sum the volume over MPI.
dx = ufl.Measure("dx", domain=mesh)
one = fem.Constant(mesh, PETSc.ScalarType(1.0))

local_volume = fem.assemble_scalar(
    fem.form(one * dx)
)
volume = mesh.comm.allreduce(
    local_volume,
    op=MPI.SUM,
)

avg_density_form = density_function / volume * dx
pde_problem.add_scalar_output(
    'avg_density',
    avg_density_form,
    'density',
)

# Compliance objective.
compliance_form = (
    ufl.dot(traction, displacements_function)
    * dss(TRACTION_TAG)
)
pde_problem.add_scalar_output(
    'compliance',
    compliance_form,
    'displacements',
)

# Clamp the left edge.
left_facets = dmesh.locate_entities_boundary(
    mesh,
    dim=facet_dim,
    marker=lambda x: np.isclose(x[0], 0.0),
)
left_dofs = fem.locate_dofs_topological(
    displacements_function_space,
    entity_dim=facet_dim,
    entities=left_facets,
)

zero_displacement = np.zeros(
    mesh.geometry.dim,
    dtype=PETSc.ScalarType,
)
left_bc = fem.dirichletbc(
    value=zero_displacement,
    dofs=left_dofs,
    V=displacements_function_space,
)
pde_problem.add_bc(left_bc)

'''
4. Setup the optimization problem
'''
prob = om.Problem(reports=True)

density_dofmap = density_function_space.dofmap
num_dof_density = (
    density_dofmap.index_map.size_global
    * density_dofmap.index_map_bs
)

comp = om.IndepVarComp()
comp.add_output(
    'density_unfiltered',
    shape=num_dof_density,
    val=np.ones(num_dof_density, dtype=np.float64),
)
prob.model.add_subsystem(
    'indep_var_comp',
    comp,
    promotes=['*'],
)

comp = GeneralFilterComp(
    density_function_space=density_function_space,
)
prob.model.add_subsystem(
    'general_filter_comp',
    comp,
    promotes=['*'],
)

group = AtomicsGroup(
    pde_problem=pde_problem,
    problem_type='nonlinear_problem',
    # Uses PETSc LU/MUMPS for the nonlinear solve and for the
    # state-equation total-derivative solves.
    linear_solver_='fenics_direct',
    fail_on_nonconvergence=True,
)
prob.model.add_subsystem(
    'atomics_group',
    group,
    promotes=['*'],
)

prob.model.add_design_var(
    'density_unfiltered',
    upper=1.0,
    lower=1.0e-3,
)
prob.model.add_objective('compliance')
prob.model.add_constraint(
    'avg_density',
    upper=0.50,
)

# Use IPOPT through pyOptSparse.
prob.driver = om.pyOptSparseDriver()
prob.driver.options['optimizer'] = 'IPOPT'
prob.driver.opt_settings['max_iter'] = 500
prob.driver.opt_settings['tol'] = 1.0e-3

prob.setup()

if False:
    prob.run_model()
    if comm.rank == 0:
        print("Compliance:", prob.get_val("compliance"))
        print("Average density:", prob.get_val("avg_density"))
else:
    prob.run_driver()


'''
5. Transfer the final replicated OpenMDAO arrays to distributed
   DOLFINx Functions and save the solution.
'''


def set_function_from_global(function, global_values):
    """Set owned Function DOFs from a replicated global vector."""
    global_values = np.asarray(global_values).reshape(-1)

    dofmap = function.function_space.dofmap
    index_map = dofmap.index_map
    block_size = dofmap.index_map_bs

    owned_blocks = index_map.size_local
    owned_size = owned_blocks * block_size

    global_blocks = index_map.local_to_global(
        np.arange(owned_blocks, dtype=np.int32)
    )
    owned_global_dofs = (
        block_size * global_blocks[:, None]
        + np.arange(
            block_size,
            dtype=np.int64,
        )[None, :]
    ).reshape(-1)

    function.x.array[:owned_size] = (
        global_values[owned_global_dofs]
    )
    function.x.scatter_forward()


set_function_from_global(
    density_function,
    prob.get_val('density'),
)
set_function_from_global(
    displacements_function,
    prob.get_val('displacements'),
)

# Evaluate the dimensionless SIMP stiffness factor C(rho) = rho**3
# in the DG0 density space. It differs from filtered density rho.
penalized_density = fem.Function(
    density_function_space
)
penalized_density.name = "penalized_density"

if method == 'SIMP':
    penalized_density_ufl = density_function**3
else:
    penalized_density_ufl = (
        density_function
        / (1.0 + 8.0 * (1.0 - density_function))
    )

penalized_density_expression = fem.Expression(
    penalized_density_ufl,
    density_function_space.element.interpolation_points(),
)
penalized_density.interpolate(
    penalized_density_expression
)
penalized_density.x.scatter_forward()

output_directory = Path(
    "solutions/"
)

if comm.rank == 0:
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )
comm.barrier()

# The XDMF files are written in ASCII format only (no HDF5).
with io.XDMFFile(
    mesh.comm,
    str(output_directory / "displacement.xdmf"),
    "w",
    encoding=io.XDMFFile.Encoding.ASCII,
) as displacement_writer:
    displacement_writer.write_mesh(mesh)
    displacement_writer.write_function(
        displacements_function,
        0.0,
    )

with io.XDMFFile(
    mesh.comm,
    str(output_directory / "penalized_density.xdmf"),
    "w",
    encoding=io.XDMFFile.Encoding.ASCII,
) as density_writer:
    density_writer.write_mesh(mesh)
    density_writer.write_function(
        penalized_density,
        0.0,
    )

# Gather only owned DG0 DOFs, excluding MPI ghosts.
owned_dofs = density_function_space.dofmap.index_map.size_local
plot_data = comm.gather(
    (
        density_function_space.tabulate_dof_coordinates()[
            :owned_dofs, :2
        ].copy(),
        density_function.x.array[:owned_dofs].copy(),
        penalized_density.x.array[:owned_dofs].copy(),
    ),
    root=0,
)

if comm.rank == 0:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    centers = np.concatenate([part[0] for part in plot_data])
    density_values = np.concatenate([part[1] for part in plot_data])
    penalized_values = np.concatenate([part[2] for part in plot_data])

    ix = np.rint(
        centers[:, 0] / (LENGTH_X / NUM_ELEMENTS_X) - 0.5
    ).astype(int)
    iy = np.rint(
        centers[:, 1] / (LENGTH_Y / NUM_ELEMENTS_Y) - 0.5
    ).astype(int)
    linear_indices = iy * NUM_ELEMENTS_X + ix
    if (
        len(centers) != NUM_ELEMENTS_X * NUM_ELEMENTS_Y
        or np.any(ix < 0) or np.any(ix >= NUM_ELEMENTS_X)
        or np.any(iy < 0) or np.any(iy >= NUM_ELEMENTS_Y)
        or len(np.unique(linear_indices)) != len(centers)
    ):
        raise RuntimeError("Could not map DG0 values to the image grid")

    cmap = LinearSegmentedColormap.from_list(
        "beam_stiffness",
        [
            (0.00, "#ffffff"),
            (0.15, "#f5edeb"),
            (0.50, "#d4a291"),
            (1.00, "#861d26"),
        ],
    )
    cmap.set_bad("white")

    for filename, values, label in (
        ("density.png", density_values, "filtered density ρ"),
        (
            "stiffness_factor.png",
            penalized_values,
            "relative stiffness factor C(ρ)",
        ),
    ):
        image = np.empty((NUM_ELEMENTS_Y, NUM_ELEMENTS_X))
        image[iy, ix] = values
        image = np.ma.masked_less(image, 1.0e-3)

        fig = plt.figure(figsize=(10, 6), facecolor="white")
        ax = fig.add_axes([0.07, 0.25, 0.86, 0.72])
        im = ax.imshow(
            image,
            origin="lower",
            extent=(0, LENGTH_X, 0, LENGTH_Y),
            interpolation="nearest",
            cmap=cmap,
            vmin=0.0,
            vmax=1.0,
            aspect="equal",
        )
        ax.set_axis_off()
        cax = fig.add_axes([0.20, 0.08, 0.60, 0.035])
        cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
        cbar.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        cbar.ax.xaxis.set_ticks_position("top")
        cbar.ax.xaxis.set_label_position("top")
        cbar.set_label(label, labelpad=8, fontsize=15)
        cbar.outline.set_visible(False)
        fig.savefig(output_directory / filename, dpi=180)
        plt.close(fig)
