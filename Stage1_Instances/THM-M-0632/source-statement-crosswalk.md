# Source-statement crosswalk

## Repository source record

The only repository-supplied claim record is `Docs/researches/math_theorems.md:4685-4690`,
introduced in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`:

| Catalog field | Received value | Statement consequence |
|---|---|---|
| title | `贝尔-豪斯多夫定理` | Names a theorem family, but does not state a proposition. |
| attribution | Rene Baire / Felix Hausdorff | Historical orientation only; no work or theorem is cited. |
| time | 1909 | Does not identify a publication, edition, theorem, or proof boundary. |
| statement | `贝尔空间的性质` | Names an open-ended topic; supplies no binders, assumptions, or conclusion. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; supplies no human or machine proof credit. |

Stage0 at `Docs/Stage0_Blueprint.md:17287-17312` repeats the gloss while leaving the formal
system, exact definitions and premises, proof route, dependencies, alternate statements, axioms,
machine status, and artifacts open. It cannot fill the absent proposition.

The repository record is a secondary compilation without a bibliography for this item. No primary
source edition, theorem/page locator, incorporated definition, assumption map, proof boundary,
correction history, errata check, translation, or independent review is supplied. It is E5 intake
provenance, not H0 or H1 evidence for an exact proposition.

## Bibliographic lead not credited

K. Yosida, *Functional Analysis*, Springer, 1965 edition, chapter "Applications of the
Baire-Hausdorff Theorem," pages 68-81, DOI `10.1007/978-3-642-52814-9_3`, is an authoritative
secondary lead. Crossref supplies the chapter metadata. The publisher abstract says completeness
of a B-space or F-space enables application of the theorem from Chapter 0 and lists uniform
boundedness, resonance, open mapping, and closed graph as applications.

This metadata neither exposes the theorem text in Chapter 0 nor reconciles it with the catalog's
1909 date and vague point-set-topology gloss. It therefore receives only E5 discovery status. A
later source audit must inspect an immutable edition, identify the exact source statement and
definitions, review corrections and errata, and determine whether the catalog intended that
formulation or another Baire-space result.

## Phrase-to-statement map

| Received or candidate component | Required source decision | Prospective Lean component | Intake result |
|---|---|---|---|
| Baire space | exact category definition and index convention | `BaireSpace`, `BaireSpace.baire_property` | adjacent definition checked; target unresolved |
| complete space | metric versus pseudometric/completely metrizable hypotheses | `BaireSpace.of_completelyPseudoMetrizable` | possible first Baire theorem; separately overlaps `THM-M-0631` |
| locally compact space | local-compactness and separation convention | `BaireSpace.of_t2Space_locallyCompactSpace` | possible second Baire theorem only |
| Baire-space properties | select one density, meagreness, residual, subspace, or cover result | declarations in `Mathlib.Topology.Baire.Lemmas` | no conclusion selected |
| dense `G_delta` subset | ambient/subtype topology and density assumptions | `IsGδ.baireSpace_of_dense` | candidate preservation result only |
| locally compact `G_delta` subset | separation and local-compactness assumptions | `IsGδ.of_t2Space_locallyCompactSpace` | candidate consequence only |
| functional-analysis applications | exact vector-space, completeness, and operator hypotheses | uniform boundedness/open mapping/closed graph families | downstream applications, not silently substituted |

There are consequently no canonical ordered binders, hypotheses, conclusion, credited alternate
encoding, statement fingerprint, obligation, or proof body.

## Formal-source boundary

A bounded inspection of repository-local Lean and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` located the following adjacent interfaces:

- `BaireSpace` and `BaireSpace.baire_property`;
- `dense_iInter_of_isOpen`, `IsGδ.baireSpace_of_dense`, `mem_residual`, and
  `not_isMeagre_of_isOpen`;
- `BaireSpace.of_completelyPseudoMetrizable`;
- `BaireSpace.of_t2Space_locallyCompactSpace` and
  `IsGδ.of_t2Space_locallyCompactSpace`.

Mathlib explicitly labels the last two instance families as first and second Baire theorems. Their
different hypotheses and conclusions expose the missing selection rather than authorize one. The
probe authenticates names and types only. This is not the dependency-ordered exhaustive anchor
audit and gives no exact-statement, source, proof-body, or machine-closure credit.

## Human-source gate

To leave `H5`, accountable reviewers must first approve a stable truth-valued target and immutable
primary or authoritative source. The crosswalk must then bind the exact theorem and incorporated
definitions, every assumption and conclusion, proof and dependency boundaries, corrections and
errata, translation, historical naming, and each source component to the mathematical and Lean
encodings. Until then, ordinary statement and theorem-proof execution remains blocked.
