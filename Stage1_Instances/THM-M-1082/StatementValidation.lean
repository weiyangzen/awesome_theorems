import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def

open MeasureTheory

namespace AwesomeTheorems.THM_M_1082_Validation

theorem canonicalTarget
    {Ω E T : Type*} {mΩ : MeasurableSpace Ω}
    [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module ℝ E]
    (X : T → Ω → E) (P : Measure Ω) :
    ProbabilityTheory.IsGaussianProcess X P ↔
      ∀ I : Finset T,
        ProbabilityTheory.HasGaussianLaw (fun ω ↦ I.restrict (X · ω)) P := by
  constructor
  · exact fun h ↦ h.hasGaussianLaw
  · exact fun h ↦ ⟨h⟩

set_option pp.universes true in
set_option pp.explicit true in
#print canonicalTarget

end AwesomeTheorems.THM_M_1082_Validation
