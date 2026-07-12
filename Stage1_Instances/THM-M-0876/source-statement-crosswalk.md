# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6418-6423` supplies exactly the title `图同构的复杂性`, collective
attribution, twentieth-century date, gloss `图同构在NP与P之间的位置`, importance "high," and status
`部分解决`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, graph encoding,
machine model, complexity-class definition, binder, hypothesis, conclusion, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23900-23925` classifies the record as an open/conjectural/not-fully-closed
item and repeats the gloss. It explicitly leaves definitions and premises, proof route,
dependencies, equivalent statements, axioms, machine status, and artifact links open. Its demand to
separate closed and ongoing branches does not identify or prove a branch. The rev-5.6 manifest
preserves `部分解决` only as untrusted source metadata and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| graph isomorphism | encoded finite-graph decision language | graph encoding plus `Nonempty (G ≃g H)` correspondence | graph model and encoding absent |
| NP | nondeterministic polynomial-time definition and membership witness | machine/language/cost API and verified polynomial bound | no source definition or pinned class API selected |
| P | deterministic polynomial-time definition and membership statement | deterministic machine and verified cost bound | catalog does not state membership or nonmembership |
| "between" / "position" | one exact relation or a typed branch ledger | one `Prop` or reviewed family of propositions | not truth-valued and potentially misleading |
| `部分解决` | source-specific closed and ongoing branches | independently evidenced node statuses | untrusted metadata; no branch credit |

The wording does not imply `GI ∈ NP \ P`. It also does not select the weaker known membership claim,
the open P-membership question, a conditional NP-intermediacy result, or a complexity upper bound.

## Author-authored partial-branch source lead

László Babai, *Graph Isomorphism in Quasipolynomial Time*, arXiv `1512.03547v2`, 19 January 2016,
was inspected from a downloaded 89-page PDF (843,393 bytes; SHA-256
`b6393ff36f4ff1c9646d7b9c5ea9ef78cfb222d52634ffdef2f05fa77daa9c62`). Its abstract states that
GI, String Isomorphism, and Coset Intersection can be solved in quasipolynomial time. Page 4 defines
quasipolynomial boundedness, Theorem 1.1.1 gives the String Isomorphism result, and Corollary 1.1.2
gives the Graph Isomorphism and Coset Intersection upper bounds.

This digest-bound PDF is immutable discovery input, but not catalog provenance, an independently
reviewed admitted source bundle, or H0 evidence. Version 2 predates the publicly reported proof flaw
and repair; that correction history and the final corrected proof source were not audited. More
importantly, the quasipolynomial branch is separately represented in the catalog by `THM-M-0873` and
`THM-M-0874`. It neither resolves what "position between NP and P" denotes nor licenses replacing
this root. No source claim or proof body is credited from the paper in this intake.

## Neighbor and duplicate records

The source catalog itself distinguishes the assigned record from `图的同构问题` at lines 6397-6402,
`Babai算法` at lines 6404-6409, and `Weisfeiler-Lehman算法` at lines 6411-6416. Stage0 maps those to
`THM-M-0873`, `THM-M-0874`, and `THM-M-0875`. It also contains a duplicate-domain generic record,
`THM-M-1567`, at `Docs/researches/math_theorems.md:11544-11549`. Their statements and evidence do not
transfer to this target.

## Source gate

There is no repository-selected truth-valued proposition. Before leaving `H5`, an accountable
reviewer must select and lawfully preserve the intended source, determine whether this target is a
theorem, an open problem, or a branch ledger, map every definition/binder/hypothesis/conclusion and
proof boundary, audit corrections and current status, reconcile the neighboring records, and
obtain independent approval. Only then may the statement phase elaborate and mutation-test an
identical Lean expression.

`H5` here does not say that graph isomorphism is false or independent. It says the received topic
cannot yet be checked by a proof kernel as one proposition.

## Lean discovery boundary

Pinned mathlib supplies `SimpleGraph.Iso` (`G ≃g H`) as adjacency-preserving vertex equivalence,
`Language` as sets of words, and `ManyOneReducible`/`OneOneReducible` as computable reductions. The
probe elaborates these exact interfaces. It does not supply a finite-graph serialization, P or NP,
quasipolynomial time, the graph-isomorphism decision language, or a complexity theorem. A bounded
case-insensitive search found no exact-topic declaration; a complete immutable formal-candidate
audit remains downstream.

The canonical module, target expression, expression and environment fingerprints, alternate
encodings, and statement mutations therefore remain null. No formal absence theorem, statement
elaboration, proof, audit completion, or theorem completion is claimed.
