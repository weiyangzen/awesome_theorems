# Scope map

## Frozen human claim

Let `n >= 2`. A finite nonzero Borel measure `mu` on the Euclidean unit sphere `S^(n-1)` is the
surface-area measure of a convex body `K` with nonempty interior exactly when

1. its vector first moment vanishes, `integral u d mu(u) = 0`; and
2. it is not concentrated on any great subsphere.

When it exists, `K` is unique up to translation. The statement phase must confirm this formulation
against the selected source before it becomes the canonical Lean expression.

## Included boundary

- Finite-dimensional real Euclidean space and its unit sphere, with `n >= 2` explicit.
- Finite Borel measures and a vector-valued integrability/first-moment condition.
- Full-dimensional compact convex bodies, rather than arbitrary closed convex sets.
- Surface-area measure defined by the outer-normal/Gauss-map distribution on the boundary.
- Both necessity and existence, plus uniqueness modulo translation.
- Nonsmooth bodies and atomic measures are included unless the source audit selects a narrower
  theorem and records its relationship to the general form.

## Exclusions and non-substitutes

- The discrete polytope version alone, the smooth positive-density Monge-Ampere/PDE version alone,
  or an approximation theorem does not close the general root.
- The Brunn-Minkowski inequality, Minkowski's first inequality, the Christoffel problem, and the
  prescribed Gaussian-curvature problem for a parametrized smooth hypersurface are adjacent but
  distinct statements.
- Existence without uniqueness, uniqueness after fixing an arbitrary normalization, or a structure
  that assumes the desired convex body as data receives no full-root credit.
- Numerical recovery of a body from sampled normals is outside the proof claim.

## Statement-phase decisions

The next phase must freeze the exact dimension indexing, sphere and great-subsphere definitions,
measure regularity, the surface-area-measure normalization, vector integration interface,
full-dimensionality predicate, equality of measures, and translation equivalence. It must also
resolve whether the source expresses nondegeneracy as non-concentration on great subspheres or an
equivalent positivity condition, and supply a checked equivalence before exchanging them.

Degenerate dimensions, the zero measure, measures supported on a great subsphere, lower-dimensional
convex sets, and translations of `K` must be explicit mutation/boundary cases. No hypothesis may be
silently strengthened to smoothness, strict convexity, or positive density.
