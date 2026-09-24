from mpi4py import MPI
import numpy as np
from scipy import sparse, spatial
from openmdao.api import ExplicitComponent


class GeneralFilterComp(ExplicitComponent):
    """
    GeneralFilterComp calculates the filtered densities
    with its derivatives.
    The filter radius is N times the average element size.
    Parameters
    ----------
    density_function_space
        The DOLFINx function space of the density variables.
    num_element_filtered : float
        The filter radius as a multiple of the average of the minimum
        and maximum cell sizes.
    Returns
    -------
    outputs[density] numpy array
        Filtered densities.
    """

    def initialize(self):
        self.options.declare('density_function_space')
        self.options.declare('num_element_filtered', default=2.)

    def setup(self):
        density_function_space = self.options['density_function_space']
        num_element_filtered = self.options['num_element_filtered']

        mesh = density_function_space.mesh
        comm = mesh.comm
        dofmap = density_function_space.dofmap
        index_map = dofmap.index_map

        # Density is expected to be a scalar field. Supporting blocked
        # vector or tensor spaces would require expanding each DOF
        # coordinate into its scalar components.
        if dofmap.index_map_bs != 1:
            raise ValueError(
                "GeneralFilterComp requires a scalar density function "
                "space with index-map block size one."
            )

        num_owned_dofs = index_map.size_local
        num_dofs = index_map.size_global

        self.add_input('density_unfiltered', shape=num_dofs)
        self.add_output('density', shape=num_dofs)

        # tabulate_dof_coordinates() returns coordinates for locally
        # available DOFs, including ghosts. Retain the owned coordinates
        # and gather them into the global DOLFINx DOF ordering.
        local_coordinates = (
            density_function_space.tabulate_dof_coordinates()
        )
        geometric_dimension = mesh.geometry.dim
        owned_coordinates = np.asarray(
            local_coordinates[:num_owned_dofs, :geometric_dimension]
        ).copy()

        owned_global_dofs = index_map.local_to_global(
            np.arange(num_owned_dofs, dtype=np.int32)
        )

        gathered_coordinates = comm.allgather(
            (owned_global_dofs, owned_coordinates)
        )

        global_coordinates = np.empty(
            (num_dofs, geometric_dimension),
            dtype=owned_coordinates.dtype,
        )
        coordinates_set = np.zeros(num_dofs, dtype=bool)

        for global_dofs, coordinates in gathered_coordinates:
            global_coordinates[global_dofs, :] = coordinates
            coordinates_set[global_dofs] = True

        if not np.all(coordinates_set):
            missing_dofs = np.flatnonzero(~coordinates_set)
            raise RuntimeError(
                "Could not determine coordinates for global density "
                "DOFs {}.".format(missing_dofs.tolist())
            )

        # DOLFINx replaces Mesh.hmin()/hmax() with Mesh.h(), which
        # computes the geometric size of specified mesh entities.
        topological_dimension = mesh.topology.dim
        cell_index_map = mesh.topology.index_map(
            topological_dimension
        )
        owned_cells = np.arange(
            cell_index_map.size_local,
            dtype=np.int32,
        )
        local_cell_sizes = mesh.h(
            topological_dimension,
            owned_cells,
        )

        if local_cell_sizes.size:
            local_mesh_size_min = float(np.min(local_cell_sizes))
            local_mesh_size_max = float(np.max(local_cell_sizes))
        else:
            local_mesh_size_min = np.inf
            local_mesh_size_max = -np.inf

        mesh_size_min = comm.allreduce(
            local_mesh_size_min,
            op=MPI.MIN,
        )
        mesh_size_max = comm.allreduce(
            local_mesh_size_max,
            op=MPI.MAX,
        )

        if not (
            np.isfinite(mesh_size_min)
            and np.isfinite(mesh_size_max)
        ):
            raise ValueError(
                "Cannot construct a density filter on a mesh with no "
                "owned cells."
            )

        radius = (
            float(num_element_filtered)
            * 0.5
            * (mesh_size_max + mesh_size_min)
        )

        if radius <= 0.0:
            raise ValueError(
                "The density-filter radius must be positive; got {}."
                .format(radius)
            )

        weight_ij = []
        rows = []
        cols = []

        # Build the tree only once and query all global DOF coordinates.
        tree = spatial.cKDTree(global_coordinates)
        neighbor_lists = tree.query_ball_point(
            global_coordinates,
            radius,
        )

        for i, neighbors in enumerate(neighbor_lists):
            # Sorting provides a deterministic OpenMDAO sparsity pattern.
            neighbors = np.asarray(
                sorted(neighbors),
                dtype=np.int64,
            )

            distances = np.linalg.norm(
                global_coordinates[i]
                - global_coordinates[neighbors],
                axis=1,
            )
            unnormalized_weights = np.maximum(
                radius - distances,
                0.0,
            )
            weight_sum = np.sum(unnormalized_weights)

            if weight_sum <= 0.0:
                raise RuntimeError(
                    "Density DOF {} has no positive filter weights."
                    .format(i)
                )

            normalized_weights = (
                unnormalized_weights / weight_sum
            )

            for j, weight in zip(neighbors, normalized_weights):
                rows.append(i)
                cols.append(j)
                weight_ij.append(weight)

        rows = np.asarray(rows, dtype=np.int64)
        cols = np.asarray(cols, dtype=np.int64)
        weight_ij = np.asarray(weight_ij)

        self.weight_mtx = sparse.csr_matrix(
            (weight_ij, (rows, cols)),
            shape=(num_dofs, num_dofs),
        )

        self.declare_partials(
            'density',
            'density_unfiltered',
            rows=rows,
            cols=cols,
            val=weight_ij,
        )

    def compute(self, inputs, outputs):
        outputs['density'] = self.weight_mtx.dot(
            inputs['density_unfiltered']
        )
