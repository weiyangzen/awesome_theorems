# THM-M-0825 scope map

## Preserved repository scope

- Target identity: `THM-M-0825`, named `Dijkstra算法` (Dijkstra's algorithm).
- Literal gloss: `单源最短路径算法` (single-source shortest-path algorithm).
- Catalog attribution and date: Edsger Dijkstra, 1959.
- Recognizable boundary: Dijkstra-family shortest-path computation from a distinguished source in a
  finite weighted graph.

This is a scope description, not a frozen proposition. The intake does not silently turn the gloss
into a theorem about one chosen graph representation or implementation.

## Proposition-changing decisions

An accountable source correction must select one immutable proposition and freeze:

1. The graph model: directed or undirected, simple graph, quiver, multigraph, loops, finite carrier,
   and representation of absent edges.
2. The edge-weight carrier and order: natural, integer, rational, real, extended nonnegative real,
   or another type; addition and comparison laws; and the exact nonnegative-weight condition.
3. The input contract: distinguished source alone or source-target pair, global connectivity versus
   partial reachability, and treatment of unreachable vertices.
4. Path semantics: paths versus walks, empty paths, accumulated cost, repeated vertices, and how a
   minimum or an infinite/no-path value is represented.
5. The algorithm: state representation, settled/frontier/unseen sets, tentative labels,
   predecessor data, relaxation rule, minimum selection, tie handling, and stopping condition.
6. The output and correctness strength: one source-target path, all distances, a predecessor tree,
   partial correctness, termination, total correctness, or a bundled result.
7. Whether the theorem includes a resource claim and, if so, the input encoding, arithmetic cost,
   queue representation, graph representation, and worst/average/amortized model.
8. The ordered binders, hypotheses, alternate encodings and transport directions, foundation/TCB/
   computation profiles, correction history, and every boundary case below.

Each choice changes truth conditions or proof obligations. This list is a resolution ledger, not a
candidate statement.

## Primary-source boundary

Dijkstra's 1959 paper considers finite nodes joined by length-labelled branches and assumes at least
one path between each pair. Problem 2 asks for a minimum-total-length path from `P` to `Q`; the
procedure constructs minimum paths from `P` in increasing length until `Q` is reached. That source
also treats a minimum-spanning-tree problem and allows direction-dependent branch lengths in a
remark. A future statement must map these conventions deliberately rather than merging the two
problems or retrofitting an unreviewed modern API.

## Candidate theorem families not credited

- Correctness for one selected source-target pair under the 1959 connectivity convention.
- Correctness of all distance labels and predecessor paths from one source.
- Correctness only on vertices reachable from the source, with an infinity result elsewhere.
- Preservation of tentative-distance and settled-set invariants during one relaxation iteration.
- Termination and total correctness of a specified executable priority-queue implementation.
- A complexity bound for an array, binary heap, Fibonacci heap, or another data structure.

No candidate is selected, combined, or credited at intake.

## Boundary cases to resolve

- zero or one vertex, source equal to target, and an empty edge set;
- disconnected graphs and unreachable vertices despite the original global-connectivity premise;
- zero-weight edges and cycles, equal-cost paths, parallel edges, self-loops, and selection ties;
- negative edges or cycles, which ordinary Dijkstra correctness must exclude or redirect;
- multiple shortest paths and nonunique predecessor trees;
- overflow or infinity sentinels, exact versus floating-point arithmetic, and malformed inputs; and
- early stopping at one target versus running until every reachable vertex is settled.

No case is excluded before a proposition is selected.

## Neighbor ownership and exclusions

| Target or record | Boundary |
|---|---|
| `THM-M-0823` Kruskal algorithm | minimum-spanning-tree algorithm; not a shortest-path result |
| `THM-M-0824` Prim algorithm | minimum-spanning-tree algorithm, including Problem 1 of Dijkstra's paper; not this target |
| `THM-M-0826` Bellman-Ford algorithm | distinct shortest-path algorithm that permits negative edges under its own conditions |
| `THM-M-0827` Floyd-Warshall algorithm | distinct all-pairs shortest-path algorithm |
| `THM-C-0091` Dijkstra correctness | separate Stage0 computer-science UID outside this M-target's owned scope; its terse gloss supplies no evidence here |

Also excluded are generic shortest-path existence, unweighted graph distance, a stored correctness
hypothesis, a single execution trace or benchmark, and the catalog's untrusted `已验证` label.

## Formal and execution boundary

Pinned `SimpleGraph.edist` is an undirected, unweighted, noncomputable infimum over walk lengths.
`Quiver.Path.addWeight` only defines and reasons about accumulated edge cost. The pinned
`Quiver.shortestPath` minimizes edge count by well-founded choice. These are adjacent mathematical
substrates, not a Dijkstra program or correctness theorem. The canonical statement, discovery
protocol, obligation registry, and exact anchor audit remain downstream work.
