# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0878` | frozen |
| execution item | `S56-M-0878-INTAKE`, rank 1431 | frozen |
| catalog name | `最小费用流` | frozen as received wording |
| catalog gloss | `带费用的网络流` | frozen literally |
| attribution | many mathematicians, twentieth century | untrusted metadata |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

## Candidate theorem families

The catalog does not choose among the following materially different roots. None is the canonical
statement at intake.

1. **Optimization problem or attainment.** A feasible flow or circulation of minimum total cost
   exists, possibly for a fixed flow value or supply/demand vector.
2. **Minimum-cost circulation optimality.** A feasible circulation is optimal exactly when its
   residual network has no negative-cost cycle, or exactly when a compatible price potential
   satisfies nonnegative reduced costs.
3. **Minimum-cost flow variants.** A flow of prescribed source-to-sink value has minimum cost, or a
   maximum-value flow has minimum cost among maximum flows. These are different optimization sets.
4. **Integrality or duality.** Integral input admits an integral optimum, or a primal minimum equals
   a dual maximum. Each needs a selected linear program and exact side conditions.
5. **Algorithm correctness or complexity.** Cycle canceling, successive shortest path, network
   simplex, cost scaling, cancel-and-tighten, or another implementation returns an optimum and may
   satisfy a source-specific termination or running-time bound.

The inspected Goldberg-Tarjan report supplies strong source candidates inside items 2 and 5. It
does not authorize selecting one as the repository root.

## Decisions required at statement freeze

1. Select and independently approve one exact primary-source proposition or an explicit composite
   whose components each receive separate obligations.
2. Fix the network representation: finite directed graph or multigraph, explicit edge identities
   versus ordered vertex pairs, loops and parallel or antiparallel arcs, and unused ambient vertices.
3. Fix terminals or balances: source and sink with a prescribed flow value, node supplies/demands,
   or a circulation with zero net balance; define feasibility when total supply is nonzero.
4. Fix capacity and lower-bound conventions, including absent edges, infinite capacities, negative
   capacities, and whether feasibility is assumed or concluded.
5. Fix the capacity, flow, cost, and objective carriers (`Nat`, `Int`, `Rat`, `Real`, `NNReal`, or
   extended values), coercions, exact arithmetic, and the meaning of cost per unit flow.
6. Define conservation, flow value, total cost, residual capacity and arcs, reverse-arc costs,
   simple cycles, negative cycles, price potentials, and any claimed optimum or dual witness.
7. Decide existence and boundedness hypotheses. Negative costs do not alone make a capacitated
   finite problem unbounded, while missing capacities or unrestricted circulations can.
8. For algorithms, freeze initialization, transition choice, determinism, termination, output
   relation, refinement to the mathematical model, primitive operations, input encoding, bit or
   unit-cost model, and asymptotic parameters.
9. Freeze minimal Lean imports, domains and universes, ordered binders, boundary cases, foundation,
   computation, TCB, freshness, and mutation profiles only after the proposition is selected.

## Boundary and degenerate cases

No case is excluded at intake. Statement work must resolve empty and singleton networks; source
equal to sink; missing terminals; no edges; disconnected networks; infeasible balances; zero
required flow; zero, negative, or infinite capacities; lower bounds; zero and negative costs;
self-loops; parallel and antiparallel arcs; multiple optima; zero-cost and negative residual
cycles; absent starting flows; and objective sets that are empty or unbounded. Integral versus real
data and fixed-value versus maximum-value objectives require explicit transports, not convention.

## Explicit exclusions

- Maximum-flow/min-cut duality, Ford-Fulkerson, Edmonds-Karp, Dinic, or push-relabel without the
  selected cost objective and its proof obligations.
- Generic network-flow vocabulary, multicommodity flow, shortest paths, assignment, matching, or
  transportation results substituted without a checked equivalence in the declared direction.
- The negative-residual-cycle criterion presented as existence, integrality, algorithm termination,
  or a complexity theorem, or conversely an algorithmic bound presented as the criterion.
- Minimum-cost circulation silently presented as prescribed-value flow or minimum-cost maximum
  flow without a checked reduction covering terminals, balances, capacities, and objective value.
- A structure, hypothesis, starting state, optimizer, price, or certificate that stores the desired
  conclusion instead of deriving it.
- A finite solver run, benchmark, floating-point result, extracted program output, URL, title match,
  or the catalog's `已验证` label used as human or kernel proof evidence.

## Neighbor and formal boundaries

`THM-M-0814` owns max-flow/min-cut, `THM-M-0828` through `THM-M-0830` own named maximum-flow
algorithms, `THM-M-0877` owns generic network flow, and `THM-M-0879` owns multicommodity flow.
Their artifacts and state do not transfer to this target.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Digraph` supplies a
directed adjacency relation, `Quiver.Path.addWeight` supplies generic additive path weights,
`Finset.sum` supplies finite aggregation, and `List.argmin` supplies finite-list minimization.
These APIs do not define capacity, conservation, residual networks, feasible flows, cost
optimization, or any candidate root. No canonical expression, statement fingerprint, checked
transport, obligation registry, discovery protocol, proof state, or completion claim is frozen at
intake.
