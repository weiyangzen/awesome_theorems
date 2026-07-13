# Scope map

## Preserved theorem family

The intake preserves the Dinic/Dinitz maximum-flow algorithm family named by the catalog: build a
level graph from the current residual network, find a blocking flow in that level graph, update the
residual state, and repeat. The intended mathematical properties include maximum-flow correctness
and the source-selected complexity result. This is a scope description, not a frozen proposition
or executable specification.

The Stage1-bearing mathematical record says only "layered algorithm for maximum flow." A separate
computer-science record says `O(V^2 E)` or `O(V E log V)`. Neither record supplies definitions,
assumptions, proof contract, algorithm-version boundary, or a decision about whether correctness
and complexity are separate roots or one conjunction.

## Proposition-changing decisions

Before statement freeze, an approved source and reviewers must decide:

1. the network representation: finite directed graph, quiver, edge-indexed multigraph, adjacency
   matrix, or another model, including parallel and antiparallel edges;
2. distinguished source and sink, whether they must differ, and whether incident source/sink edges
   or disconnected vertices are restricted;
3. the capacity codomain and assumptions: natural, integer, rational, real, nonnegative, finite,
   integral, or another source-defined class;
4. the definition of a feasible flow, including capacity constraints, conservation, flow value,
   skew symmetry or paired-edge representation, and equality of flows;
5. residual vertices and edges, forward and reverse residual capacity, zero-capacity edge removal,
   parallel-edge identity, cancellation semantics, and update invariants;
6. the level function and level graph: directed residual reachability, shortest edge count, BFS or
   an abstract distance specification, admissible edges, unreachable vertices, and tie behavior;
7. the blocking-flow contract: path blocking versus saturation/cut characterization, existence,
   construction method, current-arc optimization, and whether an abstract witness or executable
   procedure is required;
8. the outer algorithm's state transition, termination measure, and output: flow only, value,
   minimum cut, certificate, or an explicitly checked combination;
9. correctness strength: preservation of feasibility, strict level progress, absence of residual
   augmenting paths, maximum-flow optimality, max-flow/min-cut certification, or the exact
   composition selected by the source; and
10. complexity model and version: input encoding, elementary operation, meanings of `V` and `E`,
    original blocking-flow implementation, later dynamic-tree implementation, specialized unit
    networks/capacities, worst-case regime, and exact or asymptotic bound.

These choices alter binders, hypotheses, conclusion, computation profile, and proof architecture.

## Boundary cases to resolve

- empty and singleton vertex types;
- source equal to sink versus an explicit `s != t` hypothesis;
- no source-to-sink path and zero maximum flow;
- zero-capacity edges, no edges, self-loops, parallel edges, and antiparallel edges;
- natural/integral versus rational/real capacities, including fractional bottlenecks;
- disconnected components and vertices irrelevant to the source-sink component;
- unreachable vertices and their level value, zero-length paths, and admissible residual cycles;
- nonunique blocking flows, zero blocking flow, and multiple admissible-path choices;
- early saturation, reverse-edge cancellation, and whether every phase strictly raises sink level;
- whether `V` and `E` count all represented or only active edges, and how dynamic-tree operations
  are costed; and
- whether a maximum flow, its value, and a minimum-cut witness are data or existential conclusions.

No boundary case is excluded at intake.

## Explicit exclusions

- Edmonds-Karp or arbitrary-path Ford-Fulkerson in place of level graphs and blocking flows.
- Push-relabel, capacity scaling, bipartite matching, or another maximum-flow algorithm.
- The maximum-flow/minimum-cut theorem alone, without the Dinic execution and selected complexity
  result.
- An undirected simple-graph shortest-path theorem used as the directed residual level graph.
- A generic path flow that is not blocking in the source-selected sense.
- The later `O(V E log V)` dynamic-tree result or a specialized unit-network bound attributed to
  the unchanged 1970 implementation without a checked source/version bridge.
- A theorem that assumes a maximum flow, optimal cut, blocking-flow oracle, level-progress result,
  or desired complexity bound as an unexplained structure field or hypothesis.
- A fixed finite example, exhaustive enumeration, timing experiment, native evaluator result, or
  unchecked certificate.
- The companion `O(V^2 E)`/`O(V E log V)` slogan selected as the canonical root without approved
  source scope and a precise cost model.
- The catalog's untrusted verified label, bibliographic metadata, a no-match search, or the intake
  API probe treated as proof evidence.

## Neighbor boundaries

- `THM-M-0828` (Edmonds-Karp) is a shortest-single-augmentation method, not the level-graph and
  blocking-flow algorithm.
- `THM-M-0830` (push-relabel) uses preflows and local pushes rather than blocking flows.
- `THM-M-0814` is the maximum-flow/minimum-cut theorem; it may become a dependency but does not
  supply Dinic execution or complexity.
- The separate Stage0 computer-science record `THM-C-0098` makes two complexity glosses explicit,
  but it is not a Stage1 source authority and grants no statement or proof credit here.

## Formal boundary

No canonical Lean expression is frozen. Pinned generic path/metric APIs elaborate, but mathlib's
`SimpleGraph` surface is undirected and the quiver path surface supplies no capacity, feasible-flow,
residual update, level graph, blocking flow, maximality, or complexity theorem. The bounded search
is intake discovery evidence, not an exhaustive immutable anchor audit or a theorem of global
absence.
