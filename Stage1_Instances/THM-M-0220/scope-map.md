# Scope map

## Included theorem family

- A source-selected hyperbolic plane or constant-negative-curvature surface.
- A source-selected geodesic triangle in that geometry.
- The exact relationship between the triangle's hyperbolic area and its angle defect.
- The definitions, normalization, assumptions, and boundary cases needed to make that relationship
  a single truth-valued proposition.

These bullets delimit the recognizable classical family. They are not an accepted canonical
statement.

## Decisions required at statement freeze

1. Select and independently inspect an immutable primary or authoritative source with exact
   theorem, definition, page, assumption, proof-boundary, correction, and errata locators.
2. Freeze the ambient geometry: upper half-plane, disk, another analytic model, or an abstract
   complete simply connected surface of constant curvature.
3. Freeze metric scale and curvature. For curvature `K = -k^2`, a common formula is
   `Area(T) = (pi - (alpha + beta + gamma)) / k^2`; the normalized `K = -1` formula is a special
   case, not a notation-only rewrite.
4. Define a geodesic triangle, including whether vertices and edges are ordered and whether the
   enclosed region, boundary, and chosen side are part of its data.
5. Select finite triangles only, or include ideal and partially ideal vertices. Ideal angles and
   infinite-distance boundary points require definitions absent from the catalog.
6. Freeze the area object: Riemannian volume, the upper-half-plane invariant measure, a model-
   transported measure, or signed/oriented area, and prove any equality between encodings.
7. Freeze the interior-angle predicate, radians, angle representatives, tangent directions,
   orientation, and conformal-model bridge. Euclidean angle vocabulary alone is not that bridge.
8. Decide whether the result is an unsigned equality, an oriented equality, an absolute-value
   formula, or a statement about the measure of a region.
9. Resolve repeated vertices, collinear geodesics, zero-area triangles, angle `0` or `pi`, boundary
   and ideal points, self-intersection, orientation reversal, and nonmeasurable encodings.
10. Freeze ordered binders, universes, structures, coercions, hypotheses, conclusion, and every
    credited alternate encoding before proof search.

## Explicit exclusions

- Silently choosing curvature `-1` or deleting the curvature-scale factor.
- Replacing this result with the Euclidean angle-sum theorem, a spherical excess formula, a disk
  or half-plane construction theorem, a hyperbolic cosine law, or a polygon-area formula.
- Substituting the separately cataloged general Gauss-Bonnet targets, including `THM-M-0216`,
  without a checked specialization and source-identity decision.
- Substituting model targets `THM-M-0217`, `THM-M-0218`, or `THM-M-0219`; a model transport must be
  stated and kernel checked before it receives credit.
- Treating `UpperHalfPlane.dist_eq`, `UpperHalfPlane.volume_def`, generic Euclidean angle APIs, or a
  numerical area calculation as the requested theorem.
- Packaging the desired identity as an input structure field or hypothesis and projecting it.
- Treating the catalog's `已验证` label or the API-only intake probe as H or M evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the upper-half-plane modules provide a Poincare
metric and the invariant measure `dx dy / y^2`. Mathlib's Euclidean geometry provides angle
vocabulary, but the intake found no checked hyperbolic geodesic triangle, hyperbolic interior-angle
bridge, curvature normalization, or terminal area-defect theorem. These are adjacent feasibility
surfaces only. They do not determine minimal imports for the absent canonical target.
