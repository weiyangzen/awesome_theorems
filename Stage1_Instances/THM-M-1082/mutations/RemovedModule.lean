import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def
open MeasureTheory
example {Ω E T : Type*} {mΩ : MeasurableSpace Ω}
    [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E]
    (X : T → Ω → E) (P : Measure Ω) :
    ProbabilityTheory.IsGaussianProcess X P := by
  exact ⟨fun _ ↦ by trivial⟩
