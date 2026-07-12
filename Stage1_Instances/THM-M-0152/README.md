# THM-M-0152 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for Gauss's *Theorema Egregium*. The canonical
human claim is that a local isometry between smooth regular surfaces in Euclidean three-space
preserves Gaussian curvature pointwise. Equivalently, Gaussian curvature is determined by the
first fundamental form rather than by the chosen isometric embedding.

## Scope summary

The target concerns the pointwise curvature invariant, not Gauss-Bonnet, total curvature, mean
curvature, rigidity of embeddings, or the converse existence of an isometric bending. Orientation
is not part of the result. Regularity and the local-isometry hypothesis are essential parts of the
claim; a merely continuous, area-preserving, or angle-preserving map is outside its scope.

The primary-source anchor is Gauss's 1827 *Disquisitiones generales circa superficies curvas*,
Articles 11-12. Article 11 expresses the curvature measure using only the metric coefficients
`E`, `F`, `G` and their first and second derivatives. Article 12 concludes that development of one
surface on another preserves curvature at corresponding points. The detailed mapping is in
`source-statement-crosswalk.md`.

No exact Lean declaration is credited at intake. A repo-local search of the pinned mathlib source
found no Gaussian-curvature, sectional-curvature, or local-isometry API suitable for naming a
formal target. The dependent statement phase must therefore select definitions, imports, ordered
binders, and regularity assumptions, elaborate the expression, and check that it represents this
claim without replacing it by a formula-only surrogate.

The provisional root vector is `[H1, M4, R3]`. This intake freezes scope and opens the downstream
task graph only; it does not pass the statement gate, accept the repository's untrusted
`已验证` label, or claim proof, audit, or theorem completion.

