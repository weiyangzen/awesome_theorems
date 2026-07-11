# Exact-statement gate: blocked

Item: `S56-M-0175-STATEMENT`

## Decision

An exact Lean 4 target cannot yet be truthfully elaborated. The repository
source record says only "the divisor dimension formula on an algebraic curve."
It does not fix the field convention, the meaning of curve, the divisor model,
the definition of degree and genus, or the canonical-divisor/global-sections
interpretation. The intake selected a provisional modern formulation over an
arbitrary field with a smooth, projective, geometrically integral curve, while
its own crosswalk says that this normalization still requires a checked source
bridge. The candidate Hartshorne citation has not been inspected and accepted.
Consequently the provisional prose cannot establish exact statement identity.

The pinned mathlib revision also has no concrete algebraic-curve API connecting
all of the required objects: divisors, `O(D)`, canonical divisor, divisor degree,
genus, and finite-dimensional `H^0`. The legacy
`AwesomeTheorems.Stage1.S1_M_124.StatementShape` does not solve this problem. It
quantifies an abstract `RiemannRochDivisorData` whose operations and invariants
are unconstrained and merely asserts that some such package satisfies the
formula. It neither ties that package to the curve nor models projectivity,
geometric integrality, divisors, or sheaf cohomology concretely. Adopting it
would substitute a weaker, readily satisfiable proposition for Riemann-Roch and
is forbidden by the rev-5.6 exact-statement gate.

## Lean boundary checked

`StatementProbe.lean` uses only these direct pinned imports:

```lean
import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
```

It elaborates `Scheme`, `Scheme.Hom`, `Spec`, `Smooth`, `IsProper`, and
`GeometricallyIntegral`. This proves only that concrete scheme, smoothness,
properness, and geometric-integrality surfaces are present. It is not a
canonical target and supplies no theorem-proof credit.

The environment is Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, using the existing canonical
`.lake` artifact. No update, fetch, clone, or build was performed.

## Gate result and retry condition

The first failed gate is section 5 exact-statement identity. There is no
canonical declaration or elaborated-expression hash, and source-faithful
mutation tests cannot be defined. Retry after an immutable primary source is
inspected and accepted, its field and curve conventions are frozen, and a
concrete pinned Lean divisor/cohomology object model (or checked faithful
encoding) exists for every term of the formula. Machine status remains
statement/interface debt; the theorem is not proved or complete.

No `.stage1-worker-selftest.json` is emitted because the assigned statement
deliverable is blocked rather than complete.

