import ObligationTree
import Mathlib.Analysis.InnerProductSpace.LaxMilgram

/-!
# THM-M-0329 proof-phase bodies

This module binds the two frozen root-critical packages to the pinned mathlib
implementation and composes them through `root_of_packages`.  The resulting
theorem has exactly the target defined in `Statement.lean`.
-/

noncomputable section

namespace Stage1Instances.THM_M_0329

open InnerProductSpace

universe u

/-- Riesz representation for the arbitrary continuous functional datum. -/
theorem rieszPackage : ObligationTree.RieszPackage.{u} := by
  intro V _ _ _ F
  refine ⟨(toDual Real V).symm F, ?_⟩
  intro v
  simp

/-- The coercive bilinear form induces the continuous linear equivalence used
by the frozen operator package. -/
theorem operatorPackage : ObligationTree.OperatorPackage.{u} := by
  intro V _ _ _ B hB
  exact ⟨hB.continuousLinearEquivOfBilin,
    fun u v => hB.continuousLinearEquivOfBilin_apply u v⟩

/-- Exact Lax-Milgram root, composed through the frozen package interface. -/
theorem laxMilgram : LaxMilgramTarget.{u} :=
  ObligationTree.root_of_packages rieszPackage operatorPackage

#print axioms rieszPackage
#print axioms operatorPackage
#print axioms laxMilgram

end Stage1Instances.THM_M_0329
