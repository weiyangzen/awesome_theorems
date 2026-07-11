# THM-M-0424 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Brauer group theorem. Historical Stage0
labels and the legacy Lean module are discovery inputs only and supply no accepted proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Brauer classes of finite-dimensional central simple algebras over a field form an abelian group under tensor product | The source phrase "classification of central simple algebras" is too terse to choose a stronger arithmetic classification |
| Objects | fields, finite-dimensional central simple algebras, matrix stabilization, division-algebra representatives | Exact universe and typeclass ordering belong to the statement phase |
| Equivalence | stable matrix-algebra equivalence (Brauer equivalence) | Its equivalence with Morita equivalence is not silently included |
| Operations | tensor product, base-field unit, opposite-algebra inverse | Construction and well-definedness are open proof obligations |
| Classification consequence | equality of Brauer classes iff Brauer equivalence; Artin-Wedderburn normal form is a supporting result | Neither quotient tautology nor normal form alone is the full group theorem |
| Excluded variants | Brauer groups of commutative rings/schemes and Galois-cohomological or local/global computations | Separate theorems requiring additional hypotheses and infrastructure |
| Foundations | Lean 4 kernel with pinned mathlib and an audited classical/choice/quotient policy | Exact environment and TCB fingerprints remain open |

The canonical human claim and provisional Lean boundary are structured in `intake.json`. Source
wording and its relationship to Lean candidates are recorded in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The source title is ambiguous,
the primary-source premise audit is incomplete, and the full formal target has not been elaborated.
The first failed theorem gate is therefore the exact-statement gate. No theorem completion or
acceptance is claimed.

## Validation

The commands in `validation.md` validate manifest membership, repository-standard consistency,
JSON syntax, and dossier-local hygiene only. Master acceptance and all dependent phases remain
outstanding.
