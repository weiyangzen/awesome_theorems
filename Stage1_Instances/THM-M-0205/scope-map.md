# Scope map

## Preserved theorem family

The intake preserves exactly the classical Morley trisector family named by the catalog: for a
Euclidean triangle, selected intersections of its angle trisectors form an equilateral triangle.
Taylor and Marr's inspected Section 2 formulation identifies the conventional internal result by
choosing, for each side, the two trisectors adjacent to that side. This is a strong candidate scope,
not yet the frozen canonical proposition.

## Proposition-changing decisions

An accepted statement run must decide all of the following from an immutable reviewed source:

1. The ambient object: a two-dimensional oriented Euclidean affine space, `R^2` coordinates, or
   another exact plane model, including universes and typeclass assumptions.
2. The triangle predicate and orientation: three distinct noncollinear vertices, an ordered
   counterclockwise triple, a simplex, or explicit side/interior data.
3. What a trisector is: an internal ray, a point on a segment/inside the triangle, a full line, an
   oriented direction, or a predicate given only by angle equalities.
4. Which of the two internal trisectors at each vertex is adjacent to which side, and how that
   adjacency is expressed without silently accepting external rays or the supplementary angle.
5. Whether the three intersection points are constructed from unique nonparallel lines or are
   existential witnesses satisfying incidence and ray constraints.
6. The names and cyclic order of the intersection points `D`, `E`, `F`, matching the side-adjacent
   pairs in the chosen source.
7. The equilateral conclusion: all three side distances equal, a congruence predicate, or all three
   angles equal to `pi / 3`, together with checked transports for any alternate form.
8. Every ordered binder, hypothesis, conclusion, foundation/choice policy, and proof boundary.

These choices change the proposition or its trust boundary. Intake does not choose among them.

## Boundary and degenerate cases

Source review must explicitly address collinear or repeated input vertices; zero or straight
vertex angles; orientation reversal; an isosceles or already equilateral input triangle; a chosen
trisector point equal to a vertex; internal rays represented by full lines and thereby admitting
the opposite ray; parallel or coincident selected lines; nonunique intersections; coincident
`D`, `E`, or `F`; and whether an equilateral conclusion must itself include nondegeneracy.

The statement must also distinguish the six interior trisector rays from the larger family of
supporting lines and external trisectors. No boundary case is excluded at intake because no exact
proposition has been selected.

## Excluded substitutions

- The full 27-intersection/internal-and-external Morley configuration cannot replace the first
  internal Morley triangle named by the short catalog gloss without a source-approved scope change.
- A claim about arbitrary triples of trisectors, or three intersections not tied to side-adjacent
  pairs, is not the theorem.
- Angle bisection, incenter concurrency, Ceva's theorem, Napoleon's theorem, an equiangular-line
  configuration, or another equilateral-triangle construction cannot replace Morley's theorem.
- An equiangular conclusion cannot be identified with equal side lengths without the required
  nondegeneracy and a checked transport.
- A theorem for one numeric triangle, one orientation, only acute triangles, only equilateral or
  isosceles triangles, or only coordinate-normalized inputs is not the universal source target.
- A structure or hypothesis storing the trisector intersections, their equilateral property, or
  the desired side equalities supplies no proof.
- A diagram, numerical trigonometric check, theorem name, API probe, citation, or the catalog's
  untrusted `已验证` label supplies no H or M credit.

## Neighbor and name boundaries

`THM-M-0207` owns Napoleon's theorem, another construction of equilateral triangles from a source
triangle. `THM-M-0656` is Michael Morley's categoricity theorem in model theory. Neither can supply
inherited scope or status. Other triangle, angle, concurrency, and equilateral results may later be
explicit dependencies only after statement and obligation freeze.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks affine angle, triangle
angle-sum, law-of-sines, equal-side/equal-angle, collinearity, betweenness, and congruence APIs.
There is no credited trisector definition or Morley root. The bounded search is scoped discovery,
not an exhaustive anchor audit or proof of global absence.
