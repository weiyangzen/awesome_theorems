import Mathlib.Algebra.Homology.EulerCharacteristic
import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
This intake probe checks adjacent pinned interfaces only. It is not a statement of Gauss-Bonnet:
the checked imports do not provide an end-to-end Gaussian-curvature integral, boundary geodesic
curvature, topological Euler characteristic of the same surface, or their equality.
-/

open Bundle
open scoped Bundle ContDiff Manifold

namespace AwesomeTheorems.THM_M_0216.IntakeProbe

universe uE uH uM

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
  {M : Type uM} [EMetricSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
  [RiemannianBundle (fun x : M => TangentSpace I x)]
  [IsContMDiffRiemannianBundle I ∞ E (fun x : M => TangentSpace I x)]
  [IsRiemannianManifold I M]

/-- A relevant binder fragment supported by the pinned Riemannian API. This is an infrastructure
probe, not a target theorem or a credited alternate encoding. -/
def availableSurfaceContext [FiniteDimensional ℝ E] [CompactSpace M] : Prop :=
  Module.finrank ℝ E = 2

#check IsRiemannianManifold
#check IsContMDiffRiemannianBundle
#check availableSurfaceContext
#check HomologicalComplex.eulerChar
#check HomologicalComplex.homologyEulerChar

end AwesomeTheorems.THM_M_0216.IntakeProbe
