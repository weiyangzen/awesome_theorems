import Statement

/-!
# THM-M-0771 frozen obligation interfaces

This module checks only the child-to-parent composition selected by the frozen
architecture. The substantive well-order construction remains an explicit premise.
-/

universe u

namespace Stage1Instances.THM_M_0771.ObligationTree

/-- The substantive leaf: produce a strict well-order witness for one carrier. -/
def RelationWitness (alpha : Type u) : Prop :=
  Nonempty { r : alpha -> alpha -> Prop // IsWellOrder alpha r }

/-- Packaging one witness for every carrier closes the exact universal target. -/
theorem root_of_relationWitness
    (construct : forall alpha : Type u, RelationWitness alpha) :
    WellOrderingTarget.{u} := by
  intro alpha
  exact construct alpha

/-- The leaf interface is definitionally the canonical pointwise conclusion. -/
theorem relationWitness_iff (alpha : Type u) :
    RelationWitness alpha <->
      Nonempty { r : alpha -> alpha -> Prop // IsWellOrder alpha r } :=
  Iff.rfl

end Stage1Instances.THM_M_0771.ObligationTree

#print axioms Stage1Instances.THM_M_0771.ObligationTree.root_of_relationWitness
#print axioms Stage1Instances.THM_M_0771.ObligationTree.relationWitness_iff
