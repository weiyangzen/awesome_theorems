import Mathlib.Probability.Moments.Variance

/-!
# THM-M-0992: exact probability Chebyshev statement

This module freezes and tests the statement boundary only. It does not claim
proof or release completion for Chebyshev's inequality.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0992

universe u

/-- The exact intake-selected, real-valued probability form of Chebyshev's
inequality. The finite second moment is expressed by `MemLp X 2 P`. -/
def ChebyshevTarget : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P] (X : Omega → ℝ),
      MemLp X 2 P →
        ∀ r : ℝ, 0 < r →
          P {omega | r ≤ |X omega - P[X]|} ≤
            ENNReal.ofReal (variance X P / r ^ 2)

/-- Direct expansion of the human formula frozen by the intake node. -/
def PinnedIntakeShape : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P] (X : Omega → ℝ),
      MemLp X 2 P →
        ∀ r : ℝ, 0 < r →
          P {omega : Omega | r ≤ abs (X omega - ∫ x, X x ∂P)} ≤
            ENNReal.ofReal (variance X P / r ^ 2)

/-- Checked notation transport from the explicit intake formula. -/
theorem chebyshevTarget_iff_pinnedIntakeShape :
    ChebyshevTarget.{u} ↔ PinnedIntakeShape.{u} := by
  rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedProbabilitySpace : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsFiniteMeasure P] (X : Omega → ℝ),
      MemLp X 2 P →
        ∀ r : ℝ, 0 < r →
          P {omega | r ≤ |X omega - P[X]|} ≤
            ENNReal.ofReal (variance X P / r ^ 2)

def mutationChangedSampleDomain : Prop :=
  ∀ [MeasurableSpace ℝ] (P : Measure ℝ) [IsProbabilityMeasure P]
    (X : ℝ → ℝ), MemLp X 2 P →
      ∀ r : ℝ, 0 < r →
        P {omega | r ≤ |X omega - P[X]|} ≤
          ENNReal.ofReal (variance X P / r ^ 2)

def mutationChangedBinderScope : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P],
      (∀ X : Omega → ℝ, MemLp X 2 P) →
        ∀ (X : Omega → ℝ) (r : ℝ), 0 < r →
          P {omega | r ≤ |X omega - P[X]|} ≤
            ENNReal.ofReal (variance X P / r ^ 2)

def mutationAllowsZeroThreshold : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P] (X : Omega → ℝ),
      MemLp X 2 P →
        ∀ r : ℝ, 0 ≤ r →
          P {omega | r ≤ |X omega - P[X]|} ≤
            ENNReal.ofReal (variance X P / r ^ 2)

/-- Positive thresholds in the canonical target exclude division by zero. -/
theorem positive_threshold_ne_zero {r : ℝ} (hr : 0 < r) : r ≠ 0 :=
  ne_of_gt hr

/-- The selected event is the closed, two-sided absolute-deviation event. -/
theorem closed_deviation_event
    {Omega : Type u} [MeasurableSpace Omega] (P : Measure Omega)
    (X : Omega → ℝ) (r : ℝ) :
    {omega | r ≤ |X omega - P[X]|} =
      {omega | r ≤ abs (X omega - ∫ x, X x ∂P)} := by
  rfl

end Stage1Instances.THM_M_0992

set_option pp.explicit true in
#print Stage1Instances.THM_M_0992.ChebyshevTarget
