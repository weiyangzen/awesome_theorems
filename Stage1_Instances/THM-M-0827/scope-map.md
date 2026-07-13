# THM-M-0827 scope map

## Preserved theorem family

The intake preserves the Floyd-Warshall all-pairs shortest-path algorithm family named by the
catalog: a finite sequence of matrix updates that allows successively more intermediate vertices,
with an intended final relation to shortest path or walk costs. This sentence is a scope
description, not a frozen proposition or executable specification.

The separate computer-science catalog adds an `O(n^3)` slogan. That record is useful boundary
evidence but has a different UID and cannot silently broaden this mathematical target, whose
literal gloss contains no complexity clause.

## Proposition-changing decisions

Before statement freeze, approved sources and independent reviewers must decide:

1. the graph representation: directed graph, quiver, edge-indexed multigraph, weighted adjacency
   matrix, or another finite model, including loops and parallel edges;
2. the weight carrier and assumptions: natural, integer, rational, real, min-plus semiring, or
   another ordered additive structure, together with exact arithmetic and overflow policy;
3. absent-edge, diagonal, infinity, and unbounded-below conventions;
4. the definition of walks, paths, reachability, total weight, shortest value, and whether a
   minimum witness must exist;
5. the negative-cycle boundary: none anywhere, none on a relevant route, per-pair negative
   infinity, detection via the diagonal, or an explicit diagnostic result;
6. the algorithm state: vertex enumeration, initial matrix, recurrence, update order, snapshot
   versus in-place semantics, predecessor/next-hop state, and tie behavior;
7. the exact output and correctness relation: distance matrix only, path reconstruction, closure,
   negative-cycle detector, executable refinement, or a specified combination;
8. whether termination, exact operation count, or `O(n^3)` is part of this root; and
9. all ordered binders, universes, decidability/finiteness assumptions, transports, and boundary
   cases.

Each choice changes the formal target or its hypotheses.

## Boundary cases to resolve

- empty and singleton vertex types, no edges, isolated vertices, and disconnected graphs;
- self-distance, self-loops, parallel edges, and multiple equal-cost walks;
- zero, positive, and negative edge weights;
- reachable and unreachable negative cycles and pair-specific unboundedness;
- missing direct edges, infinity arithmetic, and an empty intermediate-vertex prefix;
- diagonal initialization with zero versus a negative self-loop;
- arbitrary versus fixed vertex enumeration and equality of results across enumerations;
- in-place updates whose row or column entries are read during the same iteration;
- finite shortest values that are infima versus values attained by paths; and
- mathematical exact weights versus fixed-width integer or floating-point behavior.

No boundary case is excluded at intake.

## Explicit exclusions

- Warshall Boolean transitive closure alone, without a checked transport to the selected weighted
  shortest-path theorem.
- Dijkstra or Bellman-Ford correctness, repeated single-source execution, Johnson's algorithm, or
  another all-pairs method.
- Generic shortest-path existence, triangle inequalities, or path-weight composition without the
  named dynamic-programming execution and correctness relation.
- Only an `O(n^3)` loop count without correctness, or complexity imported from `THM-C-0093` without
  an approved target decision and cost model.
- A theorem that stores the desired final matrix, invariant, paths, or correctness claim as a
  hypothesis or structure field.
- A fixed numerical matrix, finite trace, benchmark, evaluator output, or unchecked certificate.
- The catalog's untrusted `已验证` label, bibliographic metadata, a no-match search, or the API probe
  treated as proof evidence.

## Neighbor boundaries

| Target | Boundary |
|---|---|
| `THM-M-0825` Dijkstra algorithm | distinct single-source greedy algorithm, normally under nonnegative weights |
| `THM-M-0826` Bellman-Ford algorithm | distinct repeated-relaxation single-source family with its own negative-cycle boundary |
| `THM-C-0093` Floyd-Warshall algorithm | separate Stage0 computer-science record explicitly adding `O(n^3)`; not this target's authority |
| Warshall Boolean closure | historical and algebraic relative, not automatically weighted shortest-path correctness |

## Formal boundary

The canonical human proposition and Lean expression remain null. Pinned `Digraph`, `Quiver.Path`,
additive path weights, and `SimpleGraph.edist` elaborate, but no checked recurrence, all-pairs
matrix specification, negative-cycle policy, execution, or correctness theorem has been selected.
The bounded search is intake discovery evidence, not the later immutable anchor audit or a global
absence theorem.
