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

| Source component | Pinpoint source content | Catalog mapping | Intake status |
|---|---|---|---|
| graph | page 399: a finite one-dimensional complex of vertices and undirected arcs | supplies a candidate meaning of "network" | inspected lead, not accepted |
| terminals | page 399: distinguished source `a` and sink `b` | implicit in "network flow" | catalog omission open |
| chain | page 399: distinct arcs and vertices, no self-intersection | source path representation | inspected lead, exact formal encoding open |
| capacity | page 399: a positive number associated with each arc | "cut capacity" | codomain and positivity transport open |
| flow | pages 399-400: collection of nonnegative weighted source-to-sink chain flows subject to per-arc capacity | "network flow" | source uses chain decomposition, not the usual edge-flow definition |
| flow value | page 400: sum of the numbers in all component chain flows | "maximum value" | exact finite collection and maximum encoding open |
| disconnecting set | page 400: arc collection meeting every source-to-sink chain | catalog "cut" | source distinguishes disconnecting sets from inclusion-minimal cuts |
| cut value | page 400: sum of capacities in the disconnecting set | "cut capacity" | exact summation and minimum encoding open |
| conclusion | page 400, Theorem 1 | maximum flow value equals minimum disconnecting-set value | direct theorem-family match; not yet an accepted canonical statement |

The proof first establishes attainment using a closed convex polytope of finitely many chain
coordinates, then constructs a disconnecting set of arcs saturated by every maximal flow. This
helps locate the mathematical boundary but is not a proof reconstruction or proof credit.

## Unresolved source gates

- The repository does not cite the article, so source identity still requires integration review.
- The paper's `number`, positivity, finite collection, and graph-complex conventions require exact
  modern definitions rather than silent repair.
- The chain-flow formulation must be retained or related by a checked theorem to any directed
  edge-flow/conservation statement.
- The source footnote says many unrestricted sources and sinks are reducible, while page 402 gives
  a counterexample for paired source-sink shipment. Neither variant belongs to the root silently.
- No corrections, errata, later-edition comparison, complete premise-to-formal mapping, or
  independent source-review receipt is recorded.

Thus the source classification is `H1`, not `H0`.

## Formal crosswalk

| Needed concept | Pinned Lean lead | What the lead establishes | Credit |
|---|---|---|---|
| undirected finite multigraph substrate | `Mathlib.Combinatorics.Graph.Basic`, `Graph` | vertices, edges, and symmetric incidence | vocabulary only |
| edge endpoints/incidence | `Graph.IsLink`, `Graph.Inc` | edge-to-vertex relations | vocabulary only |
| parallel-edge example substrate | `Graph.banana` | an undirected multigraph with common endpoints | boundary probe only |
| finite capacity/value sums | `Finset.sum` | generic finite aggregation | vocabulary only |
| attained finite maximum | `Finset.max'` | maximum of a nonempty finite set | generic order API only |
| network/flow/cut/root theorem | none located in bounded search | no exact candidate credited | `M4` |

The probe is not a theorem statement, transport, terminal proof body, or closure evidence. The
statement phase must first freeze the exact source-mapped proposition. The later anchor audit must
then repeat discovery under an immutable protocol and inspect provenance and trust.

## Duplicate and neighbor boundaries

`Docs/researches/cs_theorems.md:171` and `THM-C-0096` carry the shorter gloss "maximum flow equals
minimum cut." `THM-C-0096` is excluded from the rev-5.6 manifest. These records are provenance,
not alternate targets or transferable evidence.

Neighboring M-series targets such as `THM-M-0813` (Menger), `THM-M-0815` (Hall marriage), and
`THM-M-0812` (Konig) can be related through reductions, but none substitutes for the capacity
equality without explicit checked bridges.

## Status boundary

The intake crosswalk freezes the literal catalog wording, inspected primary theorem family,
proposition-changing choices, formal substrate, duplicates, and exclusions. It does not freeze a
canonical mathematical or Lean proposition and does not accept a source, proof body, expression
fingerprint, H0, M0, R0, audit completion, theorem completion, or master acceptance.
