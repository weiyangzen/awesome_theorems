# Scope map

## Preserved repository scope

- Target: `THM-M-0198`, named `西姆松线定理` (Simson line theorem).
- Catalog attribution and date: Robert Simson, 1756.
- Literal gloss: `三角形外接圆上一点在三边的投影共线`.
- Direction preserved: a point on the circumcircle implies collinearity of three projections.

The final bullet matters: the repository does not state the converse or an if-and-only-if theorem.
The importance and `已验证` fields are inventory metadata, not source or proof evidence.

## Proposition-changing decisions

An immutable, independently reviewed source must fix all of the following before a canonical Lean
expression may be credited:

1. Whether the ambient domain is the Euclidean plane, an explicitly two-dimensional real affine
   inner-product space, a coordinate copy of `R^2`, or a higher-dimensional generalization with the
   point constrained to the triangle's affine plane.
2. Whether a triangle is three pairwise distinct noncollinear points, an affine-independent
   `Affine.Triangle`, or another source-faithful structure, including ordered vertex indexing.
3. Whether the circumcircle is the unique circle in the triangle's plane, mathlib's circumsphere,
   an equidistance predicate, or an existential circle, and the checked relationship between any
   credited encodings.
4. Whether the quantified point may equal a vertex and whether it must lie in the affine span of
   the triangle in an ambient space of dimension greater than two.
5. Whether each "side" means the entire affine line through two vertices, the closed side segment,
   or a directed extension. The conventional theorem uses supporting lines; projections need not
   lie in the three closed segments.
6. How each perpendicular foot is represented: orthogonal projection onto the opposite side's
   affine span, an existential point with incidence and perpendicularity, or coordinates, and how
   the three feet are indexed.
7. Whether collinearity is `Collinear Real` on a three-point set or range, membership in one affine
   line, an affine-dependence condition, or a determinant identity, with checked transports.
8. The exact ordered binders, universes, typeclass assumptions, hypotheses, conclusion,
   foundation/TCB/computation profiles, and every alternate encoding and mutation boundary.

These choices change the proposition or its proof boundary. This list is a resolution ledger, not
a theorem statement.

## Degenerate and boundary cases

The statement phase must explicitly resolve repeated or collinear vertices; zero-area triangles;
a circle point equal to a vertex; acute, right, and obtuse triangles; projections that fall on side
extensions rather than segments; coincident projection feet in boundary configurations; zero-,
one-, two-, and higher-dimensional ambient spaces; vertex reindexing; and orientations of any
coordinate or determinant formulation. No case is excluded at intake.

Mathlib's `Affine.Triangle` already encodes affine independence of its three vertices. Its
`circumsphere` and side-span projections live in an arbitrary real inner-product affine torsor.
Those are feasible candidate encodings, not an accepted decision that the catalog intended the
higher-dimensional formulation.

## Explicit exclusions

- The converse, saying pedal-point collinearity implies that the point is on the circumcircle, is
  not part of the literal forward gloss and cannot be silently added.
- An if-and-only-if Wallace-Simson theorem is stronger than the received statement.
- Projection onto the three closed side segments cannot replace projection onto the supporting
  side lines without source evidence; it can fail to describe exterior feet.
- A theorem only for acute, right, isosceles, equilateral, coordinate-normalized, or otherwise
  specialized triangles is not the general classical family.
- The nine-point-circle theorem, pedal-circle results, orthocenter results, Menelaus, Ceva, and
  Ptolemy are neighboring geometry, not substitutes.
- A structure field, premise, diagram, numerical example, theorem-name match, generic `#check`, or
  the catalog's `已验证` label supplies no H or M completion credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the candidate vocabulary
includes `Affine.Triangle`, `Affine.Simplex.circumsphere`,
`Affine.Simplex.orthogonalProjectionSpan`, and `Collinear`. A bounded search found no exact Simson,
Wallace-Simson, or pedal-line declaration. This is scoped intake discovery, not an exhaustive
anchor audit or a global absence claim.
