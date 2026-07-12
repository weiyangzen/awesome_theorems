# THM-M-0711 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Novikov-Boone theorem. The
repository gloss says only that "the word problem for groups is undecidable". The standard
mathematical theorem is an existential result: there is a finitely presented group whose word
problem is undecidable. It is not the false assertion that every group's word problem is
undecidable.

The repository does not supply a primary-source edition, theorem/page, or a precise choice between
the fixed-group and uniform-presentation formulations. The statement phase now freezes the
standard fixed-group reading for this repository, using finite signed-generator lists as the word
code. Historical source fidelity remains a separate open audit gate.

The root remains `[H1, M4, R4]`. `Statement.lean` kernel-elaborates the exact proposition under the
pinned toolchain, but supplies no proof. Exact commands and results are in `validation.md`.
