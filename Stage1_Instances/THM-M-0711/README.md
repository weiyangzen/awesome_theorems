# THM-M-0711 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Novikov-Boone theorem. The
repository gloss says only that "the word problem for groups is undecidable". The standard
mathematical theorem is an existential result: there is a finitely presented group whose word
problem is undecidable. It is not the false assertion that every group's word problem is
undecidable.

The repository does not supply a primary-source edition, theorem/page, presentation, word coding,
or a precise choice between the fixed-group and uniform-presentation formulations. Those choices
affect the Lean proposition and cannot be invented at intake. The scope and competing encodings are
therefore frozen, while the canonical formal target remains open for the statement phase.

The root remains `[H1, M4, R4]`. A pinned Lean probe confirms the availability of free groups,
presented groups, the quotient word predicate, and computability predicates. This is encoding
evidence only, not a theorem statement or proof. Exact commands and results are in `validation.md`.
