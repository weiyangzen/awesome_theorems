import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
This file checks only the pinned Riemannian-manifold context that is presently available in
mathlib.  It is deliberately not a statement of Chern-Gauss-Bonnet: the pinned dependency has no
Levi-Civita connection/curvature, Pfaffian Euler form, integration of differential forms on a
manifold, or topological Euler-characteristic API with which to state the canonical equality.
-/

open Bundle
open scoped Bundle ContDiff Manifold

namespace AwesomeTheorems.THM_M_0569.StatementInfrastructureProbe

universe uE uH uM

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
  {M : Type uM} [EMetricSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
  [RiemannianBundle (fun x : M => TangentSpace I x)]
  [IsContMDiffRiemannianBundle I ∞ E (fun x : M => TangentSpace I x)]
  [IsRiemannianManifold I M]

/-- The largest relevant binder fragment supported by the pinned Riemannian API. This is an
infrastructure probe, not a substitute theorem or a credited alternate encoding. -/
def availableEvenDimensionalContext [FiniteDimensional ℝ E] [CompactSpace M] (n : ℕ) : Prop :=
  Module.finrank ℝ E = 2 * n

#check IsRiemannianManifold
#check IsContMDiffRiemannianBundle
#check availableEvenDimensionalContext

end AwesomeTheorems.THM_M_0569.StatementInfrastructureProbe
