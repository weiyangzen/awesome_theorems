# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6327-6332` supplies exactly the title `Whitney定理`, attribution
to Hassler Whitney, the year 1932, the gloss `2-连通图的耳分解` ("ear decomposition of
2-connected graphs"), importance "high," and status `已验证`. Git history attributes all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, stable source identifier, theorem/page locator, formula, definitions, direction,
binders, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23549-23574` repeats the gloss while leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected primary source lead

Hassler Whitney, *Non-separable and planar graphs*, Transactions of the American Mathematical
Society 34(2) (1932), 339-362, DOI `10.1090/S0002-9947-1932-1501641-2`, was inspected from the
AMS-hosted PDF on 2026-07-13.

- Article pages 339-340 define finite graphs whose arcs may be loops or parallel arcs, chains,
  suspended chains, circuits, connectedness, and subgraphs.
- Article page 342 defines a non-separable connected graph by inability to split it at one vertex;
  Theorems 5-8 on pages 342-343 relate that definition to cut vertices and cyclic connectedness,
  with explicit qualifications about loops and graph size.
- Article pages 349-350, Theorem 18, prove that an arc or suspended chain can be removed from a
  non-separable graph of nullity greater than one while leaving a non-separable graph.
- Article page 350, Theorem 19, states: "We can build up any non-separable graph containing at
  least two arcs by taking first a circuit, then adding successively arcs or suspended chains, so
  that at any stage of the construction we have a non-separable graph." The next sentence states
  the converse and explains it through circuits of graphs.
- The observed 24-page PDF SHA-256 is
  `dc5b3da59a06b4b6f21bd424add1d28576b059143a470f2593257a0073d14fa5`.

Crossref confirms the author, published year, volume, issue, pages, and DOI. The paper is a strong
source lead for the catalog family, but the PDF was not added to the repository. Immutable source
admission, a complete definition/premise/proof-node/correction map, the modern 2-connected/simple-
graph transport, and independent review remain open. The source supports provisional `H1`, not
`H0`.

## Clause crosswalk

| Catalog component | Primary-source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| graph | finite graph with vertices and arcs; loops and parallel arcs allowed | likely `G : SimpleGraph V` with finite `V`, or a different multigraph model | source and pinned candidate models differ; transport open |
| 2-connected | Whitney's non-separable graph plus size/loop qualifications in Theorems 5-8 | vertex deletion, cut-vertex, or internally disjoint-path predicate | no canonical predicate; equivalence and small cases open |
| initial cycle | "taking first a circuit" in Theorem 19 | `Walk.IsCycle`, its support/toSubgraph, or cycle-graph isomorphism | exact carrier and simple-graph minimum length open |
| ear | an added arc or suspended chain; suspended chains have at least two arcs, internal vertices on no other arcs, and endpoints incident with at least two other arcs | path with old endpoints, new internal vertices and edges, attached to a partial subgraph | exact path/subgraph invariant and one-edge case open |
| decomposition | successive construction whose every stage is non-separable | finite ordered list plus partial unions, attachment, preservation, and coverage | data structure and equality with ambient graph open |
| theorem direction | Theorem 19 constructs every eligible non-separable graph | existence of an ear decomposition | source lead identified; exact modern proposition not frozen |
| converse | sentence following Theorem 19 | ear construction implies selected 2-connectivity predicate | separate source clause; root inclusion open |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H0 or M credit |

## Pinned Lean boundary

Pinned mathlib supplies `SimpleGraph.Preconnected`, `SimpleGraph.Connected`,
`Preconnected.exists_isPath`, `Walk.IsPath`, `Walk.IsCycle`, `Walk.toSubgraph`,
`Walk.connected_induce_support`, `Subgraph.induce`, and `Subgraph.deleteVerts`. These APIs cover
only parts of a possible simple-graph encoding. They do not define a Whitney ear decomposition or
state the source theorem, and ordinary `Connected` is not itself 2-vertex-connectivity.

A bounded case-insensitive search of pinned mathlib and repo-local Lean found no exact-topic
declaration for ear decompositions, suspended chains, non-separable graphs, biconnected graphs, or
named vertex-2-connectivity. Unrelated convex ears, nuclear decompositions, and Whitney names from
other domains were excluded by context. This is intake discovery only, not the later immutable
formal-candidate audit and not a global absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an immutable approved source edition, map
every incorporated definition, size and loop premise, construction invariant, conclusion, converse,
and proof node, audit corrections, and independently approve the transport from Whitney's finite
multigraph/non-separable language to the catalog's modern simple-graph/2-connected language. Only
then may the statement phase freeze the exact Lean graph model, connectivity and ear predicates,
ordered binders, minimal imports, elaborated expression and environment hashes, checked alternate
encodings, and removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
