# Source-statement crosswalk

## Source identity

The repository record is `Docs/researches/math_theorems.md`, lines 1105-1110: Gauss, 1827,
"Gaussian curvature is an intrinsic geometric quantity." That one-line status is untrusted
metadata rather than formal or source evidence.

The primary mathematical work is C. F. Gauss, *Disquisitiones generales circa superficies
curvas* (1827), Articles 11-12. Intake consulted J. C. Morehead and A. M. Hiltebeitel,
*General Investigations of Curved Surfaces* (Princeton University Library, 1902), Project Gutenberg
ebook 36856, downloaded from `https://www.gutenberg.org/files/36856/36856-pdf.pdf`. The consulted
PDF has SHA-256
`ad6f34e6068860a37af65ffb906e55b699c184038b30aa37d87f06a866480f20`.

## Claim mapping

| Claim component | Primary-source anchor | Canonical modern component | Intake assessment |
|---|---|---|---|
| Surface metric data | Article 11 defines `E`, `F`, `G` from a regular parametrized surface and uses `EG - F^2` | Induced first fundamental form on a regular surface | Direct conceptual match; a Lean regularity predicate is not yet selected |
| Intrinsic formula | Article 11 derives a curvature formula involving only `E`, `F`, `G` and their first and second derivatives | Gaussian curvature is determined locally by metric data | Primary formula route identified; detailed symbol-by-symbol transcription is later proof/source audit work |
| Isometric correspondence | Article 12 assumes one surface is "developed upon" another and notes equality `E = E'`, `F = F'`, `G = G'` | Smooth local isometry preserves the first fundamental form | Modern local-isometry wording captures the local mathematical content; formal equivalence must be checked |
| Pointwise invariant | Article 12: "the measure of curvature in each point remains unchanged" | `K_T (f p) = K_S p` | Exact conclusion match at the human level |
| Integral curvature | Article 12 also says a finite part retains integral curvature | Excluded from this root | Related corollary, not silently conjoined with the pointwise theorem |
| Developable plane case | Article 12 concludes curvature is zero for surfaces developable on a plane | Excluded consequence | Useful later mutation/example, not the root statement |

Gauss's "measure of curvature" is the quantity now called Gaussian curvature. Article 12 obtains
the invariance conclusion from the Article 11 metric formula. The canonical root uses the standard
modern local-isometry formulation and preserves the source's pointwise conclusion. It does not
claim invariance of extrinsic curvatures or a converse.

## Lean crosswalk

| Human component | Required Lean concept | Intake result |
|---|---|---|
| Regular surface in Euclidean three-space | Immersion or embedded two-manifold with induced Riemannian metric | Concrete representation open |
| Gaussian curvature | Extrinsic determinant of the shape operator or intrinsic two-dimensional sectional curvature | Concrete definition and bridge open |
| Development/local isometry | Bundled local isometry or pullback equality of induced metrics | Concrete API open |
| Pointwise preservation | Equality after evaluation at `p` and `f p` | No declaration or elaborated expression credited |

A bounded case-insensitive search of the pinned mathlib source for `gaussian curvature`,
`gauss curvature`, `sectional curvature`, and `local isometr` returned no relevant geometry API.
This negative discovery result is not a claim that no external formalization exists. External and
broader candidate discovery belongs to the anchor-audit phase after an exact Lean statement is
frozen.

## Open source gates

The translation file is content-identified and Articles 11-12 are pinpointed, supporting
provisional `H1`. `H0` is not claimed: the original Latin edition has not been independently
collated, correction and errata history has not been audited, every analytic regularity premise has
not been mapped to formal binders, and no independent reviewer has signed the crosswalk.

