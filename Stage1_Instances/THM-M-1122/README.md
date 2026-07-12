# THM-M-1122 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label
"Schramm-Loewner evolution" (SLE). The source inventory supplies only the gloss "random curves of
critical phenomena", the year 2000, and Oded Schramm's name. SLE is a parameterized family of
random planar curves/processes, not by itself a unique theorem. A theorem must fix a domain and
marked boundary points, a curve topology and parametrization, the Loewner normalization, the
driving process, and an exact conclusion.

The statement phase selects Schramm (2000), Theorem 1.3: conditional on Conjecture 1.2, the radial
Loewner solution in the unit disk driven by circle Brownian motion at time `-2t` has the same law as
the LERW scaling limit. `Statement.lean`, `statement.md`, and `statement.json` freeze and elaborate
that exact conditional target. They do not prove it or silently replace it with a modern chordal
characterization.

The provisional root vector remains `[H2, M4, R4]`. Exact statement elaboration does not provide
source-review acceptance, a formal candidate, proof, audit completion, or theorem completion. `scope-map.md` records the
proposition-changing decisions, `source-statement-crosswalk.md` records the source mapping, and
`task-dag.json` keeps every downstream phase open. Intake validation is recorded in
`validation.md`.
