# THM-M-0869 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0869`, catalogued as
`禁用子图问题` (forbidden-subgraph problem) with the gloss `禁用子图类的刻画`
(characterization of classes by forbidden subgraphs). The catalog supplies a topic family, not a
truth-valued proposition: it does not name the graph universe, containment relation, graph class,
obstruction family, finiteness or effectiveness conclusion, source theorem, or quantifiers.

Several inequivalent readings fit the words. A class closed under ordinary subgraphs has a
possibly infinite forbidden-subgraph description; hereditary classes use forbidden induced
subgraphs; minor-closed classes use forbidden minors and acquire a finite obstruction conclusion
only through substantially stronger results. Concrete characterizations such as Kuratowski,
Wagner, and the Strong Perfect Graph Theorem are separately catalogued targets. Intake records
these boundaries rather than selecting or proving one convenient interpretation.

Pinned mathlib provides ordinary and induced simple-graph containment interfaces.
`IntakeProbe.lean` checks `SimpleGraph.IsContained`, `SimpleGraph.Free`,
`SimpleGraph.IsIndContained`, and their subgraph witnesses at the pinned revision. The probe does
not define a graph class, select a forbidden family, state the catalog target, or prove a
characterization. A bounded repository and pinned-mathlib search is discovery evidence only, not
the downstream formal-anchor audit.

The provisional vector is `[H5, M4, R4]`. `H5` means the received topic label is not yet one stable
proposition; it does not refute any established forbidden-configuration theorem. No canonical Lean
target, proof body, accepted receipt, audit completion, theorem completion, or master acceptance is
claimed. The six downstream phases remain open in `task-dag.json`.
