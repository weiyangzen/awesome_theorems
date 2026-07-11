# THM-M-0135 rev-5.6 intake

This directory is the `planned` intake dossier for the Macdonald identities. The repository's
human record says only "identities on affine root systems." Macdonald's result is a family, not a
single formula. Selecting a type or normalization without a source pinpoint would substitute a
different theorem, so this intake intentionally leaves the exact root open.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Macdonald's affine-root-system identity family | Exact paper identity, affine type, and normalization are unresolved |
| Root data | real and imaginary roots, multiplicities, Weyl group/action, Weyl vector | Concrete conventions and admissibility hypotheses require a primary-source pinpoint |
| Expression domain | a completion supporting the infinite product and Weyl sum | Legacy `AddMonoidAlgebra` is finite-support and is not accepted as this domain |
| Identity sides | affine denominator product and alternating Weyl sum; eta-function specializations are source candidates | No arbitrary pair of expressions may stand in for the constructed sides |
| Lean discovery | legacy `S1_M_051.lean` and adjacent mathlib root/Coxeter APIs | Discovery only; no declaration is credited as the exact target |
| Foundations | Lean kernel, mathlib, and an audited policy for classical choice/completions | Toolchain, imports, axioms, and TCB fingerprint remain open |

The next statement phase must first select a numbered formula from a pinned primary-source edition,
transcribe every convention and hypothesis, and only then elaborate a Lean proposition. It must
also reject the legacy universal shape as a root: that structure stores arbitrary
`denominatorProduct` and `alternatingSum`, so universal equality would be false and does not encode
Macdonald's constructions.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source/statement identification. No theorem-completion or machine-proof claim is made.

## Validation

The exact commands and results establishing manifest membership, repository standard consistency,
JSON syntax, and dossier-local hygiene are recorded in `validation.md`. These are intake receipts
only, subject to master acceptance.
