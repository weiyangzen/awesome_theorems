# THM-M-0130 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the manifest target named "Shimura
varieties" (Chinese: `志村簇`). It starts from `L0 / rework_required` and inherits no proof credit
from the legacy Stage1 label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Legacy claim | "Construction of Hodge-type Shimura varieties" (`Hodge型志田簇的构造`, preserving the apparent `志田` typo in the generated source) | This phrase names a subject/construction, not yet a uniquely quantified theorem |
| Mathematical objects | Shimura data `(G, X)` of Hodge type, an embedding into a Siegel datum, the associated complex Shimura variety, and canonical models/integral models only if selected by the statement audit | No one model or base is silently selected |
| Possible conclusions | existence of the complex double quotient, a canonical model over the reflex field, or an integral canonical model | These are inequivalent theorem families with different hypotheses; all remain candidates |
| Formal target | Lean 4 proposition to be chosen only after the source statement is disambiguated | No module, declaration, expression hash, or checked transport is claimed |
| Foundations | Lean 4 kernel with a future pinned mathlib environment | Exact classical/choice/quotient and TCB profiles remain open |

The statement phase must not replace this broad record with a convenient result about schemes. It
must select a primary-source theorem, preserve its hypotheses (especially reductivity, Hodge-type
embedding, level, base, and prime restrictions), and then elaborate that exact claim.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
exact-statement identity: the repository supplies only a topic-level Chinese phrase, and the
candidate source theorems in the crosswalk have materially different conclusions. This intake is
self-tested as a scope dossier, not as a Lean theorem. The theorem is not complete.

## Files

`intake.json` is the structured authority for this planned scope.
`source_statement_crosswalk.md` records the ambiguity and primary-source discovery anchors.
`validation.md` records the exact intake checks and their results.
