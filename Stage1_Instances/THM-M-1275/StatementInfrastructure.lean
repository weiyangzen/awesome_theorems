import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-1275 statement infrastructure probe

This file checks only the Riemannian-manifold substrate in the pinned mathlib
environment. Pinned mathlib has no scalar-curvature or conformal-rescaling API,
so this file deliberately declares no proxy for the Yamabe theorem.
-/

namespace Stage1Instances.THM_M_1275.StatementInfrastructure

#check Bundle.ContMDiffRiemannianMetric
#check Bundle.RiemannianBundle
#check IsContMDiffRiemannianBundle
#check IsRiemannianManifold

end Stage1Instances.THM_M_1275.StatementInfrastructure
