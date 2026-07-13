# THM-M-0855 scope map

## Preserved claim

The source-selected mathematical family is Chvatal and Erdos 1972, Theorem 1: let `G` be a graph
with at least three vertices. If, for some `s`, `G` is `s`-connected and contains no independent
set of more than `s` vertices, then `G` has a Hamiltonian circuit.

At intake this is the canonical human claim, not an elaborated Lean expression. The statement phase
must resolve the source's incorporated definitions before it chooses ordered binders or an exact
formal encoding.

## Proposition-changing decisions

| Dimension | Preserved meaning | Open statement decision |
|---|---|---|
| graph | finite undirected graph in the 1972 source family | simple-graph encoding, vertex type, finiteness instances, decidable equality, and loop/multiedge convention |
| size | at least three vertices | exact cardinal inequality and its relationship to Hamiltonicity boundary conventions |
| parameter | "for some `s`" | whether `s` ranges over positive integers or naturals and whether further bounds are incorporated in `s`-connectivity |
| connectivity | vertex `s`-connectivity | exact deletion/Menger definition, strict deletion bound, nonempty-remnant rule, and complete-graph convention |
| independence | no independent set has more than `s` vertices | `indepNum G <= s`, `IndepSetFree (s+1)`, or a quantified set/finset form, with checked transports |
| conclusion | existence of a Hamiltonian circuit | checked relationship to mathlib's `SimpleGraph.IsHamiltonian`, including its singleton convention |

The source proof uses `s` internally as a finite count of pairwise internally disjoint paths from a
vertex outside a longest circuit to the circuit, citing Dirac 1960, Theorem 1. That use strongly
indicates vertex rather than edge connectivity, but it does not replace an audit of the cited
definition chain.

## Boundary cases

- Vertex cardinalities zero, one, and two are excluded by the printed at-least-three premise.
- `s = 0`, `s = 1`, `s >= |V|`, and deletion of all remaining vertices must be reconciled with the
  source convention rather than assigned convenient Lean meanings.
- Complete graphs, cycles, and the source's sharp complete-bipartite examples must remain within the
  source-selected conventions.
- Independent sets of exactly `s` vertices are allowed; a formulation forbidding them would
  strengthen the premise.
- A graph with an independent set of `s + 1` vertices fails the premise. The source's `K(s,s+1)`
  and Petersen examples show that relaxing the bound changes the theorem.
- Mathlib regards singleton graphs as Hamiltonian, but that convention cannot erase the explicit
  source premise of at least three vertices.

No boundary case is silently excluded beyond the printed cardinality premise. The dependent
statement gate must test removal of that premise, changes to the graph/parameter domain and binder
scope, and representative boundary cases before formal proof evidence is inspected.

## Explicit exclusions

- The source's Theorem 2, which concludes a Hamiltonian path when no independent set has `s+2`
  vertices.
- The source's Theorem 3, which concludes Hamiltonian-connectedness when there is no independent
  set of `s` vertices.
- Dirac's minimum-degree theorem, Ore's degree-sum theorem, or the Nash-Williams/Bondy large-degree
  result cited as a special regime.
- Edge connectivity (`SimpleGraph.IsEdgeConnected`) in place of vertex connectivity.
- Ordinary connectedness, Menger-style path substrate, vertex-deletion syntax, independent-set
  predicates, or Hamiltonicity definitions alone.
- An assumed connectivity witness or Hamiltonian cycle, an axiom, a bodyless declaration, a
  placeholder, a computed example, or the untrusted `已验证` label.

## Formal boundary

Pinned mathlib exposes `SimpleGraph.IsHamiltonian`, `IsIndepSet`, `IsNIndepSet`, `IndepSetFree`,
`indepNum`, `Subgraph.deleteVerts`, and `Connected`. A prospective vertex-connectivity predicate
could quantify over deleted vertex sets and connected induced remnants, but choosing it now would
settle source-sensitive small-cardinality and subtype-nonemptiness conventions without a checked
crosswalk. The intake probe therefore establishes representation feasibility only. Exact target,
transports, mutations, exhaustive anchor audit, proof bodies, obligation registry, typed graphs,
composition, trust, readability, and release evidence remain downstream.
