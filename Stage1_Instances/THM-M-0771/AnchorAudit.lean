import Mathlib.SetTheory.Cardinal.Order

/-!
# THM-M-0771 anchor audit

This module checks the two pinned mathlib candidates against the statement phase's exact
relation-level and bundled formulations. It inventories upstream closure; it is not the target's
proof-phase module.
-/

universe u

namespace Stage1Instances.THM_M_0771.AnchorAudit

def RelationTarget : Prop :=
  ∀ alpha : Type u, Nonempty { r : alpha → alpha → Prop // IsWellOrder alpha r }

def BundledTarget : Prop :=
  ∀ alpha : Type u, ∃ _ : LinearOrder alpha, WellFoundedLT alpha

/-- Exact relation-level candidate supplied by the pinned mathlib instance. -/
theorem mathlib_relation_candidate : RelationTarget.{u} := by
  intro alpha
  exact IsWellOrder.subtype_nonempty

/-- Bundled candidate supplied by the pinned mathlib theorem. -/
theorem mathlib_bundled_candidate : BundledTarget.{u} := by
  intro alpha
  exact exists_wellOrder alpha

end Stage1Instances.THM_M_0771.AnchorAudit

#check @WellOrderingRel
#check @WellOrderingRel.isWellOrder
#check @IsWellOrder.subtype_nonempty
#check @exists_wellOrder
#print axioms Stage1Instances.THM_M_0771.AnchorAudit.mathlib_relation_candidate
#print axioms Stage1Instances.THM_M_0771.AnchorAudit.mathlib_bundled_candidate
#print axioms IsWellOrder.subtype_nonempty
#print axioms exists_wellOrder

