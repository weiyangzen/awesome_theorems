import Statement

/-!
# THM-M-0580 conditional obligation composition

This module checks the boundary between topological smoothing, the smooth
three-dimensional Poincare theorem, and the exact canonical target. Both
packages are explicit premises; no proof of either package is asserted here.
-/

noncomputable section

open scoped Manifold ContDiff

namespace Stage1Instances.THM_M_0580

universe u

/-- Every topological three-manifold in the canonical context admits a smooth
atlas compatible with its fixed Euclidean chart structure. -/
def TopologicalThreeManifoldSmoothable : Prop :=
  forall (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace Euclidean3 M] [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty (IsManifold (modelWithCornersSelf ℝ Euclidean3) (⊤ : WithTop ℕ∞) M)

/-- The analytic and geometric-topology package after a compatible smooth
structure has been installed. -/
def SmoothThreeDimensionalPoincare : Prop :=
  forall (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace Euclidean3 M]
    [IsManifold (modelWithCornersSelf ℝ Euclidean3) (⊤ : WithTop ℕ∞) M]
    [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty (M ≃ₜ Sphere3)

/-- Checked conditional composition into the exact frozen topological root. -/
theorem root_of_smoothing_and_smooth_poincare
    (smoothable : TopologicalThreeManifoldSmoothable.{u})
    (smoothPoincare : SmoothThreeDimensionalPoincare.{u}) :
    PerelmanPoincareTarget.{u} := by
  intro M _topology _t2 _charted _simplyConnected _compact
  let ⟨smoothStructure⟩ := smoothable M
  letI := smoothStructure
  exact smoothPoincare M

#check root_of_smoothing_and_smooth_poincare
#print axioms root_of_smoothing_and_smooth_poincare

end Stage1Instances.THM_M_0580
