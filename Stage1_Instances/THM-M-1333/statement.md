# Statement certificate

`Statement.lean` freezes the standard finite-dimensional local Peano theorem. Joint continuity on
an open neighborhood of `(t0, x0)` yields a solution on a symmetric closed interval of strictly
positive radius. `HasDerivWithinAt` makes the endpoint convention explicit, and graph membership
keeps every evaluation of the vector field inside its declared domain.

The only direct import is `Mathlib.Analysis.Calculus.Deriv.Basic`. The checked theorem
`peanoExistenceTarget_iff_expandedTarget` expands the state-space abbreviation and solution
predicate definitionally. The validator separately elaborates and rejects expression identity for
mutations of continuity, state domain, binder order, and the positive-radius boundary.

## Fidelity boundary

The catalogue provides only the broad phrase "existence of solutions under a continuity
condition." It does not pinpoint a primary-source proposition. The formal target therefore fixes
the conventional finite-dimensional local formulation without claiming `H0`: the anchor-audit
phase must still review a primary source and its exact scope. This statement does not add a
Lipschitz condition, uniqueness, a quantitative lifespan, or global continuation.

This certificate is statement-only. It provides no proof of `PeanoExistenceTarget` and no theorem
completion evidence.
