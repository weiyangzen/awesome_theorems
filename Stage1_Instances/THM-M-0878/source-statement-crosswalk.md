# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6432-6437` supplies exactly the title `最小费用流`, collective
attribution, twentieth-century date, gloss `带费用的网络流`, high importance, and status `已验证`.
Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no theorem, bibliography,
network or flow definition, ordered binders, hypotheses, conclusion, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23954-23979` repeats the topic and explicitly leaves exact definitions and
premises, proof route, dependencies, equivalent forms, axioms, machine state, and artifact links
open. Its generic closed-result and leaf-budget prose is planning metadata. The rev-5.6 manifest
retains `已验证` only as untrusted metadata and resets this target to `L0 / rework_required`.

## Inspected primary-source lead

Andrew V. Goldberg and Robert E. Tarjan, *Finding Minimum-Cost Circulations by Canceling Negative
Cycles*, MIT Laboratory for Computer Science Technical Memo `MIT/LCS/TM-334` (July 1987), was
inspected from the MIT DSpace copy at `https://hdl.handle.net/1721.1/149134`. The 18-page,
4237080-byte PDF has SHA-256
`8450b621bc6ea4d9fa7954e44451b4e91c1cc547a1ac45a1611a85d72c3c86f7`; locally extracted layout
text has SHA-256 `e5443518cfc87ece59ec065aae4f7d01c3cf5dc9c144f078bc1012bdc0290226`.
The later journal version is *Journal of the ACM* 36(4) (1989), 873-886, DOI
`10.1145/76359.76368`; this intake inspected the 1987 report, not the journal body.

The report's introduction calls the minimum-cost circulation problem equivalent to minimum-cost
flow and transshipment. That sentence is a lead for a future checked reduction, not permission to
identify all encodings definitionally.

- PDF pages 5-6, Section 2, define a finite symmetric directed graph with real capacities,
  antisymmetric real costs, antisymmetric real circulation, capacity and conservation constraints,
  half-sum total cost, residual capacities, and simple negative residual cycles.
- Theorem 2.1 states that a circulation is minimum-cost if and only if it has no negative residual
  cycle. The theorem is attributed there to Busacker and Saaty.
- PDF pages 7-8, Theorems 3.1-3.3, give price-potential, epsilon-optimality, and minimum-cycle-mean
  characterizations.
- Theorems 3.7, 3.9, and 3.10 give distinct iteration and running-time bounds for minimum-mean
  cycle canceling under integer or arbitrary real costs.
- PDF page 15, Theorem 4.3, gives separate dynamic-tree cancel-and-tighten complexity bounds.

This is a strong primary proof-family lead and supports provisional H1. H0 and a canonical target
remain unavailable because the catalog does not cite or select the report, a theorem within it, or
another minimum-cost-flow formulation. Complete incorporated-definition, assumption, proof-node,
journal-delta, correction, and errata mapping plus independent review remain open.

## Component crosswalk

| Catalog/source phrase | Candidate mathematical component | Required Lean surface | Intake assessment |
|---|---|---|---|
| network flow | finite directed graph/multigraph plus terminals or node balances | explicit vertex/edge types, finiteness, incidence, balance model | catalog omits model |
| cost | per-arc cost and total cost objective | carrier, multiplication, finite sum, order, boundedness | generic sum only probed |
| minimum | optimum, infimum, or algorithm output | feasible set, objective comparison, attainment | conclusion not selected |
| circulation | zero-balance antisymmetric flow in the report | capacity, antisymmetry, conservation | primary candidate only |
| min-cost flow | fixed-value, supply/demand, or min-cost maximum-flow formulation | selected terminals/balances/value and checked reduction | ambiguous family |
| negative-cycle criterion | Theorem 2.1 iff characterization | residual network/cycle/cost and both directions | strong candidate, not root |
| price criterion | Theorem 3.1 complementary-slackness form | price potential and reduced costs | distinct candidate, not root |
| algorithm | cycle-canceling or cancel-and-tighten transitions | executable/relation semantics, invariants, output refinement | no algorithm selected |
| complexity | Theorems 3.7/3.9/3.10/4.3 | counted execution, input encoding, arithmetic and asymptotic model | distinct candidates |
| `已验证` | untrusted inventory status | accepted source and kernel receipts | no credit |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded
case-insensitive searches of repository Lean and pinned mathlib found no declaration named for
minimum-cost flow, minimum-cost circulation, negative residual cycles, cycle canceling, or
transshipment. Mathlib provides adjacent substrate: `Digraph`, `Digraph.Adj`, `Quiver.Path`,
`Quiver.Path.addWeight`, `Finset.sum`, and `List.argmin`.

`IntakeProbe.lean` checks those declarations in the pinned environment. They neither encode the
primary model nor close any candidate theorem, so M4 remains the truthful intake classification.
The bounded search is not a global absence claim or the immutable downstream anchor audit.

Before statement credit, reviewers must choose one exact proposition, admit and map its primary
source, freeze all ordered binders and boundary cases, elaborate and fingerprint the canonical Lean
expression under minimal imports, compile every credited transport, and run the required statement
mutations. Before H0, an independent source reviewer must approve every incorporated definition,
assumption, conclusion, proof boundary, correction, and erratum.

## Status boundary

This crosswalk freezes the literal catalog record, the inspected source family, candidate roots,
proposition-changing choices, formal substrate, and exclusions. It does not freeze or prove a
canonical mathematical or Lean proposition and does not accept H0, M0, R0, audit completion,
theorem completion, or master acceptance.
