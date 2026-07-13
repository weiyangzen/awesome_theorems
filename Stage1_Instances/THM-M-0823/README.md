# THM-M-0823 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Kruskal算法`
(Kruskal's algorithm). The catalog supplies Joseph Kruskal, the year 1956, and only the gloss
`最小生成树的贪心算法` ("a greedy algorithm for a minimum spanning tree"). Its `已验证`
("verified") label is untrusted metadata and supplies no human-source or Lean proof credit.

Kruskal's 1956 paper *On the shortest spanning subtree of a graph and the traveling salesman
problem* is a strong source-family lead. Its bibliographic identity matches the catalog, and the
paper's Construction A is the familiar greedy loop-avoiding edge procedure. But the catalog does
not cite the paper or freeze whether the intended root is construction correctness, minimum-tree
existence, distinct-weight uniqueness, a total executable specification, or a complexity result.
It also omits the graph model, weight order, tie policy, output contract, and boundary cases.

The intake therefore records the 1956 paper only as a discovery lead. The canonical human and Lean
statements remain null pending an independently reviewed source selection and complete definition
crosswalk. The provisional vector is `[H5, M4, R4]`: the received algorithm-family gloss is not
one stable truth-valued proposition and requires an approved target selection; no usable exact Lean
formalization is identified; and no proof reconstruction exists. `H5` classifies this catalog
wording, not the established mathematics of Kruskal's algorithm.

`instance.json` is the structured scope authority. `scope-map.md` freezes the candidate boundary
and prohibited substitutions, while `source-statement-crosswalk.md` records every proposition-
changing choice still open. The six dependent phases are open in `task-dag.json`. `IntakeProbe.lean`
checks adjacent pinned simple-graph interfaces only and states no target theorem. No H0, M0, R0,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
