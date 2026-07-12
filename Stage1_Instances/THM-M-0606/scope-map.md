# Scope map

## Included human claim

- Smooth, closed, oriented manifolds homotopy equivalent to a sphere in the high-dimensional range
  covered by the selected Kervaire-Milnor theorem.
- The source's equivalence relation on homotopy spheres and connected sum as the relevant group
  operation.
- The group customarily denoted `Theta_n`, the subgroup customarily denoted `bP_(n+1)` of spheres
  bounding parallelizable manifolds, and the stable-homotopy comparison used by the selected
  classification statement.
- Dimension restrictions and exceptional cases exactly as stated in the selected primary result.

## Decisions required before the statement gate

The primary-source inspection must choose one exact root proposition rather than formalizing the
whole paper under a slogan. It must fix: smooth versus piecewise-linear category; oriented
diffeomorphism versus oriented h-cobordism; whether a chosen orientation-reversing map is relevant;
the lower bound and excluded dimensions; the definitions and indexing of `Theta_n` and `bP`; the
precise stable `J`-homomorphism quotient; and whether the conclusion is group structure, finiteness,
an exact sequence, an order computation, or a combination explicitly packaged as a conjunction.

Boundary cases to map separately include the standard sphere, orientation reversal, low dimensions
(especially dimensions three and four), even/odd dimensions, and any Kervaire-invariant term. The
Lean binder order, universes, quotient construction, and propositions must follow these decisions.

## Explicit exclusions

- The generalized Poincare conjecture or a homeomorphism classification in place of the smooth
  classification.
- The unresolved smooth four-dimensional Poincare problem.
- Milnor's existence of exotic seven-spheres alone.
- A lookup table of known group orders without the classification theorem and provenance.
- An abstract structure that assumes the classification map, exactness, or finiteness as a field.
- The Stage0 label `已验证` as machine or human-source evidence.

## Formalization surface

The exact Lean target will require concrete encodings of smooth homotopy spheres, orientation,
connected sum, the chosen equivalence relation and quotient group, parallelizable bounding
manifolds, and the stable-homotopy comparison. Intake records no claim that pinned mathlib currently
provides these APIs. Missing infrastructure is a statement-phase blocker, not permission to replace
the theorem with an abstract proxy.
