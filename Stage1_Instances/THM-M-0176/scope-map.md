# Scope map

## Intended mathematical root

The source-selection target is the classical Hirzebruch-Riemann-Roch identity for a smooth
projective complex variety `X` and an algebraic vector bundle `E`:

`chi(X, E) = integral_X (ch(E) cup td(T_X))`.

Here `chi` is the alternating sum of coherent-sheaf cohomology dimensions, `ch` is the Chern
character, and `td(T_X)` is the Todd class of the tangent bundle; only the component in top degree
is evaluated on the fundamental class. This formula is an intake-level description, not a frozen
Lean proposition or proof claim.

## Objects and boundary choices to freeze

- Smooth projective variety over `C`, its dimension, tangent bundle, and fundamental class.
- Algebraic vector bundle versus locally free coherent sheaf, including finite-rank assumptions.
- Chow-ring/rational equivalence versus singular-cohomology characteristic classes and the checked
  comparison map between them.
- Definition and finiteness of sheaf-cohomological Euler characteristic.
- Normalization and grading conventions for Chern character, Todd class, cup/intersection product,
  top-degree extraction, and integration/pushforward to a point.
- Dimension zero, the zero bundle, disconnected varieties, and whether empty varieties are allowed.

## Explicit exclusions

- The curve-only Riemann-Roch theorem, Grothendieck-Riemann-Roch for an arbitrary proper morphism,
  Atiyah-Singer as a substitute, or a purely analytic index formula without checked transports.
- Singular or merely proper varieties unless the selected source theorem explicitly covers them.
- An abstract equality obtained by assuming the desired index/characteristic-number equality.
- The metadata label `已验证` or a legacy file as rev-5.6 evidence.

The statement phase must select one source theorem, preserve its hypotheses exactly, and freeze
universes, ordered binders, imports, declaration type, environment fingerprint, and mutation tests.
