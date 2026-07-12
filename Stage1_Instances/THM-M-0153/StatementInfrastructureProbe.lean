import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
This file checks only the portion of the intended binder context available from the pinned
Riemannian-manifold API. It is not a statement of Chern-Gauss-Bonnet: the pinned dependency does
not provide the terms needed for the Levi-Civita curvature, normalized Pfaffian Euler form,
manifold integration, and topological Euler characteristic in the canonical equality.
-/

open Bundle
open scoped Bundle ContDiff Manifold

namespace AwesomeTheorems.THM_M_0153.StatementInfrastructureProbe

universe uE uH uM

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
  {M : Type uM} [EMetricSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
  [RiemannianBundle (fun x : M => TangentSpace I x)]
  [IsContMDiffRiemannianBundle I ∞ E (fun x : M => TangentSpace I x)]
  [IsRiemannianManifold I M]

/-- The available even-dimensional compact Riemannian context. This infrastructure probe is not
the target theorem and receives no statement or proof credit. -/
def availableEvenDimensionalContext [FiniteDimensional ℝ E] [CompactSpace M] (n : ℕ) : Prop :=
  Module.finrank ℝ E = 2 * n

#check IsRiemannianManifold
#check IsContMDiffRiemannianBundle
#check availableEvenDimensionalContext

end AwesomeTheorems.THM_M_0153.StatementInfrastructureProbe
