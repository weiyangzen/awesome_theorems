# THM-M-0866 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository's Wagner-theorem
record. The catalog supplies Klaus Wagner, 1937, and only the gloss "forbidden-minor
characterization of planar graphs." That recognizes the classical graph-theory family, but it does
not state one binder-complete proposition or cite a theorem-level source.

The familiar candidate says that a finite graph is planar exactly when it has neither the complete
graph on five vertices nor the complete bipartite graph on three plus three vertices as a graph
minor. It is preserved only as a candidate meaning. The catalog does not fix finiteness and graph
model, abstract planarity, the graph-minor witness relation and its direction, the two obstruction
encodings, or degenerate cases. Crossref identifies Wagner's 1937 article, *Über eine Eigenschaft
der ebenen Komplexe*, but its full statement and incorporated definitions were not available for
pinpoint review. A historical JFM review describes a more detailed contraction/basis result and
flags an incorrect final sentence in the paper's introduction, so source-era scope and correction
review are material. No exact source proposition is promoted at intake.

Pinned mathlib supplies finite simple graphs, complete and complete-bipartite graphs, graph copies,
induced graphs, and embeddings. `IntakeProbe.lean` authenticates those adjacent interfaces. A
bounded search found no graph-planarity or graph-minor interface and no Wagner theorem. In
particular, mathlib's matroid-minor vocabulary is not a graph-minor substitute.

The provisional vector is `[H1, M4, R4]`: the established theorem family and primary bibliographic
lead are known, but exact source fidelity and independent review remain open; no source-identical
Lean artifact is credited; and no source-faithful readable proof reconstruction exists.
`instance.json` is the structured scope authority and `task-dag.json` keeps all six downstream
phases open. No canonical statement, H0, M0, R0, accepted execution state, audit completion,
theorem completion, accepted receipt, or master acceptance is claimed.
