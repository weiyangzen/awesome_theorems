# THM-M-1465 scope map

## Preserved repository scope

- Target identity: `THM-M-1465`, named `有限差分法` (finite difference method).
- Catalog attribution and date: many mathematicians, twentieth century.
- Literal gloss: `偏微分方程的差分离散` (finite-difference discretization of PDEs).
- Subject boundary: finite-difference spatial or space-time discretization of partial
  differential equations in numerical analysis.

This is all the mathematical scope fixed by the repository. It does not determine a proposition.

## Candidate theorem families not credited

1. Consistency or an order estimate for a three-, five-, nine-, or other source-defined stencil.
2. Existence or uniqueness of the discrete solution of an elliptic boundary-value problem.
3. Stability and convergence of a finite-difference Poisson or other elliptic scheme.
4. Semidiscrete method-of-lines consistency, stability, or convergence for a parabolic PDE.
5. Fully discrete explicit or implicit heat-equation stability and error estimates.
6. A hyperbolic upwind, Lax-Friedrichs, Lax-Wendroff, leapfrog, or other scheme theorem.
7. A source-specific CFL necessity/sufficiency result or von Neumann stability calculation.

These are separate possible roots, not an accepted conjunction or interchangeable special cases.

## Decisions required before statement freeze

An approved target correction must select one immutable source proposition and freeze:

1. The PDE and class: linear or nonlinear, scalar or system, elliptic, parabolic, hyperbolic,
   mixed, stationary, or time dependent.
2. The coefficient and solution carriers, spatial dimension, continuous domain, time interval,
   coefficient/data regularity, and classical, weak, viscosity, or other solution notion.
3. Initial and boundary conditions, compatibility, well-posedness, coercivity, monotonicity,
   smoothness, and every other analytic hypothesis.
4. Grid geometry, index sets, spatial and time step parameters, uniformity, refinement regime,
   endpoint or boundary treatment, ghost values, and admissible mesh restrictions.
5. The discrete spatial operator, time integrator, stencil, explicit/implicit recurrence,
   startup values, algebraic solve, and precise discrete-solution predicate.
6. The conclusion: local truncation error, consistency/order, discrete solvability, stability,
   convergence, or error bound, including norm, constants, rate, quantifier order, and whether
   bounds are uniform as mesh sizes tend to zero.
7. Exact versus floating-point arithmetic, roundoff and solver tolerances, computational
   certificates, ordered binders, minimal imports, profiles, checked encodings, and mutations.

Each choice changes truth conditions and proof obligations. This list is a resolution checklist,
not a canonical claim.

## Boundary and degenerate cases

Source review must decide empty, singleton, zero-dimensional, and nonrectangular grids; zero,
negative, unequal, or nonconforming mesh sizes; a final time not aligned with the time grid; empty
or degenerate domains; corners and mixed or incompatible boundary data; nonsmooth coefficients,
data, domains, or solutions; nonunique or nonexistent continuous solutions; singular discrete
systems; multiple or nonexistent discrete solutions; unstable parameter regimes; exact-polynomial
and constant solutions; finite versus infinite time; and constants that depend on the mesh,
domain, solution, or final time.

No case is excluded at intake because no proposition has been selected.

## Neighbor and substitution exclusions

- `THM-M-1395` owns the separate same-name ODE gloss `ODE的数值解法`; its statement and evidence
  cannot be merged into this PDE target.
- `THM-M-1461` finite elements, `THM-M-1466` finite volumes, and `THM-M-1460` spectral methods
  are different discretization families and grant no proof credit here.
- `THM-M-1472` Lax equivalence, `THM-M-1473` CFL, and `THM-M-1474` von Neumann stability are
  separately cataloged results; none may silently become this root.
- A five-point Laplacian formula, derivative approximation, one heat/advection scheme, or other
  convenient special case cannot substitute for the unfrozen method-family gloss.
- Algebraic `fwdDiff`, the continuous Laplacian, and generic Taylor remainders are substrate only.
- Defining a grid or discrete operator, assuming the desired stability/error result as data, or
  running a finite computation or numerical experiment supplies no theorem closure.
- The catalog's `已验证` label and the discovery probe supply no H or M credit.

## Formal boundary and handoff

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` exposes algebraic
forward-difference identities, the continuous finite-dimensional Laplacian, and a one-dimensional
Taylor remainder bound. A bounded search found no finite-difference PDE scheme, discrete solution,
or scheme-analysis declaration in pinned mathlib or tracked repo-local Lean. This is intake
discovery only, not an exhaustive downstream anchor audit or a global absence proof.

The statement phase must first replace the catalog method label with an independently reviewed,
source-selected truth-valued proposition. Only later phases may freeze a formal target,
obligations, typed graphs, proof bodies, composition, trust closure, or completion state.
