import Mathlib.Probability.StrongLaw

/-!
# Exact statement for THM-M-0985

This module freezes the real-valued iid, finite-first-moment Kolmogorov strong
law target. It deliberately contains no proof of the target.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THMM0985

universe u

/-- The arithmetic mean of the first `n` random variables. At `n = 0` this is
zero; that value does not affect convergence along `atTop`. -/
def arithmeticMean {Ω : Type u} (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  (n : ℝ)⁻¹ * ∑ i ∈ range n, X i ω

/--
The exact real-valued iid Kolmogorov strong law: measurable, mutually
independent, identically distributed random variables with finite first
absolute moment have sample averages converging almost surely to their common
expectation.
-/
def KolmogorovStrongLaw : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
      (X : ℕ → Ω → ℝ),
    (∀ n, Measurable (X n)) →
    ProbabilityTheory.iIndepFun X μ →
    (∀ n, ProbabilityTheory.IdentDistrib (X n) (X 0) μ μ) →
    Integrable (X 0) μ →
    ∀ᵐ ω ∂μ,
      Tendsto (fun n : ℕ => arithmeticMean X n ω) atTop (𝓝 (∫ x, X 0 x ∂μ))

/-- Checked definitional expansion fixing universes, binder order, assumptions,
indexing, convergence mode, and the expectation convention. -/
theorem kolmogorovStrongLaw_iff :
    KolmogorovStrongLaw.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
          (X : ℕ → Ω → ℝ),
        (∀ n, Measurable (X n)) →
        ProbabilityTheory.iIndepFun X μ →
        (∀ n, ProbabilityTheory.IdentDistrib (X n) (X 0) μ μ) →
        Integrable (X 0) μ →
        ∀ᵐ ω ∂μ,
          Tendsto
            (fun n : ℕ => (n : ℝ)⁻¹ * ∑ i ∈ range n, X i ω)
            atTop (𝓝 (∫ x, X 0 x ∂μ)) :=
  Iff.rfl

/-- Boundary check for the chosen zero-indexed arithmetic mean. -/
theorem arithmeticMean_zero {Ω : Type u} (X : ℕ → Ω → ℝ) (ω : Ω) :
    arithmeticMean X 0 ω = 0 := by
  simp [arithmeticMean]

/-- The first nonempty average is exactly the zeroth random variable. -/
theorem arithmeticMean_one {Ω : Type u} (X : ℕ → Ω → ℝ) (ω : Ω) :
    arithmeticMean X 1 ω = X 0 ω := by
  simp [arithmeticMean]

namespace MutationProbes

/-- Removed-hypothesis probe: measurability is intentionally absent. -/
def WithoutMeasurability : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
      (X : ℕ → Ω → ℝ),
    ProbabilityTheory.iIndepFun X μ →
    (∀ n, ProbabilityTheory.IdentDistrib (X n) (X 0) μ μ) →
    Integrable (X 0) μ →
    ∀ᵐ ω ∂μ, Tendsto (fun n : ℕ => arithmeticMean X n ω) atTop (𝓝 (∫ x, X 0 x ∂μ))

/-- Changed-domain probe: the random variables are integer-valued. -/
def IntegerValued : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
      (X : ℕ → Ω → ℤ), X = X

/-- Binder-scope probe: identical distribution is asserted only eventually. -/
def EventuallyIdenticallyDistributed : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
      (X : ℕ → Ω → ℝ),
    (∀ᶠ n in atTop, ProbabilityTheory.IdentDistrib (X n) (X 0) μ μ) → True

/-- Boundary probe: one-based sums differ from the canonical first-`n` range. -/
def OneBasedMean {Ω : Type u} (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  (n : ℝ)⁻¹ * ∑ i ∈ Icc 1 n, X i ω

end MutationProbes

set_option pp.universes true in
set_option pp.explicit true in
#print KolmogorovStrongLaw

end Stage1Instances.THMM0985
