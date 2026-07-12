# THM-M-0535 rev-5.6 intake

This directory is the fail-closed `planned` intake for the excision theorem in relative singular
homology. The repository source fixes only the phrase "the excision property of relative homology
groups." That phrase identifies a theorem family, but it does not fix the exact neighborhood
hypothesis, coefficients, reduced/unreduced convention, or source proposition.

The intended classical variant says that, when the closure of a subspace `Z` is contained in the
interior of a subspace `A` of `X`, inclusion of pairs `(X \ Z, A \ Z) -> (X, A)` induces an
isomorphism on relative singular homology in every degree. The statement phase must verify this
wording against an immutable primary or standard source and freeze all conventions. The
provisional root vector is `[H1, M4, R4]`; no exact Lean target, source-fidelity acceptance, proof,
audit completion, or theorem completion is claimed.

`scope-map.md` records proposition-changing choices, `source-statement-crosswalk.md` separates
repository metadata from source evidence, and `task-dag.json` leaves every later phase open. The
commands actually run for this intake are recorded in `validation.md`.
