# Scope map

## Preserved theorem family

The repository fixes the algorithm name, authors, year, and maximum-flow subject. The inspected
primary paper gives several materially different propositions within that family:

1. **Generic conditional correctness.** If the generic preflow algorithm terminates with finite
   distance labels, its preflow is a maximum flow (Theorem 3.4).
2. **Generic termination and operation bound.** The generic algorithm terminates after
   `O(n^2 m)` push and relabel operations (Theorem 3.11), which combines with Theorem 3.4.
3. **FIFO sequential implementation.** The queue-based discharge implementation runs in
   `O(n^3)` time (Theorem 4.5); its output correctness depends on the generic results and an exact
   refinement from the implementation to the generic transition system.
4. **Other implementations.** Maximum-distance and wave selection have `O(n^3)` bounds, while the
   dynamic-tree version and parallel/distributed variants have different statements and costs.

The math catalog's gloss does not select one of these roots. The separate `THM-C-0099` record's
`O(V^3)` wording is evidence for the FIFO-complexity candidate, not authority to replace
`THM-M-0830` with it.

## Decisions required at statement freeze

1. Select the exact primary theorem or approved composite root: correctness, termination,
   `O(n^2 m)` operations, FIFO `O(n^3)` time, or a precisely typed conjunction.
2. Freeze the network representation: finite vertex type, directed edge relation or capacity
   matrix, distinct source and sink, positive edge capacities, zero capacity off edges, and whether
   antiparallel edges and self-loops are allowed.
3. Freeze the capacity/flow carrier. The paper uses real-valued capacities and an antisymmetric
   function on all vertex pairs; integer, natural, nonnegative-real, edge-indexed, or multigraph
   encodings require checked transports.
4. Define flow, preflow, excess, residual capacity and graph, active vertices, distance labels,
   initialization, admissible push, relabel, discharge, FIFO queue state, and final output.
5. Specify determinism and scheduling: generic arbitrary enabled operations versus FIFO, exact
   discharge stopping convention, edge-list order, and how choices are quantified.
6. Freeze termination semantics and the link between "no active vertices," finite labels, flow
   conservation, absence of an augmenting path, and maximum flow.
7. For complexity, freeze `n`, `m`, the paper's `m >= n - 1` convention, unit-cost arithmetic/data
   structure model, primitive operations, queue/edge scans, asymptotic relation, and small-network
   behavior.
8. Resolve empty, singleton, source-equals-sink, unreachable-sink, zero-capacity, no-edge,
   antiparallel-edge, self-loop, disconnected, and zero-flow cases before excluding any of them.
9. Freeze exact Lean imports, foundation/choice, computation, TCB, freshness, and mutation profiles
   only after the proposition and algorithm semantics are selected.

## Explicit exclusions

- Maximum-flow/min-cut existence or the Ford-Fulkerson augmenting-path theorem alone.
- Edmonds-Karp, Dinic, Karzanov, highest-label, wave, dynamic-tree, parallel, distributed, or
  minimum-cost-flow results substituted for the selected push-relabel variant.
- Generic correctness alone advertised as an `O(n^3)` result, or Theorem 4.5 advertised as output
  correctness without the required refinement and generic proof dependencies.
- A capacity structure, execution trace, termination hypothesis, maximum-flow witness, or cost
  certificate that stores the desired conclusion.
- A finite benchmark, extracted program run, floating-point result, or unchecked cost experiment.
- The catalog label `已验证`, the CS duplicate row, a primary-source citation, or an elaborated API
  probe treated as H0, machine proof, or theorem-completion evidence.

No canonical expression, statement fingerprint, checked alternate encoding, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.
