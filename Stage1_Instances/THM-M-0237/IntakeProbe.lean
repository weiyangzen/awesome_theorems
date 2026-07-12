import Mathlib.Analysis.Meromorphic.Basic
import Mathlib.Geometry.Manifold.Complex

/-!
# THM-M-0237 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for complex manifolds, compact spaces,
manifold holomorphicity, and plane-domain meromorphic functions. They do not define divisors or
line bundles on compact Riemann surfaces, state Riemann-Roch, or supply proof credit.
-/

#check ModelWithCorners
#check ChartedSpace
#check IsManifold
#check CompactSpace
#check MDifferentiable
#check MDifferentiable.isLocallyConstant
#check MDifferentiable.exists_eq_const_of_compactSpace
#check MeromorphicAt
#check MeromorphicOn
#check Meromorphic
