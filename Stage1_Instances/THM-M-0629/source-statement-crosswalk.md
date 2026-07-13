# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4664-4669` supplies the title `一点紧化定理`, attribution Pavel
Alexandrov, year 1924, gloss `局部紧Hausdorff空间的一点紧化`, high importance, and status
`已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, definition,
theorem/page locator, binders, assumptions, conclusion, proof passage, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:17206-17231` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact links
open. The rev-5.6 manifest preserves `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Inspected primary source

Paul Alexandroff, *Uber die Metrisation der im Kleinen kompakten topologischen Raume*,
*Mathematische Annalen* 92 (1924), 294-301, DOI `10.1007/BF01448011`, is available as an archival
scan from the Gottingen State and University Library under stable article PURL
`http://resolver.sub.uni-goettingen.de/purl?GDZPPN002270099`. The retrieved nine-page article PDF
(`LOG_0024`) has SHA-256
`27697384150aac1383aa684ccf0743e7ce5494a27d714431dbb4692422c65cfa`.

Section 1, journal page 294, defines local `bikompakt`/`kompakt` at a point by existence of a
neighborhood whose closure, as a subspace, is `bikompakt`/`kompakt`, and defines the global local
property pointwise. Its footnote assumes Hausdorff's foundational definitions and earlier works.

Section 2, `Fundamentalsatz 1`, journal page 296, states:

> Ein jeder im Kleinen bikompakte topologische Raum R lasst sich (falls er nicht selbst bikompakt
> ist) durch Hinzufugung eines einzigen Punktes zu einem bikompakten Raume vervollstandigen; dies
> ist ausserdem nur auf eine Weise moglich.

A close English rendering is: every locally bicompact topological space `R`, provided it is not
itself bicompact, can be completed to a bicompact space by adjoining one point; moreover this is
possible in only one way. The proof constructs neighborhoods of the new point from complements of
finite unions of closures of beta-regions, checks the Hausdorff neighborhood axioms and
bicompactness, and asserts equivalence of every other such neighborhood system for uniqueness.

Journal page 297 says replacing `bikompakt` by `kompakt` gives an analogous existence theorem, but
then emphasizes that one can generally obtain several different one-point extensions and that
`bikompakt` is indispensable for uniqueness. Thus non-bicompactness and uniqueness are present in
the pinpoint primary root, while a qualified reviewer must still map historical `bikompakt`,
`kompakt`, `vervollstandigen`, and neighborhood terminology to modern compact Hausdorff and Lean
notions. The article also imports results and notation from prior works named in footnote 1; those
dependencies, translation, corrections, errata, and an independent review remain open. The scan is
an E4 candidate and justifies H1, not accepted H0.

## Clause crosswalk

| Catalog component | Conventional mathematical component | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| locally compact | primary page 294: some neighborhood has `bikompakt` closure at every point | `WeaklyLocallyCompactSpace` with `T2Space X`, or reviewed transport | exact historical-to-modern definition transport open |
| Hausdorff | Hausdorff foundations assumed in primary footnote 1 | `T2Space X` | modern separation mapping and imported-definition boundary open |
| one point | add an infinity outside the image | `OnePoint X`, `OnePoint.infty`, `OnePoint.compl_range_coe` | carrier and singleton-complement interfaces authenticated |
| compactification | compact Hausdorff extension by an embedding | `CompactSpace (OnePoint X)`, `T4Space (OnePoint X)`, `OnePoint.isOpenEmbedding_coe` | direct components exist; catalog does not choose the root bundle |
| noncompact input | primary page 296: `falls er nicht selbst bikompakt ist` | `NoncompactSpace X` | present in primary root but omitted by catalog gloss; reviewed transport required |
| dense image | implicit in completion/extension semantics; not a separate phrase in the displayed theorem | `OnePoint.isDenseEmbedding_coe` under `NoncompactSpace X` | relationship to historical `vervollstandigen` remains to be checked |
| uniqueness | primary page 296: `nur auf eine Weise`; page 297 says this fails for merely compact analogue | `OnePoint.equivOfIsEmbeddingOfRangeEq` | exact notion of sameness and checked component composition open |
| verified | untrusted inventory label | accepted source and kernel receipts would be required | no H or M completion credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Compactification.OnePoint.Basic` explicitly states that `OnePoint X` adds an
isolated point when `X` is already compact. The module constructs the topology and proves the
interfaces listed above. `IntakeProbe.lean` checks those interfaces and their axiom reports, but no
target theorem is declared and no exact conjunction or source transport is credited.

This bounded inspection is not the dependency-ordered anchor audit. Before H0, reviewers must
independently approve the archival source, audit its imported definitions and proof dependencies,
map every premise and proof transition, resolve translation and historical terminology, and audit
corrections and errata. Before statement acceptance, Lean work must
freeze exact binders, minimal imports, expression and environment fingerprints, checked alternate
encodings, and the required statement mutations.
