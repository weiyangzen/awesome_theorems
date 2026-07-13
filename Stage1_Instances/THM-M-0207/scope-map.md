# Scope map

## Preserved theorem family

The intake preserves the catalog's external Napoleon-theorem family: start with one triangle,
construct one equilateral triangle externally on each side, select the corresponding three centers,
and assert that those centers form an equilateral triangle. It does not substitute the internal
variant, a statement about areas or orientation, or a coordinate identity detached from the stated
construction.

This paragraph identifies the family only. It is not an accepted canonical proposition.

## Decisions required at statement freeze

1. Admit and independently review an immutable primary or authoritative source with an exact
   theorem/page, incorporated definitions, proof boundary, translation, corrections, and errata.
2. Fix the ambient model: the Euclidean plane, `Complex`, a two-dimensional oriented real
   inner-product space, or an affine torsor with an explicitly supplied orientation.
3. Fix the input representation and nondegeneracy assumptions: ordered points, an affinely
   independent `Affine.Triangle`, or a weaker triple that permits collinearity or repeated points.
4. Define "external" relative to the oriented input triangle or its opposite-side open half-plane.
   Reversing vertex order must not silently change which third vertex is selected on a side.
5. Specify the side-to-triangle correspondence and ordered vertices for all three equilateral
   constructions, including whether each side endpoint order is significant.
6. Define "center." Centroid, circumcenter, incenter, and orthocenter coincide for a nondegenerate
   equilateral triangle, but that equivalence is mathematical proof work, not a license to leave the
   term unspecified.
7. Fix the conclusion encoding: an `Affine.Triangle` with `Equilateral`, three pairwise distance
   equalities, or a coordinate identity, together with checked transports for credited alternates.
8. Freeze ordered binders, universes, inferred structures, foundation/TCB/computation profiles,
   exact hypotheses and conclusion, minimal imports, and every boundary decision before hashing or
   proof search.

## Boundary cases to resolve

- coincident or collinear input vertices and zero-area triangles;
- side length zero and failure or nonuniqueness of an external equilateral construction;
- clockwise versus counterclockwise input ordering;
- the two possible equilateral third vertices on each supporting line;
- whether "outside" uses open half-planes, closed half-planes, signed area, or orientation;
- coincident constructed centers or a degenerate output triple;
- a two-dimensional plane embedded in a higher-dimensional Euclidean space;
- centroid versus other classical centers and any equality proof used to transport between them;
- internal, external, mixed-orientation, and reflected construction variants.

No case is excluded at intake because no exact source proposition has been accepted.

## Excluded substitutions

- The internal Napoleon theorem, or a conjunction of internal and external variants.
- A theorem assuming the three selected centers are already equilateral.
- Only the fact that an input or constructed triangle is equilateral.
- Only a centroid formula, a 60-degree rotation identity, or equality of three distances without a
  checked mapping to the source construction.
- A numerical diagram, coordinate experiment, floating-point check, or generated certificate.
- A theorem for three arbitrary equilateral triangles without the source-required side attachment
  and outward orientation.
- The catalog's `已验证` label, a theorem-name match, or a passing API probe as H0 or M0 evidence.

## Neighbor and ownership boundaries

`THM-M-0205` owns Morley's theorem, `THM-M-0206` owns van Aubel's theorem, and `THM-M-0208` owns
Viviani's theorem. Similar use of equilateral triangles, centers, or distance equalities does not
transfer statement or proof credit between targets.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.Geometry.Euclidean.Simplex` provides
`Affine.Triangle`, `Affine.Simplex.Equilateral`, centroid interfaces, and elementary consequences
of equilateralness. A bounded repository and pinned-mathlib search found no exact Napoleon theorem
or construction of outward equilateral triangles. This is an intake discovery boundary, not an
exhaustive anchor audit or a global absence theorem.
