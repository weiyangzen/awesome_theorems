# THM-M-0812 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0812`, Konig's
matching-cover theorem. The repository names Denes Konig, dates the result to 1931, and states
`二部图中最大匹配等于最小顶点覆盖`: in a bipartite graph, a maximum matching and a minimum
vertex cover have equal sizes. The catalog's `已验证` field is untrusted metadata and grants no
source or proof credit.

The canonical human claim is now scoped to finite bipartite graphs: the maximum number of
pairwise vertex-disjoint edges equals the minimum number of vertices incident to every edge. This
scope is supported by Gabor Szarnyas's English translation of Denes Konig's 1931 paper, *Graphok es
matrixok*, arXiv:`2009.03780v1`. The translation defines a finite bipartite graph, matching size,
and edge-covering vertex sets; constructs a cover from a maximum matching by alternating paths;
and states the equality on page 3.

This remains `H1`, not `H0`. The inspected artifact is a 2020 translation, while the Hungarian
original, translation fidelity, corrections and errata, source-to-obligation mapping, and
independent source review remain open. The original-volume archive was identified but its full PDF
was not successfully preserved and inspected in this intake.

Pinned mathlib exposes bipartite-graph, matching, and vertex-cover APIs, including the `ENat`-valued
`SimpleGraph.vertexCoverNum`, but no maximum-matching-number definition or exact Konig equality was
found in the bounded intake search. `IntakeProbe.lean` authenticates adjacent interfaces only.

The statement phase now freezes `KonigMatchingCoverTarget` as a finite two-sorted incidence model:
finite typed vertex sides, a finite edge-identity type, and endpoint maps. Attained witness plus
universal-bound predicates express the maximum matching edge count and minimum cover vertex count.
A kernel-checked iff to `SimpleRelationKonigTarget` proves parallel-edge erasure preserves both
extrema, resolving the translation's silent simple-versus-parallel convention. The expanded iff,
four structural mutations, and edgeless and single-edge boundaries also elaborate under the two
minimal pinned imports. Exact details and hashes are in `statement.json` and
`statement-validation.md`.

The provisional vector remains `[H1, M3, R2]`. The dossier gives a source-derived proof summary, but
important formal branches, stable obligation anchors, local transition ledgers, and independent
readability review remain open. No H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed. The intake and statement worker receipts both
remain provisional until dependency-ordered integration-lane acceptance.
