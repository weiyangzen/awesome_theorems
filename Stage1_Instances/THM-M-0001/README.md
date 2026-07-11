# THM-M-0001 rev-5.6 intake

This directory is the `planned` intake for the theorem that a short exact sequence of chain
complexes induces a long exact sequence in homology. The dossier freezes the intended human scope
and, importantly, excludes replacing the continuing sequence by an unqualified finite window.

The dependent statement worker has now proposed an exact, elaborated formal encoding in
`Statement.lean` and `statement.json`. It quantifies over every degree and every adjacent pair, so
it does not substitute a finite window for the continuing sequence. This proposal remains pending
master acceptance. Source pinpoint audit, mathlib anchor audit, obligation registry, proof, and
release checks remain downstream work. The provisional vector remains `[H1, M3, R3]`; no accepted
proof state, audit completion, or theorem completion is claimed.

The scope and source crosswalk are in the adjacent Markdown files; the dependency-ordered open work
is recorded in `task-dag.json`; exact self-tests are recorded in `validation.md`.
