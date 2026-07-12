import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
Kernel-checked infrastructure probe for the THM-M-1325 statement gate.

The repository source does not determine an exact Bishop-Gromov proposition, and the pinned
Riemannian-manifold API does not expose Ricci curvature or a Riemannian volume measure. Accordingly
this module declares no canonical target. It only checks the available manifold, distance-ball,
and generic measure vocabulary without postulating the missing geometry.
-/

namespace Stage1Instances.THM_M_1325.StatementInfrastructure

open Bundle MeasureTheory

#check IsRiemannianManifold
#check Metric.ball
#check Measure
#check Measure.restrict

end Stage1Instances.THM_M_1325.StatementInfrastructure
