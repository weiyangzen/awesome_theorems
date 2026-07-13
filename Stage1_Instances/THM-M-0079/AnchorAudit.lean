import Mathlib.GroupTheory.FreeGroup.NielsenSchreier

/-!
# THM-M-0079 anchor-audit probes

This module checks the exact pinned mathlib candidate against a literal copy of the frozen target.
The wrapper is candidate evidence for the anchor-audit node, not an accepted proof-phase or
theorem-completion declaration.
-/

namespace Stage1Instances.THM_M_0079_AnchorAudit

universe u

/-- Literal audit copy of the statement gate's canonical proposition. -/
def ExactTarget : Prop :=
  forall (G : Type u) [Group G] [IsFreeGroup G],
    forall H : Subgroup G, IsFreeGroup H

/-- Exact adapter from the frozen target to the pinned mathlib theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u} := by
  intro G _ _ H
  exact subgroupIsFreeOfIsFree H

#check subgroupIsFreeOfIsFree
#check IsFreeGroup.ofMulEquiv
#check CategoryTheory.ActionCategory.endMulEquivSubgroup
#check IsFreeGroupoid.actionGroupoidIsFree
#check IsFreeGroupoid.SpanningTree.endIsFree
#check IsFreeGroupoid.endIsFreeOfConnectedFree

#print subgroupIsFreeOfIsFree
#print IsFreeGroupoid.endIsFreeOfConnectedFree
#print IsFreeGroupoid.actionGroupoidIsFree
#print axioms subgroupIsFreeOfIsFree
#print axioms IsFreeGroupoid.endIsFreeOfConnectedFree
#print axioms IsFreeGroupoid.actionGroupoidIsFree
#print axioms IsFreeGroupoid.SpanningTree.endIsFree
#print axioms exactTarget_mathlib_candidate
#print sorries subgroupIsFreeOfIsFree
#print sorries IsFreeGroupoid.endIsFreeOfConnectedFree
#print sorries IsFreeGroupoid.actionGroupoidIsFree
#print sorries IsFreeGroupoid.SpanningTree.endIsFree
#print sorries exactTarget_mathlib_candidate

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0079_AnchorAudit
