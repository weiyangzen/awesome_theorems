# THM-M-0879 scope map

## Received scope

The repository fixes only the title `多商品流`, collective attribution `众多数学家`, period
`20世纪`, and gloss `多种商品的并发流`. It gives no bibliography, definition, ordered binders,
hypotheses, conclusion, proof, or formal artifact. Stage0 repeats the gloss and explicitly leaves
the formal system, foundations, exact definitions and premises, proof route, dependencies,
alternate forms, axioms, machine status, and artifact links open. The `已验证` label is untrusted.

The phrase most naturally identifies multicommodity or concurrent network flow. That identifies a
subject, not an exact theorem. No familiar textbook formulation may fill the missing mathematics
without a reviewed source decision.

## Candidate mathematical families

An eventual source-approved target could concern one of the following, but none is asserted or
credited at intake:

- feasibility of simultaneously routing a finite family of source-sink demands;
- existence or characterization of a maximum concurrent-flow scaling factor;
- minimization of congestion for fixed demands;
- a linear-programming duality between a splittable multicommodity flow and a metric or path-length
  optimization problem;
- a flow-cut gap or sparsest-cut approximation theorem;
- an algorithm or approximation scheme with a precise running-time and error guarantee; or
- a special two-commodity, integral, unsplittable, directed, or undirected result.

These are not logically interchangeable and have different domains, assumptions, conclusions, and
proof obligations.

## Proposition-changing decisions

Before the statement phase can freeze a canonical claim, an accepted source and reviewer must fix:

1. The network model: finite directed graph, undirected graph, multigraph, or symmetric arcs, and
   the treatment of loops and parallel edges.
2. The commodity index and data: ordered terminal pairs, demands, supplies, weights, and whether
   repeated or zero-demand commodities are allowed.
3. The capacity model: edge or vertex capacities, shared versus commodity-specific capacities,
   capacity codomain, positivity, and finiteness.
4. The flow representation: directed edge values, antisymmetric undirected values, weighted paths,
   or a decomposition quotient.
5. Feasibility: nonnegativity, conservation at nonterminals, exact versus lower-bound demand
   satisfaction, and the shared-capacity aggregation constraint.
6. Splittable fractional, integral, or unsplittable routing and whether cycles or circulations are
   admitted.
7. The objective: maximum common throughput, maximum total throughput, minimum congestion,
   feasibility only, cost minimization, or another optimization problem.
8. Whether an optimum is a maximum/minimum or only a supremum/infimum, and which compactness or
   finiteness hypotheses ensure attainment.
9. The conclusion: existence, exact value equality, LP duality, path-cut relation, integrality,
   approximation factor, or algorithm correctness and complexity.
10. Every constant, quantifier order, normalization, source correction, proof boundary, and
    representation transport.

## Boundary and degenerate cases

No case is excluded before a proposition is selected. Source review must decide empty vertex,
edge, and commodity types; source equal to sink; disconnected terminal pairs; zero, negative, or
infinite capacities and demands; zero total demand; repeated terminal pairs; loops and parallel
edges; empty paths; circulations; infeasible instances; throughput zero; unbounded objectives;
division by zero in ratios; and nonattainment of optima.

These cases matter. For example, storing feasible per-commodity flows in a hypothesis can make an
existence claim circular, while allowing every demand to be zero can make a concurrency statement
vacuous.

## Non-substitution boundary

The following cannot close this target without an accepted exact statement and checked bridge:

- `THM-M-0814`, the single-commodity max-flow min-cut theorem;
- `THM-M-0877`, generic network flow, or `THM-M-0878`, minimum-cost flow;
- `THM-M-0880`, sparse cut, or a flow-cut-gap theorem selected from that neighboring scope;
- feasibility or weak duality alone when the selected target is an optimum or approximation result;
- an integral, unsplittable, two-commodity, uniform-capacity, or all-pairs special case substituted
  for a general fractional claim, or conversely;
- correctness of one routing algorithm or a numerical solution of one network instance;
- a structure or hypothesis that stores the desired optimum, dual certificate, or routing;
- generic graph, path, and finite-sum APIs checked by the intake probe; or
- the catalog's untrusted verified label, a title match, or bibliographic abstract used as proof.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe authenticates
undirected multigraph incidence (`Graph`, `Graph.IsLink`, `Graph.Inc`), simple-graph paths, and
finite summation. A bounded exact-topic query over repo-local Lean and pinned mathlib found no
multicommodity-flow, concurrent-flow, network-flow, max-flow, or min-cut declaration. This is an
intake observation, not a global absence claim or the downstream immutable anchor audit.

`S56-M-0879-STATEMENT` must first select and independently approve one immutable proposition, then
freeze the network, commodity, capacity, flow, objective, extrema, binder, and boundary choices and
elaborate that exact Lean target. Every later phase remains dependency-ordered and open.
