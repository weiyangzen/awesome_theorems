# THM-M-0824 scope map

## Received scope

The authoritative target inventory names `Prim算法` in combinatorics/graph theory. Its only
mathematical gloss is "another algorithm for minimum spanning trees." The attribution and year
make Prim's shortest-connection method the intended family, while the wording does not state one
theorem. Intake preserves that family and refuses to choose missing mathematics.

## Proposition-changing choices

An exact downstream statement must freeze all of the following before it can receive proof credit:

| Dimension | Choices that remain open |
|---|---|
| graph object | finite simple graph, finite edge set on a larger type, multigraph, or an explicit edge-list representation |
| direction and incidence | undirected edges are intended by minimum spanning tree, but loops, parallel edges, and endpoint encoding are not specified |
| input hypotheses | nonempty vertex set, connected graph, or a component-wise minimum spanning forest convention |
| weights | carrier, total/preorder versus linear order, addition and finite sum, negative values, infinities, and computable comparison |
| initialization | arbitrary or fixed start vertex, initial visited set, and behavior on zero or one vertex |
| step | frontier definition, minimum crossing-edge selection, endpoint insertion, state invariant, and deterministic or nondeterministic ties |
| termination | exact stopping condition, failure state, recursion measure, and treatment of disconnected input |
| output | edge set, simple graph, subgraph, parent map, traversal trace, or executable result type |
| correctness | termination, subgraph/spanning/tree validity, equality with a specified trace, minimum total weight, uniqueness, or a conjunction |
| resources | abstract edge selections, comparison count, adjacency matrix/list/heap model, runtime, and worst-case convention |
| formal boundary | mathematical nondeterministic algorithm, one executable implementation, or refinement between the two |

The prospective mathematical core is correctness of a source-selected Prim iteration on a finite
connected undirected weighted graph: it terminates with a spanning tree whose total edge weight is
minimal among spanning trees. That sentence is a scope guide only. It is not the canonical claim
because the repository does not fix the data, algorithm, assumptions, quantifier order, or exact
conjunction above.

## Cases to resolve

- Empty and singleton vertex types, an empty edge set, and a disconnected input.
- Loops or parallel edges if a non-simple graph representation is selected.
- Equal-weight frontier edges, nonunique minimum spanning trees, and deterministic versus
  nondeterministic output.
- Negative, zero, unbounded, infinite, or noncomputably ordered weights.
- A missing or invalid start vertex and a start vertex in only one component.
- Stuck states, repeated vertices or edges, and whether partial output is returned on failure.
- Exact mathematical weights versus machine integers, floating point, overflow, and comparison
  instability.

No case is excluded at intake. Assuming a minimum spanning tree, an optimal output, or the key cut
invariant as an input field would be circular if the selected target is meant to establish it.

## Candidate claims not credited

- Existence of some spanning tree in every connected simple graph.
- The cut property or exchange lemma for minimum spanning trees.
- Preservation of an acyclic connected-growth invariant by one Prim step.
- Termination after the source-selected number of vertex or edge additions.
- Tree validity and minimum-total-weight optimality of a complete run.
- Independence of optimal total weight from tie choices, or uniqueness under distinct weights.
- A heap-, matrix-, or list-specific complexity result.

These may later become root components or dependencies, but none is selected or proved here.

## Neighbor and substitution exclusions

- `THM-M-0823` separately owns Kruskal's algorithm. A generic greedy-tree or matroid proof does not
  identify Prim's state transition without a checked bridge.
- `THM-M-0825` separately owns Dijkstra's shortest-path algorithm. Similar frontier syntax does not
  transfer correctness or optimality.
- Stage0 record `THM-C-0095` is a related computer-science catalog wording, not a rev-5.6 target,
  source citation, accepted deduplication map, or second proof.
- A generic spanning-tree existence theorem, tree cardinality theorem, or minimum of a finite set
  is substrate only.
- A definition, pseudocode trace, program test, benchmark, or computed example is not universal
  correctness.
- A structure or hypothesis storing the desired tree, minimality, or successful run supplies no
  proof.
- The catalog's `已验证` label and the discovery-only Lean probe supply no H or M credit.

## Formal boundary

Pinned mathlib provides finite simple graphs, spanning subgraphs, trees, finite edge sets, and the
fact that a connected simple graph contains a tree subgraph. It does not thereby choose a weight
model, define Prim's algorithm, or prove minimum-weight correctness. The probe authenticates only
that adjacent interface. Exact target selection, exhaustive anchor discovery, obligation freezing,
proof bodies, composition, trust, readability, and release evidence belong to later open phases.
