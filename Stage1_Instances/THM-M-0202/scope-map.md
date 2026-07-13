# Scope map

## Preserved theorem family

The intake preserves the repository family conventionally called Brahmagupta's formula: the area
of a cyclic Euclidean quadrilateral is determined by its four side lengths through a semiperimeter
expression. A familiar candidate presentation is

```text
s = (a + b + c + d) / 2,
K = sqrt ((s - a) * (s - b) * (s - c) * (s - d)).
```

This is a scope description, not the frozen canonical proposition. The repository itself supplies
neither this formula nor definitions and assumptions that select one of its variants.

## Decisions required at statement freeze

1. Admit and independently review an immutable source edition, exact proposition, incorporated
   definitions and proof boundary, translation, historical attribution, corrections, and errata.
2. Fix the ambient domain: the Euclidean plane, an oriented two-dimensional real inner-product
   affine space, or a higher-dimensional Euclidean space with an explicit coplanarity condition.
3. Fix the quadrilateral object and boundary order. An unordered set of four cospherical points
   does not determine which distances are consecutive sides, nor whether the polygon is convex,
   simple, self-crossing, or degenerate.
4. Fix the cyclicity predicate: membership on one positive-radius circle, `Concyclic`, or
   `Cospherical` plus the required coplanarity and order transports.
5. Fix the area object: nonnegative polygon area, absolute signed shoelace/determinant area, a sum
   of two triangle areas along a selected diagonal, or a measure of the convex hull. These are not
   definitionally interchangeable.
6. Fix ordered binders and side correspondence, including cyclic rotations and reversal. For
   ordered vertices `A B C D`, decide whether `a = AB`, `b = BC`, `c = CD`, and `d = DA` and how
   every accepted permutation is transported.
7. Fix nondegeneracy: four distinct vertices in strict convex cyclic order, weak cyclic polygons
   allowing consecutive equality, or a source-selected intermediate policy.
8. Fix semiperimeter syntax, real coercions, multiplication association, and the proof that every
   factor or the complete radicand has the sign required by the selected square-root route.
9. Decide whether the root is `K = sqrt (...)`, `K^2 = (...)`, or a checked package of equivalent
   forms; fix equality orientation and every absolute-value or nonnegativity premise needed for
   transport between them.
10. Fix universes, typeclass assumptions, foundation and computation profiles, and mutation tests
    for removed hypotheses, changed domains, binder scope, and boundary cases.

## Boundary and degenerate cases

- all four vertices equal, three equal, or exactly one pair of vertices equal;
- distinct points on a zero-radius versus positive-radius circle;
- three or four collinear points and whether the chosen cyclicity definition admits them;
- self-crossing vertex orders, repeated nonconsecutive vertices, and bow-tie signed-area behavior;
- weakly convex configurations and a vertex lying on a side or diagonal;
- cyclic quadrilaterals whose limiting area is zero;
- cyclic rotations and orientation reversal of the same geometric boundary;
- higher-dimensional cospherical points that are not constrained to one affine plane;
- abstract nonnegative side quadruples that do not realize a cyclic quadrilateral;
- negative candidate factors, negative radicands outside geometric inputs, and totalized
  `Real.sqrt` behavior;
- nonnegative geometric area versus signed, absolute, determinant, triangulated, convex-hull, and
  measure encodings.

No case is excluded at intake because no exact proposition has been selected.

## Adjacent formal substrate, not credited

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Geometry.Euclidean.Sphere.Basic` defines `EuclideanGeometry.Cospherical` and
`EuclideanGeometry.Concyclic`. `Mathlib.Geometry.Euclidean.Angle.Sphere` provides
`EuclideanGeometry.Cospherical.two_zsmul_oangle_eq`, an angle relation for four cospherical
points. `Mathlib.Geometry.Euclidean.Triangle` provides triangle distance and angle identities, and
mathlib supplies exact real square-root algebra.

These interfaces authenticate possible building blocks only. They do not define an ordered cyclic
quadrilateral area, state Brahmagupta's radicand equality, or supply a target-specific reduction.
The statement phase must first encode an accepted source claim. The later anchor audit must repeat
the formal search at immutable revisions and separately assess candidate identity, provenance,
dependencies, axioms, placeholders, unsafe/oracle boundaries, and trust.

## Excluded substitutions

- Heron's triangle formula (`THM-M-0203`), even though Brahmagupta's expression specializes to a
  related three-side formula in a degenerate limiting presentation;
- Bretschneider's formula for a general quadrilateral without an accepted checked specialization
  to the cyclic case;
- Ptolemy's side-and-diagonal identity (`THM-M-0201`) or its inequality;
- only the fact that opposite angles of a cyclic quadrilateral are supplementary;
- a shoelace, determinant, triangulation, or `1 / 2 * a * b * sin gamma` area formula without the
  four-side semiperimeter equality;
- only the squared identity when the source selects nonnegative area, or only the square-root form
  when it selects a polynomial identity, unless a checked transport closes the difference;
- a rectangle, square, numeric example, plotted diagram, floating-point result, or unchecked
  symbolic normalization;
- a structure, hypothesis, axiom, oracle, or certificate that stores the desired equality;
- the catalog's `已验证` field, a citation, theorem name, API probe, or adjacent theorem used as
  source or proof credit.

## Neighbor boundaries

`THM-M-0201` separately owns Ptolemy's cyclic-quadrilateral distance-product theorem,
`THM-M-0203` Heron's triangle area formula, and `THM-M-0209` Descartes' circle-tangency curvature
theorem. The first two may become dependencies only after exact statement and obligation freezes;
the third merely shares circle vocabulary. None shares scope, state, or proof credit with this
target.
