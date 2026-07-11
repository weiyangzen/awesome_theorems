# Scope map

## Included claim

- A complete finite-dimensional Riemannian manifold and a chosen center point.
- A pointwise Ricci lower bound normalized as `Ric >= (n - 1) k`.
- Metric/geodesic balls and their Riemannian volumes.
- The same-dimensional simply connected constant-sectional-curvature `k` model and its ball
  volume `V_k`.
- Monotonicity in the radius of `Vol(B(p,r)) / V_k(r)`, including the resulting two-radius
  comparison once the source-exact radius domain is fixed.

## Decisions reserved for the statement phase

Primary-source inspection must fix regularity, connectedness, dimension restrictions, open versus
closed balls, strict positivity and ordering of radii, and the admissible radius range when `k > 0`.
It must also fix whether the theorem uses a global Ricci bound or only a ball-local bound, the
normalization of curvature, and how the limit ratio at radius zero is represented. Binder order,
universes, volume normalization, extended-real coercions, and division-by-zero guards follow those
choices.

## Explicit exclusions

- Substituting Bishop's absolute upper bound for the ratio-monotonicity theorem.
- Substituting a sectional-curvature, scalar-curvature, weighted-measure, synthetic `CD(K,N)`, or
  discrete metric-measure theorem.
- Assuming the desired volume-ratio monotonicity as a field or hypothesis.
- Replacing geodesic balls by Euclidean balls without a proved geometric transport.
- Crediting the Stage0 `已验证` label as source or machine evidence.

The later Lean target must expose concrete Riemannian metric, Ricci lower bound, geodesic ball,
Riemannian volume, model space, and monotonicity interfaces, or record the exact missing API.
