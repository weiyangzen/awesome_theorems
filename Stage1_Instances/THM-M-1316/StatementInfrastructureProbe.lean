import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-1316 statement infrastructure probe

This file checks only the closest pinned mathlib Riemannian-manifold substrate.
It is not a statement of the positive mass theorem: the pinned dependency has
no definitions of an asymptotically flat end, ADM mass, or scalar curvature.
-/

#check IsRiemannianManifold
#check Bundle.ContMDiffRiemannianMetric
#check riemannianMetricVectorSpace
