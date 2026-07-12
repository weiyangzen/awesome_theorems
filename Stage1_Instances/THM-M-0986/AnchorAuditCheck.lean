import Mathlib.Probability.StrongLaw

/-! A narrow elaboration check for the pinned mathlib candidate audited for THM-M-0986. -/

noncomputable section

open Filter Finset MeasureTheory
open scoped BigOperators MeasureTheory ProbabilityTheory Topology Function

namespace Stage1Instances.THM_M_0986.AnchorAudit

universe u

/-- Exact adapter from mathlib's stronger almost-sure law to the frozen real-valued target. -/
theorem exactTarget_from_strong_law
    (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real)
    (hint : Integrable (X 0) mu)
    (hindep : Pairwise ((fun f g => ProbabilityTheory.IndepFun f g mu) on X))
    (hident : forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) :
    TendstoInMeasure mu
      (fun (n : Nat) omega => (n : Real)⁻¹ * ∑ i ∈ range n, X i omega)
      atTop (fun _omega => mu[X 0]) := by
  have hmeas : forall i, AEStronglyMeasurable (X i) mu := fun i =>
    (hident i).aestronglyMeasurable_iff.2 hint.1
  have havg (n : Nat) :
      AEStronglyMeasurable
        (fun omega => (n : Real)⁻¹ * ∑ i ∈ range n, X i omega) mu := by
    simpa only [smul_eq_mul] using AEStronglyMeasurable.const_smul
      (aestronglyMeasurable_fun_sum (range n) fun i _ => hmeas i) (n : Real)⁻¹
  exact tendstoInMeasure_of_tendsto_ae havg
    (ProbabilityTheory.strong_law_ae X hint hindep hident)

end Stage1Instances.THM_M_0986.AnchorAudit

#print axioms Stage1Instances.THM_M_0986.AnchorAudit.exactTarget_from_strong_law
