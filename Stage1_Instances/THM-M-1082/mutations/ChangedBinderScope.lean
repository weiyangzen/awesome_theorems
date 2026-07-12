import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def
open MeasureTheory
example {Ω E T : Type*} {mΩ : MeasurableSpace Ω}
    [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module ℝ E]
    (X : T → Ω → E) (P : Measure Ω) :
    ProbabilityTheory.HasGaussianLaw (fun ω ↦ I.restrict (X · ω)) P := by
  trivial
