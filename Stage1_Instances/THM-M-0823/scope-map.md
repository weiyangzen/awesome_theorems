# Scope map

## Preserved source scope

The repository fixes only the Kruskal-algorithm label, Joseph Kruskal attribution, year 1956, and
the phrase "a greedy algorithm for a minimum spanning tree." The closest primary-source lead is
Kruskal's 1956 paper, whose first problem asks for a practical construction of a shortest spanning
tree and whose Construction A repeatedly chooses a shortest unchosen edge that does not create a
loop. This identifies the likely theorem family; intake does not promote it to the canonical claim.

The likely subject is a finite weighted graph, a greedy sequence of accepted edges, preservation of
acyclicity, termination with a spanning tree, and minimal total edge weight among spanning trees.
Those components are only a candidate family until an accountable source reviewer approves one
exact root.

## Decisions required at statement freeze

1. Approve an immutable source edition and exact problem, construction, assertion, proof, correction,
   errata, and independent-review boundary.
2. Decide whether the root is correctness of Construction A, existence of a minimum spanning tree,
   uniqueness under distinct weights, a bundled correctness theorem, or executable total correctness.
3. Fix finite simple graph versus finite multigraph, connected versus componentwise forest input,
   nonempty versus possibly empty vertex type, and the representation of undirected edges.
4. Fix the edge-weight codomain and hypotheses: positive real lengths as in the source lead, arbitrary
   linearly ordered additive weights, distinct weights, or ties.
5. Specify how equal-weight edges are ordered, whether every tie-breaking order must work, and whether
   the algorithm is deterministic, nondeterministic, relational, or parameterized by a sorted list.
6. Define the algorithm state, the `does not form a loop` test, accepted and rejected edges, termination
   measure, and the precise returned subgraph or edge set.
7. Define spanning-tree feasibility, total weight, and minimality over all spanning trees; decide whether
   uniqueness is part of the conclusion and how equality of trees is represented.
8. Resolve zero- and one-vertex graphs, graphs with no edges, disconnected graphs, loops or parallel
   edges if admitted, negative or zero weights if admitted, and repeated weights.
9. Decide whether complexity, data-structure behavior, or only mathematical correctness is in scope.

## Explicit exclusions

- The Kruskal-Katona theorem, which shares a surname but concerns shadows of uniform set families.
- Prim's algorithm (`THM-M-0824`) or another minimum-spanning-tree algorithm substituted for Kruskal's.
- The separate Stage0 record `THM-C-0094` ("Kruskal algorithm correctness") silently used as the
  source authority or as evidence owned by this target.
- A generic spanning-tree existence theorem without weights or the named greedy construction.
- The distinct-weights uniqueness theorem without the algorithm-correctness conclusion, unless an
  approved source review selects it as the repository root.
- A function whose output is assumed, rather than proved, to be acyclic, spanning, or minimum.
- A special complete graph, fixed edge list, fixed vertex count, or uniquely weighted case substituted
  for a broader approved root.
- The catalog's untrusted `已验证` label or an adjacent API check used as source or kernel evidence.

## Formal boundary

Pinned mathlib exposes `SimpleGraph.IsAcyclic`, `SimpleGraph.IsTree`,
`SimpleGraph.Subgraph.IsSpanning`, subgraph edge sets, and existence of a tree below a connected
graph. These are representation and unweighted graph-theory substrate only. A bounded local search
found no Kruskal minimum-spanning-tree algorithm or weighted optimality declaration; `KruskalKatona`
is unrelated. The probe is intake feasibility evidence, not an exhaustive anchor audit and not
proof of global absence.
