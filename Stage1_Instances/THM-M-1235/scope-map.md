# Scope map

## Included theorem family

- The two-dimensional incompressible Euler equations for a homogeneous ideal fluid on the exact
  spatial domain used by the selected primary result.
- Divergence-free initial velocity (or the source-equivalent stream-function/vorticity data), with
  all source regularity and boundary compatibility conditions.
- Classical existence on every finite forward time interval, or an equivalent global continuation
  statement, exactly as supported by the selected source theorem.
- Pressure reconstruction, uniqueness, continuous dependence, and conservation laws only when
  they occur in the selected result or are separately identified consequences.

## Decisions required before statement freeze

The statement phase must inspect a stable primary-source copy and fix the planar domain and its
boundary smoothness/topology, Eulerian or Lagrangian formulation, velocity and pressure
regularities, initial and boundary conditions, time interval convention, and the meaning of
classical solution. It must determine whether the theorem states uniqueness, how pressure is
normalized, and whether globality means one solution on `[0, infinity)` or compatible solutions on
all bounded intervals. Binder order, scalar field, derivative conventions, and degenerate cases
must then be frozen explicitly.

## Explicit exclusions

- Three-dimensional Euler global regularity or any theorem assuming the desired global solution.
- Navier-Stokes existence, a finite-dimensional particle/ODE model, or a local-existence theorem
  substituted for the global Euler conclusion.
- A periodic-torus or whole-plane theorem substituted for a bounded-domain source statement (or
  conversely) without a checked equivalence.
- Weak or measure-valued existence substituted for the source's classical solution class.
- Global existence derived merely by adding a continuation hypothesis as an assumption.

The formal target must expose the concrete equation, domain, data class, solution predicate, and
global time quantification, or record a precise infrastructure blocker.
