# Scope map

## Preserved repository scope

- Target: `THM-M-0197`, named `费马点定理` (Fermat point theorem).
- Attribution and date: Pierre de Fermat, 1643.
- Literal gloss: `三角形内到三顶点距离之和最小的点`.
- Intended subject: Euclidean triangle geometry and minimization of a sum of three distances.

The repository supplies no bibliography, definitions, binders, hypotheses, or conclusion. The
importance and `已验证` fields are catalog metadata only.

## Candidate semantic reading, not credited

A natural reading introduces vertices `A`, `B`, and `C`, a point `P`, and the objective
`dist P A + dist P B + dist P C`. Even that reading leaves open whether `P` ranges over the whole
ambient plane, the closed triangular region, or its strict interior; whether the claim is existence,
uniqueness, a minimization inequality, a geometric construction, or a characterization; and which
triangle cases are admitted. It is therefore a discovery model, not the canonical statement.

## Proposition-changing decisions

An approved statement run must freeze all of the following from an immutable reviewed source:

- the ambient space, normally a two-dimensional Euclidean affine space, versus `R^2` coordinates
  or a more general real inner-product space;
- three distinct noncollinear vertices versus repeated or collinear points, and the exact triangle
  predicate;
- strict interior, relative interior, closed convex hull, or the entire plane as the comparison
  domain, including the precise meaning of the Chinese word `内`;
- whether the theorem asserts existence, uniqueness, both, or only characterizes a point already
  assumed to minimize the sum of distances;
- whether minimization is written with `IsMinOn`, a universal inequality, or an `argmin`, and a
  checked relationship between any credited encodings;
- the complete angle split: every vertex angle strictly below 120 degrees versus one angle greater
  than or equal to 120 degrees, including equality at 120 degrees;
- in the first branch, whether the minimizer is asserted to lie in the strict interior and whether
  all three angles at it equal 120 degrees in both directions of a characterization;
- in the second branch, whether the corresponding vertex is asserted to be the unique global
  minimizer and how ties or degenerate triangles are excluded;
- ordered binders, every hypothesis and conclusion, foundation and choice policy, and all
  transports between affine, vector, and coordinate representations.

## Boundary and degenerate cases

- A nondegenerate triangle with an angle at least 120 degrees has its minimizer at that vertex, not
  in the strict interior. This is the central blocker for the literal unrestricted reading.
- Equality at exactly 120 degrees must be assigned to a branch explicitly.
- Collinear distinct vertices have a median-point minimization problem rather than the ordinary
  interior 120-degree configuration.
- Repeated vertices change both uniqueness and the optimality condition.
- An empty strict-interior domain for a degenerate triangle cannot support an existence claim.
- "Minimum over the triangle" and "minimum over the whole plane, with a result that lies in the
  triangle" are different statements until a checked reduction relates them.

No boundary case is excluded at intake because no proposition has been selected.

## Explicit exclusions

- No silent addition of an all-angles-less-than-120-degrees hypothesis to rescue an interior-only
  statement.
- No silent broadening of strict interior to the closed triangle or whole plane.
- No substitution of the full two-branch Fermat-Torricelli theorem for the shorter catalog gloss
  without a reviewed source-to-target decision.
- No substitution of the geometric median for an arbitrary finite point set, a weighted problem,
  a Steiner tree, a Weiszfeld-algorithm convergence theorem, or a spherical/normed-space variant.
- No structure field or hypothesis that assumes the desired minimizer, uniqueness, or 120-degree
  conclusion.
- No numerical construction, diagram, metadata label, generic API, or citation treated as proof.
