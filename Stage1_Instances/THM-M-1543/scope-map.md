# Scope map

## Included theorem family

- A Ward/Penrose transform relating anti-self-dual connection data on a four-dimensional
  conformal manifold to holomorphic bundle data on its twistor space.
- Quotienting on the gauge side and bundle isomorphism on the twistor side.
- Holomorphic triviality on the distinguished twistor lines and the source's real-structure
  condition.
- Framing, rank/gauge group, topological charge, compactification, and smoothness conditions only
  as fixed by the exact selected source result.

## Decisions required before statement freeze

The statement phase must inspect a stable primary source and fix whether the base is Euclidean
four-space or its conformal compactification, whether connections are framed, the structure group
and rank, finite-action and regularity hypotheses, self-dual versus anti-self-dual orientation,
charge/Chern-class conventions, and the exact equivalence relations. It must define the twistor
space, its real involution and real lines, holomorphic bundles, line restrictions, and the bundle
reality structure without packaging the desired correspondence as an assumed structure field.
Degenerate rank or charge and reducible connections must be treated explicitly.

## Explicit exclusions

- The legacy abstract `WardTransformAPI`, whose inverse and correspondence laws are assumptions.
- A bijection between arbitrary user-supplied types as a substitute for the geometric theorem.
- Point-set facts about projective lines or bundle restrictions alone.
- The ADHM classification, Penrose transform, or a special instanton construction unless proved
  to be the exact source statement or a checked component of it.
- Experimental or physical claims not rewritten as mathematical propositions.

No downstream statement may claim the classical result until its concrete geometric objects and
both quotient notions are exposed or a precise missing-API blocker is recorded.
