# THM-M-1147 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Kelvin transform".
The available source wording, "inversion of harmonic functions", identifies a theorem family but
not an exact theorem: it omits dimension, domain, inversion radius and center, scalar field,
regularity assumptions, and the transform's normalization.

No member of that family is silently selected here. In particular, the familiar Euclidean formula
`v(x) = |x|^(2-n) u(x / |x|^2)` is recorded only as a candidate requiring source confirmation, not
as the canonical claim. The provisional root vector is `[H4, M4, R4]`; no exact statement, Lean
elaboration, proof, audit completion, or theorem completion is claimed.

`scope-map.md` and `source-statement-crosswalk.md` freeze what the repository actually says and the
decisions still required. `task-dag.json` records the open downstream phases. Exact intake checks
and their results are recorded in `validation.md`.
