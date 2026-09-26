# ATOmiCS
ATOmiCS stands for **A**utomated **T**opology **O**ptimization for **m**ultidisciplinary problems using FEn**iCS**. It is a Python module that performs topology optimization for various physics problems with automated derivatives. ATOmiCS is implemented based on [OpenMDAO](https://openmdao.org/) and [FEniCSx](https://fenicsproject.org/). The details of ATOmiCS can be found in the following article:

```
@article{yan2022topology,
  title={Topology optimization with automated derivative computation for multidisciplinary design problems},
  author={Yan, Jiayao and Xiang, Ru and Kamensky, David and Tolley, Michael T and Hwang, John T},
  journal={Structural and Multidisciplinary Optimization},
  volume={65},
  number={5},
  pages={1--20},
  year={2022},
  publisher={Springer}
}
```

A preprint of the above article can be found [here](https://github.com/LSDOlab/lsdo_bib/blob/main/pdf/yan2022topology.pdf).

## Migration from Legacy FEniCS

This repository has been migrated from the original [LSDOlab/atomics](https://github.com/LSDOlab/atomics) repository and now uses **FEniCSx** (the next-generation FEniCS project) instead of legacy FEniCS 2019.1.0. The key changes include:

- **Updated solver backend**: Uses modern `dolfinx` for finite element computations
- **MPI support**: Built-in support for distributed computing via `mpi4py` and PETSc
- **Parallel computation**: Supports multi-process and multi-core optimization workflows

### Parallel Computation

Parallel computation can be enabled for many optimization problems through OpenMDAO's built-in parallel processing capabilities. However, the performance improvement depends on several factors:

- **Problem size**: Small problems may not see speedup due to parallelization overhead exceeding computation time savings
- **Linear solver choice**: Sequential solvers (e.g., direct solvers) provide less parallelization benefit than iterative solvers (e.g., Krylov methods with PETSc preconditioners)
- **Communication overhead**: Fine-grained parallelization in sensitivity computations may be limited by inter-process communication costs
- **Memory scaling**: Very large problems may benefit from distributed memory parallelization via MPI, but smaller problems may not
- **Problem structure**: Loosely coupled multidisciplinary problems often see better parallelization benefits than tightly coupled problems

For typical topology optimization problems, moderate parallelization (2-4 processes) often provides the best balance between speedup and overhead.

Getting started
===============
For a detailed tutorial of ATOMiCS (automated topology optimization using OpenMDAO and FEniCSx), please check our online documentations (lsdolab.github.io/atomics/).

Core Dependencies
-----------------
- **OpenMDAO** (3.35.0+): Multidisciplinary optimization framework
- **FEniCSx/dolfinx**: Finite element solver for PDE-constrained optimization
- **PETSc**: Scalable linear algebra solvers for distributed computing
- **mpi4py**: Python bindings for MPI parallel computing
- **NumPy**: Numerical computing
- **Dash**: Dashboard components for visualization

Installing
----------
To install ATOMiCS and run topology optimization problems, you need to follow these steps:

1. **Install FEniCSx** (recommended via conda):

   ```bash
   conda create -n atomics-env -c conda-forge fenics-dolfinx python=3.11
   conda activate atomics-env
   ```

   This will install FEniCSx with all necessary dependencies including PETSc and mpi4py.

2. **Install OpenMDAO**:

   ```bash
   pip install 'openmdao[all]'
   ```

3. **Install ATOMiCS**:

   ```bash
   git clone https://github.com/alfiyandyhr/atomics.git
   cd atomics
   pip install -e .
   ```

Optional Optimizers
-------------------
While the ``scipy`` optimizer in OpenMDAO works for small-scale problems, we recommend using more advanced optimizers for better performance:

- **IPOPT**: Open-source large-scale nonlinear optimizer (https://github.com/coin-or/Ipopt/)
- **SNOPT**: Commercial optimizer with superior performance for nonlinear problems (http://ccom.ucsd.edu/~optimizers/downloads/)
