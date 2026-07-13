# THM-M-0826 scope map

## Preserved repository scope

The literal repository boundary is the label `Bellman-Ford算法`, glossed as
`带负权边的最短路径算法` and attributed to Richard Bellman and Lester Ford in 1958. This
identifies the Bellman-Ford family for weighted directed shortest paths, including settings with
negative edge weights. It does not select one mathematical proposition or one executable program.

Candidate results that require separate source decisions include:

- correctness of source-to-every-vertex distance estimates when no relevant negative cycle exists;
- construction and correctness of predecessor paths or an arborescence;
- soundness and completeness of a final relaxation pass as a negative-cycle detector;
- termination and iteration bounds for a specified edge-relaxation schedule;
- an `O(|V||E|)` running-time theorem under a fixed input and cost model; and
- refinement of a concrete array, map, or imperative implementation to a mathematical recurrence.

None is the canonical target at intake.

## Decisions required before statement freeze

1. Admit and independently review an immutable primary or authoritative source, then select one
   exact theorem or algorithm-correctness proposition with incorporated definitions and proof
   boundary.
2. Fix the graph model: directed or undirected, finite vertex and edge representations, parallel
   edges and self-loops, source and optional target, and all decidability/finiteness assumptions.
3. Fix the weight domain and arithmetic: integers, rationals, reals, or another ordered additive
   structure; representation of infinity; overflow policy; and whether all finite sums are exact.
4. Define walks, paths, simple paths, reachability, path weight, shortest distance, and when a
   shortest value is undefined or negative infinity.
5. Fix the algorithm: initialization, relaxation operator, edge traversal order, number of passes,
   early stopping, predecessor updates, tie behavior, output type, and negative-cycle check.
6. Fix the negative-cycle premise and output contract: no cycle anywhere, no cycle reachable from
   the source, no negative cycle on a source-to-queried-vertex route, per-vertex unboundedness, or a
   global diagnostic.
7. Fix the exact conclusion: distance equality, path witness validity, detector equivalence,
   termination, complexity, implementation refinement, or a specified conjunction.
8. Freeze ordered binders, hypotheses, universes, alternate encodings and transport directions,
   foundation/TCB/computation profiles, and every boundary case before elaboration.

## Degenerate and boundary cases to resolve

- empty and singleton vertex types, absent source, no edges, isolated and unreachable vertices;
- source-to-source distance, self-loops, parallel edges, zero-weight and negative-weight edges;
- a negative self-loop, reachable and unreachable negative cycles, and cycles that cannot reach a
  queried target;
- multiple equal shortest paths, predecessor ties, and zero-weight cycles;
- graphs with a finite minimum but negative edges, and graphs whose walk weights are unbounded
  below;
- fewer than `|V| - 1` meaningful passes, early convergence, and a final relaxable edge;
- exact mathematical weights versus fixed-width integer or floating-point implementation behavior;
  and
- overflow, sentinel collision, malformed input, and resource exhaustion in executable variants.

No case is excluded until a proposition is selected.

## Explicit non-substitutions

- Dijkstra correctness, which normally assumes nonnegative edge weights, is not Bellman-Ford
  correctness.
- Floyd-Warshall all-pairs correctness, DAG shortest paths, breadth-first search, and unweighted
  shortest-path length are distinct targets.
- The path optimality principle, triangle inequality for distances, or additive path-weight
  identities alone do not prove an algorithm correct.
- A theorem assuming the desired distances, shortest paths, or negative-cycle diagnostic as an
  input field is circular and supplies no proof.
- Correctness only on acyclic, nonnegative, fixed-size, or otherwise specialized graphs cannot
  replace an unidentified general target.
- A successful run on examples, benchmark timing, pseudocode trace, or unchecked certificate is
  not theorem evidence.
- The untrusted `已验证` label, a citation, or `IntakeProbe.lean` provides no source or proof credit.

## Neighbor-target boundaries

| Target | Boundary |
|---|---|
| `THM-M-0825` Dijkstra algorithm | single-source shortest paths under a materially different nonnegative-weight regime |
| `THM-M-0827` Floyd-Warshall algorithm | all-pairs dynamic programming rather than this repeated edge-relaxation family |
| `THM-M-0823` Kruskal algorithm | minimum spanning trees, not shortest directed paths |
| `THM-M-0824` Prim algorithm | minimum spanning trees, not shortest directed paths |

## Formal and execution boundary

The canonical human statement and Lean expression remain null. Pinned mathlib's `Digraph`,
`Quiver.Path`, and additive path-weight operations are possible substrate, not a Bellman-Ford
specification or theorem. No obligation registry or discovery protocol is frozen, no formal
candidate is credited, and no proof tree may be constructed from the topic gloss. The first
downstream task must select and review one source proposition before it can freeze minimal imports,
an elaborated expression, checked transports, and required statement mutations.
