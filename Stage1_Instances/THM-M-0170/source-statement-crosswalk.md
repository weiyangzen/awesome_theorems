# Source-statement crosswalk

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Smooth isometric embedding in Euclidean space | John Nash, "The imbedding problem for Riemannian manifolds," *Annals of Mathematics* 63(1), 1956, pp. 20-63, DOI 10.2307/1969989 | Canonical existential root described in `intake.json` | Primary proof paper identified; exact theorem/page premise mapping, scanned-edition hash, and errata review remain open, so status is `H1` |
| Compact and noncompact cases | Nash 1956 treats the global smooth embedding problem with separate technical constructions and dimension estimates | Future case nodes beneath the same root | Required architecture distinction; no node closure or bound is credited |
| Isometry condition | Preservation of the Riemannian line element, represented formally as equality of the pullback Euclidean metric with `g` | Future pullback-metric equality | Exact mathlib tensor/pullback encoding is unresolved and belongs to the statement phase |
| Embedding rather than immersion | The source's global imbedding conclusion | Future smooth embedding predicate plus metric equality | A mere injective immersion or local isometry is expressly insufficient |
| Nearby `C^1` result | John Nash, "C1 isometric imbeddings," *Annals of Mathematics* 60(3), 1954, pp. 383-396, DOI 10.2307/1969840 | No root candidate | Exclusion anchor only: the Nash-Kuiper regularity class must not be substituted for the smooth theorem |

The Stage0 sentence "Riemannian manifolds can be isometrically embedded in Euclidean space" omits
regularity, manifold conventions, and whether a dimension bound is part of the claim. This intake
resolves that ambiguity in favor of Nash's 1956 smooth existential theorem. It does not assert that
the prose-to-Lean bridge has been kernel checked.

Discovery links (not immutable evidence receipts):

- Nash 1956: <https://doi.org/10.2307/1969989>
- Nash 1954: <https://doi.org/10.2307/1969840>

No `H0` claim is made. Source audit must acquire an immutable edition, record exact theorem and
page-level assumptions, check corrections/errata and terminology, map every premise to frozen
obligation nodes, and obtain independent review.
