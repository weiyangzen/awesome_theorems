# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9964-9969` supplies exactly the title `Peixoto定理`, Mauricio
Peixoto, 1962, the gloss `二维系统的结构稳定性`, importance `high`, and status `已验证`. Git history
places all six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. A second copy at
lines 10215-10220 is verbatim metadata duplication, not independent evidence.

`Docs/Stage0_Blueprint.md:37182-37207` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine-checked status, and artifact links open. The rev-5.6 target manifest preserves `已验证` only
as untrusted metadata and resets this target to `L0 / rework_required`.

The catalog contains no bibliography, numbered theorem, page, manifold or boundary convention,
regularity/topology, definition of structural stability, ordered binders, hypotheses, exact
conclusion, proof boundary, correction history, reviewer, or formal artifact. Its noun phrase does
not choose a stable proposition.

## Primary bibliographic leads

M. M. Peixoto, "Structural stability on two-dimensional manifolds," *Topology* 1(2), April 1962,
pages 101-120, DOI `10.1016/0040-9383(65)90018-2`. Crossref metadata confirms the author, title,
date, journal, volume, issue, and pages, matching every bibliographic clue in the repository. The
publisher's full text was not available through the inspected unauthenticated APIs, so no exact
theorem wording or page-level premise/conclusion crosswalk is claimed.

M. M. Peixoto, "Structural stability on two-dimensional manifolds: A further remark," *Topology*
2(1-2), 1963, pages 179-180, DOI `10.1016/0040-9383(63)90032-6`. Crossref confirms a same-title
follow-up; Semantic Scholar supplies the subtitle "A further remark." Its precise relationship to
the 1962 theorem must be reviewed as a correction/follow-up before any source packet can reach
`H0`. Article-level metadata is discovery evidence only.

## Inspected modern discriminator

Charles Pugh and Mauricio Matos Peixoto, "Structural stability," *Scholarpedia* 3(9):4008 (2008),
DOI `10.4249/scholarpedia.4008`, revision 137910, was inspected as an authorial modern overview. It
defines flow structural stability using a `C^1` neighborhood of vector fields and an
orientation-preserving orbit homeomorphism. In its "Structural Stability in Dimension Two"
section it separates the following claims:

- on a compact orientable two-manifold, for `C^r` flows with `r >= 1`, the structurally stable locus
  is open-dense;
- structurally stable flows are characterized by hyperbolic periodic orbits, no other recurrence,
  and no saddle connections; and
- density on nonorientable surfaces for `r >= 2` is described as open except for three specified
  surfaces, whereas for `r = 1` orientability is irrelevant.

It later summarizes the surface result as Morse-Smale equals structurally stable and structural
stability is generic. This source makes the catalog ambiguity and boundary risk concrete, but it is
not the catalog's cited source, a verbatim edition of the 1962 article, or an independently accepted
primary proof packet. It receives no `H0` credit.

## Component crosswalk

| Catalog/source component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "two-dimensional systems" | flows of `C^r` vector fields on compact surfaces; disc/boundary or closed-manifold variants; orientable/nonorientable cases | manifold model, `ContMDiffSection`, generated/global `Flow Real M` | domain, boundary, regularity, and generation relation open |
| structural stability | nearby vector fields have orbit-equivalent flows; possible epsilon-small equivalence or conjugacy variants | topology/uniformity on vector-field sections plus quantified `Homeomorph` and orbit relation | core definitions absent and exact variant open |
| characterization | hyperbolic singular and periodic orbits, no other recurrence, no saddle connections | derivative/Poincare-map hyperbolicity, omega/alpha limits, separatrix and connection predicates | major infrastructure not identified as one pinned API |
| openness | structurally stable locus is open | `IsOpen` in a source-selected vector-field topology | distinct conclusion, not selected |
| density/genericity | structurally stable locus is dense, open-dense, or residual | `Dense`, `DenseInducing`, `IsOpen`, or Baire-category predicates | wording and hypotheses materially open |
| orientability/regularity | orientable all `r >= 1`; nonorientable `C^1`; higher-regularity exceptions/open boundary | surface-orientation structure and differentiability index | source-sensitive hypothesis; cannot be omitted |
| `已验证` | untrusted inventory label | no declaration or proof object | explicitly rejected as evidence |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
imports manifold integral curves, smooth sections, flows, omega limits, and diffeomorphisms. It
checks `TangentSpace`, `TangentBundle`, `ContMDiffSection`, `IsMIntegralCurve`, `Flow`,
`Flow.orbit`, `Flow.toHomeomorph`, `Flow.IsSemiconjugacy`, `omegaLimit`,
`Flow.isInvariant_omegaLimit`, `Homeomorph`, and `Diffeomorph`.

A case-insensitive bounded search of repo-local and pinned-mathlib Lean sources found no declaration
named for Peixoto or dynamical structural stability. Generic flow semiconjugacy requires a
continuous surjection commuting at equal times; the source's orbit equivalence may permit time
reparametrization, so it is not silently credited as the same relation. The search is intake
discovery, not an exhaustive external-project anchor audit or proof of global absence.

## Source and statement exit gate

The statement phase must select and independently approve one exact source theorem, including its
edition, theorem/page locator, incorporated definitions, proof boundary, follow-up/correction and
errata status, and every domain, topology, regularity, orientability, boundary, recurrence,
connection, and genericity convention. It must then elaborate and fingerprint the binder-complete
Lean expression with minimal pinned imports, add checked transports for credited alternate
encodings, and run all four required mutation classes. Until then the provisional status is
`[H1, M4, R4]`; no statement or proof closure is claimed.
