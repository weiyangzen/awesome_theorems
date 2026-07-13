import Mathlib.GroupTheory.Perm.Subgroup

/-!
# THM-M-0063 discovery-only intake probe

These checks authenticate the pinned Cayley-theorem interface and its regular-action specialization.
They do not freeze the canonical source statement, create a target wrapper, or claim proof credit.
-/

namespace Stage1Instances.THM_M_0063

#check Equiv.Perm.subgroupOfMulAction
#check MulAction.toPermHom
#check MulAction.toPerm_injective
#check FaithfulSMul
#check Equiv.mulLeft
#check RightCancelMonoid.faithfulSMul

/-- Exact candidate specialization for discovery only; statement acceptance remains downstream. -/
noncomputable example (G : Type*) [Group G] :
    G ≃* (MulAction.toPermHom G G).range :=
  Equiv.Perm.subgroupOfMulAction G G

#print axioms Equiv.Perm.subgroupOfMulAction

end Stage1Instances.THM_M_0063
