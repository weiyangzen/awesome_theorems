import Mathlib.Data.Nat.Choose.Basic

/-!
# THM-M-0912 conditional obligation composition

This module checks the child-to-parent interfaces frozen by the obligation
registry.  The imported recurrence remains an explicit premise, so this phase
does not install the audited mathlib candidate as the canonical proof.
-/

namespace Stage1Instances.THM_M_0912.ObligationTree

/-- Architecture-local literal copy of the frozen DLMF-constrained target. -/
def Root : Prop :=
  forall (m n : Nat), n <= m -> 1 <= n ->
    Nat.choose m n =
      Nat.choose (m - 1) n + Nat.choose (m - 1) (n - 1)

/-- The positivity normalization consumed by the predecessor recurrence. -/
def PositiveRowBridge : Prop :=
  forall (m n : Nat), n <= m -> 1 <= n -> 0 < m

/-- The pinned theorem's exact predecessor-form interface. -/
def PredecessorRecurrenceAnchor : Prop :=
  forall (m n : Nat), 0 < m -> 0 < n ->
    Nat.choose m n =
      Nat.choose (m - 1) (n - 1) + Nat.choose (m - 1) n

/-- Positive columns can be represented as a successor without changing them. -/
def PositiveColumnReindex : Prop :=
  forall n : Nat, 0 < n -> exists k : Nat, n = k + 1

/-- The row-positive successor-column recurrence used by the terminal body. -/
def ChooseSuccRightAnchor : Prop :=
  forall (m k : Nat), 0 < m ->
    Nat.choose m (k + 1) =
      Nat.choose (m - 1) k + Nat.choose (m - 1) (k + 1)

/-- The summand-order transport needed to return to the source display. -/
def SummandOrderBridge : Prop :=
  forall (a b c : Nat), a = b + c -> a = c + b

/-- Checked normalization from the source domain to a positive row. -/
theorem positiveRowBridge_checked : PositiveRowBridge := by
  intro m n hnm hn
  exact lt_of_lt_of_le hn hnm

/-- Checked commutative transport across the source/mathlib summand order. -/
theorem summandOrderBridge_checked : SummandOrderBridge := by
  intro a b c h
  simpa only [Nat.add_comm] using h

/-- Checked composition of the two material children in the pinned theorem body. -/
theorem predecessorRecurrence_of_chooseSuccRight_and_reindex
    (reindex : PositiveColumnReindex)
    (chooseSuccRight : ChooseSuccRightAnchor) : PredecessorRecurrenceAnchor := by
  intro m n hm hn
  obtain ⟨k, rfl⟩ := reindex n hn
  simpa only [Nat.add_one_sub_one] using chooseSuccRight m k hm

/-- Checked root composition. Every mathematical proof child stays explicit. -/
theorem root_of_bridges_and_predecessorAnchor
    (positiveRow : PositiveRowBridge)
    (anchor : PredecessorRecurrenceAnchor)
    (summandOrder : SummandOrderBridge) : Root := by
  intro m n hnm hn
  exact summandOrder _ _ _ (anchor m n (positiveRow m n hnm hn) hn)

#check @Nat.choose_eq_choose_pred_add
#print axioms positiveRowBridge_checked
#print axioms summandOrderBridge_checked
#print axioms predecessorRecurrence_of_chooseSuccRight_and_reindex
#print axioms root_of_bridges_and_predecessorAnchor
#print sorries positiveRowBridge_checked
#print sorries summandOrderBridge_checked
#print sorries predecessorRecurrence_of_chooseSuccRight_and_reindex
#print sorries root_of_bridges_and_predecessorAnchor

set_option pp.universes true in
set_option pp.explicit true in
#print Root

end Stage1Instances.THM_M_0912.ObligationTree
