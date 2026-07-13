# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:656-661` supplies exactly the title `彼得-外尔定理`, attribution
to Fritz Peter and Hermann Weyl, the year 1927, the gloss `紧群表示的完备性` ("completeness of
compact-group representations"), importance `high`, and status `verified`. Git history places all
six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2551-2576` repeats the metadata while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axiom
policy, machine-checked status, and artifact links open. The rev-5.6 manifest preserves `verified`
only as untrusted metadata and resets the target to `L0 / rework_required`.

The catalog contains no bibliography, formula, theorem/page locator, group separation assumptions,
representation category, coefficient definition, Haar normalization, topology of closure, ordered
binders, proof boundary, correction history, or reviewer. Its gloss names a theorem family but does
not select a stable proposition.

## Original source lead

Crossref's record for DOI `10.1007/BF01447892` identifies F. Peter and H. Weyl, *Die
Vollstandigkeit der primitiven Darstellungen einer geschlossenen kontinuierlichen Gruppe*,
*Mathematische Annalen* 97, issue 1 (December 1927), pages 737-755. Its metadata and Unixref record
were inspected on 2026-07-13; the records supply authors, journal, date, volume, issue, page range,
DOI, and publisher links.

The article scan in the Gottinger Digitalisierungszentrum volume `PPN235181684_0097`, article
`LOG_0039`, was also inspected. Page 737 begins with representations of a "closed continuous group"
by homogeneous linear transformations or matrices and invokes infinitesimal Lie concepts for its
invariant volume. Page 752 states a Parseval-type `Fundamentalsatz` over inequivalent irreducible
representations for continuous functions. Page 753 states an `Approximationssatz`: every continuous
function on the group is uniformly approximable by a finite sum of entries of irreducible
representations. Page 754 separately gives uniform approximation of continuous class functions by
finite linear combinations of irreducible characters and separation consequences for group
elements and conjugacy classes.

These pinpoints expose the ambiguity rather than resolving it. The catalog does not choose the page
752, 753, or 754 result, and a modern arbitrary compact-Hausdorff-group formulation would require
an explicit generalizing source or checked transport from the paper's matrix/Lie setting. No full
definition/assumption/conclusion/proof-node map, translation, correction or errata audit, repository
preservation, or independent review is credited. Thus the source supports provisional `H1`, not
`H0`.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "compact group" | compact Hausdorff group, closed continuous group in the paper's terminology, or a more specialized group class | `Group G`, topological-group structures, compactness and separation typeclasses | exact source assumptions absent |
| "representations" | finite-dimensional continuous complex representations, unitary representatives, irreducibles, or the regular representation | `Representation Complex G V`, `FDRep Complex G`, continuous/unitary refinements | representation contract absent |
| "completeness" | uniform density of matrix coefficients in `C(G)`, density/basis in `L2(G)`, or regular-representation direct-sum completeness | submodule closure, `Lp`, `HilbertBasis`, or a unitary direct-sum equivalence | conclusion and topology absent |
| matrix coefficients | evaluation against dual vectors or complex inner products, possibly indexed by irreducible representatives | future continuous coefficient map into functions on `G` | definition and conjugation convention absent |
| Haar integration | normalized invariant measure on the compact group | `MeasureTheory.Measure.haar`, finite-measure and normalization witnesses | source normalization and `L2` convention absent |
| `verified` | untrusted inventory label | no declaration, wrapper, or proof body | explicitly rejected as evidence |

## Variant boundary

The uniform-density and `L2`-completeness formulations may be related using continuous-function
density in `L2`; regular-representation decomposition may encode comparable mathematics; and point
separation is a consequence used in compact-group structure theory. None is adopted as the root
without a pinpoint source crosswalk. In particular, the short catalog gloss cannot decide the
normed topology, measure normalization, irreducible indexing, multiplicities, continuity model, or
whether a conclusion is density, an orthogonal basis, or an isomorphism.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
checks `Representation`, `FDRep`, `MeasureTheory.Measure.haar`,
`ContinuousMap.toLp_denseRange`, and generic `HilbertBasis` interfaces. These are necessary-looking
substrate only. A bounded case-insensitive search found no `Peter-Weyl` or `matrix coefficient`
target in repo-local Lean or pinned mathlib. That observation is not an exhaustive external-project
audit and cannot prove absence.

## Required source admission

The statement phase must preserve and hash a lawful complete source edition, select an exact result
and proof boundary, map every incorporated definition, ordered binder, hypothesis, conclusion and
boundary case, audit translation and corrections, and obtain independent source review. It must
then freeze and mutation-test the same exact Lean expression. Until then the canonical mathematical
and Lean targets remain null and the source classification remains `H1`.
