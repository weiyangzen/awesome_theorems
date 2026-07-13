# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1513-1518` supplies exactly the Chinese title, Girard Desargues
attribution, year 1648, gloss `两个三角形透视的条件`, high importance, and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, theorem locator,
formula, definitions, direction, hypotheses, proof boundary, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:5833-5858` repeats the gloss while explicitly leaving the target system,
foundation, precise definitions and premises, proof path, dependencies, alternate statement, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected projective and formal source lead

Nicolas Magaud, Julien Narboux, and Pascal Schreck, "A Case Study in Formalizing Projective
Geometry in Coq: Desargues Theorem," *Computational Geometry* 45(8), 2012, pages 406-424, DOI
`10.1016/j.comgeo.2010.06.004`, was inspected at the versioned HAL record
`inria-00432810v2` (submitted 2012-01-24). Section 3, printed page 7, states the conventional
projective point-to-line direction: if the three lines joining corresponding vertices of two
triangles meet at `O`, the three intersections of corresponding sides are collinear.

The source immediately distinguishes ambient assumptions: the property is independent of the bare
two-dimensional projective-plane axioms, while it is a theorem in projective dimension at least
three. Sections 5.1-5.3, printed pages 20-32, give the rank axioms, three-dimensional theorem,
planar lifting with explicit nondegeneracy ranks, and the Coq proposition. The paper reports more
than 10,000 Coq proof lines and about 280 lemmas. The inspected HAL PDF SHA-256 is
`e8c0c4d2956253a20b63ca944ce9a7cf23eb6756fc7bb44d6ab2381185866bb8`.

This is strong human-source and historical machine-formalization discovery evidence, but it is not
Lean 4 evidence. The Coq sources, exact revision, toolchain, terminal declarations, axioms, and
dependency closure are not pinned or checked in this repository; the paper's source model has not
been independently mapped to the catalog gloss. It therefore grants no H0, M0, or usable Lean
candidate status.

## Inspected affine source lead

David Hilbert, *The Foundations of Geometry*, authorized translation by E. J. Townsend, Open Court
reprint edition (1950; translation copyright 1902), was inspected in the Project Gutenberg edition
17384, most recently updated 2025-07-14. In Section 22, Theorem 32, printed page 46, Hilbert states:

- if homologous sides of two coplanar triangles are respectively parallel, the joins of homologous
  vertices are concurrent or mutually parallel; and
- conversely, if those vertex joins are concurrent or parallel and two pairs of homologous sides
  are parallel, then the third pair is parallel.

The observed PDF SHA-256 is
`c6f04965b5a8ca67a05c2e969357083b9ec0e7a0a2dd30dbf1ebb025cdcf1161`.
This is an inspected authoritative source lead, but the catalog does not cite it. Hilbert's Theorem
32 is an affine line-at-infinity specialization and its converse, rather than a source-selected full
projective formulation with finite side intersections. Its incorporated axioms, translation,
edition history, errata, exact relation to Desargues's 1648 work, and source-to-Lean transport have
not been independently reviewed. It supports provisional `H1`, not `H0`.

The historical attribution to Girard Desargues in 1648 is retained from the catalog. No primary
1648 edition, exact passage, language/translation chain, proof, or correction history was inspected
or credited.

## Clause crosswalk

| Repository element | Source or standard-family component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `两个三角形` (two triangles) | Hilbert uses two coplanar triangles with homologous vertices and sides | two ordered triples of points plus triangle/nondegeneracy predicates | ordering, distinctness, noncollinearity, and coplanarity open |
| `透视` (perspective) | standard family distinguishes perspective from a point and from a line; Hilbert states a parallel special case | concurrency of vertex joins; collinearity of side meets; or an affine parallel predicate | meaning and direction not selected |
| `条件` (condition) | could indicate implication, converse, necessary-and-sufficient condition, or informal characterization | `→`, reverse `→`, or checked `↔` | logical shape open |
| side intersections | finite projective meets in the standard form; points at infinity encode affine parallels | projective subspaces, homogeneous representatives, cross products, or existential incidence witnesses | intersection existence/uniqueness and infinity transport open |
| ambient geometry | Magaud et al. distinguish independent abstract-plane, Pappusian-plane, and dimension-at-least-three settings; Hilbert uses selected plane axioms | affine space, `Projectivization K V`, or a future incidence-plane/rank structure | model, dimension, and scalar assumptions open |
| Girard Desargues / 1648 | historical attribution from the catalog | provenance only, never a Lean hypothesis | primary-source identity unverified |
| `已验证` | untrusted inventory label | source review and kernel receipts would be required | no H or M credit |

## Pinned Lean boundary

Pinned mathlib provides `Collinear`, affine spans and lines, `Projectivization`, its one-dimensional
submodule representation, projective subspaces, and cross/dot-product operations for homogeneous
three-coordinate models. These APIs can support future encodings, but none states that concurrent
corresponding-vertex joins force collinear corresponding-side intersections, its converse, or
Hilbert's complete affine specialization.

A bounded exact-topic search of repo-local Lean and pinned mathlib found no declaration named or
documented for Desargues and no complete perspective-triangle incidence theorem. The probe checks
adjacent interfaces only. This observation is not the later precommitted exhaustive anchor audit and
does not establish that no external Lean formalization exists. The inspected Coq formalization is
an external non-Lean lead and cannot be silently translated into mathlib closure.

## Source and statement gates

Before leaving `H1`, accountable reviewers must preserve a lawful immutable source edition, select
one exact theorem and all incorporated definitions and axioms, map every binder, hypothesis,
direction, conclusion, incidence construction, parallel/infinity convention, and degenerate case,
audit translations and errata, reconcile the historical attribution, and independently approve
fidelity to `THM-M-0210`.

The statement phase must then choose minimal pinned imports, elaborate the exact Lean expression,
record normalized-expression and environment fingerprints, compile every credited affine,
projective, incidence, or coordinate transport, and mutation-test removed hypotheses, changed
domains, binder scope, direction, dimension, and boundary cases. Until then, the formal target,
obligation registry, proof tree, and all proof credit remain open.
