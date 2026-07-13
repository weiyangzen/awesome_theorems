import Mathlib.Combinatorics.Enumerative.Bell
import Mathlib.Combinatorics.Enumerative.Stirling

/-!
# THM-M-0923 discovery-only intake probe

These commands authenticate pinned Bell and Stirling definitions, recurrence candidates, and their
trust surface. They do not select a canonical set-partition proposition, establish a cardinality
interpretation, declare the THM-M-0923 target, or grant proof credit.
-/

#check Nat.bell
#check Nat.bell_succ
#check Nat.bell_succ'
#check Nat.bell_zero
#check Nat.bell_one
#check Nat.bell_two
#check Multiset.bell
#check Multiset.bell_mul_eq
#check Nat.uniformBell
#check Nat.stirlingSecond
#check Nat.stirlingSecond_succ_succ

#print Nat.bell
#print Nat.bell_succ
#print axioms Nat.bell_succ
#print axioms Multiset.bell_mul_eq
#print axioms Nat.stirlingSecond_succ_succ
