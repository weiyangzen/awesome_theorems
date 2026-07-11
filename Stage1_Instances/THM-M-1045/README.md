# THM-M-1045 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Cameron-Martin theorem. Historical
`S1_M_238.lean` content is discovery material and carries no accepted proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | quasi-invariance iff the translation is a Cameron-Martin direction, plus the exponential RN density | Exact path-space, sigma-algebra, translation orientation, and stochastic integral must be frozen in the statement phase |
| Wiener model | continuous real paths starting at zero, Wiener measure, coordinate Brownian process | The legacy scaffold assumes rather than constructs Wiener measure |
| Cameron-Martin space | absolutely continuous paths starting at zero with square-integrable derivative | The embedding and Hilbert norm need exact Lean encodings |
| Positive branch | finite-dimensional shifts, cylinder density, extension to the generated sigma-algebra, RN identification | No terminal proof credit at intake |
| Negative branch | singularity for translations outside the Cameron-Martin space | This required half is absent from the legacy equivalence-only interface |
| Generalization | abstract Gaussian measures and their reproducing-kernel/Cameron-Martin space | Candidate architecture, not a substitute for the Wiener statement |
| Foundations | Lean 4 kernel, pinned mathlib, classical measure theory and stochastic integration | Environment and trust fingerprints remain open |

The structured claim, domains, edge cases, and candidate Lean boundary are in `intake.json`. Human
source genealogy and statement correspondence are in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: no elaborated expression hash, environment fingerprint, checked
transport, or mutation test exists. The theorem is not complete.

## Validation

The commands in `validation.md` establish manifest membership, repository-standard consistency,
JSON syntax, and dossier-local hygiene only. No Lean declaration was added in this intake phase.
