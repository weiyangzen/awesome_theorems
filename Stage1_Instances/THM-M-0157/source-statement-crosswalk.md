# Source-statement crosswalk

## Repository record and candidate sources

The repository inventory supplies only the Chinese title "Gauss map theorem", attribution to Carl
Friedrich Gauss, the year 1827, and the gloss "properties of the Gauss map of a surface". Its
`已验证` field is explicitly untrusted under rev-5.6. It gives no theorem locator, regularity,
orientation, local/global scope, or conclusion, so it cannot identify an exact proposition.

A historical primary-source candidate is Carl Friedrich Gauss, *Disquisitiones generales circa
superficies curvas* (1827). This is a discovery anchor consistent with the inventory attribution and
date, not `H0` evidence. An immutable edition and translation must be inspected to determine whether
the intended modern Gauss-map formulation is stated there directly or is a later reformulation, and
to record an exact section/page, definitions, assumptions, and corrections.

A modern source candidate for disambiguation is Manfredo P. do Carmo, *Differential Geometry of
Curves and Surfaces*, in the chapter material on the Gauss map and its differential. It can clarify
modern sign and regularity conventions, but it must not silently replace the historical source.
Exact edition, theorem/page, wording, and errata remain open. Both entries are discovery anchors
rather than reviewed proof evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "surface" | regular parametrized, embedded, or immersed oriented surface in Euclidean three-space | manifold/patch, immersion derivative, Euclidean orientation | family identified; encoding open |
| "Gauss map" | chosen unit normal as a map to the unit sphere | normal field, sphere-valued map, coercion to ambient space | intended object identified; local/global choice open |
| differential property | derivative of the normal map and its tangent endomorphism | Fréchet/manifold derivative and tangent-space identification | candidate local conclusion; sign convention open |
| shape operator | negative or positive differential according to convention | linear endomorphism with convention made explicit | related formulation; exact root status open |
| Gaussian curvature | determinant of the shape operator/Gauss-map derivative | finite-dimensional determinant and curvature definition | candidate consequence; orientation convention open |
| 1827 / Gauss | historical attribution and source locator | no machine-proof credit | candidate work identified; exact locator open |

## Human and machine boundary

The repository-wide name search found no theorem-specific Lean artifact for `THM-M-0157`. A narrow
text search of the pinned mathlib tree found no declaration named for a Gauss map, shape operator,
or Weingarten map; this is only intake discovery and not the later exhaustive anchor audit.

Before `H0`, an independent reviewer must inspect an immutable primary edition, select the exact
proposition, record its section/page and translation, map every hypothesis and convention, check
errata or later corrections, and approve the row-by-row source mapping. Before statement credit,
the selected claim must map to an elaborated Lean target without changing local/global scope,
dropping orientability or regularity, choosing a convenient sign silently, or replacing the theorem
with a special surface computation.
