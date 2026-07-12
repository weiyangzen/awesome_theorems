import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Integral.Bochner.Basic

open Filter Function MeasureTheory
open scoped BigOperators

namespace Stage1.THM_M_1053

universe u

/-- The forward Cesaro average through time `n`.  Defining the value at `n = 0` is harmless,
because the target is convergence along `atTop`. -/
noncomputable def timeAverage {X : Type u} (T : X → X) (f : X → ℝ) (n : ℕ) (x : X) : ℝ :=
  (n : ℝ)⁻¹ * ∑ k ∈ Finset.range n, f ((T^[k]) x)

/-- Canonical modern real-valued form of the Birkhoff pointwise ergodic theorem selected by the
THM-M-1053 intake.  The final implication is the ergodic specialization usually summarized as
"time average equals space average". -/
def StatementShape : Prop :=
  ∀ (X : Type u) (_ : MeasurableSpace X) (μ : Measure X) (_ : IsProbabilityMeasure μ)
    (T : X → X),
    MeasurePreserving T μ μ →
      ∀ f : X → ℝ, Integrable f μ →
        ∃ g : X → ℝ,
          Integrable g μ ∧
          g ∘ T =ᵐ[μ] g ∧
          (∀ᵐ x ∂μ, Tendsto (fun n : ℕ => timeAverage T f n x) atTop (nhds (g x))) ∧
          (Ergodic T μ → g =ᵐ[μ] fun _ => ∫ x, f x ∂μ)

-- Structural mutations are elaborated and compared by `check_statement.py`.
def mutationRemovedErgodicIdentification : Prop :=
  ∀ (X : Type u) (_ : MeasurableSpace X) (μ : Measure X) (_ : IsProbabilityMeasure μ)
    (T : X → X), MeasurePreserving T μ μ → ∀ f : X → ℝ, Integrable f μ →
      ∃ g : X → ℝ, Integrable g μ ∧ g ∘ T =ᵐ[μ] g ∧
        ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => timeAverage T f n x) atTop (nhds (g x))

def mutationFiniteMeasureOnly : Prop :=
  ∀ (X : Type u) (_ : MeasurableSpace X) (μ : Measure X) (_ : IsFiniteMeasure μ)
    (T : X → X), MeasurePreserving T μ μ → ∀ f : X → ℝ, Integrable f μ →
      ∃ g : X → ℝ, Integrable g μ ∧ g ∘ T =ᵐ[μ] g ∧
        (∀ᵐ x ∂μ, Tendsto (fun n : ℕ => timeAverage T f n x) atTop (nhds (g x))) ∧
        (Ergodic T μ → g =ᵐ[μ] fun _ => ∫ x, f x ∂μ)

def mutationAssumedConvergence : Prop :=
  ∀ (X : Type u) (_ : MeasurableSpace X) (μ : Measure X) (_ : IsProbabilityMeasure μ)
    (T : X → X), MeasurePreserving T μ μ → ∀ f g : X → ℝ,
      Integrable f μ → Integrable g μ →
      (∀ᵐ x ∂μ, Tendsto (fun n : ℕ => timeAverage T f n x) atTop (nhds (g x))) →
      Ergodic T μ → g =ᵐ[μ] fun _ => ∫ x, f x ∂μ

def mutationNormConvergence : Prop :=
  ∀ (X : Type u) (_ : MeasurableSpace X) (μ : Measure X) (_ : IsProbabilityMeasure μ)
    (T : X → X), MeasurePreserving T μ μ → ∀ f : X → ℝ, Integrable f μ →
      ∃ g : X → ℝ, Integrable g μ ∧ Tendsto
        (fun n : ℕ => ∫ x, |timeAverage T f n x - g x| ∂μ) atTop (nhds 0)

theorem timeAverage_zero {X : Type u} (T : X → X) (f : X → ℝ) (x : X) :
    timeAverage T f 0 x = 0 := by simp [timeAverage]

set_option pp.explicit true in
#print StatementShape

end Stage1.THM_M_1053
