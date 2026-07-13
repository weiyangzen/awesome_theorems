# Scope map

## Preserved theorem family

The intake preserves the planar Descartes circle-theorem family named by the catalog: four
mutually tangent circles have curvatures satisfying a quadratic relation. An inspected modern
source writes the candidate relation as

```text
(b1 + b2 + b3 + b4)^2 = 2 * (b1^2 + b2^2 + b3^2 + b4^2).
```

Here the `bi` are bends (reciprocals of radii) for the disjoint-interior case, or signed bends for
a compatible orientation when an enclosing circle or a straight-line degeneration is allowed.
This is a candidate scope description, not the frozen canonical proposition.

## Decisions required at statement freeze

An immutable, independently reviewed source must decide all of the following before one Lean root
can be credited:

1. Whether the root is only the ordinary four finite circles with disjoint interiors and positive
   radii, or the source's larger compatible oriented configuration including enclosing circles and
   straight lines.
2. The exact definition of a Descartes configuration: pairwise tangency, exclusion of three circles
   sharing one tangent, distinct tangency points, distinct circles, and the interior-disjointness or
   compatible-orientation condition.
3. Whether tangency is external for every pair, or includes an internally tangent enclosing circle;
   how the six pairwise tangencies and their contact points are represented.
4. Whether curvature is `1 / r` for positive radii, signed reciprocal oriented radius, or primitive
   data constrained by an approved relationship to the geometric circles.
5. Whether straight lines count as circles of infinite radius and bend zero, and, if so, how their
   positions, normals, orientations, and tangencies are encoded in Lean.
6. Whether the conclusion is the quadratic identity, a cleared-denominator radius identity, the
   two possible fourth-bend formula, a converse/existence statement, or a conjunction. These are
   not interchangeable without checked hypotheses and transports.
7. The precise planar model, ordered binders, universes, typeclass assumptions, foundation/TCB
   profiles, conclusion, and every alternate encoding with a checked relationship.

## Degenerate and boundary cases

Source review must explicitly address an enclosing circle with negative signed bend; one or two
straight lines with zero bend; parallel lines; zero-radius spheres (permitted by mathlib's bare
`Sphere` structure); coincident circles or centers; common or repeated tangency points; three
circles sharing one tangent; failure of interior disjointness; global reversal of all orientations;
and denominators or square roots introduced by alternate formulas. The ordinary positive-radius
case cannot silently prove the signed enclosing-circle case, or conversely.

## Excluded substitutions

- The Soddy-Gossett theorem in higher dimensions is a generalization, not the exact planar root.
- The complex or augmented Descartes theorems involving circle centers are stronger related
  results, not substitutes for the catalog's curvature relation.
- The converse assertion that every nonzero real solution is realized by a configuration, the
  replacement-circle formula, and integrality results for Apollonian packings are distinct claims.
- Descartes' rule of signs, the Cantor-Bendixson theorem, and Poincare-Bendixson results are name
  collisions and unrelated mathematics.
- A result for only four externally tangent positive-radius mathlib spheres does not cover an
  enclosing circle unless a source-approved signed transport is checked.
- A structure that stores the curvature identity, pairwise tangencies, or desired result as an
  input field supplies no proof.
- A diagram, numerical example, algebraic test, theorem-name match, `#check`, or the catalog's
  `已验证` label supplies no H or M credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Geometry.Euclidean.Sphere.Tangent` provides `EuclideanGeometry.Sphere`, external and
internal tangency predicates, and exact center-distance characterizations. Its sphere radius is an
ordinary real value and tangency forces nonnegative radii; it does not provide compatible oriented
circles, signed bends, a four-circle configuration predicate, or the Descartes curvature identity.
No canonical Lean expression, minimal import set, expression fingerprint, checked alternate
encoding, discovery protocol, obligation registry, or proof state is frozen at intake.
