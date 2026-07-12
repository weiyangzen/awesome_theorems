# Source-statement crosswalk

## Primary source

David Hilbert, "Ueber Flächen von constanter Gaussscher Krümmung," *Transactions
of the American Mathematical Society* **2** (1901), no. 1, 87-99,
DOI `10.1090/S0002-9947-1901-1500557-5`. The paper says it was presented on
1900-10-27 and received on 1900-10-09.

For discovery validation, the AMS version-of-record PDF was retrieved on 2026-07-12 from the DOI
landing infrastructure. Its SHA-256 was
`7cd418f655153b1651927e39b4e9f54c3278d90254a38787c93724be58b51b98`; PDF metadata reports 13
pages. The PDF is not vendored, and the digest is discovery provenance rather than an immutable
repository source receipt. No errata search or independent source review has been accepted.

## Crosswalk

| Repository/source component | Primary-source anchor | Proposed formal component | Intake assessment |
|---|---|---|---|
| Constant negative curvature | Printed p. 87 begins with an analytic surface of constant curvature `-1`; local normal form has principal-curvature product fixed by `4ab = -1` | `sectionalCurvature = -1` on a two-dimensional Riemannian manifold | Strong semantic match; sign conventions and the Lean curvature API remain open |
| Global nonsingularity/regularity | Printed pp. 87-88 assumes an analytic surface regular everywhere in finite space and without singular points | Selected differentiability class for `M`, its metric, and `f` | Not yet identical: Hilbert states analytic regularity, while the repository wording omits regularity |
| Global completeness condition | Printed p. 87 requires every finite accumulation point of surface points also to be a surface point; pp. 90-91 use indefinite continuation of asymptotic curves | metric/geodesic completeness of `M` | The modern completeness bridge is plausible but unproved and is the first statement blocker |
| Immersion in Euclidean three-space | The paper treats the surface via analytic coordinate functions `x(u,v), y(u,v), z(u,v)` and its first fundamental form (printed pp. 88-90) | immersion `f : M -> EuclideanSpace Real (Fin 3)` with pullback Euclidean metric equal to `g` | Modern invariant encoding candidate; exact correspondence to Hilbert's surface model requires review |
| Global asymptotic-coordinate argument | Printed pp. 91-96 proves properties 1-4 for the two families of asymptotic curves and concludes the `uv` parametrization is globally one-to-one and the surface simply connected | explicit global-coordinate/topology obligations | Proof-architecture scope only; no formal closure |
| Finite area | Printed p. 96 uses asymptotic quadrilaterals and their angle sum to bound total area by `2*pi` (the OCR text renders the limiting equality ambiguously) | finite-area branch | The exact inequality/limit statement must be checked against the typeset formula before freezing obligations |
| Infinite area | Printed pp. 96-97 uses geodesic disks and Lobachevskian area growth to force unbounded total area | geodesic-disk area branch | Source proof node located; all analytic and global prerequisites remain open |
| Nonexistence conclusion | Printed p. 97 rejects the basic assumption: no singularity-free, everywhere regular analytic surface of constant negative curvature; in particular the whole Lobachevskian plane has no regular analytic realization in space | `¬ ∃ f, IsometricImmersion f` under the selected complete constant-curvature hypotheses | Same theorem family, but not yet an exact checked source-to-modern-statement identity |

## Statement decisions still required

1. Freeze whether the canonical theorem follows Hilbert's analytic surface formulation or a modern
   `C^2`/smooth complete Riemannian formulation, with a primary-source theorem for any strengthening.
2. State connectedness, boundarylessness, dimension, manifold regularity, immersion regularity,
   and metric versus geodesic completeness explicitly.
3. Decide whether curvature is normalized to `-1` or universally quantified over `K < 0`; any
   scaling transport must be kernel checked before it receives credit.
4. Identify the exact Lean encodings of Gaussian/sectional curvature, pullback metrics,
   completeness, and immersion, or record missing pinned APIs as blockers.
5. Audit translations, later regularity improvements, errata, and an independent source reading
   before raising `H1` to `H0`.

The source is a genuine human proof anchor, but this crosswalk intentionally makes no `H0`, Lean
elaboration, formal-anchor, or theorem-completion claim.
