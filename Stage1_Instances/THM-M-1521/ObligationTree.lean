import Mathlib.Dynamics.Ergodic.Conservative
import «Stage1_Instances».«THM-M-1521».Statement

/-!
Conditional composition certificate for the frozen THM-M-1521 obligation
architecture. The two central imported-theorem packages remain explicit
premises here; this file does not claim root proof acceptance.
-/

noncomputable section

namespace Stage1Instances.THM_M_1521.ObligationTree

open Filter Set

universe u

/-- The finite-measure bridge from preservation to conservativity. -/
def PreservingToConservative : Prop :=
  forall (alpha : Type u) [MeasurableSpace alpha]
    (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
      MeasureTheory.IsFiniteMeasure mu ->
        MeasureTheory.MeasurePreserving f mu mu ->
          MeasureTheory.Conservative f mu

/-- The recurrence engine for an arbitrary conservative system. -/
def ConservativeToSetRecurrence : Prop :=
  forall (alpha : Type u) [MeasurableSpace alpha]
    (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
      MeasureTheory.Conservative f mu ->
        Stage1Instances.THM_M_1521.SetRecurrenceConclusion f mu

/-- Checked child-to-parent composition into the exact statement target. -/
theorem exactTarget_of_packages
    (preserving : PreservingToConservative.{u})
    (recurrence : ConservativeToSetRecurrence.{u})
    (alpha : Type u) [MeasurableSpace alpha] :
    Stage1Instances.THM_M_1521.PoincareRecurrenceTarget alpha := by
  intro f mu hFinite hf
  exact recurrence alpha f mu (preserving alpha f mu hFinite hf)

#check exactTarget_of_packages
#print axioms exactTarget_of_packages

end Stage1Instances.THM_M_1521.ObligationTree
