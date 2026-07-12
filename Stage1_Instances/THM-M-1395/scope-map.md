# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1395`, the title `有限差分法`, the gloss `ODE的数值解法`, the
attribution to many mathematicians, and the twentieth-century date. Importance `high` and status
`已验证` are catalog metadata, not human-source or kernel evidence.

The wording constrains the subject to finite-difference numerical treatment of ordinary
differential equations. It does not identify an initial-value or boundary-value problem, an
algorithm, or one proposition. A later statement phase may select a result only from an immutable,
independently reviewed source passage.

## Candidate families not credited

The following are distinct discovery hypotheses, not accepted formulations of this target:

1. Forward, backward, or centered difference approximation of a derivative, with a local
   truncation-error estimate.
2. A one-step initial-value recurrence, including explicit or implicit Euler as a special case.
3. A finite-difference boundary-value discretization and solvability of the resulting algebraic
   system.
4. Consistency or an order-of-accuracy theorem for a chosen scheme.
5. Zero-stability, absolute stability, or another source-specific stability theorem.
6. Convergence of discrete approximations to the exact ODE solution as the mesh tends to zero.
7. A local or global error bound in a named norm on a fixed or variable grid.

A method label cannot silently turn these results into a conjunction, and no one special case may
replace an unstated general root.

## Proposition-changing decisions

Before statement work can close, an immutable source and independent review must fix:

- the exact numbered theorem or source-defined conjunction and its incorporated definitions;
- an initial-value problem, boundary-value problem, or another ODE formulation;
- scalar or vector state, real or complex field, finite dimension or Banach-space generality, and
  all universes and typeclass assumptions;
- autonomous or nonautonomous vector field, interval, initial or boundary data, and the exact
  classical, weak, or other solution notion;
- coefficient and exact-solution regularity, Lipschitz, monotonicity, coercivity, invertibility, or
  other well-posedness hypotheses;
- uniform or nonuniform mesh, positive step size, indexing range, endpoint treatment, and any
  step-size restrictions;
- the difference stencil, explicit or implicit update, startup values, nonlinear solve, and exact
  discrete-solution definition;
- consistency, stability, convergence, solvability, or error conclusion; its norm, constants,
  order, and quantifier order; and
- every boundary case, correction, erratum, proof boundary, and source-to-node mapping.

## Degenerate cases to resolve

- zero, negative, or excessively large step size; an empty grid; a single grid point; and a final
  time not aligned with the mesh;
- zero-dimensional state, constant or zero vector field, equilibrium solutions, and an interval of
  zero length;
- nonsmooth or non-Lipschitz vector fields, nonunique or finite-time-blow-up solutions, and data
  outside the source domain;
- singular implicit updates or boundary matrices, multiple discrete solutions, and inconsistent
  initial or boundary data;
- local versus global error, finite versus infinite time horizons, norm choice, and whether error
  constants are uniform in the mesh; and
- order zero, exact polynomial cases, roundoff versus exact arithmetic, and variable-step grids.

No case is excluded at intake because no proposition has been selected.

## Neighbor and substitution exclusions

- `THM-M-1465` owns the separate PDE finite-difference-discretization gloss; its statement and
  evidence cannot be imported into this ODE target.
- `THM-M-1394` shooting, `THM-M-1396` Runge-Kutta, `THM-M-1397` Adams, `THM-M-1398` stiff
  equations, and `THM-M-1399` backward differentiation retain their own target ownership.
- The algebraic operator `fwdDiff`, its Gregory-Newton identities, a generic Taylor theorem, or an
  ODE integral-curve predicate is infrastructure, not a numerical-method convergence theorem.
- Defining an update rule or calculating one sample trajectory is not a proof of consistency,
  stability, convergence, solvability, or an error bound.
- A structure that stores the exact solution, discrete solution, desired bound, or convergence
  result as data supplies no proof.
- Floating-point experiments, plots, sampled errors, or unchecked solver output receive no machine
  proof credit.
- The repository's `已验证` label and this intake probe receive no source-fidelity or kernel credit.

## Formal boundary

Pinned mathlib exposes an algebraic forward-difference operator and iterated-difference identities,
ODE integral-curve predicates, and generic Taylor estimates. The probe authenticates those adjacent
interfaces only. It does not choose a grid, scheme, discrete solution, error measure, or limiting
claim. The exhaustive repo-local, mathlib, and external Lean anchor audit remains downstream.
