import Mathlib.FieldTheory.Finite.Basic

/-! Discovery-only checks for the pinned APIs adjacent to Fermat's little theorem. -/

#check Nat.Prime
#check Nat.Coprime
#check Nat.ModEq
#check ZMod.pow_card_sub_one_eq_one
#check Int.ModEq.pow_card_sub_one_eq_one
#check Int.ModEq.pow_prime_eq_self
#check Nat.ModEq.pow_card_sub_one_eq_one
#check Nat.pow_card_sub_one_sub_one_mod_card

#print axioms Nat.ModEq.pow_card_sub_one_eq_one

example (a p : Nat) (hp : p.Prime) (ha : a.Coprime p) :
    a ^ (p - 1) ≡ 1 [MOD p] :=
  Nat.ModEq.pow_card_sub_one_eq_one hp ha

example (a p : Nat) (hp : p.Prime) (ha : Not (p ∣ a)) :
    a ^ (p - 1) ≡ 1 [MOD p] :=
  Nat.ModEq.pow_card_sub_one_eq_one hp (hp.coprime_iff_not_dvd.mpr ha).symm

theorem prime_coprime_crosswalk (a p : Nat) (hp : p.Prime) :
    a.Coprime p ↔ Not (p ∣ a) := by
  rw [Nat.coprime_comm, hp.coprime_iff_not_dvd]

example (p : Nat) (hp : p.Prime) : Not (p ^ (p - 1) ≡ 1 [MOD p]) := by
  rw [Nat.ModEq, Nat.pow_mod]
  simp [Nat.sub_ne_zero_iff_lt.mpr hp.one_lt, hp.ne_one]
