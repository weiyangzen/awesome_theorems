# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6306-6311` supplies exactly the title `Shannon定理`, attribution
to Claude Shannon, the year 1949, the gloss `边色数的上界` (upper bound for the chromatic index),
importance `高`, and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, graph model,
definitions, formula, binders, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23468-23493` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Primary-source lead

Crossref metadata identifies Claude E. Shannon, *A Theorem on Coloring the Lines of a Network*,
*Journal of Mathematics and Physics* 28, issue 1-4 (April 1949), pages 148-152, DOI
`10.1002/sapm1949281148`. The author, year, topic-bearing title, and page range strongly match the
catalog family. Unpaywall reports the article closed and no repository copy; the publisher PDF was
not accessible in this run.

The primary text was therefore not inspected at theorem-page granularity. Its network and line
definitions, exact inequality, loop and multiplicity conventions, theorem numbering, incorporated
assumptions, sharpness status, proof boundary, and errata remain unknown to this intake. The
bibliographic record supports provisional `H1`, not H0 or an E4 primary-source packet.

An inspected modern secondary source, Aboulker, Aubian, and Huang, *Vizing's and Shannon's
Theorems for Defective Edge Colouring*, *Electronic Journal of Combinatorics* 29(4) (2022),
article P4.1, DOI `10.37236/11049`, states in its introduction that graphs there are finite,
undirected, loopless multigraphs and identifies the `d = 1` case as Shannon's bound
`chi'(G) <= floor (3 * Delta(G) / 2)`. This corroborates the candidate family only. It does not
replace Shannon's primary source or authorize importing the secondary paper's conventions into the
canonical root without review.

## Clause crosswalk

| Repository phrase | Source-resolution candidate | Prospective Lean surface | Intake status |
|---|---|---|---|
| `Shannon定理` / 1949 | Shannon's line-colouring article | one source-approved canonical `Prop` | primary article identified; exact text uninspected |
| graph/network | finite undirected loopless multigraph | `Graph V E` plus explicit finiteness and loopless predicates | carrier and finiteness encoding open |
| edge/line colouring | a colour for every edge, distinct on incident distinct edges | future proper-coloring predicate on `E(G)` | no pinned multigraph coloring API located |
| edge chromatic number | least number of colours in a proper edge-colouring | future `chromaticIndex` or existential palette formulation | definition and transport open |
| upper bound | `chi'(G) <= floor (3 * Delta(G) / 2)` | natural-number inequality or equivalent existence result | familiar modern candidate; not canonical |
| maximum degree | maximum incidence cardinality with multiplicity | future multigraph degree/max-degree definitions | pinned `Graph` API lacks located degree layer |
| sharpness | three-vertex parallel-edge examples attain the bound | optional extremal clause or separate obligation | inclusion in root unresolved |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H0 or M credit |

## Neighbor boundaries

The catalog places `THM-M-0859` Vizing immediately before this target and `THM-M-0861` Konig edge
colouring immediately after it. Vizing's standard simple-graph bound and Konig's bipartite equality
are mathematically adjacent but neither selects, substitutes for, or proves the universal
multigraph Shannon bound. `THM-M-0858` Brooks concerns vertex coloring. Their future artifacts may
be shared only as explicitly frozen bridge dependencies, never as inherited scope or status.

## Lean discovery boundary

Pinned mathlib's `Mathlib.Combinatorics.Graph.Basic` defines `Graph`, `IsLink`, `Inc`, `IsLoopAt`,
`IsNonloopAt`, and `Adj`; `Mathlib.Combinatorics.Graph.Subgraph` defines explicit-edge subgraphs.
`Mathlib.Combinatorics.SimpleGraph.EdgeLabeling` provides arbitrary labels on simple-graph edges,
while `Mathlib.Combinatorics.SimpleGraph.Finite` provides simple-graph `degree` and `maxDegree`.
These interfaces are only substrate. In particular, the simple-graph edge type cannot faithfully
represent distinct parallel edges without a checked encoding.

A bounded case-insensitive search of pinned mathlib and repository-local Lean found no Shannon
edge-colouring, chromatic-index, or proper multigraph edge-colouring declaration. This is intake
discovery evidence only, not the later immutable anchor audit and not a global absence claim.

## Source gate

Before leaving `H1`, accountable reviewers must lawfully preserve and hash an immutable primary
edition; transcribe and map every incorporated graph, incidence, loop, degree, coloring, palette,
chromatic-index, rounding, binder, hypothesis, conclusion, extremal, proof-boundary, and correction
clause; reconcile the modern secondary formulation; and independently approve fidelity to
`THM-M-0860`. The statement phase may only then freeze and mutation-test the identical Lean
proposition and checked transports.
