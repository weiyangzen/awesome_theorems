# THM-M-0861 source-statement crosswalk

## Repository source and provenance

The complete catalog record is `Docs/researches/math_theorems.md:6313-6318`:

| Field | Literal value | Intake meaning |
|---|---|---|
| title | `König边着色定理` | identifies König's edge-coloring theorem family |
| proposer | `Dénes Kőnig` | historical attribution only |
| time | `1916` | bibliographic locator |
| statement | `二部图的边色数等于最大度` | edge chromatic number of a bipartite graph equals maximum degree |
| importance | `高` | scheduling metadata only |
| formalization status | `已验证` | explicitly untrusted; no H/M credit |

All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:23495-23520`
repeats the claim while expressly leaving exact definitions and premises, source, proof route,
dependencies, alternate forms, axioms, machine status, and formal artifacts open.

## Inspected primary source lead

Dénes König, *Über Graphen und ihre Anwendung auf Determinantentheorie und Mengenlehre*,
*Mathematische Annalen* 77(4) (1916), 453-465, DOI `10.1007/BF01456961`, was inspected on
2026-07-13 from the open scan at Zenodo record `2395248`. The observed 13-page PDF has SHA-256
`46ad3d33fd7dc835ea0e1d1f12b56302988bff0e2ac898bfa72549d0560bb7eb`.

- Printed page 453 defines a graph from finitely many vertices and permits one or more finitely
  many edges between a selected vertex pair. The source is therefore a multigraph source, not a
  simple-graph source.
- Printed pages 453-454 define a `paarer Graph` by even closed edge-trails/walks and prove that this is
  equivalent to partitioning the vertices into two groups with edges only between groups.
- Printed page 455, Satz C, states: if at most `k` edges meet at every vertex of such a graph, its
  edges can be assigned one of `k` indices so any two incident edges receive different indices.
- Printed pages 455-456 prove Satz C by induction on the number of edges. After deleting one edge,
  the proof either assigns a color missing at both endpoints or swaps two indices along a maximal
  alternating path; bipartiteness prevents that path from reaching the other endpoint.
- Satz B on page 455, decomposition of a regular bipartite graph into `k` one-factors, is presented
  as a consequence of Satz C. It is not the catalog root and cannot replace it.

The catalog equality is a modern reformulation of Satz C plus the lower bound saying that all
edges incident to a maximum-degree vertex need distinct colors. This crosswalk is strong evidence
for the intended theorem family, but it is not yet `H0`: the scan has not been lawfully admitted as
an immutable repository source, a reviewer has not independently checked transcription and
translation, no corrections or errata search is accepted, and the equality transport and every
source premise have not received node-specific review.

## Clause crosswalk

| Catalog component | Primary-source component | Prospective Lean surface | Intake result |
|---|---|---|---|
| graph | finite graph allowing parallel edges, pp.453-454 | finite multigraph representation with reviewed loop policy | exact structure and universe open |
| bipartite | `paarer Graph`, equivalent to a two-part vertex partition, p.454 | property or supplied bipartition | source family identified; encoding open |
| maximum degree | at most `k` incident edges at every vertex, Satz C | multigraph incidence degree and maximum | exact finite maximum and decidability open |
| edge coloring | assign one of `k` indices; incident edges have distinct indices | dependent edge type to `Fin k` plus properness | no canonical predicate frozen |
| upper bound | Satz C supplies a proper coloring with `k` colors | existence at `k = Delta` | primary statement/proof lead inspected |
| lower bound | all incident edges at a maximum-degree vertex need different colors | injectivity/cardinality argument | elementary bridge, not separately source-mapped or reviewed |
| equality | modern `chi'(G) = Delta(G)` crosswalk | minimum number of proper edge colors | exact definition and checked transport open |
| `已验证` | untrusted inventory label | accepted source/kernel receipts required | no credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.Graph.Basic` defines a multigraph `Graph α β` with separate edge identity,
parallel edges, loops, `IsLink`, `Inc`, and `incidenceSet`. This is source-relevant representation
substrate, but the two pinned `Combinatorics.Graph` modules do not supply multigraph bipartiteness,
degree, proper edge coloring, chromatic index, or König's theorem.

`SimpleGraph.IsBipartite`, `SimpleGraph.lineGraph`, `SimpleGraph.Coloring`,
`SimpleGraph.chromaticNumber`, `SimpleGraph.maxDegree`, and `SimpleGraph.EdgeLabeling` provide
useful simple-graph substrate. `lineGraph_adj_iff_exists` identifies adjacency of distinct incident
simple-graph edges. `EdgeLabeling.lean` explicitly reserves "edge-colouring" for the additional
proper-incidence condition, which it does not define.

For the prospective simple-graph encoding, `G.lineGraph.chromaticNumber` has type `ENat` while
`G.maxDegree` has type `Nat`; even that restricted equality needs a coercion and finiteness
argument. More importantly, `SimpleGraph` collapses the parallel edges allowed by the source.
A bounded exact-topic search found no König edge-coloring or chromatic-index declaration in pinned
mathlib or repo-local Lean. This is intake discovery only, not the later immutable anchor audit and
not a global absence theorem.

## Exit gate

Before statement freeze, accountable source and formal reviewers must independently approve the
source transcription, translation, premise/conclusion map, equality bridge, correction/errata
status, and multigraph representation. The statement phase must then freeze the exact binders,
incidence and degree definitions, edge-coloring and chromatic-index predicates, minimal imports,
foundation/TCB/computation profiles, expression and environment hashes, alternate transports, and
all four required mutation classes. Until then the root remains `[H1, M4, R4]`.
