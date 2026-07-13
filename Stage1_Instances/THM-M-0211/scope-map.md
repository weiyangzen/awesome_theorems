# Scope map

## Preserved repository scope

- Target: `THM-M-0211`, named `帕斯卡定理` (Pascal's theorem).
- Attribution and date: Blaise Pascal, 1640.
- Literal gloss: `圆锥曲线内接六边形的共线性质`.
- Intended family: a conic, an ordered inscribed hexagon, three intersections of pairs of opposite
  sides, and a collinearity conclusion.

The repository supplies no bibliography, definitions, binders, hypotheses, or exact conclusion.
Its importance and `已验证` fields are inventory metadata only.

## Candidate semantic reading, not credited

A standard forward reading places ordered points `a,b,c,d,e,f` on a conic in a projective plane
and concludes that `ab ∩ de`, `bc ∩ ef`, and `cd ∩ fa` are collinear. This is only a discovery
model. It does not decide the field, conic or incidence encoding, whether the conic is nonsingular,
whether vertices may repeat, how tangent sides arise, which intersections must be well-defined, or
whether the converse is part of the target.

## Proposition-changing decisions

An approved statement run must freeze all of the following from an immutable reviewed source:

- a synthetic projective-plane axiom system versus `P(K^3)` or another coordinatized model;
- the scalar field and characteristic hypotheses, including whether real, complex, algebraically
  closed, or arbitrary fields are intended;
- a conic as the projective zero locus of a quadratic form, a rational normal curve, or a synthetic
  object, together with smoothness, irreducibility, and nondegeneracy requirements;
- an ordered sextuple and the exact cyclic order used to form sides and opposite-side pairs;
- whether the six vertices are pairwise distinct, in general position, or may coincide;
- whether a repeated adjacent pair denotes a tangent, and the differentiability or algebraic
  definition of that tangent;
- the line-through-two-points and line-intersection encodings, including required inequalities so
  coincident lines do not turn a chosen total operation into a fake intersection;
- projective collinearity as containment in a projective line, linear dependence of homogeneous
  representatives, or a determinant equation, with checked transports between credited forms;
- forward Pascal only, its converse, or an explicit equivalence, and whether degenerate conics are
  included;
- ordered binders, every hypothesis and conclusion, foundation and choice policy, and the mutation
  behavior of all excluded cases.

## Boundary and degenerate cases

- In an affine rendering, opposite sides may be parallel; projective completion supplies an ideal
  intersection, while an affine-only theorem requires a separate exclusion or transport.
- Coincident opposite sides do not determine a unique intersection point. Mathlib's total
  `Projectivization.cross` returns an input on equality, so distinctness hypotheses are semantic,
  not cosmetic.
- Repeated adjacent vertices require a tangent convention; without it, a side is not determined.
- Repeated nonadjacent vertices can make opposite sides or their intersections coincide.
- Three equal intersection points, two equal points, or otherwise degenerate collinearity may make
  a broad formulation trivially true while the intended Pascal line is not uniquely determined.
- A reducible conic can recover a Pappus configuration, but sources differ on whether it belongs to
  Pascal's theorem or is a separate degeneration.
- In characteristic two, quadratic-form and conic conventions can differ materially; no field case
  is admitted by default.

No boundary case is excluded at intake because no proposition has been selected.

## Neighbor and substitution boundaries

- `THM-M-0210` (Desargues) is a different incidence theorem about perspective triangles.
- `THM-M-0212` (Brianchon) is the projective dual theorem for a circumscribed hexagon and is not a
  proof or alternate encoding of this target without an explicit checked duality transport.
- Pappus, Braikenridge-Maclaurin, Cayley-Bacharach, higher-dimensional rational-normal-curve
  generalizations, and Pascal-line coincidence or degeneration results are not substitutes.
- A coordinate determinant identity, generic projective incidence API, affine `Collinear`, diagram,
  numerical example, or a structure field assuming the desired alignment supplies no root proof.
