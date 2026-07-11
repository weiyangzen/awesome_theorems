# THM-M-0138 rev-5.6 intake

This is a new `planned` dossier for the abelian regular-integral form of
Beilinson-Bernstein localization. It inherits no proof credit from the legacy Stage1 file.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Equivalence between a regular-integral central-character representation block and quasi-coherent twisted D-modules on the full flag variety | Exact conventions and Lean expression remain open |
| Representation side | Complex semisimple Lie algebra, `U(g)`, Harish-Chandra central character/reduction, selected module block | Mathlib anchors are discovery inputs only |
| Geometry side | Full flag variety, twisting parameter, sheaf of twisted differential operators, quasi-coherent module category | No suitable concrete Lean model is credited |
| Functors | Localization and global sections, including their adjunction and unit/counit | Abstract legacy functors do not construct the mathematical functors |
| Hypotheses | Regularity, integrality, compatible dominance, characteristic zero | Binder order and convention mutations await statement work |
| Exclusions | Derived/singular, parabolic/partial-flag, positive-characteristic, quantum variants | They cannot substitute for this root |
| Foundations | Lean kernel plus versioned mathlib and accepted category/choice policy | Fingerprint and transitive TCB remain open |

The intended claim and provisional formal target are structured in `intake.json`. Source genealogy,
claim-component mapping, and known convention risks are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no normalized expression hash, environment fingerprint,
concrete flag-variety/twisted-D-module model, checked transport, or mutation record. No theorem
completion or legacy machine closure is claimed.

## Validation

The exact intake-only checks and their results on base revision
`478034dee4145f887a572a3c645a3a2ea81bc883` are recorded in `validation.md`.
