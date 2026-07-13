import Mathlib.Data.Nat.Choose.Basic

/-!
# THM-M-0912 immutable mathlib anchor audit

This module repeats the frozen constrained Pascal-identity target literally and checks two exact
adapters through declarations in the manifest-pinned mathlib revision. It is candidate evidence
for `S56-M-0912-ANCHOR_AUDIT`, not proof-phase adoption or theorem-completion evidence.
-/

namespace Stage1Instances.THM_M_0912_AnchorAudit

/-- Literal audit copy of the statement-phase proposition. -/
def ExactTarget : Prop :=
  forall (m n : Nat), n <= m -> 1 <= n ->
    Nat.choose m n =
      Nat.choose (m - 1) n + Nat.choose (m - 1) (n - 1)

/-- Exact adapter through mathlib's positive-index predecessor recurrence. -/
theorem exactTarget_mathlib_predecessor : ExactTarget := by
  intro m n hnm hn
  have hm : 0 < m := lt_of_lt_of_le hn hnm
  simpa only [Nat.add_comm] using Nat.choose_eq_choose_pred_add hm hn

/-- Independent exact adapter through the definitionally proved successor recurrence. -/
theorem exactTarget_mathlib_successor : ExactTarget := by
  intro m n hnm hn
  have hm : 0 < m := lt_of_lt_of_le hn hnm
  obtain ⟨r, rfl⟩ := Nat.exists_eq_add_of_le' hm
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le' hn
  simpa only [Nat.add_comm, Nat.add_one_sub_one] using Nat.choose_succ_succ' r k

#check Nat.choose
#check @Nat.choose_succ_succ
#check @Nat.choose_succ_succ'
#check @Nat.choose_succ_left
#check @Nat.choose_succ_right
#check @Nat.choose_eq_choose_pred_add

#print Nat.choose
#print Nat.choose_succ_succ
#print Nat.choose_succ_succ'
#print Nat.choose_succ_left
#print Nat.choose_succ_right
#print Nat.choose_eq_choose_pred_add

#print axioms Nat.choose_succ_succ
#print axioms Nat.choose_succ_succ'
#print axioms Nat.choose_succ_left
#print axioms Nat.choose_succ_right
#print axioms Nat.choose_eq_choose_pred_add
#print axioms exactTarget_mathlib_predecessor
#print axioms exactTarget_mathlib_successor

#print sorries Nat.choose_succ_succ
#print sorries Nat.choose_succ_succ'
#print sorries Nat.choose_succ_left
#print sorries Nat.choose_succ_right
#print sorries Nat.choose_eq_choose_pred_add
#print sorries exactTarget_mathlib_predecessor
#print sorries exactTarget_mathlib_successor

set_option pp.explicit true in
set_option pp.universes true in
#print ExactTarget

end Stage1Instances.THM_M_0912_AnchorAudit
