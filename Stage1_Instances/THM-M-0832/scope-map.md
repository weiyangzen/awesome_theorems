# Scope map

## Preserved algorithm family

The repository identifies the Stoer-Wagner deterministic global-minimum-cut algorithm. The source
family is the following procedure for an undirected edge-weighted graph:

1. Run a maximum-adjacency-search phase, repeatedly adding an outside vertex of greatest total
   weight to the already-added set.
2. Treat the last vertex and the rest as the cut of the phase; the last two added vertices are
   `s` and `t`.
3. Merge `s` and `t`, summing weights of their edges to every remaining vertex and removing the
   internal edge.
4. Repeat until one supervertex remains and return the lightest phase cut, interpreted back on the
   original vertex set.

This is a scope description, not a canonical formal proposition.

## Candidate source results

The inspected expanded paper contains several related claims that must not be conflated:

- Theorem 2.1: the global minimum cut of `G` is obtained by comparing a minimum `s`-`t` cut in `G`
  with a minimum cut of the graph formed by merging `s` and `t`.
- Lemma 3.1: a maximum-adjacency-search phase produces a minimum `s`-`t` cut, where `s` and `t`
  are the two vertices added last.
- End-to-end correctness: repeated phases and contractions return a minimum cut of the original
  graph.
- Running time: a phase uses `O(|E| + |V| log |V|)` priority-queue time, yielding
  `O(|V||E| + |V|^2 log |V|)` overall under the paper's implementation model.

The catalog may intend end-to-end correctness alone or correctness plus the complexity result. No
candidate is selected or credited at intake.

## Decisions required at statement freeze

1. Select and independently review one immutable source edition and one exact root proposition or
   explicitly sourced conjunction.
2. Fix the graph carrier: finite ordinary undirected graph, simple graph with a total weight
   function, weighted multigraph, or an equivalent symmetric capacity matrix. State how absent,
   zero-weight, and parallel edges are represented.
3. Fix the weight domain and premises. The inspected paper uses nonnegative real weights; a theorem
   over naturals, rationals, a canonically ordered additive monoid, or arbitrary reals changes the
   claim and proof obligations.
4. Define a cut as a nontrivial bipartition or one nonempty proper vertex subset, define crossing
   edges, and fix whether the result returns a subset, bipartition, weight, or certified pair.
5. Specify maximum-adjacency-search state, the starting vertex, tie breaking, selection semantics,
   phase output, and termination.
6. Specify contraction and original-vertex provenance: how supervertices are represented, how
   parallel incident weights are summed, how self-loops are removed, and how a phase cut is lifted
   back to the original graph.
7. Decide whether the root asserts only partial correctness, total correctness and termination,
   exact minimum weight, a witnessing partition, the phase lemma, the contraction recurrence, or an
   exact conjunction of these.
8. If runtime is included, freeze the graph representation, priority queue, unit-cost operations,
   Fibonacci-heap assumptions, input-size measure, asymptotic notation, and arithmetic-cost model.
9. Freeze ordered binders, universes, decidability and finiteness instances, hypotheses, conclusion,
   checked alternate encodings, and foundation/TCB/computation profiles.

## Boundary cases

- empty and singleton vertex types, for which a nontrivial cut does not exist;
- two vertices, no edges, disconnected graphs, isolated vertices, and zero total cut weight;
- zero-weight edges, repeated maximum-adjacency keys, and arbitrary starting vertices;
- negative weights, which are outside the inspected paper's stated domain;
- parallel edges and loops before and after contraction;
- multiple minimum cuts and whether any witness or a canonical witness is required;
- a phase with one or two current supervertices and lifting cuts through repeated contractions;
- exact real weights versus executable rational or natural weights; and
- overflow, floating-point error, cancellation, or resource limits for any executable version.

No boundary case is excluded at intake because no proposition is selected.

## Explicit exclusions

- Karger's randomized minimum-cut algorithm (`THM-M-0831`), a max-flow/min-cut algorithm, or a
  directed `s`-`t` minimum-cut theorem substituted for Stoer-Wagner.
- Nagamochi-Ibaraki sparsification or edge-connectivity results presented as the target algorithm.
- Unweighted edge connectivity alone, including `SimpleGraph.IsEdgeConnected`, without weights,
  algorithm semantics, and a checked bridge to the selected root.
- A theorem restricted to a convenient special graph class, weight domain, fixed start order, or
  unique-minimum case unless the reviewed source root has exactly that scope.
- An assumed cut witness, a structure field storing correctness, a finite example, benchmark,
  floating-point experiment, unchecked certificate, or external executable result.
- The catalog label `已验证`, a source URL, or a successful `#check` treated as human-source,
  kernel-proof, audit-completion, or theorem-completion evidence.

## Lean feasibility boundary

Pinned mathlib has finite simple-graph edges and degrees and an unweighted edge-connectivity
predicate. It does not provide a weighted graph object specialized to this algorithm, a cut-weight
definition, contraction with summed weights and original-vertex provenance, maximum-adjacency
search, or an end-to-end Stoer-Wagner theorem in the bounded search. The intake probe authenticates
only the adjacent APIs. Exact formal design and exhaustive candidate discovery belong to later
phases.
