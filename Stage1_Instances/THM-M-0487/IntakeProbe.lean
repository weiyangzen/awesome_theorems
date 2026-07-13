import Mathlib.Data.Nat.Prime.Basic

/-!
# THM-M-0487 discovery-only intake probe

These checks authenticate pinned prime, parity, strict-bound, and additive APIs needed to state
weak Goldbach. The boundary example only checks that repeated summands and the even prime must be
representable. This file defines no canonical target and proves no unbounded Goldbach result.
-/

#check Nat.Prime
#check Nat.prime_two
#check Nat.prime_three
#check Odd
#check Nat.not_even_iff_odd
#check Nat.lt_iff_add_one_le

example : 5 < (7 : Nat) := by decide

example : Odd (7 : Nat) := by decide

example :
    Nat.Prime 2 ∧ Nat.Prime 2 ∧ Nat.Prime 3 ∧ (7 : Nat) = 2 + 2 + 3 := by
  exact ⟨Nat.prime_two, Nat.prime_two, Nat.prime_three, rfl⟩

#print axioms Nat.prime_two
#print axioms Nat.prime_three
