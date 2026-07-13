# THM-M-0867 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item named the
Robertson-Seymour graph minor theorem. The repository attributes it to Neil Robertson and Paul
Seymour, dates it to 2004, and gives only the gloss `图子式良拟序定理` (the well-quasi-ordering
theorem for graph minors). Its `已验证` label is untrusted metadata, not source or proof evidence.

The recognizable theorem family says that finite graphs are well-quasi-ordered by the minor
relation. The catalog does not fix the graph model, representation up to isomorphism, definition
and orientation of the minor relation, set-versus-sequence formulation, quantifier order, or
degenerate cases. Selecting a familiar encoding at intake would add proposition-changing choices.

Robertson and Seymour's *Graph Minors. XX. Wagner's conjecture* was inspected as a primary-source
lead. Its abstract states the infinite-set formulation, its introduction says all graphs in the
paper are finite, and Theorem 10.5 gives a countable-sequence directed-graph strengthening that
implies the standard undirected form. The inspected author-hosted PDF is digest-bound in the
crosswalk. A complete definition chain, equivalence between the source formulations and the
catalog's WQO wording, correction/errata audit, and independent review remain open, so this is
provisional `H1`, not `H0`.

Pinned mathlib provides `WellQuasiOrdered` and finite simple-graph, isomorphism, induced-subgraph,
edge-deletion, and graph-map interfaces. It does not expose a graph-minor predicate, edge
contraction construction, quotient type of finite graphs up to isomorphism, or the Robertson-
Seymour closure in the bounded intake search. `IntakeProbe.lean` authenticates only those adjacent
interfaces. They support an `M3` statement-shape classification, not proof credit.

The provisional vector is `[H1, M3, R4]`. All six downstream tasks remain open. No canonical
statement, exact Lean target, H0, M0, R0, accepted state, audit completion, theorem completion,
accepted receipt, or master acceptance is claimed.
