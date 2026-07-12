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

The anchor phase found no exact or transport-ready proof in pinned mathlib or the immutable external
Lean 4 candidates inspected. `AnchorAudit.lean` kernel-checks the adjacent representation and
halting anchors, while `anchor-audit.md` records the bounded negative search and integration cut.
The root remains `[H1, M4, R4]`: `Statement.lean` elaborates the exact proposition, but no finite
presentation construction or undecidability reduction has been supplied. Exact commands and
results are in `validation.md`.

The obligation-tree phase freezes 17 canonical semantic obligations and seven separate typed
graphs. `ObligationTree.lean` checks only that an explicit fixed-presentation noncomputability
witness assembles into the exact root. The central construction/reduction and foundation audit are
still open, so this architecture supplies no theorem closure.
