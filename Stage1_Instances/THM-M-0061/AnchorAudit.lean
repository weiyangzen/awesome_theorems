import Mathlib.GroupTheory.Coset.Card

/-!
# THM-M-0061 anchor-audit probes

This file checks the pinned mathlib Lagrange candidate against a literal copy of the frozen
finite-group target. The wrapper is candidate evidence for this audit node, not an accepted
proof-phase or theorem-completion declaration.
-/

noncomputable section

namespace Stage1Instances.THM_M_0061_AnchorAudit

universe u

/-- Literal audit copy of the frozen canonical proposition. -/
def ExactTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G] (H : Subgroup G),
    Nat.card H ∣ Nat.card G

/-- Exact finite-scope adapter to the stronger pinned mathlib theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u} := by
  intro G _ _ H
  exact Subgroup.card_subgroup_dvd_card H

#check Subgroup.card_subgroup_dvd_card
#check Subgroup.card_eq_card_quotient_mul_card_subgroup
#check AddSubgroup.card_addSubgroup_dvd_card
#print Subgroup.card_subgroup_dvd_card
#print Subgroup.card_eq_card_quotient_mul_card_subgroup
#print axioms Subgroup.card_subgroup_dvd_card
#print axioms Subgroup.card_eq_card_quotient_mul_card_subgroup
#print axioms AddSubgroup.card_addSubgroup_dvd_card
#print axioms exactTarget_mathlib_candidate

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0061_AnchorAudit
