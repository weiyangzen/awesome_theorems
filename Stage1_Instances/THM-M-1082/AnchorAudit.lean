import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def

open MeasureTheory

namespace AwesomeTheorems.THM_M_1082_AnchorAudit

#check ProbabilityTheory.IsGaussianProcess
#check ProbabilityTheory.IsGaussianProcess.hasGaussianLaw

/-- Independent audit probe for the exact mathlib-definition transport used by the frozen target. -/
theorem exactMathlibAnchor
    {Ω E T : Type*} {mΩ : MeasurableSpace Ω}
    [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module ℝ E]
    (X : T → Ω → E) (P : Measure Ω) :
    ProbabilityTheory.IsGaussianProcess X P ↔
      ∀ I : Finset T,
        ProbabilityTheory.HasGaussianLaw (fun ω ↦ I.restrict (X · ω)) P := by
  constructor
  · exact ProbabilityTheory.IsGaussianProcess.hasGaussianLaw
  · exact ProbabilityTheory.IsGaussianProcess.mk

#print axioms exactMathlibAnchor

end AwesomeTheorems.THM_M_1082_AnchorAudit
