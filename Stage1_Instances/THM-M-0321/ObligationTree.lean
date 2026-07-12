import «Stage1_Instances».«THM-M-0321».Statement

/-!
# THM-M-0321 conditional obligation composition

This module checks the handoff from the finite-family theorem and the compact
finite-intersection upgrade to the exact frozen target. It deliberately takes
both mathematical packages as hypotheses and therefore proves neither one.
-/

open Set

namespace Stage1Instances.THM_M_0321.ObligationTree

universe u v

/-- Every finite subfamily has a common fixed point in `K`. -/
def FiniteFamilyStep : Prop :=
  ∀ (E : Type u) [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    [LocallyConvexSpace ℝ E] (I : Type v) (K : Set E) (f : I → E → E),
      K.Nonempty → IsCompact K → Convex ℝ K →
      (∀ i, MapsTo (f i) K K) → (∀ i, ContinuousOn (f i) K) →
      (∀ i, IsAffineOn K (f i)) →
      (∀ i j, ∀ x ∈ K, f i (f j x) = f j (f i x)) →
      ∀ s : Finset I, ∃ x ∈ K, ∀ i ∈ s, f i x = x

/-- Compactness upgrades the finite-intersection property of the fixed sets
to a point fixed by the entire family. -/
def CompactnessUpgrade : Prop :=
  ∀ (E : Type u) [TopologicalSpace E] (I : Type v) (K : Set E) (f : I → E → E),
    IsCompact K →
    (∀ s : Finset I, ∃ x ∈ K, ∀ i ∈ s, f i x = x) →
    HasCommonFixedPoint K f

/-- Checked child-to-parent composition. Both required children are consumed,
and the result is definitionally the canonical target. -/
theorem root_compose
    (finiteFamily : FiniteFamilyStep.{u, v})
    (compactness : CompactnessUpgrade.{u, v}) :
    MarkovKakutaniTarget.{u, v} := by
  intro E _ _ _ _ _ _ _ I K f hK hCompact hConvex hMaps hContinuous hAffine hCommute
  apply compactness E I K f hCompact
  exact finiteFamily E I K f hK hCompact hConvex hMaps hContinuous hAffine hCommute

theorem root_exact_type :
    MarkovKakutaniTarget.{u, v} = MarkovKakutaniTarget.{u, v} := rfl

#print root_compose
#print axioms root_compose

end Stage1Instances.THM_M_0321.ObligationTree
