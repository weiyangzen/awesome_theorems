import Statement

/-!
# THM-M-0986 independent validation probe

This module reconstructs the exact frozen root without importing `Proof.lean`
or its package composition. It directly specializes the pinned mathlib strong
law and supplies the measurability premise of the AE-to-in-measure bridge.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped BigOperators MeasureTheory ProbabilityTheory Topology Function

namespace Stage1Instances.THM_M_0986.Validation

universe u

/-- A separately written kernel check of the exact frozen weak-law target. -/
theorem independentKhinchinWeakLaw :
    Stage1Instances.THM_M_0986.KhinchinWeakLawTarget.{u} := by
  intro Omega _ mu _ X hint hindep hident
  have hmeas : forall i, AEStronglyMeasurable (X i) mu := fun i =>
    (hident i).aestronglyMeasurable_iff.2 hint.1
  apply tendstoInMeasure_of_tendsto_ae
  · intro n
    unfold Stage1Instances.THM_M_0986.empiricalAverage
    exact AEStronglyMeasurable.const_mul
      (aestronglyMeasurable_fun_sum (range n) fun i _ => hmeas i) (n : Real)⁻¹
  · simpa only [Stage1Instances.THM_M_0986.empiricalAverage, smul_eq_mul] using
      (ProbabilityTheory.strong_law_ae X hint hindep hident)

#print axioms independentKhinchinWeakLaw

end Stage1Instances.THM_M_0986.Validation
