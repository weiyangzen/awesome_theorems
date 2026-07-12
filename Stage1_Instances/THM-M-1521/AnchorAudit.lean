import Mathlib.Dynamics.Ergodic.Conservative
import «Stage1_Instances».«THM-M-1521».Statement

/-!
Kernel witness for the THM-M-1521 anchor audit. This file does not promote the
candidate or claim theorem completion; it checks that the pinned mathlib
declarations compose to the exact statement-phase target.
-/

noncomputable section

open Filter Set

namespace Stage1Instances.THM_M_1521.AnchorAudit

universe u

/-- Exact candidate wrapper over the two terminal mathlib declarations audited here. -/
theorem exactTargetFromPinnedMathlib
    (alpha : Type u) [MeasurableSpace alpha] :
    Stage1Instances.THM_M_1521.PoincareRecurrenceTarget alpha := by
  intro f mu hFinite hf s hs
  letI : MeasureTheory.IsFiniteMeasure mu := hFinite
  exact hf.conservative.ae_mem_imp_frequently_image_mem hs

#check MeasureTheory.MeasurePreserving.conservative
#check MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem
#check MeasureTheory.Conservative.ae_frequently_mem_of_mem_nhds
#check exactTargetFromPinnedMathlib

#print axioms MeasureTheory.MeasurePreserving.conservative
#print axioms MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem
#print axioms exactTargetFromPinnedMathlib

end Stage1Instances.THM_M_1521.AnchorAudit
