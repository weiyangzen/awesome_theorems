import Mathlib.Dynamics.Ergodic.Conservative
import «Stage1_Instances».«THM-M-1521».Statement

/-!
An independent exact-target probe for the validation phase.  This deliberately
does not import `Proof` or `ObligationTree`: it reconstructs the short pinned
mathlib composition directly at the canonical statement type.
-/

noncomputable section

namespace Stage1Instances.THM_M_1521.Validation

open Filter Set

universe u

theorem independentPoincareRecurrence
    (alpha : Type u) [MeasurableSpace alpha] :
    PoincareRecurrenceTarget alpha := by
  intro f mu hFinite hf s hs
  letI : MeasureTheory.IsFiniteMeasure mu := hFinite
  exact hf.conservative.ae_mem_imp_frequently_image_mem hs

#check independentPoincareRecurrence
#print axioms independentPoincareRecurrence

end Stage1Instances.THM_M_1521.Validation
