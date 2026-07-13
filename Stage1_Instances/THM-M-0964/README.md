# THM-M-0964: Hilton-Milner theorem

This directory is the fail-closed rev-5.6 intake dossier for `S56-M-0964-INTAKE`. The repository
catalog fixes the 1967 Hilton-Milner attribution and the subject "maximum size of a nontrivial
intersecting family," but does not provide a formula, parameter range, definition of nontriviality,
or equality scope.

The primary article's bibliography and DOI were authenticated, but its text was not accessible from
this worker environment. Two immutable secondary sources repeat the classical uniform-family upper
bound. One also states the extremal-family classification and the exceptional `k = 3` family. The
catalog does not decide whether that classification belongs to the requested root, and the sources
use different endpoint ranges. Consequently the canonical mathematical and Lean statements remain
null rather than silently selecting a convenient variant.

## Dossier navigation

- [`instance.json`](instance.json): structured planned-instance authority.
- [`scope-map.md`](scope-map.md): variants, parameters, boundary cases, and exclusions.
- [`source-statement-crosswalk.md`](source-statement-crosswalk.md): repository, source, and Lean
  component map.
- [`task-dag.json`](task-dag.json): six open downstream tasks.
- [`IntakeProbe.lean`](IntakeProbe.lean): discovery-only pinned API and candidate-shape probe.
- [`validation.md`](validation.md): exact commands, results, and evidence boundaries.
- [`intake-receipt.json`](intake-receipt.json): provisional worker receipt awaiting integration.

## Status boundary

The proposed vector is `H1 / M3 / R4`. Precise immutable secondary restatements and an authenticated
primary bibliography support `H1`, but the primary passage, corrections, exact scope, and independent
review remain open. The candidate proposition shape elaborates against pinned mathlib, but no exact
Hilton-Milner declaration or proof body was located, so machine status is only `M3`. No
source-faithful readable proof reconstruction is frozen. This intake asserts no accepted state,
audit completion, theorem completion, or master acceptance.
