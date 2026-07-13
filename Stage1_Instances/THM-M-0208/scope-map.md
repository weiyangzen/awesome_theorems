# Scope map

## Preserved repository scope

- Target: `THM-M-0208`, `维维亚尼定理` (Viviani's theorem).
- Catalog attribution and date: Vincenzo Viviani, 1659.
- Literal gloss: `等边三角形内点到三边距离之和为常数`.
- Subject: Euclidean geometry of an equilateral triangle and distances from an interior point to
  its three sides.

The importance and `已验证` fields are catalog metadata. The repository supplies no bibliography,
formula, definitions, binders, hypotheses, conclusion, proof, correction record, or formal link.

## Candidate classical form, not credited

For an equilateral triangle with altitude `h` and a point `P` inside it, let `p_a`, `p_b`, and
`p_c` be the nonnegative perpendicular distances from `P` to its three side lines. The standard
form is

```text
p_a + p_b + p_c = h.
```

The inspected modern leads justify retaining this as a useful alternate-form candidate. The 1659
primary theorem states equality between sums at arbitrary admitted points, not equality to an
altitude. The altitude value is derived by specializing to a triangle and comparing with a boundary
point. The catalog itself only says that the sum is constant, so this transport, the exact distance
object, and scope remain statement-phase decisions rather than frozen intake facts.

## Proposition-changing decisions

1. Independently review the preserved primary locator and working translation, decide whether the
   catalog root is literal point-independence or the derived altitude equality, and accept an exact
   source-to-target specialization and proof boundary.
2. Fix an ordered nondegenerate equilateral triangle in the Euclidean plane, or specify and justify
   a dimension-independent affine-simplex formulation inside its two-dimensional affine span.
3. Preserve the catalog's strict-interior scope or explicitly approve the primary source's broader
   closed-region scope. The broader result cannot be inherited silently.
4. Decide whether a side means the finite segment, its supporting affine line, or the opposite
   face span. For an interior point the numerical distances coincide, but the Lean propositions and
   boundary transports differ.
5. Choose unsigned metric distance, absolute signed distance, or consistently oriented signed
   distance, and check every conversion.
6. Decide whether the conclusion is equality to one selected altitude, to every equal altitude,
   or existence of a constant independent of the point.
7. Freeze ordered binders, universes, typeclasses, coercions, quantifier scope, hypotheses, and the
   exact conclusion, then compile transports for every credited alternate encoding.
8. Resolve repeated or collinear vertices, points on a side or vertex, points outside the triangle,
   orientation reversal, vertex reindexing, zero side length, and zero-dimensional ambient cases.

## Formal candidates and boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the closest interface is
an `Affine.Triangle ℝ P`, already affinely independent by construction, with:

- `Affine.Simplex.Equilateral` for equal edge lengths;
- `Affine.Simplex.interior` and `closedInterior` for strict and closed barycentric interiors;
- `Affine.Simplex.signedInfDist` for signed distances to opposite face spans;
- `signedInfDist_affineCombination` for trilinear-coordinate evaluation;
- `abs_signedInfDist_eq_dist_of_mem_affineSpan_range` for metric-distance conversion; and
- `Affine.Simplex.height` for vertex-to-opposite-face altitude length.

These ingredients make a later exact statement plausible and justify provisional `M3`. They do not
package the three-distance sum, prove equality of the three heights from equilateralness, choose an
interior convention, or provide a source transport. A bounded search found no named Viviani or
sum-of-side-distances theorem. This is intake discovery only, not an exhaustive anchor audit.

## Excluded substitutions

- A theorem for arbitrary polygons, regular polygons, polyhedra, or oriented hyperplane families is
  an extension, not the triangle root.
- The converse characterizing equilateral triangles by constant distance sum is a distinct theorem.
- A formula for signed distances at every ambient point is not silently interchangeable with the
  unsigned interior-point theorem.
- A coordinate theorem in `ℝ × ℝ`, a theorem only at the centroid or incenter, or a numerical
  diagram is not the unrestricted affine theorem.
- The sum of distances to the three vertices, the Fermat point theorem, triangle area decomposition,
  or an altitude theorem alone is not Viviani's conclusion.
- A premise or structure field assuming the desired sum, a theorem name, URL, `#check`, API
  signature, catalog label, or source abstract supplies no proof credit.

## Neighbor boundaries

`THM-M-0197` separately owns the Fermat point theorem; `THM-M-0203` owns Heron's formula;
`THM-M-0204` owns Stewart's theorem; and `THM-M-0207` owns Napoleon's theorem. Their geometry may
later provide definitions or proof ingredients, but no neighboring target grants scope or proof
credit here.
