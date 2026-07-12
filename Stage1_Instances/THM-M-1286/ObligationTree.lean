import «Stage1_Instances».«THM-M-1286».Statement

/-!
Conditional composition certificate for the frozen Polya-Szego architecture.
The construction and gradient-estimate packages are explicit premises and
remain open; this file checks only their exact composition into the root.
-/

open scoped ENNReal MeasureTheory

namespace Stage1Instances.THM_M_1286.ObligationTree

open MeasureTheory

/-- Construction of the Schwarz rearrangement with all non-gradient properties. -/
def RearrangementConstruction : Prop :=
  ∀ (n : ℕ) (p : ℝ≥0∞), 1 ≤ n → 1 ≤ p → p ≠ ∞ →
    ∀ (u : Euclidean n → ℝ),
      (∀ x, 0 ≤ u x) → AEStronglyMeasurable u volume → MemLp u p volume →
      VanishesAtInfinity u →
      ∃ uStar : Euclidean n → ℝ,
        AEStronglyMeasurable uStar volume ∧ MemLp uStar p volume ∧
        IsSymmetricDecreasing uStar ∧ Equimeasurable u uStar

/-- The analytic Polya-Szego estimate for the constructed rearrangement. -/
def GradientEstimate : Prop :=
  ∀ (n : ℕ) (p : ℝ≥0∞), 1 ≤ n → 1 ≤ p → p ≠ ∞ →
    ∀ (u uStar : Euclidean n → ℝ) (g : Euclidean n → Euclidean n),
      (∀ x, 0 ≤ u x) → AEStronglyMeasurable u volume → MemLp u p volume →
      VanishesAtInfinity u → HasWeakGradient u g → MemLp g p volume →
      AEStronglyMeasurable uStar volume → MemLp uStar p volume →
      IsSymmetricDecreasing uStar → Equimeasurable u uStar →
      ∃ gStar : Euclidean n → Euclidean n,
        HasWeakGradient uStar gStar ∧ MemLp gStar p volume ∧
        eLpNorm gStar p volume ≤ eLpNorm g p volume

/-- Checked child-to-parent composition into the exact frozen target. -/
theorem exactTarget_of_packages
    (construction : RearrangementConstruction)
    (estimate : GradientEstimate) : PolyaSzegoTarget := by
  intro n p hn hp hpFinite u g huNonneg huMeas huLp huVanish huGrad hgLp
  obtain ⟨uStar, huStarMeas, huStarLp, huStarSymm, huEqui⟩ :=
    construction n p hn hp hpFinite u huNonneg huMeas huLp huVanish
  obtain ⟨gStar, huStarGrad, hgStarLp, henergy⟩ :=
    estimate n p hn hp hpFinite u uStar g huNonneg huMeas huLp huVanish
      huGrad hgLp huStarMeas huStarLp huStarSymm huEqui
  exact ⟨uStar, gStar, huStarMeas, huStarLp, huStarSymm, huEqui,
    huStarGrad, hgStarLp, henergy⟩

#check exactTarget_of_packages
#print axioms exactTarget_of_packages

end Stage1Instances.THM_M_1286.ObligationTree
