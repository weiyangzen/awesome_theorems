import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def
open MeasureTheory
example {Ω E T : Type*} {mΩ : MeasurableSpace Ω} {mT : MeasurableSpace T}
    [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module ℝ E]
    (X : T → Ω → E) (P : Measure T) :
    ProbabilityTheory.IsGaussianProcess X P := by
  exact ⟨fun _ ↦ by trivial⟩
