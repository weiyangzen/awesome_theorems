import Mathlib.Data.Nat.Choose.Sum

/-!
# THM-M-0911 discovery-only intake probe

These checks authenticate pinned binomial-theorem interfaces, agreement between the commutative
and commuting-elements forms, and representative boundaries. They do not freeze the canonical
target, complete the later anchor/provenance audit, or grant proof credit.
-/

open Nat Finset

#check Nat.choose
#check Commute.add_pow
#check Commute.add_pow'
#check add_pow

#print axioms Commute.add_pow
#print axioms add_pow

example {R : Type*} [CommSemiring R] (a b : R) (n : Nat) :
    (a + b) ^ n = ∑ m ∈ range (n + 1), a ^ m * b ^ (n - m) * n.choose m := by
  exact add_pow a b n

example {R : Type*} [CommSemiring R] (a b : R) (n : Nat) :
    (Commute.all a b).add_pow n = add_pow a b n := rfl

example :
    (2 + 3 : Nat) ^ 0 = ∑ m ∈ range (0 + 1), 2 ^ m * 3 ^ (0 - m) * Nat.choose 0 m := by
  exact add_pow 2 3 0

example :
    (2 + 3 : Nat) ^ 2 = ∑ m ∈ range (2 + 1), 2 ^ m * 3 ^ (2 - m) * Nat.choose 2 m := by
  exact add_pow 2 3 2

example :
    (2 + 3 : Nat) ^ 2 =
      ∑ m ∈ antidiagonal 2, Nat.choose 2 m.1 • (2 ^ m.1 * 3 ^ m.2) := by
  exact (Commute.all 2 3).add_pow' 2
