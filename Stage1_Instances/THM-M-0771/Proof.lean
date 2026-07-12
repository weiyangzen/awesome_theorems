import ObligationTree
import Mathlib.SetTheory.Cardinal.Order

/-!
# THM-M-0771 proof-phase bodies

This module closes the frozen pointwise construction with mathlib's pinned
well-ordering relation, then applies the frozen universal composition to prove
the exact relation-level target.
-/

universe u

namespace Stage1Instances.THM_M_0771

/-- The frozen substantive leaf, supplied by the pinned mathlib construction. -/
theorem wellOrderConstruction_proof (alpha : Type u) :
    ObligationTree.RelationWitness alpha := by
  exact IsWellOrder.subtype_nonempty

/-- Exact proof of the canonical well-ordering target frozen in `Statement.lean`. -/
theorem wellOrderingTheorem_proof : WellOrderingTarget.{u} := by
  exact ObligationTree.root_of_relationWitness wellOrderConstruction_proof

#check wellOrderConstruction_proof
#check wellOrderingTheorem_proof
#print axioms wellOrderConstruction_proof
#print axioms wellOrderingTheorem_proof

end Stage1Instances.THM_M_0771
