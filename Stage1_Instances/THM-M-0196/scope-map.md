# Scope map

## Preserved theorem family

- Target: `THM-M-0196`, named `九点圆定理` (nine-point circle theorem).
- Catalog attribution and date: Karl Wilhelm Feuerbach, 1822.
- Literal gloss: `三角形九点共圆` ("the nine points of a triangle are concyclic").
- Conventional candidate reading: one circle contains the three side midpoints, the three
  midpoints between vertices and the orthocenter, and the three altitude feet of a Euclidean
  triangle.

The final bullet disambiguates the named theorem for planning only. The catalog does not define the
nine points or cite a source that selects this formulation.

## Decisions required at statement freeze

An immutable, independently reviewed source must decide all of the following before a canonical
Lean expression may be credited:

1. Whether a triangle is three distinct noncollinear points, an affine-independent
   `Affine.Triangle`, or another equivalent structure, and the exact ambient Euclidean dimension.
2. Whether "the nine points" are exactly the three side midpoints, three vertex-orthocenter
   midpoints, and three altitude feet, including how repeated coincidences in special triangles are
   treated.
3. Whether the conclusion exhibits a circle, asserts membership in a specified nine-point circle,
   asserts equality with the medial triangle's circumcircle, or uses an abstract concyclicity
   predicate, and which transports between these forms are required.
4. The definition of the orthocenter and each altitude foot, plus the indexing correspondence
   between a vertex and its opposite side.
5. Whether the theorem is a conjunction of three indexed membership families, a set-containment
   statement, or a cardinality-sensitive claim about nine distinct points.
6. Exact ordered binders, universes, typeclass assumptions, foundation profile, conclusion, and
   every alternate encoding with a checked relationship.

## Degenerate and boundary cases

The classical theorem normally assumes a nondegenerate triangle. A collinear or repeated-vertex
triple may have no uniquely determined ordinary circumcircle or orthocenter. In an equilateral,
isosceles, or right triangle, some of the conventional nine constructed points can coincide; the
incidence theorem can still make sense while a statement asserting nine distinct points becomes
false. An ambient affine space may have dimension greater than two even though the triangle spans a
plane. These cases must be mapped from the selected source rather than silently excluded or added.

Mathlib's `Affine.Triangle` is an affine-independent 2-simplex, so it already encodes a
nondegeneracy boundary. Its `Sphere` formulation lives in an arbitrary real inner-product affine
space, not only a coordinate copy of the plane. Those are promising encoding choices, not yet an
accepted source transport.

## Explicit exclusions

- Feuerbach's theorem that the nine-point circle is tangent to the incircle and excircles is a
  different theorem despite sharing Feuerbach's name.
- The Euler-line theorem about orthocenter, centroid, and circumcenter does not by itself prove all
  nine incidences.
- The higher-dimensional `3(n+1)`-point sphere of a simplex is a generalization, not a substitute
  for the triangle root.
- A result proving only the three side midpoints, only the three altitude feet, or only the three
  vertex-orthocenter midpoints is partial coverage, not the nine-point theorem.
- A theorem for only acute, right, isosceles, or equilateral triangles cannot replace the general
  nondegenerate-triangle claim.
- A structure field, premise, or definition that assumes the desired circle memberships supplies no
  proof.
- A diagram, numerical coordinate check, theorem-name match, `#check`, or the catalog's `已验证`
  label supplies no H or M completion credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the exact-topic module
defines `Affine.Simplex.ninePointCircle` and exposes separate membership results for all three
families. Intake records them as candidates only. The dependent statement phase must select and
fingerprint one source-faithful root; the anchor audit must then classify exact-body provenance and
trust without counting three families, wrappers, or transports as duplicate root proof credit.
