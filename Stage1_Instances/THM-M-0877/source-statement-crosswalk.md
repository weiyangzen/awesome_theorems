# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6425-6430` supplies exactly the title `网络流`, collective
attribution, twentieth-century date, gloss `最大流与最小割理论`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, network model,
capacity domain, flow or cut definition, binder, hypothesis, conclusion, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23927-23952` repeats the family gloss and explicitly leaves the formal
system, foundations, precise definitions and premises, proof route, dependencies, equivalent
statements, axioms, machine status, and artifact links open. The rev-5.6 manifest preserves the
verified label only as untrusted metadata and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| network flow | finite network, terminals, capacities, feasible flows | selected graph type, capacity map, conservation or chain-flow predicates | all definitions absent |
| maximum flow | value function, feasible set, order, attainment or supremum | exact optimization expression and finiteness/order assumptions | not fixed |
| minimum cut | source-sink cut, capacity sum, minimum or infimum | exact cut predicate, crossing orientation, aggregation and optimum | not fixed |
| "theory" | one theorem or an explicitly typed family ledger | one `Prop` or reviewed set of independent roots | not truth-valued |
| `已验证` | source-specific human or formal evidence | receipt-bound declaration and proof body | untrusted metadata only |

The wording does not by itself entail equality, existence of optimizers, integrality, an augmenting-
path characterization, or correctness of any algorithm.

## Primary-source discriminator

L. R. Ford, Jr. and D. R. Fulkerson, *Maximal Flow Through a Network*, *Canadian Journal of
Mathematics* 8 (1956), 399-404, DOI `10.4153/CJM-1956-045-5`, was inspected from the publisher PDF
(569,595 bytes, six pages; SHA-256
`344c1288f84ccddba6e292751813d613657c69fbe71b9bedb7b19df72a3bdf08`; extracted-text SHA-256
`c70d333cecdfff7c0fdc30a7aae11b32e63bb4e6baab3384c5feab4d6d305ab5`). Definitions on printed
pages 399-400 and Theorem 1 on page 400 state a precise minimum-cut theorem for a finite undirected
network with distinct source and sink, positive numerical arc capacities, and a flow represented
by nonnegative weighted simple source-to-sink chains. A disconnecting set meets every such chain,
and the theorem equates the maximal flow value with the minimum capacity of a disconnecting set.

This is a primary source for the exact result already represented by `THM-M-0814`, not evidence that
the broad `THM-M-0877` family label selects the same root. The familiar directed edge-flow and
conservation formulation also needs a checked source-approved transport from the paper's encoding.
The paper is therefore a digest-bound discovery discriminator only: it supplies no H1/H0 transfer,
canonical statement, proof node, or machine credit here.

## Neighbor and duplicate records

`Docs/researches/math_theorems.md:5984-5989` separately records `THM-M-0814`, "max-flow min-cut
theorem," with the explicit equality gloss and Ford/Fulkerson attribution. Its rev-5.6 dossier is
read-only neighboring provenance. `Docs/researches/cs_theorems.md:171` contains a shorter excluded
computer-science duplicate. The catalog then separately records minimum-cost flow and multicommodity
flow as `THM-M-0878` and `THM-M-0879`. This structure makes silent substitution particularly unsafe.

## Source gate

There is no repository-selected truth-valued proposition for `THM-M-0877`. Before leaving `H5`, an
accountable reviewer must either redirect the target to one exact immutable-source theorem, approve
an explicitly typed theorem-family ledger, or reconcile it as a duplicate without importing another
target's status. Every definition, binder, hypothesis, conclusion, proof boundary, correction and
errata decision, and neighbor relationship then needs independent review.

`H5` here does not classify established network-flow mathematics as false or independent. It says
the received topic and "theory" gloss are not yet one proposition against which source fidelity can
be audited.

## Lean discovery boundary

Pinned mathlib supplies `Graph`, `Graph.IsLink`, and `Graph.Inc` as undirected multigraph incidence
substrate, `Digraph` for a directed relation, `Finset.sum` for finite aggregation, and `Finset.max'`
for a nonempty finite maximum. The probe elaborates these APIs only. They do not supply capacities,
feasible flows, conservation, cuts, extrema, a network-flow theorem, or a proof body.

The canonical module, target expression, expression and environment fingerprints, alternate
encodings, and statement mutations therefore remain null. No formal absence theorem, exact
statement elaboration, audit completion, or theorem completion is claimed.
