# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6635-6640` supplies exactly:

| Catalog field | Verbatim value | Intake interpretation |
|---|---|---|
| title | `Alon-Tarsi定理` | named theorem family, but no theorem locator |
| attribution | `Noga Alon/Michael Tarsi` | matches an exact-topic primary paper |
| time | `1992` | matches that paper's publication year |
| statement | `列表着色的组合Nullstellensatz方法` | method/family gloss, not a proposition |
| importance | `高` | metadata only |
| formalization status | `已验证` | explicitly untrusted under rev-5.6 |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Their exact extract has SHA-256
`1fee371861085fe236b42b570019b7bf5f9fc73c49bff5c507065d472cf4073f`. The record has no
citation, formula, definition chain, assumptions, conclusion, proof boundary, errata, or formal
declaration.

The stable-ID history has one material trap. Before deduplication, this Alon-Tarsi record was
`THM-M-0934`, while the bare ID `THM-M-0907` denoted a different sparse-cut record. Commit
`c61be3c80710c07c5f7626e3404e51f40ecb39a6` renumbered the Alon-Tarsi record to the current
`THM-M-0907` and the sparse-cut record to `THM-M-0880`. Provenance must therefore bind the current
ID to the theorem name, gloss, and post-dedup source lines; a pre-dedup ID-only lookup is invalid.

`Docs/Stage0_Blueprint.md:24737-24762` repeats these fields and explicitly leaves the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Its exact projection extract has SHA-256
`2640a9d833a8e0035b347e5c479ec267e1e6e05d5ffa52330d1049c4f3650a31`.

## Inspected primary-source lead

N. Alon and M. Tarsi, *Colorings and orientations of graphs*, *Combinatorica* 12(2) (June 1992),
pages 125-134, DOI `10.1007/BF01204715`. Crossref and the publisher landing page agree on authors,
title, journal, volume, issue, date, and pagination. An author-hosted PDF at
`http://www.math.tau.ac.il/~nogaa/PDFS/chrom3.pdf` was inspected outside the repository; it is
149,795 bytes with SHA-256
`aaf67fe67852b7f0d4a14feaabed7f7b2916c384214324e8253029d7242ee565`.

Printed page 1 defines an Eulerian subdigraph by equal indegree and outdegree at every vertex,
allows it to be disconnected, classifies parity by edge count, and declares the empty subgraph
even. The proof later treats these subdigraphs as edge subsets of a fixed orientation; whether a
Lean encoding uses a spanning edge-subset object is a provisional source-convention decision, not
verbatim theorem text. Theorem 1.1 gives the per-vertex outdegree-plus-one integer-list coloring
criterion under `EE(D) != EO(D)`. Printed pages 2-4 prove it through the graph polynomial, an orientation/
coefficient count, and finite-grid polynomial interpolation. The paper describes Theorem 1.1 as a
choosability statement and applies it in Section 3.

This is an authoritative primary proof candidate and supports provisional `H1`, not `H0`. The
catalog does not cite or explicitly choose Theorem 1.1, source graph conventions are not yet fully
formalized, no complete source-to-obligation or correction/errata audit exists, and no independent
reviewer has signed the mapping. The downloaded bytes were not vendored or accepted as a dependency.
Crossref exposes no `update-to`, `updated-by`, or relation record, and a bounded erratum search found
no correction. That is only a no-match observation, not evidence that no erratum exists.

## Candidate roots in the same source

| Source node | Mathematical content | Intake boundary |
|---|---|---|
| Theorem 1.1, p.125 | orientation/Eulerian-parity criterion for per-vertex list coloring | strongest candidate, not yet canonical |
| Corollary 1.2, p.125 | `(d+1)` ordinary colorability from a maximum-outdegree orientation | weaker constant-palette corollary |
| Corollary 2.3, p.127 | graph-polynomial coefficient equals the absolute Eulerian parity-count difference | algebraic bridge, not the list-coloring conclusion |
| Proposition 2.7, p.129 | seven equivalent Nullstellensatz-type descriptions of non-`k`-colorability | distinct theorem, proof omitted in the paper |
| Theorem 3.2, p.131 | a density bound for choosability of bipartite graphs | application, not the general orientation criterion |
| Dinitz discussion, p.132 | a conditional Latin-square enumeration reduction and checked `m=4,6` cases | belongs to neighboring target scope and is not a full Dinitz proof |

The 1992 paper predates Alon's paper titled *Combinatorial Nullstellensatz* (1999). Therefore the
catalog's capitalized method label may be retrospective. A future source decision must not silently
replace the 1992 interpolation proof with the later general theorem without a checked bridge.

## Phrase-to-proposition crosswalk

| Repository phrase | Source component | Prospective Lean component | Intake result |
|---|---|---|---|
| list coloring | one allowed integer set per vertex and a legal coloring choosing from it | a finite-set family and proper coloring of an exact underlying graph | candidate identified; representation and transport open |
| Alon-Tarsi theorem | Theorem 1.1 is the strongest exact-topic candidate | a quantified implication from Eulerian parity counts to a coloring witness | root selection pending review |
| combinatorial Nullstellensatz method | graph polynomial plus interpolation in the 1992 proof; later 1999 theorem is adjacent | `MvPolynomial` graph encoding plus a checked polynomial nonvanishing result | route identity and bridge open |
| 1992 | publication date of the inspected paper | immutable source-revision metadata | identity match only |
| verified | catalog status | no proposition or proof term | rejected as H/M evidence |

## Formal crosswalk

Pinned mathlib supplies `Digraph`, `Digraph.toSimpleGraphInclusive`, ordinary
`SimpleGraph.Coloring`, and three generic Combinatorial Nullstellensatz declarations. It does not
supply, in the bounded intake search, a named Alon-Tarsi theorem, list-coloring/choosability API,
Eulerian spanning-subdigraph parity counter, graph polynomial, or source-to-Lean bridge. The
generic Nullstellensatz formalization follows Alon 1999 and is not itself the target.

No canonical Lean statement, formal module, expression hash, environment fingerprint, or proof
body is credited. The provisional root is `[H1, M4, R4]`; no H0, M0, R0, accepted state, audit
completion, or theorem completion is claimed.

## Source gate

Before statement acceptance, accountable reviewers must preserve a lawful immutable edition,
select the exact source root, transcribe every incorporated definition, binder, hypothesis,
conclusion, proof dependency, and boundary case, inspect corrections and errata, decide the 1992-
versus-1999 algebraic route, map every source node and graph representation, and independently
approve the crosswalk. Until then the canonical mathematical and Lean statements remain null.
