import Mathlib.NumberTheory.Bertrand

/-!
# THM-M-0481 discovery-only intake probe

These checks authenticate the pinned Bertrand statement and adjacent proof-architecture APIs. They
do not select a source-faithful canonical target, audit terminal proof provenance, or add a proof.
-/

#check Nat.Prime
#check Nat.exists_prime_lt_and_le_two_mul
#check Nat.bertrand
#check Nat.exists_prime_lt_and_le_two_mul_eventually
#check Nat.exists_prime_lt_and_le_two_mul_succ

example (n : Nat) (hn : n ≠ 0) :
    Exists fun p => Nat.Prime p ∧ n < p ∧ p <= 2 * n :=
  Nat.exists_prime_lt_and_le_two_mul n hn

example : Exists fun p => Nat.Prime p ∧ 1 < p ∧ p <= 2 * 1 := by
  exact Nat.exists_prime_lt_and_le_two_mul 1 (by decide)

example : Not (Exists fun p => Nat.Prime p ∧ 0 < p ∧ p <= 2 * 0) := by
  simp

example : Not (Exists fun p => Nat.Prime p ∧ 1 < p ∧ p < 2 * 1) := by
  simp
