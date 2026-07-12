import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion

/-!
Kernel-checked infrastructure probe for the THM-M-0164 statement gate.

Pinned mathlib supplies smooth Riemannian metrics, general covariant derivatives, and their torsion
tensor. It does not supply the Levi-Civita connection, its curvature tensor, geodesics, covariant
differentiation along a curve, or Jacobi fields. Consequently this module deliberately declares no
canonical theorem, unsupported declaration, proof, or proxy predicate.
-/

namespace Stage1Instances.THM_M_0164.StatementInfrastructure

#check Bundle.ContMDiffRiemannianMetric
#check CovariantDerivative
#check CovariantDerivative.torsion
#check CovariantDerivative.torsion_eq_zero_iff
#check TangentSpace

end Stage1Instances.THM_M_0164.StatementInfrastructure
