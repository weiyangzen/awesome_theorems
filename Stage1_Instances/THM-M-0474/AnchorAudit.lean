import Mathlib.FieldTheory.Finite.Basic
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0474 immutable mathlib anchor

This module independently restates the frozen natural-number target and checks
the exact adapter to the manifest-pinned mathlib declaration. It is evidence
for the anchor-audit phase only, not the proof-phase canonical declaration.
-/

namespace Stage1Instances.THM_M_0474.AnchorAudit

/-- Literal audit copy of the frozen target. -/
def ExactTarget : Prop :=
  forall (p a : Nat), p.Prime -> a.Coprime p ->
    a ^ (p - 1) ≡ 1 [MOD p]

/-- Exact candidate wrapper over pinned mathlib. -/
theorem exactTarget_mathlib_candidate : ExactTarget := by
  intro p a hp ha
  exact Nat.ModEq.pow_card_sub_one_eq_one hp ha

#check Nat.ModEq.pow_card_sub_one_eq_one
#check Int.ModEq.pow_card_sub_one_eq_one
#check ZMod.pow_card_sub_one_eq_one
#check FiniteField.pow_card_sub_one_eq_one

assert_no_sorry Nat.ModEq.pow_card_sub_one_eq_one
assert_no_sorry exactTarget_mathlib_candidate
#print sorries Nat.ModEq.pow_card_sub_one_eq_one exactTarget_mathlib_candidate
#print axioms Nat.ModEq.pow_card_sub_one_eq_one
#print axioms exactTarget_mathlib_candidate
#print exactTarget_mathlib_candidate

end Stage1Instances.THM_M_0474.AnchorAudit
