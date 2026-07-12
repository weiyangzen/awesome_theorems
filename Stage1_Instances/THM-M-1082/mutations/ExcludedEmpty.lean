import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def
open MeasureTheory
example {Ω E T : Type*} {mΩ : MeasurableSpace Ω}
    [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module ℝ E]
    (X : T → Ω → E) (P : Measure Ω)
    (h : ∀ I : Finset T, I.Nonempty →
      ProbabilityTheory.HasGaussianLaw (fun ω ↦ I.restrict (X · ω)) P) :
    ProbabilityTheory.IsGaussianProcess X P := by
  exact ⟨fun I ↦ h I⟩
