# THM-M-1021 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Bochner's theorem in its
one-dimensional probability form. The historical `已验证` label is discovery
metadata only and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Characterization of characteristic functions on `Real` by normalization, continuity, and positive definiteness | Lean elaboration and an expression fingerprint belong to the dependent statement phase |
| Forward direction | A Borel probability measure has a normalized, continuous, positive-definite Fourier transform | Candidate architecture only |
| Reverse direction | Such a function is the Fourier transform of a Borel probability measure | Existence is the substantive Bochner direction; uniqueness is excluded from this root |
| Positivity | For every finite complex coefficient/point family, the associated Hermitian quadratic sum is nonnegative | The precise Lean predicate and real-valued coercion must be frozen during statement work |
| Regularity | Continuity on all of `Real` | Equivalent continuity-at-zero formulations are transports, not alternate roots |
| Measure boundary | Borel probability measures on `Real`; transform convention `integral exp(i * t * x) dμ(x)` | Sign convention is immaterial only after a checked reflection transport |
| Foundations | Lean 4 kernel, pinned mathlib, classical measure/integration and complex exponential APIs | Exact toolchain, imports, axioms, and TCB remain open |

The canonical claim and ordered mathematical binders are structured in
`intake.json`. Source genealogy and statement correspondence are recorded in
`source_statement_crosswalk.md`. No proof or external formalization is credited.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first
failed theorem gate is the exact Lean statement gate: there is no elaborated
declaration, normalized expression hash, environment fingerprint, checked
transport, or mutation result. The theorem is not complete.

## Validation

The commands in `validation.md` establish manifest membership, repository
standard consistency, JSON syntax, and dossier-local hygiene only.
