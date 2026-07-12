import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic

/-!
# THM-M-1327 statement-infrastructure probe

This file checks the closest pinned mathlib interfaces found for a future Hessian-comparison
statement. It is deliberately not a canonical target: the intake has not identified a
source-exact theorem variant, and the pinned dependency has no distance-Hessian, sectional-
curvature, exponential-map, or cut-locus interface from which to express that variant.
-/

#check IsRiemannianManifold
#check Bundle.RiemannianBundle
#check IsContMDiffRiemannianBundle
#check TangentSpace
#check CovariantDerivative
#check dist
#check inner
