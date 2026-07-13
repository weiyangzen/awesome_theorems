# THM-M-0887 source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6495-6500` supplies exactly the title `谱图理论`, attribution
`众多数学家`, period `20世纪`, gloss `图的谱性质`, importance `高`, and status `已验证`. All six
uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, graph class, matrix,
spectrum convention, theorem/page locator, proof, erratum, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:24197-24222` mechanically projects the same gloss. It explicitly leaves
the formal system, foundation, exact definitions and premises, proof route, dependent lemmas,
equivalent forms, axioms, machine status, and artifact links as `待补充`. The rev-5.6 target
manifest retains `已验证` only as `source_status_untrusted`, resets the item to
`L0 / rework_required`, and states `theorem_complete=false`.

## Literal crosswalk

| Repository element | Missing mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| `谱图理论` | one theorem rather than a field containing many results | one canonical `Prop` | subject label only |
| `图` | graph model, carrier, finiteness, direction, weights, loops, connectivity | `SimpleGraph V` or another source-selected graph/operator type with exact instances | all choices open |
| `谱` | operator, scalar field, eigenvalue/set spectrum, ordering, multiplicity, normalization | `adjMatrix`, `lapMatrix`, Hermitian eigenvalues, algebraic `spectrum`, or a new exact definition | no spectrum selected |
| `性质` | exact hypotheses, conclusion, constants, equality/converse conditions, and quantifier order | binder-complete expression plus checked encodings | no proposition supplied |
| `众多数学家`, `20世纪` | immutable primary or authoritative work and pinpoint result | source ID, edition, theorem/page, premise/proof/errata map | no source credit |
| `已验证` | accepted human proof and kernel evidence | accepted source and node receipts | explicitly rejected as evidence |

The literal record cannot populate canonical domains, universes, binders, hypotheses, conclusion,
alternate encodings, excluded cases, formal module, declaration, expression fingerprint, or
environment fingerprint.

## Catalog-cluster boundary

The surrounding source records confirm a spectral-graph subject cluster but also prevent silent
substitution. Immediately before this record are separate Ramanujan and MSS construction entries.
Immediately after it are separate Cheeger, Alon-Milman, Hoffman, and Wilf entries concerning
spectral gaps, expansion, independent sets, or coloring. The cluster supports the English subject
translation but assigns no one neighboring proposition to `THM-M-0887`; no statement, source,
proof, or status transfers across IDs.

## Source-family leads not credited

The broad title is shared by textbooks and monographs containing many distinct results. A bounded
bibliographic attempt considered the AMS monograph family commonly titled *Spectral Graph Theory*,
but Crossref returned HTTP 429 and the author-hosted page failed certificate verification in this
worker environment. No source file was fetched, vendored, admitted, or reviewed. More importantly,
even successful bibliographic metadata would identify a book-sized field, not select a numbered
theorem. This failed observation receives no source or H credit.

An H0 crosswalk requires a lawful immutable edition or archival snapshot, stable identifier,
numbered theorem/section/page, all incorporated definitions, ordered assumptions and conclusion,
dependent source IDs, proof boundary, correction and errata disposition, and identified independent
reviewer. None exists for this target.

## Pinned Lean crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
the following adjacent declarations:

| Declaration | What it supplies | Why it is not THM-M-0887 |
|---|---|---|
| `SimpleGraph.adjMatrix` | adjacency matrix of a decidable finite simple graph | definition only; no source-selected property |
| `SimpleGraph.isHermitian_adjMatrix` | Hermitian symmetry of that matrix | one generic fact among many candidate roots |
| `Matrix.IsHermitian.eigenvalues` | a real eigenvalue enumeration for Hermitian matrices | no graph theorem or selected ordering claim |
| `SimpleGraph.adjMatrix_pow_apply_eq_card_walk` | adjacency powers count fixed-length walks | plausible spectral substrate, not the catalog statement |
| `SimpleGraph.lapMatrix` | combinatorial degree-minus-adjacency matrix | no normalization or root theorem selected |
| `SimpleGraph.posSemidef_lapMatrix` | positive semidefiniteness of the combinatorial Laplacian | one candidate theorem, not source-identical evidence |
| `SimpleGraph.card_connectedComponent_eq_finrank_ker_toLin'_lapMatrix` | component count equals real Laplacian nullity | another distinct candidate theorem |
| `Matrix.IsHermitian.eigenvalues_mem_spectrum_real` | chosen eigenvalues lie in real algebraic spectrum | matrix bridge only |

A bounded case-insensitive exact-topic search over repo-local Lean and pinned mathlib found no
declaration named for spectral graph theory, graph spectra, or the literal claim. That observation
is neither an exhaustive anchor audit nor an absence proof. Generic graph/matrix declarations do
not determine a source proposition, terminal proof body, or M credit.

## Exact-statement gate

The provisional human classification is `H5`: the received catalog wording is not a stable
truth-valued proposition. This classification does not assert that established spectral graph
theorems are false or open. `M4` records that no source-identical usable formal artifact is credited,
and `R4` that no proof reconstruction can attach to an unselected claim.

The dependent statement phase is blocked until accountable reviewers select and approve one
immutable pinpoint source proposition and resolve every row above plus all scope-map boundary cases.
It must then freeze the exact Lean expression, minimal imports, environment fingerprint, checked
alternate encodings, and removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
