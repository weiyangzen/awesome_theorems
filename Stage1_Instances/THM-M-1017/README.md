# THM-M-1017 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the characteristic-function inversion
formula. The repository source only says "recover a distribution from its characteristic
function"; it does not specify which of the density, interval-mass, or distribution-function
inversion formulas is intended. Accordingly this intake preserves that scope and does not invent
an exact Lean theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Root claim | Recovery of a Borel probability distribution on `Real` from its characteristic function | Exact inversion variant is unresolved and blocks the statement gate |
| Distribution form | Recovery of interval mass / CDF increments at continuity endpoints | Candidate interpretation, not a frozen formal target |
| Density form | Fourier inversion when a density exists and the characteristic function is integrable | Candidate specialization, not interchangeable with the root |
| Uniqueness | Equality of characteristic functions implies equality of distributions | Consequence/candidate bridge, not itself accepted as the inversion formula |
| Boundary behavior | Atoms, continuity points, endpoint half-masses, improper-integral limits | Must be explicit in the statement phase |
| Foundations | Lean 4 kernel, mathlib measure theory, Bochner integration, complex Fourier analysis | Exact imports, instances, and logical profile remain open |

The ordered claim components and candidate encodings are recorded in `intake.json`. Source wording,
candidate primary references, and the ambiguity that must be resolved are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
exact-source identification: the screened metadata is too broad to choose among inequivalent
inversion formulas. No expression hash, environment fingerprint, checked transport, proof credit,
or theorem completion is claimed.

## Validation

The commands and results in `validation.md` establish target membership, standard consistency,
JSON syntax, and dossier-local integrity only.
