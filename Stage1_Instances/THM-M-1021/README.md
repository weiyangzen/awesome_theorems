# THM-M-1021 rev-5.6 dossier

This directory is the rev-5.6 `planned` instance for Bochner's theorem in its
one-dimensional probability form. The historical `已验证` label is discovery
metadata only and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Characterization of characteristic functions on `Real` by normalization, continuity, and positive definiteness | `BochnerStatement.lean` elaborates the frozen proposition; `statement.json` records its fingerprint |
| Forward direction | A Borel probability measure has a normalized, continuous, positive-definite Fourier transform | Candidate architecture only |
| Reverse direction | Such a function is the Fourier transform of a Borel probability measure | Existence is the substantive Bochner direction; uniqueness is excluded from this root |
| Positivity | For every finite complex coefficient/point family, the associated Hermitian quadratic sum is nonnegative | Frozen as equality to the coercion of an existential nonnegative `Real` |
| Regularity | Continuity on all of `Real` | Equivalent continuity-at-zero formulations are transports, not alternate roots |
| Measure boundary | Borel probability measures on `Real`; transform convention `integral exp(i * t * x) dμ(x)` | Sign convention is immaterial only after a checked reflection transport |
| Foundations | Lean 4 kernel, pinned mathlib, classical measure/integration and complex exponential APIs | Exact toolchain, imports, axioms, and TCB remain open |

The canonical claim and ordered mathematical binders are structured in
`intake.json`. Source genealogy and statement correspondence are recorded in
`source_statement_crosswalk.md`. No proof or external formalization is credited.

## Statement verdict

Lifecycle remains `planned`; provisional root vector remains `[H1, M3, R3]`.
The exact statement now elaborates with one pinned mathlib import and has a
reproducible printed-expression fingerprint. No proof is present or claimed.
The bounded anchor audit is recorded in `anchor_audit.md` and
`anchor_audit.json`. Pinned mathlib provides characteristic-function encoding,
continuity, normalization, and uniqueness support, but no exact representation
theorem candidate was found. The root remains `not_repo_local_closed` with
formalization debt. Master acceptance is still required, and the theorem is not
complete.

## Validation

The commands in `validation.md` include the narrow kernel elaboration check and
environment fingerprints, in addition to dossier-local structural checks.
