# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6159-6164` supplies exactly the title `完美图定理`, attribution to
Laszlo Lovasz, year 1972, claim `图的完美性与其补图的完美性等价`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record supplies no bibliography, definition of
perfectness, graph domain, binders, hypotheses, proof boundary, correction history, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:22901-22926` repeats the claim while explicitly leaving definitions and
premises, proof process, dependencies, alternate forms, axioms, machine state, and artifact links
open. Its generic planning claim about known closure is not evidence. The rev-5.6 manifest retains
`已验证` only as untrusted metadata and resets this target to `L0 / rework_required`.

## Primary-source identity leads

Crossref identifies two 1972 Lovasz papers directly tied to the result:

> L. Lovasz, *Normal hypergraphs and the perfect graph conjecture*, *Discrete Mathematics* 2(3)
> (June 1972), 253-267, DOI `10.1016/0012-365X(72)90006-4`, PII `0012365X72900064`.

> L. Lovasz, *A characterization of perfect graphs*, *Journal of Combinatorial Theory, Series B*
> 13(2) (October 1972), 95-98, DOI `10.1016/0095-8956(72)90045-7`, PII
> `0095895672900457`.

OpenAIRE exposes the first paper's published abstract, which defines normal hypergraphs in outline,
announces a normal-hypergraph min-max characterization, and says: "This theorem implies the following
conjecture of Berge: The complement of a perfect graph is perfect." This matches the catalog's
attribution, year, and complement implication. Applying the implication to the complement, together
with complement involution, is the familiar equivalence, but that transport is not yet source- or
Lean-checked here.

The second paper's published abstract says that a graph is perfect iff a maximum-clique times
stability-number inequality holds for each induced subgraph, and that Berge's complement conjecture
follows immediately. This is a second, more graph-specific source lead, but its compact abstract is
not a replacement for the paper's definitions, formula, numbered result, or proof.

Neither primary full text was admitted during this bounded intake. Publisher PDF requests were
blocked, the unauthenticated Elsevier API exposed metadata but not the full text, and the inspected
Unpaywall responses reported no open-access location for either DOI. OpenAIRE access flags did not
yield an admitted full text. Consequently no exact numbered theorem, page-level proof passage,
incorporated perfect-graph definition, premise map, or errata record was inspected. The papers form
a strong `H1` source family, not an `H0` packet.

Lovasz's author-hosted publication list, observed SHA-256
`399677d8d67733e01ac69f69d8ced789f157ad8a2a623d228645777c3c8ef082`, independently lists the
first paper as publication 19 with a 1984 reprint at pages 29-42 and the second as publication 24.
The 1984 reprint is indexed under the clarifying title *Normal Hypergraphs and the Weak Perfect
Graph Conjecture*, DOI `10.1016/S0304-0208(08)72920-7`. A bibliography confirms identity and
republication; it does not expose the proof or close the source gate.

## Secondary formalization corroboration

Singh and Natarajan, *A Constructive Formalization of the Weak Perfect Graph Theorem*, arXiv
`1912.02211v1` / CPP 2020, was inspected (observed PDF SHA-256
`a65c6f372dfe85309585752c76c8b267d7cacaf29dfaa97eff15f39176a68fbb`). Its abstract and
Definition 1 use finite simple graphs and define a graph to be perfect when its chromatic number
equals its clique number for every induced subgraph; Conjecture 2 and Section 1.3 state that a graph
is perfect iff its complement is perfect. It reports a constructive Coq proof through the Lovasz
replication lemma. This is a precise secondary discriminator and external formalization lead, not
the primary human proof, a Lean 4 artifact, or `M1` evidence under the unperformed immutable build
and exact-statement audit.

## Clause crosswalk

| Catalog/source component | Standard mathematical reading to verify | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "graph" | finite simple undirected loopless graph | `G : SimpleGraph V` plus finite carrier data | source domain and typeclass encoding open |
| "perfectness" | every induced subgraph has chromatic number equal to clique number | future predicate over subsets and `G.induce` | catalog gives no definition; source text not inspected |
| "complement" | nonedges between distinct vertices on the same carrier | `Gᶜ`, characterized by `SimpleGraph.compl_adj` | pinned interface located; exact source transport open |
| "equivalent" | `Perfect G <-> Perfect Gᶜ` | future checked `Iff`, or one implication plus involution | catalog states equivalence; paper abstract states one implication |
| chromatic number | minimum number of colors, finite for finite graphs | `G.chromaticNumber : ENat` | finite-value and coercion conventions open |
| clique number | maximum clique cardinality | `G.cliqueNum : Nat` | definition substrate only |
| all induced subgraphs | heredity clause essential to standard perfectness | `forall s : Set V, ... (G.induce s)` | subset/subtype and empty-case conventions open |
| `已验证` | untrusted catalog status | accepted source and kernel receipts would be required | no H or M credit |

## Neighbor and theorem-name boundary

The source record immediately follows this target with `THM-M-0840`, `强完美图定理`, attributed to
Chudnovsky, Robertson, Seymour, and Thomas in 2006 and glossed as a forbidden-subgraph
characterization. That neighboring target is the strong perfect graph theorem. It cannot be used as
the present root, though it may eventually imply it through separately checked mathematics.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
authenticates complement, induce, chromatic-number, clique-number, clique lower-bound, and
complement-clique APIs. A bounded search over pinned mathlib and repository Lean sources found no
perfect-graph predicate or Lovasz weak perfect graph declaration; matches for perfect matchings,
perfect groups, and perfect powers are unrelated.

These are definition ingredients, not an exact formal target, so the machine status is `M4`, not
`M3`. Canonical module and expression, expression and environment fingerprints, checked alternate
encodings, mutation tests, proof-body provenance, and the exhaustive formal-candidate audit remain
open. No formal absence theorem, exact statement, proof, audit completion, or theorem completion is
claimed.
