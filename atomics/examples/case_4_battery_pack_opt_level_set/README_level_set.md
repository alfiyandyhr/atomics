# Battery-pack level-set example

`run_battery_pack_top_opt_level_set.py` reuses `PDEProblem`, `AtomicsGroup`,
the original thermoelastic residual and ATOmiCS's automatic derivatives.
No framework files need modification. The density example stays unchanged.

The new design variables are signed control-grid values, rather than one
material density per finite element. Bilinear interpolation defines a
continuous field `phi(x)` on a 9 × 9 control grid over the quadrant.
The zero contour defines the interface; positive values denote solid.
At DG0 cell centroids, the material map is

```text
H_beta(phi) = 0.5 * (1 + tanh(beta * phi))
rho = rho_min + (1 - rho_min) * H_beta(phi),  rho_min = 1e-4
```

An explicit OpenMDAO component supplies the sparse analytic Jacobian, so the
existing PDE derivatives propagate back to the level-set controls. Cells in
the original prescribed-solid bands and every cell adjacent to a loaded or
heated boundary have `rho = 1` and zero design sensitivity. This enforces
prescribed solids directly; it replaces the density example's equality
constraints on filtered densities.

This is a **regularized parameterized level-set method**. A classical
Hamilton–Jacobi method would additionally need interface velocities,
a transport solver, reinitialization and handling of topology changes.
Those capabilities are not implemented here.

For background on optimizing parameters of an implicit interface, see
[Wang and Wang (2006)](https://onlinelibrary.wiley.com/doi/10.1002/nme.1536).
That work uses radial basis functions; this example uses bilinear controls.

Run from the repository root in the same FEniCSx/OpenMDAO environment as the
original example:

```bash
python atomics/examples/case_4_battery_pack_top_opt/run_battery_pack_top_opt_level_set.py
python atomics/examples/case_4_battery_pack_top_opt/run_battery_pack_top_opt_level_set.py --objective compliance
```

IPOPT through pyOptSparse is the default; `--optimizer SLSQP` selects SciPy.
The default continuation stages use `beta = 2, 4`, with up to 500
iterations **per stage**, retaining the previous controls as the next
initial guess. A failed stage stops continuation, exports its current
design with a failure message and returns a nonzero exit status.
`--run-model` evaluates only the initial field; `--check-partials` checks the
new component by complex step.
`--control-points`, `--mesh-size`, `--betas`, and `--output-dir` are configurable.

The mass objective integrates `H_beta(phi)`, excluding the numerical void
floor. The compliance case preserves the original `avg_density_p <= 0.51`
constraint: it limits the average RAMP stiffness factor, not material volume.
The original temperature limits (50 for mass, 55 for compliance), loads,
thermal expansion/stress convention and RAMP law are retained. Stress is
reported, as in the original example; there is no stress constraint.

Outputs go to `solutions/battery_pack_<objective>_level_set/`. They include
XDMF fields for level set, material indicator, ersatz density, binary solid
region, displacement, temperature, stiffness and stress; PNGs for material,
stiffness and the zero contour; and an NPZ containing optimized controls.
`level_set.xdmf` is a CG1 nodal approximation of the continuous control-grid
field. `level_set_centroids.xdmf` records the exact samples used by the map.
The prescribed-solid mask overrides the raw level-set sign.

Finite-beta designs contain a transition region. Sharpening does not
guarantee a binary design, and the control spacing does not guarantee a
minimum feature size or connectivity. The binary solid-region export and
zero-contour image are visualizations; the reported physics use regularized
material. Verify mesh/control-grid resolution and analyze a binary geometry
separately before interpreting it as a finished design.

Validation with DOLFINx 0.9 and OpenMDAO 3.45 included complex-step checks of
the material map, finite-difference checks of PDE total derivatives, and
serial/two-rank MPI model evaluations and exports. Both objective modes
converged through all three stages on a coarse 0.012 m mesh with 5 × 5
controls. At the default resolution, both objectives converged for beta 2
and 4. An additional beta 8 stage converged for compliance; mass satisfied
the temperature bound but reached the iteration limit. To experiment with
sharper interfaces use `--betas 2 4 8`; treat a failed stage as an unfinished
optimization. Increasing beta can worsen conditioning and convergence;
convergence is not guaranteed.

Component regression checks (no FEniCS installation needed):

```bash
python -m unittest discover -s atomics/examples/case_4_battery_pack_top_opt -p 'test_level_set_material.py'
```
