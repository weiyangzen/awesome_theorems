import Mathlib.Probability.Independence.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Analysis.SpecialFunctions.Exp

/-!
# THM-M-0994: exact Hoeffding inequality statement

This module freezes the one-sided finite-family statement. It intentionally
contains no proof of Hoeffding's inequality.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Real
open scoped BigOperators ENNReal NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0994

universe u v

/-- The exact target: the centered upper tail for a finite independent family
of almost surely interval-bounded real random variables. -/
def HoeffdingTarget : Prop :=
  ∀ (I : Type v) [Fintype I]
    (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : I → Ω → ℝ) (a b : I → ℝ),
      (∀ i, Measurable (X i)) →
      iIndepFun X μ →
      (∀ i, ∀ᵐ ω ∂μ, X i ω ∈ Set.Icc (a i) (b i)) →
      ∀ ε : ℝ, 0 ≤ ε →
        μ.real {ω | ε ≤ ∑ i, (X i ω - ∫ x, X i x ∂μ)} ≤
          exp ((-2 * ε ^ 2) / ∑ i, (b i - a i) ^ 2)

-- Structural mutations. The validator requires their elaborated expressions
-- to differ from the frozen target; none is used as theorem evidence.

/-- Mutation removing the independence hypothesis. -/
def mutationRemovedIndependence : Prop :=
  ∀ (I : Type v) [Fintype I]
    (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : I → Ω → ℝ) (a b : I → ℝ),
      (∀ i, Measurable (X i)) →
      (∀ i, ∀ᵐ ω ∂μ, X i ω ∈ Set.Icc (a i) (b i)) →
      ∀ ε : ℝ, 0 ≤ ε →
        μ.real {ω | ε ≤ ∑ i, (X i ω - ∫ x, X i x ∂μ)} ≤
          exp ((-2 * ε ^ 2) / ∑ i, (b i - a i) ^ 2)

/-- Mutation restricting the arbitrary finite index type to an initial segment. -/
def mutationChangedIndexDomain : Prop :=
  ∀ (n : ℕ)
    (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : Fin n → Ω → ℝ) (a b : Fin n → ℝ),
      (∀ i, Measurable (X i)) →
      iIndepFun X μ →
      (∀ i, ∀ᵐ ω ∂μ, X i ω ∈ Set.Icc (a i) (b i)) →
      ∀ ε : ℝ, 0 ≤ ε →
        μ.real {ω | ε ≤ ∑ i, (X i ω - ∫ x, X i x ∂μ)} ≤
          exp ((-2 * ε ^ 2) / ∑ i, (b i - a i) ^ 2)

/-- Mutation replacing coordinate measurability by measurability of each
finite centered sum, changing the scope and content of that binder. -/
def mutationChangedBinderScope : Prop :=
  ∀ (I : Type v) [Fintype I]
    (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : I → Ω → ℝ) (a b : I → ℝ),
      Measurable (fun ω ↦ ∑ i, (X i ω - ∫ x, X i x ∂μ)) →
      iIndepFun X μ →
      (∀ i, ∀ᵐ ω ∂μ, X i ω ∈ Set.Icc (a i) (b i)) →
      ∀ ε : ℝ, 0 ≤ ε →
        μ.real {ω | ε ≤ ∑ i, (X i ω - ∫ x, X i x ∂μ)} ≤
          exp ((-2 * ε ^ 2) / ∑ i, (b i - a i) ^ 2)

/-- Boundary mutation excluding empty and zero-total-width families. -/
def mutationExcludedZeroWidth : Prop :=
  ∀ (I : Type v) [Fintype I]
    (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : I → Ω → ℝ) (a b : I → ℝ),
      0 < ∑ i, (b i - a i) ^ 2 →
      (∀ i, Measurable (X i)) →
      iIndepFun X μ →
      (∀ i, ∀ᵐ ω ∂μ, X i ω ∈ Set.Icc (a i) (b i)) →
      ∀ ε : ℝ, 0 ≤ ε →
        μ.real {ω | ε ≤ ∑ i, (X i ω - ∫ x, X i x ∂μ)} ≤
          exp ((-2 * ε ^ 2) / ∑ i, (b i - a i) ^ 2)

end Stage1Instances.THM_M_0994

set_option pp.explicit true in
#print Stage1Instances.THM_M_0994.HoeffdingTarget
