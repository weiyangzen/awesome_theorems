import Mathlib.Data.Nat.ChineseRemainder
import Mathlib.Data.ZMod.Basic

/-!
# THM-M-0477 discovery-only intake probe

These commands authenticate materially different Chinese-remainder interfaces in the pinned
mathlib snapshot. They do not select a catalog root, establish source-to-Lean identity, or provide
proof credit for the assigned theorem.
-/

#check Nat.chineseRemainder'
#check Nat.chineseRemainder
#check Nat.chineseRemainder'_lt_lcm
#check Nat.chineseRemainder_lt_mul
#check Nat.chineseRemainder_modEq_unique
#check Nat.chineseRemainderOfList
#check Nat.chineseRemainderOfList_lt_prod
#check Nat.chineseRemainderOfList_modEq_unique
#check Nat.chineseRemainderOfFinset
#check Nat.chineseRemainderOfFinset_lt_prod
#check ZMod.chineseRemainder

#print axioms Nat.chineseRemainder'
#print axioms Nat.chineseRemainderOfList
#print axioms ZMod.chineseRemainder
