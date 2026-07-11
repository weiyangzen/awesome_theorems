# Scope map

## Preserved source scope

- Subject: a boundary-value problem for an unspecified differential equation.
- Boundary character: described literally as "mixed" under the name Robin problem.
- Attribution and date: Victor Robin, 1886, as repository metadata only.
- Asserted result: none beyond the untrusted label `verified`.

This is all the mathematical scope supported by the available repository source.

## Decisions required before statement freeze

The statement phase must identify a primary source and freeze the operator and equation, scalar
field and dimension, domain and boundary regularity, weak or classical solution space, boundary
partition (if any), the exact Robin condition and sign convention, coefficient hypotheses, forcing
and boundary data, compatibility/coercivity assumptions, and the claimed result (existence,
uniqueness, estimates, regularity, or another property). It must state constant dependencies and
handle zero coefficients, pure Dirichlet/Neumann limiting cases, empty boundary pieces, disconnected
domains, and noncoercive cases wherever relevant to the selected source theorem.

## Explicit exclusions

- Treating the phrase "Robin problem" itself as a proposition.
- Substituting an arbitrary existence/uniqueness theorem for `-Delta u = f` with
  `partial_n u + alpha u = g` merely because it is conventional.
- Conflating Robin conditions with piecewise Dirichlet/Neumann boundary conditions; terminology
  varies and must be resolved from the primary source.
- Crediting the metadata label `verified` as human proof or Lean kernel evidence.
- Broadening the target to all elliptic, parabolic, or nonlinear Robin problems.
