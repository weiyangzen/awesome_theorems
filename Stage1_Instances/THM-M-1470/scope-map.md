# THM-M-1470 scope map

## Catalog scope preserved

- Target identity: `THM-M-1470`, named `后验误差估计`.
- Catalog attribution and date: Ivo Babuška, 1971.
- Literal gloss: `数值解的误差估计` (error estimation for a numerical solution).
- Recognizable topic boundary: an estimate computed after obtaining a numerical approximation,
  intended to control or assess its error.

This identifies a numerical-analysis theorem family, not one proposition.

## Decisions required before statement freeze

An accountable source correction must select one immutable proposition and freeze:

1. The continuous problem: algebraic, ODE, PDE, eigenvalue, fixed-point, or other model; its
   domain, coefficients, boundary and initial data, exact solution concept, and well-posedness.
2. The discretization and numerical approximation: finite element, Galerkin, finite difference,
   finite volume, iterative solver, time stepping, or another source-defined scheme.
3. The mesh or approximation family, polynomial order, conformity, shape regularity, refinement,
   quadrature, solver, regularity, and consistency assumptions.
4. The error quantity and norm: energy, residual, dual, `L2`, `H1`, goal functional, eigenvalue,
   iterate distance, or another exact quantity, including local versus global aggregation.
5. The computable information and estimator: element and edge residuals, flux equilibration,
   recovery, hierarchical surplus, dual-weighted residual, defect, successive-iterate distance,
   or another construction with every weight and oscillation term.
6. The conclusion: reliability upper bound, efficiency lower bound, a two-sided equivalence,
   asymptotic exactness, estimator reduction, contraction, stopping guarantee, or a conjunction.
7. Every constant and dependency: whether constants are explicit or existential, mesh independent,
   coefficient robust, local or global, and whether data oscillation or higher-order terms occur.
8. Ordered binders, degenerate cases, alternate encodings, logical principles, and the boundary
   between exact proof and numerical or floating-point computation.

These choices change truth conditions and proof obligations. They are a resolution checklist, not
a canonical statement.

## Candidate theorem families not credited

- Reliability of a residual estimator for a source-selected conforming finite-element solution.
- Local or global efficiency, possibly only up to data oscillation and a shape-regularity constant.
- A guaranteed two-sided energy-error bound from an equilibrated flux reconstruction.
- A posteriori control of an eigenpair, time-stepping error, nonlinear iterate, or fixed-point
  iterate under a source-selected model.
- Estimator reduction or contraction used by an adaptive finite-element convergence theorem.

## Degenerate and boundary cases

Source review must explicitly resolve zero exact error, zero estimator, zero forcing, exact
representation of the solution, an empty mesh or approximation family, zero-dimensional spaces,
singular or nonunique continuous problems, inconsistent discrete equations, degenerate elements,
vanishing or unbounded coefficients, nonpositive constants, zero denominators, oscillation-free
data, boundary residuals, local-to-global aggregation, and exact versus inexact solver output.

## Explicit exclusions

- `THM-M-1461` finite element method, `THM-M-1462` Galerkin method, `THM-M-1469` adaptive finite
  element method, and `THM-M-1471` a priori error estimation are separate targets; no proof or
  status transfers.
- A generic best-approximation, Céa, Lax-Milgram, interpolation, stability, or convergence theorem
  alone is not an a posteriori estimator theorem.
- Mathlib's fixed-point `ContractingWith.aposteriori_dist_iterate_fixedPoint_le` is not Babuška's
  finite-element error-bound family and cannot be chosen because its name is convenient.
- A norm inequality, residual definition, estimator structure, or certificate that assumes the
  desired reliability or efficiency inequality supplies no root proof.
- Numerical experiments, effectivity indices, plots, mesh-refinement runs, solver tolerances, and
  floating-point outputs cannot replace a kernel-checked theorem.
- The untrusted label `已验证`, publisher metadata, and the discovery probe supply no H or M credit.

No canonical Lean target, expression fingerprint, checked transport, discovery protocol,
obligation registry, or proof state is frozen at intake.
