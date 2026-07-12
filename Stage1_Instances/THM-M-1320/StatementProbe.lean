import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
Capability probe for `S56-M-1320-STATEMENT`.

This is deliberately not the canonical theorem: pinned mathlib has the Riemannian manifold and
metric-diameter vocabulary below, but no Ricci-curvature or Laplace-Beltrami spectral interface from
which the source-exact Li-Yau target can be formed.
-/

#check IsRiemannianManifold
#check Metric.diam
#check IsCompact
