# Scope map

## Preserved theorem family

The intake preserves the Edmonds-Karp maximum-flow algorithm family named by the catalog: repeated
augmentation along a minimum-edge-count source-to-sink path in the current residual network,
together with the mathematical properties that make this a correct polynomial-time maximum-flow
method. This is a scope description, not a frozen proposition or executable specification.

The companion computer-science catalog says `O(VE^2)` while the Stage1-bearing mathematical record
says only "polynomial." Neither record supplies definitions, assumptions, a proof contract, or a
decision about whether correctness and complexity are separate roots or one conjunction.

## Proposition-changing decisions

Before statement freeze, an approved source and reviewers must decide:

1. the network representation: finite directed graph, quiver, edge-indexed multigraph, adjacency
   matrix, or another model, including parallel and antiparallel edges;
2. distinguished source and sink, whether they must differ, and whether incident source/sink edges
   or disconnected vertices are restricted;
3. the capacity codomain and assumptions: natural, integer, rational, real, nonnegative, finite,
   integral, or another source-defined class;
4. the definition of a feasible flow, including capacity constraints, conservation, skew symmetry
   or paired-edge representation, flow value, and equality of flows;
5. residual vertices and edges, forward and reverse residual capacity, zero-capacity edge removal,
   parallel-edge identity, and cancellation semantics;
6. the exact shortest augmenting-path rule: breadth-first search by edge count, allowed tie breaking,
   and whether an abstract shortest-path choice or a concrete executable queue implementation is
   required;
7. augmentation amount, state update, termination criterion, and output: flow only, flow and value,
   minimum cut, certificate, or an explicitly checked combination;
8. correctness strength: preservation of feasibility, termination, lack of augmenting paths,
   maximum-flow optimality, maximum-flow/minimum-cut equality, or the exact composition selected by
   the source; and
9. complexity model: input encoding, elementary operation, meanings of `V` and `E`, treatment of
   zero and parallel edges, worst-case versus another regime, and exact versus asymptotic bound.

These choices alter binders, hypotheses, conclusion, computation profile, and proof architecture.

## Boundary cases to resolve

- empty and singleton vertex types;
- source equal to sink versus an explicit `s != t` hypothesis;
- no source-to-sink path and zero maximum flow;
- zero-capacity edges, no edges, self-loops, parallel edges, and antiparallel edges;
- natural/integral versus rational/real capacities, including fractional bottlenecks;
- disconnected components and vertices irrelevant to the source-sink component;
- zero-length paths and residual paths containing a forward and reverse edge for the same original
  edge;
- multiple breadth-first shortest augmenting paths and arbitrary versus deterministic tie breaking;
- whether `V` and `E` count all represented vertices/edges or only positive-residual/current edges;
- whether a maximum flow, its value, and a minimum-cut witness are data or existential conclusions.

No boundary case is excluded at intake.

## Explicit exclusions

- Ford-Fulkerson with an arbitrary augmenting-path rule in place of the breadth-first rule.
- The maximum-flow/minimum-cut theorem alone, without the Edmonds-Karp execution and complexity
  result.
- Dinic, push-relabel, capacity scaling, bipartite matching, or another maximum-flow algorithm.
- An undirected simple-graph shortest-path theorem used as the residual-network algorithm.
- A theorem that assumes a maximum flow, optimal cut, augmenting-path oracle, or desired complexity
  bound as a structure field or hypothesis.
- A fixed finite example, exhaustive enumeration, timing experiment, native evaluator result, or
  unchecked certificate.
- The familiar `O(VE^2)` slogan selected as the canonical root without approved source scope and a
  precise cost model.
- The catalog's untrusted verified label, DOI metadata, a no-match search, or the intake API probe
  treated as proof evidence.

## Neighbor boundaries

- `THM-M-0827` (Floyd-Warshall) is an all-pairs shortest-path target, not a residual augmentation
  theorem.
- `THM-M-0829` (Dinic) and `THM-M-0830` (push-relabel) are distinct maximum-flow algorithms with
  different state transitions and complexity arguments.
- The separate Stage0 computer-science record `THM-C-0097` makes the `O(VE^2)` gloss explicit, but it
  is not a Stage1 source authority and grants no statement or proof credit here.
- Maximum-flow/minimum-cut and Ford-Fulkerson may become dependencies after statement and obligation
  freezes; they cannot close this target by proximity.

## Formal boundary

No canonical Lean expression is frozen. Pinned generic path/metric APIs elaborate, but mathlib's
`SimpleGraph` surface is undirected and the quiver path surface supplies no capacity, feasible-flow,
residual-update, BFS execution, maximality, or complexity theorem. The bounded search is intake
discovery evidence, not an exhaustive immutable anchor audit or a theorem of global absence.
