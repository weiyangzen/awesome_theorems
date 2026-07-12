# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md:6481-6486` contains exactly the name `Morgenstern theorem`, Moshe
Morgenstern, 1994, and the phrase `existence of Ramanujan graphs`, plus importance and an untrusted
formalization label. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no citation, definitions, formula,
assumptions, theorem number, page, proof boundary, errata status, or formal artifact.

`Docs/Stage0_Blueprint.md:24143-24168` repeats that gloss while explicitly leaving precise
definitions and premises, proof route, equivalences, axioms, and machine artifacts open. Its
generic assertion that a closed result is known is scheduling prose, not a source review.

## Bibliographic discovery candidate

Crossref DOI metadata and DBLP record `journals/jct/Morgenstern94` identify:

> Moshe Morgenstern, "Existence and Explicit Constructions of q + 1 Regular Ramanujan Graphs for
> Every Prime Power q," *Journal of Combinatorial Theory, Series B* 62(1), September 1994,
> pages 44-62, DOI `10.1006/jctb.1994.1054`, PII `S0095895684710549`.

The title, author, year, and subject make this the exact-match source candidate. During intake,
Crossref and DBLP bibliographic records were inspected; an article edition containing the numbered
theorems and definitions was not admitted. The source candidate therefore remains below `H0`: no
immutable theorem-text hash, pinpoint theorem/page, full premise and definition mapping, errata
audit, proof-boundary crosswalk, or independent review exists.

## Clause crosswalk

| Repository or bibliographic phrase | Candidate mathematical component | Lean surface required later | Intake status |
|---|---|---|---|
| `Ramanujan graph` | finite regular graph with a source-specific bound on nontrivial adjacency eigenvalues | graph model, regularity, adjacency matrix/operator, spectrum and exclusion predicate | object family only; definitions absent from catalog |
| `existence` | one graph, an unbounded family, or an explicit effective construction | exact existential/family binders and constructive output | ambiguous in catalog |
| `q + 1 regular` | degree indexed by a prime power `q` | prime-power predicate or finite-field witness and `SimpleGraph.IsRegularOfDegree` or checked equivalent | article-title candidate only |
| `for every prime power q` | outer parameter range | ordered quantifiers and all exceptional cases | article-title candidate only |
| `explicit constructions` | algebraic construction with source-specific auxiliary data | construction object, graph extraction, invariants, and effectiveness claim | article-title candidate only |
| `verified` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow intake
probe confirms general APIs for finite simple graphs, vertex degree regularity, real adjacency
matrices, Hermitian symmetry, real eigenvalue indexing, and real square roots. A bounded exact-topic
search found no `Morgenstern` or `Ramanujan graph` occurrence in repo-local or pinned-mathlib Lean
sources. This is feasibility and discovery evidence only, not a complete anchor audit or a global
absence claim. In particular, mathlib has no source-selected predicate in this dossier deciding
which adjacency eigenvalues are trivial, and the API probe does not encode an existence theorem.

## Required source acceptance work

A later statement/source audit must preserve an immutable article edition, locate every root
theorem and incorporated definition, transcribe the exact quantifiers and hypotheses, map the graph
and spectral conventions clause by clause, identify all construction branches and exceptions,
check corrections or errata, reconcile the neighboring targets, and obtain independent source
review. Until then the canonical claim and formal target remain null, human debt is `H1`, and no
source or machine closure is credited.
