# Scope map

## Preserved theorem family

The intake preserves the ODE solution-sensitivity family named by the catalog. A later statement
phase may select a root only after an immutable authoritative source passage is mapped and
independently reviewed. Candidate mathematical components, none yet credited as the theorem, are:

- a source-selected time domain and finite-dimensional or Banach state space;
- an autonomous or time-dependent vector field, possibly with an external parameter;
- a unique source-defined local or maximal solution and a common interval of existence;
- a base initial state, initial time, parameter, and corresponding base trajectory;
- a derivative of the solution map with respect to initial state, initial time, parameter, or a
  specified combination;
- a homogeneous or inhomogeneous linear ODE along the base trajectory; and
- a source-specified initial tangent or linear-map condition.

## Decisions required at statement freeze

The statement phase must freeze all of the following from an approved source rather than from a
textbook convention:

1. The exact edition, result or equation locator, incorporated definitions, proof boundary,
   correction history, and independent review.
2. Whether the root asserts differentiability of the solution map, the equation satisfied by an
   already-assumed derivative, existence and uniqueness for the linearized equation, or a bundle of
   these claims.
3. Whether sensitivity is with respect to initial state, initial time, a scalar parameter, a
   vector-valued parameter, the vector field itself, or several variables jointly.
4. Whether the ODE is autonomous or nonautonomous and whether the state and parameter spaces are
   real finite-dimensional spaces or more general complete normed spaces.
5. The state domain, parameter domain, time interval, neighborhood, and exact common-existence
   condition for the compared solutions.
6. Every continuity, local-Lipschitz, differentiability, and higher-regularity hypothesis on the
   vector field, including which variables each derivative concerns.
7. The solution encoding: classical derivative, derivative within an interval, integral curve,
   local flow, maximal flow, or another source-defined object.
8. The exact Jacobian or Frechet derivative orientation and whether sensitivities are vectors,
   matrices, or continuous linear maps.
9. Homogeneous initial-state linearization versus the inhomogeneous parameter equation, including
   every forcing term and initial condition.
10. The conclusion's ordered binders, quantifier dependencies, endpoint semantics, regularity, and
    uniqueness strength.

## Degenerate and boundary cases

Source review must explicitly dispose of zero-width intervals; empty state or parameter domains;
zero-dimensional state or parameter spaces; constant vector fields; equilibrium trajectories;
zero tangent directions; parameters absent from the field; parameter-dependent initial data;
singular or noninvertible state Jacobians; solutions approaching the boundary of the source domain;
and loss of a common existence interval. These cases can change the initial condition, forcing
term, or truth of the intended claim.

## Neighbor and substitution exclusions

- `THM-M-1339`, continuous dependence on initial values and parameters, is not replaced by a
  differentiability or variational-equation claim.
- `THM-M-1340`, differentiability with respect to parameters, is not silently duplicated; a later
  review must decide whether `THM-M-1341` is the equation consequence, an initial-state variant, or
  another source-selected root.
- Picard-Lindelof existence, ODE uniqueness, Gronwall estimates, a generic chain rule, or a linear
  ODE interface alone is not the requested sensitivity equation.
- The derivative equation cannot be assumed as a hypothesis and then returned tautologically.
- A scalar, autonomous, global, equilibrium-only, or one-dimensional special case cannot replace a
  broader source theorem without an approved identity or directional transport.
- Numerical finite differences, automatic-differentiation output, or trajectory plots provide no
  kernel proof credit.
- The repository label `verified` supplies no human-source or machine-proof evidence.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, or proof state is frozen at intake.
