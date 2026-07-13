# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md:6502-6507` contains exactly the name `Cheeger inequality`, Jeff
Cheeger, 1970, the phrase `the spectral gap and isoperimetric constant of a graph`, importance, and
an untrusted formalization label. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, theorem number, page,
definitions, formula, assumptions, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:24224-24249` repeats the same metadata while explicitly leaving exact
definitions and premises, proof route, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Its generic scheduling prose about a known closed result is not a primary
source review. The `verified` label is rejected as evidence under rev-5.6.

## Source identity blocker

No primary theorem text is admitted at intake. The attribution `Jeff Cheeger, 1970` points toward
the geometric origin of Cheeger's inequality, but the repository gloss explicitly asks for a graph
spectral gap and graph isoperimetric constant. The record does not identify which discrete theorem,
adaptation, textbook formulation, or attribution convention owns that graph claim. Selecting a
standard modern graph formula would therefore invent source identity, definitions, and constants.

This gives provisional `H5` for the received catalog target: it is not yet a stable proposition.
It is not a claim that any reviewed geometric or graph Cheeger theorem is false, independent, or
open. A corrected source-selected proposition can enter ordinary theorem execution after review.

## Clause crosswalk

| Repository phrase | Possible mathematical component | Lean surface required later | Intake disposition |
|---|---|---|---|
| `Cheeger inequality` | geometric or discrete theorem family; one-sided or two-sided inequality | one source-exact proposition and checked ownership decision | family identified; root not selected |
| `graph` | finite, locally finite, or infinite; simple, multiple-edge, weighted, directed, regular, or irregular graph | exact graph structure, finiteness/local-finiteness, weight, reversibility and decidability context | finite simple graph is only an adjacent candidate |
| `spectral gap` | adjacency gap, first positive combinatorial-Laplacian value, second normalized-Laplacian value, random-walk gap, or spectral bottom/infimum | operator, coefficient domain, eigenvalue or spectrum encoding, ordering, multiplicity, attainment and normalization | ambiguous |
| `isoperimetric constant` | edge expansion, conductance, vertex expansion, or weighted boundary ratio | boundary definition, volume/cardinality denominator, tested subsets and infimum/minimum | ambiguous |
| relation between the two | lower bound, upper bound, or a two-sided conjunction with convention-dependent constants | exact inequalities, square/square-root terms, coercions and side conditions | absent |
| Jeff Cheeger / 1970 | geometric historical attribution or intended provenance for a discrete descendant | immutable source edition, theorem/page, definition and proof-boundary crosswalk | attribution conflict unresolved |
| `verified` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Missing source-to-statement map

An accepted crosswalk must identify a stable source edition and pinpoint theorem, every incorporated
definition, the complete ordered premises and conclusion, graph and spectral normalizations,
constants and inequality directions, all exceptional cases, proof boundaries and imported results,
corrections or errata, and an independent reviewer. It must also explain why the selected theorem is
this target rather than `THM-M-0880`, `THM-M-0887`, `THM-M-0889`, or a manifold theorem. This is
especially important because Alon-Milman is a historical source family for a discrete Cheeger-type
relationship, while sparse-cut formulations can reuse conductance or edge-boundary definitions.

Until that work is complete, there is no canonical human statement, ordered binder list, hypothesis
list, conclusion formula, alternate encoding, excluded-case list, source fingerprint, or H0 credit.

## Pinned Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow intake probe
checks these adjacent interfaces:

- `SimpleGraph.edgeFinset`, `neighborFinset`, `degree`, and `IsRegularOfDegree`;
- `SimpleGraph.adjMatrix`, `lapMatrix`, and `lapMatrix_toLinearMap₂'`;
- `SimpleGraph.posSemidef_lapMatrix` and
  `card_connectedComponent_eq_finrank_ker_toLin'_lapMatrix`;
- `SimpleGraph.IsEdgeConnected` as nearby cut/connectivity infrastructure.

A bounded literal query over repo-local Lean and pinned mathlib found no graph-Cheeger,
conductance, isoperimetric-constant, edge-expansion, or spectral-gap theorem candidate. The checked
declarations are generic substrate and do not define the source isoperimetric constant, select a
spectral gap, or prove their relationship. The query is not the downstream immutable anchor audit,
and neither its result nor the API probe grants M credit. The canonical formal target, minimal
imports, expression hash, environment fingerprint, transports, mutations, proof body, axioms, and
trust closure all remain open.

## Retry condition

The statement phase may retry after independent graph-spectral and source reviewers approve one
immutable graph proposition, its historical attribution and neighboring-target ownership, all
definition and premise mappings, constants, boundary cases, proof and correction boundaries, and
the exact relationship to a proposed Lean encoding. Until then the root remains null and no proof
search may silently choose a convenient variant.
