import Statement

/-!
# THM-M-0311 differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
root directly from the pinned `MeasureTheory.Lp` completeness instance so that validation does not
merely replay the proof-phase wrapper.
-/

namespace Stage1Instances.THM_M_0311.Validation

open MeasureTheory
open scoped ENNReal

universe u

/-- Independent source-level reconstruction of the exact frozen target. -/
theorem rieszFischerTarget_direct : RieszFischerTarget.{u} := by
  intro _ _ _
  exact ⟨inferInstance, inferInstance⟩

#check rieszFischerTarget_direct
#print axioms rieszFischerTarget_direct

end Stage1Instances.THM_M_0311.Validation
