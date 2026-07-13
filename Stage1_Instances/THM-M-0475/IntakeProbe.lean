import Mathlib.FieldTheory.Finite.Basic

/-!
# THM-M-0475 discovery-only intake probe

This file checks pinned interfaces adjacent to Euler's totient theorem and concrete scope
boundaries. It does not select a source-exact target or claim proof credit.
-/

#check Nat.Coprime
#check Nat.ModEq
#check Nat.totient
#check Nat.totient_zero
#check Nat.totient_one
#check ZMod.pow_totient
#check Nat.ModEq.pow_totient

#print axioms Nat.ModEq.pow_totient

example (a n : Nat) (h : a.Coprime n) : a ^ n.totient ≡ 1 [MOD n] :=
  Nat.ModEq.pow_totient h

example (a : Nat) (h : a.Coprime 0) : a ^ Nat.totient 0 ≡ 1 [MOD 0] :=
  Nat.ModEq.pow_totient h

example (a : Nat) : a ^ Nat.totient 1 ≡ 1 [MOD 1] :=
  Nat.ModEq.pow_totient (Nat.coprime_one_right a)

example : Not (2 ^ Nat.totient 4 ≡ 1 [MOD 4]) := by decide
