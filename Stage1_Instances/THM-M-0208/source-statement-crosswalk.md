# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1499-1504` supplies exactly the title `维维亚尼定理`, attribution
to Vincenzo Viviani, year 1659, the gloss `等边三角形内点到三边距离之和为常数` (for an interior
point of an equilateral triangle, the sum of distances to its three sides is constant), medium
importance, and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:5779-5804` repeats the gloss but explicitly leaves the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected primary source

The licensed MPIWG/ECHO transcription of Vincenzio Viviani, *De maximis et minimis, geometrica
divinatio* (1659), identifier `ECHO:QN4GHYBF.xml`, was inspected. The exact target-family passage is
Appendix `LEMMA II. PROP. II.`, original printed pages 146-147, scan pages 332-333. The statement is
at transcription elements `echoid-s9208` and `echoid-s9209`; binders and cases are made explicit in
`echoid-s9211` through `echoid-s9216`; and the proof is `echoid-s9218` through `echoid-s9227`.

The theorem says that in any regular polygon, the sums of the perpendiculars from arbitrary points
not outside its perimeter to all its sides are equal. It explicitly chooses two arbitrary points
inside or on the perimeter. The proof joins both points to all vertices, partitions the same
polygon into two families of triangles, takes the perpendiculars as bases and the regular polygon's
equal sides as their corresponding altitudes, invokes the preceding comparison, and deduces
equality of the sums of the perpendicular bases. It separately proves that an exterior
point has a greater sum.

The catalog claim is therefore a narrower regular-triangle, strict-interior specialization of a
located primary theorem. The primary text gives point-to-point constancy, not literally equality to
the triangle altitude. The latter follows by a boundary-point specialization and is a derived
alternate form requiring an explicit transport.

The retrieved XML was 1,729,692 bytes with SHA-256
`57a438ef902213671bf06b0cac8088bfc50b10f4127f7eb0b18b0ebe16a8535e`.
Its metadata identifies Viviani, the title and year, Latin language, CC-BY-SA 3.0 licensing, and the
MPIWG Library as rights holder. `primary-source-excerpt.md` preserves attribution, the exact
locator, normalized Latin, a working translation, proof synopsis, and the source hash. A DML author
index independently cross-links the same `QN4GHYBF` holding.

This materially identifies the source and proof, but it is not yet `H0`: no independent Latin
review, critical-edition comparison, correction or errata audit, approved translation, exact
regular-polygon-to-equilateral-triangle specialization, or source-to-Lean review is accepted.

## Inspected modern source leads

Elias Abboud, *On Viviani's Theorem and its Extensions*, arXiv `0903.0753v3`, was inspected from
the versioned PDF. The abstract and introduction define the distance-sum function on the boundary
and interior of a polygon and state that equilateral triangles have the constant Viviani sum
property. The introduction gives the familiar proof boundary: joining the interior point to the
vertices decomposes the triangle into three triangles; equality of their total area with the
original area makes the sum equal to the triangle's height. Section 2.1 then defines side lengths
and the three distances for a point inside a triangle and analyzes the general distance-sum
function. The observed PDF SHA-256 was
`e00b9b38c5d7c925f1a2cf9b9e7d4aae9e3cbad0637dd01cc9deead09a5cdeab`.

Li Zhou, *Viviani Polytopes and Fermat Points*, arXiv `1008.1236v2`, was also inspected from the
versioned PDF. Its historical section says that the sum of distances from any point inside an
equilateral triangle to its sides is constant, commonly called Viviani's theorem, and identifies
Viviani's 1659 *De Maximis et Minimis* as the historical source. Zhou states that Viviani's full
result also treated regular polygons and exterior points. The modern signed-hyperplane Theorem 1
characterizes constant signed distance sums by vanishing sum of unit normals; it is useful context
but is broader than this target. The observed PDF SHA-256 was
`ee772a99068720d50e2e5703baccabca9ff22d67ac9b21e3a64555d0b30fbc22`.

These credible, versioned modern leads corroborate the candidate altitude formula and proof
architecture. They do not themselves add `H0`; the remaining primary-source specialization,
translation, correction, and independent-review gates above still apply.

## Clause crosswalk

| Catalog component | Modern-source lead | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| equilateral triangle | primary: any regular polygon; catalog: equilateral triangle | `Affine.Triangle ℝ P` plus `Affine.Simplex.Equilateral` | triangle specialization and ambient dimension open |
| interior point | primary: inside or on perimeter; catalog: interior | `p ∈ t.interior`; primary extension uses `closedInterior` | preserve strict catalog scope unless broadening is approved |
| three sides | side segments/supporting lines of the triangle | opposite face spans indexed by `Fin 3` | line-versus-segment and reindex transports open |
| distance | nonnegative perpendicular length | `|t.signedInfDist i p|` or distance to orthogonal projection | unsigned/signed encoding not selected |
| sum is constant | primary: equal at arbitrary admitted points; modern derived value: altitude | point-independence or `∑ i, |t.signedInfDist i p| = t.height j` | exact conclusion and checked altitude transport open |
| proof | decompose total area into three subtriangle areas | later area or barycentric/signed-distance proof obligations | no proof body or obligation credit at intake |
| `已验证` | untrusted inventory label | kernel and receipt gates would be required | no H0 or M0 credit |

## Pinned Lean boundary

`IntakeProbe.lean` authenticates `Affine.Triangle`, equilateralness, strict and closed interiors,
height, signed face distance, trilinear-coordinate evaluation, and absolute-distance conversion in
the pinned snapshot. `signedInfDist_affineCombination` and
`abs_signedInfDist_eq_dist_of_mem_affineSpan_range` report only `propext`, `Classical.choice`, and
`Quot.sound` through `#print axioms`. No theorem root or proof body is declared by the probe.

A bounded case-insensitive search over repository-local Lean and pinned mathlib found no exact
`Viviani` occurrence or packaged theorem relating the sum of three face distances to an altitude.
This is discovery-only feasibility evidence, not the later immutable anchor audit and not a global
absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must independently check the primary transcription and
working translation against the scan, audit critical editions and corrections, map every
incorporated definition, binder, hypothesis, conclusion, and proof step, and approve the regular-
polygon-to-strict-interior-triangle specialization. The statement phase must select point-
independence versus derived altitude equality, strict/closed interior, and
line/segment/signed-distance conventions, freeze minimal imports and an elaborated expression, and
compile all credited transports and required mutations.
