# Scope map

## Included claim

- The incompressible Navier-Stokes momentum equation and distributional incompressibility.
- Spatial dimension `d = 2` or `d = 3`, positive viscosity, and finite-energy divergence-free
  initial velocity.
- A solution defined for all nonnegative times in the standard energy class, attaining the initial
  datum in the source-prescribed weak sense and satisfying the energy inequality.
- External forcing only if, and in exactly the function space in which, it occurs in the selected
  source statement.

## Statement-phase decisions

Primary-source inspection must fix the domain (`R^d`, periodic, or bounded), boundary conditions,
real/complex scalars, pressure treatment, test-function class, Bochner/Sobolev spaces, time
representative, force regularity, initial trace, and whether the energy inequality holds for every
time or almost every initial time. It must also fix whether the canonical theorem follows Leray's
whole-space formulation or Hopf's bounded-domain formulation. Binder order and universes follow
that choice.

Degenerate cases needing explicit treatment are zero initial data, zero force, dimension two versus
three, and zero viscosity (excluded from Navier-Stokes existence unless the source says otherwise).

## Exclusions

- Smoothness, uniqueness, or global strong solutions in three dimensions.
- The Euler equation, stationary Navier-Stokes, or a finite-dimensional Galerkin approximation as
  a substitute for the limiting weak solution.
- A structure that assumes existence or the energy inequality as fields.
- A generic PDE fixed-point theorem without a checked instantiation to this exact weak formulation.

The later Lean target must expose concrete weak-form equation, divergence-free space, time/space
integrability, initial trace, and energy inequality rather than encode the conclusion as a premise.
