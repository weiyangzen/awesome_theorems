# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6096-6101` supplies exactly `Push-Relabel算法`, attribution
Andrew Goldberg/Robert Tarjan, year 1988, gloss `最大流的推送重标算法` (the push-relabel algorithm
for maximum flow), high importance, and status `已验证`. All six uncited lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no domain, algorithm semantics,
truth-valued conclusion, theorem/page, proof boundary, complexity model, or formal declaration.

`Docs/Stage0_Blueprint.md:22658-22694` repeats the gloss and explicitly leaves exact definitions and
premises, proof route, dependencies, alternate statements, axioms, machine state, and artifact
links open. Its generic closed-result and leaf-budget prose is planning metadata. The rev-5.6
manifest retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

A separate computer-science survey row, `Docs/researches/cs_theorems.md:174`, says Goldberg and
Tarjan's 1988 Push-Relabel algorithm is an `O(V^3)` maximum-flow algorithm and labels it merely
`可验证`. Stage0 assigns that record the distinct identifier `THM-C-0099`. It is a neighboring
candidate-scope signal, not the source statement or authority for `THM-M-0830`.

## Inspected primary source

Andrew V. Goldberg and Robert E. Tarjan, *A New Approach to the Maximum-Flow Problem*, *Journal of
the ACM* 35(4) (October 1988), 921-940, DOI `10.1145/48014.61051`. The inspected Princeton-hosted
copy has SHA-256 `e0c93940c1f450c801443af639fff047ac49c9bc43f9f55c9f2ac5d5889fb808`.

- Pages 923-924 define a finite directed flow network, positive real capacities extended by zero,
  antisymmetric real-valued flows, conservation, flow value, maximum flow, preflow, excess,
  residual capacity, and residual graph.
- Pages 924-926 define valid distance labels, active vertices, initialization, push and relabel;
  Lemma 2.1 establishes progress for an active vertex.
- Pages 926-928 prove correctness and termination. Theorem 3.4 gives conditional maximum-flow
  correctness; Lemmas 3.5-3.10 establish finite label and operation bounds; Theorem 3.11 gives
  termination after `O(n^2 m)` basic operations.
- Pages 929-931 define the sequential edge-list implementation and FIFO discharge strategy.
  Theorem 4.2 bounds all work except nonsaturating pushes, Lemma 4.3 bounds queue passes,
  Corollary 4.4 bounds nonsaturating pushes, and Theorem 4.5 concludes `O(n^3)` time.

This is a strong primary proof source for the recognizable catalog family and supports provisional
H1. H0 remains unavailable because the catalog does not identify which theorem or composite is the
root, and no approved exact premise/definition/errata crosswalk or independent source review exists.

## Component crosswalk

| Catalog/source component | Primary-paper meaning | Required Lean component | Intake assessment |
|---|---|---|---|
| maximum flow | a flow with maximum net inflow to the sink | finite network, feasible-flow predicate, value, maximality | exact representation open |
| push/relabel | local preflow transitions on residual edges and valid labels | transition relation or executable state machine plus invariants | definitions absent from pinned library |
| algorithm correctness | termination yields a maximum flow, completed using termination and finite labels | refinement from run/output to the generic invariants and maximum-flow predicate | plausible root, not selected |
| generic complexity | `O(n^2 m)` basic operations | counted transition semantics and asymptotic theorem | plausible root, not selected |
| FIFO complexity | queue discharge implementation runs in `O(n^3)` time | FIFO semantics, cost model, implementation refinement, asymptotic bound | matches separate CS gloss only |
| `已验证` | untrusted inventory status | accepted source and kernel receipts | no credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded case-insensitive
searches of repository Lean sources and mathlib found no declaration or implementation named for
push-relabel, preflow, maximum flow, max-flow, flow network, or residual network. Mathlib does
provide generic substrate such as `Digraph`, `Digraph.Adj`, `Quiver.Path`, path length/weights, and
finite sums. `IntakeProbe.lean` elaborates representative interfaces against the pinned environment.
Those ingredients neither encode the primary algorithm nor close any candidate root, so the machine
status remains M4. A complete anchor/provenance audit belongs to the downstream anchor-audit phase.

Before leaving H1, accountable reviewers must select the root, verify the incorporated primary
passages and corrections, and map every definition, assumption, conclusion, and complexity clause.
Before machine credit, the statement phase must freeze and mutation-test the exact elaborated target
and every checked transport.
