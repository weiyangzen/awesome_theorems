import Mathlib.MeasureTheory.Group.GeometryOfNumbers

/-!
# THM-M-0417 obligation composition

This module checks a conditional composition harness for the frozen proof
architecture. The three inputs are obligations, not assertions that those
obligations have already been discharged.
-/

namespace Stage1Instances.THM_M_0417.ObligationTree

open MeasureTheory Module
open scoped Pointwise

universe u

def Collision (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (L : AddSubgroup E) (s : Set E) : Prop :=
  ∃ x y : L, x ≠ y ∧ ¬Disjoint (x +ᵥ ((2⁻¹ : ℝ) • s)) (y +ᵥ ((2⁻¹ : ℝ) • s))

def HalfBodyVolume : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      (mu : Measure E) [mu.IsAddHaarMeasure]
      (L : AddSubgroup E) [Countable L] (F s : Set E),
    IsAddFundamentalDomain L F mu →
      (∀ x ∈ s, -x ∈ s) → Convex ℝ s →
        mu F * 2 ^ finrank ℝ E < mu s →
          mu F < mu ((2⁻¹ : ℝ) • s)

def BlichfeldtBridge : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      (mu : Measure E) [mu.IsAddHaarMeasure]
      (L : AddSubgroup E) [Countable L] (F s : Set E),
    IsAddFundamentalDomain L F mu → Convex ℝ s →
      mu F < mu ((2⁻¹ : ℝ) • s) → Collision E L s

def DifferenceExtraction : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      (L : AddSubgroup E) (s : Set E),
    (∀ x ∈ s, -x ∈ s) → Convex ℝ s → Collision E L s →
      ∃ x ≠ 0, ((x : L) : E) ∈ s

def Root : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      (mu : Measure E) [mu.IsAddHaarMeasure]
      (L : AddSubgroup E) [Countable L] (F s : Set E),
    IsAddFundamentalDomain L F mu →
      (∀ x ∈ s, -x ∈ s) → Convex ℝ s →
        mu F * 2 ^ finrank ℝ E < mu s →
          ∃ x ≠ 0, ((x : L) : E) ∈ s

/-- Every required proof input is explicit and consumed. This certificate
checks only child-to-root composition, not the children themselves. -/
theorem root_compose
    (halfBody : HalfBodyVolume.{u})
    (blichfeldt : BlichfeldtBridge.{u})
    (extract : DifferenceExtraction.{u}) : Root.{u} := by
  intro E _ _ _ _ _ mu _ L _ F s fund hSymm hConv hMeasure
  have hHalf := halfBody E mu L F s fund hSymm hConv hMeasure
  have hCollision := blichfeldt E mu L F s fund hConv hHalf
  exact extract E L s hSymm hConv hCollision

theorem root_exact_type :
    Root.{u} =
      (∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
          [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
          (mu : Measure E) [mu.IsAddHaarMeasure]
          (L : AddSubgroup E) [Countable L] (F s : Set E),
        IsAddFundamentalDomain L F mu →
          (∀ x ∈ s, -x ∈ s) → Convex ℝ s →
            mu F * 2 ^ finrank ℝ E < mu s →
              ∃ x ≠ 0, ((x : L) : E) ∈ s) :=
  rfl

#check root_compose
#print axioms root_compose

end Stage1Instances.THM_M_0417.ObligationTree
