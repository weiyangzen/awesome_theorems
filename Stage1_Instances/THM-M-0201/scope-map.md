# Scope map

## Preserved theorem family

- Target: `THM-M-0201`, named `托勒密定理` (Ptolemy's theorem).
- Catalog attribution and date: Claudius Ptolemy, approximately 150 CE.
- Literal gloss: `圆内接四边形对角线乘积等于对边乘积之和`.
- Conventional candidate reading: for vertices `A, B, C, D` in cyclic order on one Euclidean
  circle, `AC * BD = AB * CD + BC * DA`, with every symbol denoting segment length.

The last bullet expands the recognizable name for planning only. The catalog does not supply a
bibliography or definitions that make it a frozen canonical statement.

## Decisions required at statement freeze

An immutable, independently reviewed source must decide all of the following before a canonical
Lean expression may be credited:

1. Whether the ambient domain is the Euclidean plane, an oriented two-dimensional inner-product
   affine space, or a higher-dimensional Euclidean space containing a planar quadrilateral.
2. Whether a cyclic quadrilateral is an ordered four-tuple of vertices, a polygon object, or four
   points plus a circle and an order predicate; `Cospherical {A, B, C, D}` alone forgets order.
3. Which point order makes `AC` and `BD` the diagonals and `AB`, `BC`, `CD`, and `DA` the sides,
   including whether reversal and cyclic rotation are accepted transports.
4. Whether convexity, simple-boundary order, or the existence of a strict interior intersection of
   the diagonals is explicit or derived from the selected cyclic-polygon definition.
5. Whether all four vertices must be distinct, only consecutive vertices distinct, or weak cyclic
   quadrilaterals with repeated consecutive vertices are admitted.
6. Whether `circle` means planar concyclicity, equidistance from a center, membership in a named
   sphere, or another equivalent definition, and which relationships are machine checked.
7. Whether segment products are products of real-valued metric distances and whether the equality
   is oriented, unsigned, squared, or unsquared.
8. Exact ordered binders, universes, typeclass assumptions, hypotheses, conclusion, foundation
   profile, and each alternate encoding with its checked direction.

## Degenerate and boundary cases

- The pinned candidate's angle hypotheses `angle A P C = pi` and `angle B P D = pi` force `P` to
  lie strictly between each pair of opposite vertices; they provide more than mere collinearity.
  They do not alone assert a transverse or unique intersection in every degenerate configuration.
  The catalog does not state this encoding.
- Those hypotheses force each diagonal's endpoints to differ from the intersection point, but the
  exact admissibility of repeated adjacent vertices still needs a source decision.
- Four cospherical points in an ambient dimension above two need not express a planar circle unless
  coplanarity is separately required or derived. Mathlib's `Concyclic` combines cospherical and
  coplanar conditions, while the candidate equality theorem assumes only `Cospherical` plus the
  diagonal intersection.
- A zero-radius circle, repeated vertices, collinear configurations, tangential or self-crossing
  polygon orders, and a diagonal intersection on the boundary can change the proposition or make
  it vacuous. No case is silently included or excluded at intake.
- The equality identity is invariant under some cyclic rotations and reversal but not arbitrary
  permutations unless the side/diagonal roles are transported accordingly.

## Candidate formal encoding, not credited

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the exact-topic theorem
has the candidate shape:

```text
{A B C D P : Point} ->
Cospherical {A, B, C, D} ->
angle A P C = pi -> angle B P D = pi ->
dist A B * dist C D + dist B C * dist D A = dist A C * dist B D
```

Its conclusion maps directly to the conventional side-product and diagonal-product roles. Its
fifth point and two angle premises represent a point lying strictly inside both diagonal segments,
not wording present in the catalog. A checked source-to-candidate transport therefore belongs to
the statement phase. The stronger ambient-space generality and weak-degeneracy behavior must not be
accepted by name alone.

## Explicit exclusions

- `EuclideanGeometry.mul_dist_le_mul_dist_add_mul_dist`, Ptolemy's inequality for arbitrary four
  points, is not the catalog's cyclic-quadrilateral equality.
- The converse characterization of equality, a criterion for concyclicity, or a complex-number
  identity is not substituted for the forward theorem.
- A theorem for only rectangles, regular polygons, a coordinate example, or a numerical diagram is
  not the general root.
- Four unordered cospherical points without an order or diagonal relation do not by themselves
  select the catalog equation.
- A hypothesis, structure field, or definition that assumes the desired distance equality supplies
  no proof.
- The theorem name, a `#check`, an axiom report, or the catalog label `已验证` supplies no accepted
  human-source or machine-proof credit.

## First downstream gate

The statement phase must admit an immutable source proposition and fix the ordered quadrilateral,
circle/planarity predicate, intersection or convexity encoding, point-distinctness policy, boundary
cases, and exact distance equation. It must then elaborate a minimal-import Lean root, record the
expression and environment fingerprints, compile checked transports, and execute all required
statement mutations. Only afterward may the anchor audit classify the pinned candidate's terminal
body, dependencies, axioms, placeholders, unsafe/oracle boundaries, and trust closure.
