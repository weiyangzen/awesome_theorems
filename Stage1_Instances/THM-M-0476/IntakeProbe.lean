import Mathlib.NumberTheory.Wilson

/-!
# THM-M-0476 discovery-only intake probe

These checks authenticate pinned Wilson-theorem interfaces, an explicit-primality wrapper, and
representative boundary behavior. They do not freeze the canonical target, complete the later
anchor/provenance audit, or grant proof credit.
-/

open scoped Nat

#check Nat.Prime
#check Nat.factorial
#check ZMod.wilsons_lemma
#check ZMod.prod_Ico_one_prime
#check Nat.prime_of_fac_equiv_neg_one
#check Nat.prime_iff_fac_equiv_neg_one

#print axioms ZMod.wilsons_lemma
#print axioms Nat.prime_iff_fac_equiv_neg_one

example (p : Nat) (hp : p.Prime) : ((p - 1)! : ZMod p) = -1 := by
  letI : Fact p.Prime := ⟨hp⟩
  exact ZMod.wilsons_lemma p

example : ((2 - 1)! : ZMod 2) = -1 := by decide

example : Not (((4 - 1)! : ZMod 4) = -1) := by decide

example : ((1 - 1)! : ZMod 1) = -1 := Subsingleton.elim _ _
