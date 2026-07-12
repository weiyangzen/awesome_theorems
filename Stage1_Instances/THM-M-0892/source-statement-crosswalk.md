# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6530-6535` supplies exactly the Chinese title
`Hoffman-Singleton theorem`, Alan Hoffman and Robert Singleton, 1960, the gloss `existence of
Moore graphs`, high importance, and status `verified`. Git history places all six uncited fields in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:24332-24357` repeats that gloss while leaving the target formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axiom
policy, machine status, and artifact links open. The rev-5.6 manifest preserves `verified` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

The word "existence" has no degree, diameter, girth, order, uniqueness clause, or quantifier. It
therefore does not distinguish a known example from the general degree classification or the open
degree-57 case.

## Primary-source lead

Crossref, DBLP, OpenAlex, and Semantic Scholar metadata consistently identify Alan J. Hoffman and
Robert R. Singleton, *On Moore Graphs with Diameters 2 and 3*, *IBM Journal of Research and
Development* **4**(5) (November 1960), 497-504, DOI `10.1147/rd.45.0497`. Crossref metadata were
captured with SHA-256
`fe75750bf210b237d10d6c495973aa238d06d2b85d97ab1cc5eb2916c63625ab`; OpenAlex and Semantic
Scholar classify the published article as closed access and expose no lawful open PDF.

A complete eight-page scan was inspected temporarily, with observed SHA-256
`fa0d15639b1abadce856004863bc4a57e5ac61bf37a69127317fa16aed83dc09`. Its abstract and Section 1,
page 497, define a Moore graph of type `(d,k)` as a connected undirected graph homogeneous of
degree `d`, diameter `k`, and attaining equality in the Moore vertex bound. For diameter `2`, the
paper says the types with degrees `2`, `3`, and `7` exist uniquely and no other degree is possible
except `57`, whose existence is undecided. Section 4, pages 498-499, derives the four candidates;
Theorem 5 on page 500 proves uniqueness at degree `3`, Theorem 11 on page 503 proves uniqueness at
degree `7`, and Theorem 13 on page 504 gives the sole diameter-3 graph.

This inspection sharpens the ambiguity but is still only `H1`. The scan's access and provenance are
not suitable for a lawful public source packet; no complete versioned transcription, correction or
errata audit, source admission, proof-node mapping, or independent review exists. The diameter-2
result is also a compound narrative across several pages rather than one numbered theorem, while
the catalog says only existence of Moore graphs. It therefore does not select construction,
uniqueness, classification, diameter `2`, diameter `3`, or their conjunction.

## Authoritative discriminator

Ichiro Shimada, *The graphs of Hoffman-Singleton, Higman-Sims, and McLaughlin, and the Hermitian
curve of degree 6 in characteristic 5*, arXiv `1405.4643v1` (2014), was inspected as an immutable
modern construction source (PDF SHA-256
`601815148551ed1d1c1cbdaaf5d2857629a5e9d340dc4dd689376af43911e8c5`). Its introduction states
that the Hoffman-Singleton graph is the unique strongly regular graph with parameters
`(v, k, lambda, mu) = (50, 7, 0, 1)`, and Theorem 1.8 constructs three connected components each
isomorphic to it. This confirms a standard degree-7 existence/uniqueness family but is not the
catalog-selected primary result and is not independently admitted as `H0`.

## Component crosswalk

| Repository or source element | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Moore graph | source-defined connected regular graph attaining the Moore order bound, or a later equivalent girth formulation | `SimpleGraph`, `IsRegularOfDegree`, `diam`, `girth`, `Fintype.card` | HS60 definition inspected; exact encoding and transport open |
| existence | one graph at degree `7`, examples at all known degrees, or a graph at an unspecified degree | existential vertex type and graph, with exact parameter predicates | quantifier and parameters absent |
| Hoffman-Singleton | the degree-7 graph, its construction, or a classification theorem bearing both authors' names | exact existence, isomorphism, or degree-classification proposition | root not selected |
| 50 vertices / degree 7 | the known diameter-2 Moore example | `Fintype.card V = 50`, `G.IsRegularOfDegree 7` | credible candidate only |
| diameter 2 / girth 5 | metric and cage characterizations | `G.diam = 2`, `G.girth = 5` with connected/nonacyclic guards | mathlib conventions require boundary mapping |
| `(50, 7, 0, 1)` | strongly regular characterization | `G.IsSRGWith 50 7 0 1` | pinned API exists; transport to Moore definition open |
| uniqueness | unique graph up to isomorphism | future `SimpleGraph.Iso` statement | not mentioned by catalog gloss |
| degree 57 | unresolved diameter-2 Moore possibility | open existential branch or classification alternative | must never be asserted as known existence |
| `verified` | untrusted inventory label | no declaration or proof object | explicitly rejected as evidence |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
checks finite simple graphs, degree regularity, graph distance and diameter, girth, and strongly
regular parameter packages. The natural-valued `diam` and `girth` APIs have junk-value boundary
conventions that must be guarded in an exact statement. A bounded source-name search found no
Hoffman-Singleton or Moore-graph target declaration in repo-local or pinned-mathlib Lean sources.

These checks establish only that candidate encodings have adjacent pinned infrastructure. They are
not a precommitted exhaustive anchor audit and supply no exact statement or proof credit.

## Required source admission

Before leaving `H1`, accountable reviewers must preserve a lawful immutable complete source,
select the exact proposition and locator, transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, and boundary case, and independently approve
the mapping. The selection must explicitly separate the known degree-7 graph from the degree
classification and open degree-57 existence question. Only then may the statement phase freeze
minimal imports, an elaborated expression, checked transports, and all required mutation classes.
