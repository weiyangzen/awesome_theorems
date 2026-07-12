import Mathlib.Dynamics.Ergodic.Conservative
import «Stage1_Instances».«THM-M-1521».Statement
import «Stage1_Instances».«THM-M-1521».ObligationTree

/-!
# THM-M-1521 proof execution

This module imports the two pinned mathlib proof bodies identified by the
anchor audit, packages them at the frozen obligation interfaces, and checks
their composition at the exact statement-phase target.
-/

noncomputable section

namespace Stage1Instances.THM_M_1521.Proof

open Filter Set

universe u

/-- Frozen `M1521-L-CONSERVATIVE`: preservation of a finite measure makes the
self-map conservative. The explicit proposition is installed as the typeclass
required by mathlib's pinned bridge. -/
theorem preservingToConservative_proof :
    ObligationTree.PreservingToConservative.{u} := by
  intro alpha _ f mu hFinite hf
  letI : MeasureTheory.IsFiniteMeasure mu := hFinite
  exact hf.conservative

/-- Frozen `M1521-L-RECURRENCE`: conservativity gives almost-everywhere
infinitely frequent return to every null-measurable set. -/
theorem conservativeToSetRecurrence_proof :
    ObligationTree.ConservativeToSetRecurrence.{u} := by
  intro alpha _ f mu hf s hs
  exact hf.ae_mem_imp_frequently_image_mem hs

/-- Exact child-to-parent composition through the frozen obligation tree. -/
theorem poincareRecurrence_proof
    (alpha : Type u) [MeasurableSpace alpha] :
    PoincareRecurrenceTarget alpha :=
  ObligationTree.exactTarget_of_packages
    preservingToConservative_proof conservativeToSetRecurrence_proof alpha

#check preservingToConservative_proof
#check conservativeToSetRecurrence_proof
#check poincareRecurrence_proof

#print axioms MeasureTheory.MeasurePreserving.conservative
#print axioms MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem
#print axioms preservingToConservative_proof
#print axioms conservativeToSetRecurrence_proof
#print axioms poincareRecurrence_proof

end Stage1Instances.THM_M_1521.Proof
