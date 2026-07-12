# THM-M-0594 rev-5.6 instance

This directory is the new rev-5.6 `planned` instance for the Whitney embedding
theorem. Historical Stage1 files are discovery inputs only and confer no proof
credit or accepted state.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Canonical human root | Every finite-dimensional, Hausdorff, second-countable smooth manifold admits a smooth embedding into some finite-dimensional Euclidean space | The source record does not specify a sharp dimension bound; selecting `R^(2m)` or `R^(2m+1)` would strengthen the frozen claim |
| Manifold hypotheses | A smooth manifold of finite dimension `m`, with the standard Hausdorff and second-countability assumptions | Boundary, corners, non-Hausdorff, and non-second-countable variants are not silently included |
| Embedding conclusion | A smooth map that is a topological embedding and has injective differential at every point | The exact correspondence with current mathlib predicates belongs to the statement phase |
| Compact branch | Compact finite-dimensional manifolds and mathlib's existing Euclidean embedding candidate | Candidate specialization only; it does not close the unrestricted root |
| Noncompact branch | General second-countable finite-dimensional manifolds | Open formalization boundary at intake |
| Dimension refinements | Weak `2m+1` and strong `2m` formulations | Alternate candidates requiring explicit source and checked transports; neither is credited here |
| Foundations | Lean 4 kernel with a versioned classical/choice/quotient policy | Exact profile, imports, and fingerprint remain open |

The structured intake claim and ordered scope are in `intake.json`. The exact
Lean expression is in `Statement.lean`, with its environment and expression
fingerprints in `statement.json`. Human-source
genealogy and its unresolved relationship to Lean candidates are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle remains `planned`; provisional root vector is `[H1, M3, R3]`. The
statement phase has now self-tested an exact formal expression, checked
expansion, environment fingerprint, and four negative identity mutations.
Master acceptance and every proof, source, obligation, provenance, trust,
composition, readability, reproducibility, and release gate remain open. This
instance does not claim theorem completion.

## Validation

The intake commands remain in `validation.md`; statement-specific kernel
checks and their exact results are recorded in `statement-validation.md`.
