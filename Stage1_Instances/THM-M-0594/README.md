# THM-M-0594 rev-5.6 intake

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

The structured claim and ordered scope are in `intake.json`. Human-source
genealogy and its unresolved relationship to Lean candidates are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first
failed theorem gate is the Lean statement gate: there is no accepted formal
expression, normalized expression hash, environment fingerprint, checked
transport, or mutation suite. This intake does not claim theorem completion.

## Validation

The commands in `validation.md` establish manifest membership, standard
consistency, JSON syntax, and dossier-local integrity only.
