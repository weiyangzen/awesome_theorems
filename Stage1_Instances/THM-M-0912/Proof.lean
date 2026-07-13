import Statement
import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0912 proof execution

This module installs the manifest-pinned Pascal recurrence at the interfaces
in the frozen obligation tree and composes those interfaces into the exact
DLMF-constrained target. The direct pinned route and the expanded-child route
share the same mathlib proof family and receive no duplicate proof credit.
-/

namespace Stage1Instances.THM_M_0912.Proof

open Stage1Instances.THM_M_0912
open Stage1Instances.THM_M_0912.ObligationTree

/-! Exact implementations of the two leaves exposed by the pinned body. -/

/-- Represent a positive column as a successor
(`M0912-L-POSITIVE-COLUMN-REINDEX`). -/
theorem positiveColumnReindex_proof : PositiveColumnReindex := by
  intro n hn
  exact Nat.exists_eq_add_of_le' hn

/-- Install the pinned successor-column recurrence
(`M0912-L-CHOOSE-SUCC-RIGHT`). -/
theorem chooseSuccRight_proof : ChooseSuccRightAnchor := by
  intro m k hm
  exact Nat.choose_succ_right m k hm

/-- Compose the two exposed children into the predecessor recurrence. -/
theorem predecessorRecurrence_from_frozen_children :
    PredecessorRecurrenceAnchor :=
  predecessorRecurrence_of_chooseSuccRight_and_reindex
    positiveColumnReindex_proof chooseSuccRight_proof

/-- Adopt the exact audited terminal declaration from pinned mathlib
(`M0912-T-PREDECESSOR-COMPOSE`). -/
theorem predecessorRecurrence_pinned : PredecessorRecurrenceAnchor := by
  intro m n hm hn
  exact Nat.choose_eq_choose_pred_add hm hn

/-- Compose row positivity, the pinned predecessor body, and summand order
through the frozen root interface. -/
theorem root_via_pinned_composition : Root :=
  root_of_bridges_and_predecessorAnchor positiveRowBridge_checked
    predecessorRecurrence_pinned summandOrderBridge_checked

/-- Independently exercise the frozen expansion of the pinned predecessor
body through both registered children. -/
theorem root_via_frozen_children : Root :=
  root_of_bridges_and_predecessorAnchor positiveRowBridge_checked
    predecessorRecurrence_from_frozen_children summandOrderBridge_checked

/-- Exact canonical root proof through the audited pinned declaration. -/
theorem pascalIdentityTarget_proof : PascalIdentityTarget :=
  root_via_pinned_composition

/-- Exact canonical root cross-check through every frozen proof child. -/
theorem pascalIdentityTarget_via_frozen_children : PascalIdentityTarget :=
  root_via_frozen_children

assert_no_sorry Nat.choose_succ_right
assert_no_sorry Nat.choose_eq_choose_pred_add
assert_no_sorry positiveColumnReindex_proof
assert_no_sorry chooseSuccRight_proof
assert_no_sorry predecessorRecurrence_from_frozen_children
assert_no_sorry predecessorRecurrence_pinned
assert_no_sorry root_via_pinned_composition
assert_no_sorry root_via_frozen_children
assert_no_sorry pascalIdentityTarget_proof
assert_no_sorry pascalIdentityTarget_via_frozen_children

#print sorries Nat.choose_succ_right
#print sorries Nat.choose_eq_choose_pred_add
#print sorries positiveColumnReindex_proof
#print sorries chooseSuccRight_proof
#print sorries predecessorRecurrence_from_frozen_children
#print sorries predecessorRecurrence_pinned
#print sorries root_via_pinned_composition
#print sorries root_via_frozen_children
#print sorries pascalIdentityTarget_proof
#print sorries pascalIdentityTarget_via_frozen_children

#print axioms Nat.choose_succ_right
#print axioms Nat.choose_eq_choose_pred_add
#print axioms positiveColumnReindex_proof
#print axioms chooseSuccRight_proof
#print axioms predecessorRecurrence_from_frozen_children
#print axioms predecessorRecurrence_pinned
#print axioms root_via_pinned_composition
#print axioms root_via_frozen_children
#print axioms pascalIdentityTarget_proof
#print axioms pascalIdentityTarget_via_frozen_children

end Stage1Instances.THM_M_0912.Proof
