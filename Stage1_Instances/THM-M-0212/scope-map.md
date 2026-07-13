# Scope map

## Preserved repository scope

- Target: `THM-M-0212`, named `布里昂雄定理` (Brianchon's theorem).
- Attribution and date: Charles Julien Brianchon, 1806.
- Literal gloss: `圆锥曲线外切六边形的共点性质`.
- Intended family: a conic, an ordered circumscribed hexagon, its three principal diagonals, and a
  concurrency conclusion.

The repository supplies no bibliography, definitions, binders, hypotheses, or exact conclusion.
Its importance and `已验证` fields are inventory metadata only.

## Candidate semantic reading, not credited

A standard forward reading takes six cyclically ordered lines tangent to a plane conic, forms the
six vertices from adjacent-line intersections, and concludes that the lines joining the three
pairs of opposite vertices are concurrent. This is only a discovery model. It does not decide the
field, conic or tangency encoding, how coincident or parallel lines are handled, whether vertices
are primitive or constructed, or whether any converse or degenerate version belongs to the root.

## Proposition-changing decisions

An approved statement run must freeze all of the following from an immutable reviewed source:

- a synthetic projective-plane axiom system versus `P(K^3)` or another coordinatized model;
- the scalar field and characteristic hypotheses, including whether real, complex, algebraically
  closed, or arbitrary fields are intended;
- a conic as the projective zero locus of a quadratic form, a parametrized curve, or a synthetic
  object, together with smoothness, irreducibility, and nondegeneracy requirements;
- an ordered sextuple of side lines and the exact cyclic order used to construct six vertices;
- tangency as a contact-point predicate, a polar relation, an intersection-multiplicity condition,
  or supplied tangent data, including existence and uniqueness obligations;
- whether tangent lines and contact points must be pairwise distinct and in general position;
- the line-intersection encoding for adjacent sides, including inequalities needed to prevent a
  totalized operation from manufacturing a vertex for coincident lines;
- the exact opposite-vertex pairs and the line-through-two-points contract for all three principal
  diagonals;
- concurrency as existence of a common projective point, linear dependence of line coordinates,
  or a determinant equation, with checked transports between credited forms;
- forward Brianchon only, a converse, a projective-dual transport from Pascal, or an equivalence;
- ordered binders, every hypothesis and conclusion, foundation and choice policy, and the mutation
  behavior of all excluded cases.

## Boundary and degenerate cases

- Affinely parallel adjacent sides meet at an ideal point after projective completion; an
  affine-only statement needs an exclusion or a checked transport.
- Coincident adjacent tangent lines do not determine a unique vertex. Mathlib's total
  `Projectivization.cross` returns an input on equality, so noncoincidence is semantic.
- Repeated tangency points may force repeated side lines and vertices; a multiplicity-aware source
  may instead use limiting tangents or nonreduced contact data.
- Opposite vertices can coincide, making a principal diagonal underdetermined; two principal
  diagonals can coincide, making a common-point formulation nonunique or trivial.
- A singular or reducible conic can change the meaning or existence of tangent lines and polarity.
- In characteristic two, polar forms and conic duality can behave materially differently.
- A projective concurrency result may include ideal concurrency that an affine gloss would omit.

No boundary case is excluded at intake because no proposition has been selected.

## Neighbor and substitution boundaries

- `THM-M-0211` (Pascal) is the projective dual theorem for an inscribed hexagon and is not a proof
  or alternate encoding of this target without an explicit checked duality transport.
- `THM-M-0210` (Desargues), Ceva, Pappus, dual Mobius generalizations, Poncelet porisms, and
  theorems about the many Brianchon points of one six-line configuration are not substitutes.
- A coordinate determinant, generic projective-incidence API, affine concurrency result, diagram,
  numerical example, or a structure field assuming the desired common point supplies no root
  proof.
