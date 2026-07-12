import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def

open MeasureTheory

namespace AwesomeTheorems.THM_M_1082

/-- The exact finite-dimensional-distribution characterization of a Gaussian process. -/
theorem gaussianProcess_iff_finiteDimensionalGaussian
    {Ω E T : Type*} {mΩ : MeasurableSpace Ω}
    [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module ℝ E]
    (X : T → Ω → E) (P : Measure Ω) :
    ProbabilityTheory.IsGaussianProcess X P ↔
      ∀ I : Finset T,
        ProbabilityTheory.HasGaussianLaw (fun ω ↦ I.restrict (X · ω)) P := by
  constructor
  · exact fun h ↦ h.hasGaussianLaw
  · exact fun h ↦ ⟨h⟩

end AwesomeTheorems.THM_M_1082
