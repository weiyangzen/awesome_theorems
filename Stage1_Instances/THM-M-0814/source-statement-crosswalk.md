# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5984-5989` supplies exactly the title
`最大流最小割定理`, attribution L. R. Ford / D. R. Fulkerson, year 1956, gloss
`网络流的最大值等于最小割容量`, importance "high," and status `已验证`. Git history attributes
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

The record does not define a network, flow, cut, or capacity; state finiteness, terminal, capacity,
or conservation assumptions; cite a theorem/page; identify an edition or correction policy; or
link a formal artifact. Stage0 repeats these omissions. The verified label is therefore untrusted
metadata and gives no H or M credit.

## Inspected primary source lead

L. R. Ford, Jr. and D. R. Fulkerson, *Maximal Flow Through a Network*, *Canadian Journal of
Mathematics* 8 (1956), 399-404, DOI `10.4153/CJM-1956-045-5`, was inspected in the publisher PDF
observed on 2026-07-13. The six-page PDF has SHA-256
`344c1288f84ccddba6e292751813d613657c69fbe71b9bedb7b19df72a3bdf08`.

The pinpoint statement is Section 1, Theorem 1, printed page 400. The definitions begin on printed
pages 399-400 and the proof ends on page 402. The source says:

> The maximal flow value obtainable in a network N is the minimum of v(D) taken over all
> disconnecting sets D.

The source explicitly defines the following premises and terms before Theorem 1:

| Source component | Pinpoint source content | Frozen Lean mapping | Status |
|---|---|---|---|
| graph | page 399: finite one-dimensional complex with undirected arcs | `Graph V E` with finite ambient types | encoded; graph-complex and loop-convention review open |
| terminals | distinguished source `a` and sink `b` | `HasTerminals G source sink` | encoded |
| chain | distinct arcs and vertices, no self-intersection | injective arrays and `Graph.IsLink` in `Chain` | encoded |
| capacity | positive number on each arc | `HasPositiveCapacities` over `NNReal` | encoded; codomain review open |
| flow | finite nonnegative weighted chains under per-arc capacity | `Finsupp Chain NNReal` plus `IsFeasible` | encoded |
| flow value | sum of component numbers | `flowValue` | encoded |
| disconnecting set | arc collection meeting every source-to-sink chain | `IsDisconnecting` | encoded |
| cut value | sum of member capacities | `cutValue` | encoded |
| conclusion | page 400, Theorem 1 | `MaxFlowMinCutTarget` with attained extrema and equality | elaborated; proof/source acceptance open |

The proof first establishes attainment using a closed convex polytope of finitely many chain
coordinates, then constructs a disconnecting set of arcs saturated by every maximal flow. This
helps locate the mathematical boundary but is not a proof reconstruction or proof credit.

## Unresolved source gates

- The repository does not cite the article, so source identity still requires integration review.
- The paper's `number`, positivity, finite collection, and graph-complex conventions require exact
  modern definitions rather than silent repair.
- The chain-flow formulation is retained. No directed edge-flow/conservation transport is credited.
- The source footnote says many unrestricted sources and sinks are reducible, while page 402 gives
  a counterexample for paired source-sink shipment. Neither variant belongs to the root silently.
- No corrections, errata, later-edition comparison, complete premise-to-formal mapping, or
  independent source-review receipt is recorded.

Thus the source classification remains `H1`, not `H0`, despite exact machine elaboration.

## Formal crosswalk

| Needed concept | Pinned Lean realization | What it establishes | Credit |
|---|---|---|---|
| undirected finite multigraph substrate | `Graph` and `Graph.IsLink` | source graph and chain incidence | statement definition |
| nonnegative values | `NNReal` | nonnegative-real subtype and strict capacity premise | statement definition |
| finite collection and sums | `Finsupp.sum` and `Finset.sum` | finite support, loads, and values | statement definition |
| network/flow/cut/root theorem | local `Statement.lean` declarations | exact proposition elaborates; no proof body | `M3` interface only |

The earlier probe remains discovery-only. `Statement.lean` supersedes its null-target boundary for
this phase, but is not a terminal proof body or closure evidence. The later anchor audit must repeat
discovery under an immutable protocol and inspect provenance and trust.

## Duplicate and neighbor boundaries

`Docs/researches/cs_theorems.md:171` and `THM-C-0096` carry the shorter gloss "maximum flow equals
minimum cut." `THM-C-0096` is excluded from the rev-5.6 manifest. These records are provenance,
not alternate targets or transferable evidence.

Neighboring M-series targets such as `THM-M-0813` (Menger), `THM-M-0815` (Hall marriage), and
`THM-M-0812` (Konig) can be related through reductions, but none substitutes for the capacity
equality without explicit checked bridges.

## Status boundary

The statement crosswalk maps the selected 1956 proposition and definitions to a fingerprinted Lean
target. It does not accept the source at H0, inspect or credit a proof body, establish M0/R0,
complete the audit or theorem, release evidence, or provide master acceptance.
