# Scope map

## Preserved repository scope

- Target: `THM-M-0210`, named `笛沙格定理` (Desargues's theorem).
- Attribution and date: Girard Desargues, 1648.
- Literal gloss: `两个三角形透视的条件`.
- Catalog subject: Euclidean geometry, with a high-importance and untrusted `已验证` label.

The intake preserves the classical two-triangle perspectivity theorem family. It does not turn the
short gloss into a stronger projective theorem, a weaker affine parallel special case, or a
bidirectional equivalence without source approval.

## Candidate classical reading, not credited

A conventional projective-plane form starts with triangles `ABC` and `A'B'C'`. If the three lines
joining corresponding vertices are concurrent, then the three intersection points of corresponding
sides are collinear. The converse exchanges those hypotheses and conclusions. This description is
a discovery model only. It is not the frozen canonical statement because the repository neither
states the direction nor fixes the incidence setting and degenerate cases needed to make it exact.

## Proposition-changing decisions

The statement phase must select an immutable reviewed source and decide:

1. Whether the root is the point-to-line implication, its converse, or both as an equivalence.
2. Whether it lives in an abstract projective plane, a projectivized three-dimensional vector
   space, an affine plane with explicit parallel alternatives, Euclidean coordinates, or a
   three-dimensional incidence geometry whose triangles lie in a plane.
3. The scalar assumptions for a coordinatized model: field, division ring, commutativity,
   characteristic, and dimension or rank requirements.
4. How a triangle, corresponding vertices and sides, lines, concurrency, side intersections, and
   collinearity are represented, including the precise correspondence order.
5. Whether side-intersection points are existential witnesses, unique intersections of distinct
   lines, joins/meets in an incidence lattice, or homogeneous cross products.
6. How affine parallel lines and points or a line at infinity map to the projective formulation.
7. Every distinctness, noncollinearity, noncoincidence, coplanarity, and general-position
   hypothesis, with ordered binders and universes.
8. Whether the theorem is presented as an incidence implication, a checked `Iff`, a determinant
   identity, or another encoding, and the checked transports among any credited forms.

## Boundary and degenerate cases

Source review must resolve coincident corresponding vertices; repeated or collinear vertices within
a triangle; coincident corresponding sides; a center lying on a triangle side; parallel joins or
sides in an affine model; intersections at infinity; repeated axis points; identical triangles;
triangles in the same versus different planes; and ambient dimension below, equal to, or above the
selected plane model. Some abstract projective planes are non-Desarguesian, so the ambient incidence
axioms or coordinatization assumptions cannot be omitted.

No boundary case is excluded at intake because no exact proposition has been selected.

## Excluded substitutions

- Pappus's theorem, Pascal's theorem, Brianchon's theorem, Ceva's theorem, Menelaus's theorem, or
  an unrelated triangle-concurrency result cannot replace Desargues's theorem.
- A proof only of Hilbert's parallel-side specialization cannot silently replace the full finite
  projective intersection form, or conversely.
- The point-to-line direction cannot be used for a requested converse or equivalence without a
  checked source-approved transport.
- A three-dimensional proof cannot silently change a theorem asserted for an arbitrary abstract
  projective plane; non-Desarguesian planes make that boundary material.
- A determinant or cross-product identity is not the geometric target until all nonzero,
  incidence, and quotient-representative transports are checked.
- A structure or hypothesis storing the desired concurrency, collinearity, implication, or
  equivalence supplies no proof.
- A diagram, coordinate experiment, theorem name, API check, citation, or the catalog's untrusted
  status supplies no H or M credit.

## Neighbor boundaries

`THM-M-0211` owns Pascal's theorem. Other geometry targets own their named concurrency,
collinearity, projective, or Euclidean results. They may later become explicit proof dependencies,
but no nearby name or status grants evidence to this target.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks affine `Collinear` and span APIs,
projectivization and projective subspaces, and cross products in a homogeneous three-coordinate
projective-plane model.
A bounded search found no Desargues theorem, perspectivity definition, or complete line-intersection
API matching the catalog root. This is narrow intake discovery, not an exhaustive anchor audit or a
proof of global absence.
