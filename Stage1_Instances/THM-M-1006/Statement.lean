import Mathlib.Probability.Martingale.Basic

open MeasureTheory

namespace Stage1Instances.THM_M_1006

universe u

/-- The largest absolute value attained by a finite real-valued process up to time `n`. -/
noncomputable def maximalProcess (f : Nat -> Ω -> Real) (n : Nat) (ω : Ω) : Real :=
  Finset.sup' (Finset.range (n + 1)) (by simp) fun k => |f k ω|

/-- The discrete quadratic variation of `f` through time `n`. -/
noncomputable def quadraticVariation (f : Nat -> Ω -> Real) (n : Nat) (ω : Ω) : Real :=
  ∑ k ∈ Finset.range n, (f (k + 1) ω - f k ω) ^ 2

/-- Finite-time, real-valued Burkholder-Davis-Gundy inequalities.

The constants are quantified before the probability space, filtration, martingale, and horizon, so
they depend only on `p`.  The martingale starts at zero; consequently its discrete quadratic
variation contains every increment relevant to the maximal process. -/
def StatementShape (p : Real) : Prop :=
  0 < p ->
    ∃ c C : ENNReal, 0 < c ∧ c < ⊤ ∧ 0 < C ∧ C < ⊤ ∧
      ∀ (Ω : Type u) (m : MeasurableSpace Ω) (μ : Measure Ω),
        @IsProbabilityMeasure Ω m μ ->
        ∀ (F : Filtration Nat m) (f : Nat -> Ω -> Real),
          Martingale f F μ -> f 0 = 0 -> ∀ n : Nat,
            c * ∫⁻ ω, (ENNReal.ofReal (quadraticVariation f n ω)).rpow (p / 2) ∂μ <=
                ∫⁻ ω, (ENNReal.ofReal (maximalProcess f n ω)).rpow p ∂μ ∧
              ∫⁻ ω, (ENNReal.ofReal (maximalProcess f n ω)).rpow p ∂μ <=
                C * ∫⁻ ω, (ENNReal.ofReal (quadraticVariation f n ω)).rpow (p / 2) ∂μ

#check maximalProcess
#check quadraticVariation
#check StatementShape

end Stage1Instances.THM_M_1006
