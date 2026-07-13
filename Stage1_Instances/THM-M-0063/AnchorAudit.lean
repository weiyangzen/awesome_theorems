import Mathlib.GroupTheory.Perm.Subgroup

/-!
# THM-M-0063 anchor-audit probes

This module checks the exact pinned mathlib candidate against a literal audit copy of the frozen
Cayley target. The adapter is candidate evidence for this node, not an accepted proof-phase
declaration or theorem-completion receipt.
-/

namespace Stage1Instances.THM_M_0063_AnchorAudit

universe u

/-- Literal audit copy of the statement gate's exact range-subgroup target. -/
def ExactTarget : Prop :=
  forall (G : Type u) [Group G],
    Nonempty (G ≃* (MulAction.toPermHom G G).range)

/-- Exact regular-action specialization of mathlib's generalized Cayley theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u} := by
  intro G _
  exact ⟨Equiv.Perm.subgroupOfMulAction G G⟩

/--
Independent exact construction from the injective regular permutation representation. This uses
the statement imports' lower-level APIs and deduplicates to the same toPerm_injective route.
-/
theorem exactTarget_from_injective_candidate : ExactTarget.{u} := by
  intro G _
  exact ⟨MonoidHom.ofInjective MulAction.toPerm_injective⟩

#check Equiv.Perm.subgroupOfMulAction
#check MulAction.toPerm_injective
#check MonoidHom.ofInjective
#print Equiv.Perm.subgroupOfMulAction
#print axioms Equiv.Perm.subgroupOfMulAction
#print axioms MulAction.toPerm_injective
#print axioms exactTarget_mathlib_candidate
#print axioms exactTarget_from_injective_candidate
#print sorries Equiv.Perm.subgroupOfMulAction
#print sorries exactTarget_mathlib_candidate
#print sorries exactTarget_from_injective_candidate

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0063_AnchorAudit
