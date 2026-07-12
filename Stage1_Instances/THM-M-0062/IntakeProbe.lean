import Mathlib.GroupTheory.Sylow

/-!
# THM-M-0062 discovery-only intake probe

These checks authenticate pinned definitions and declarations adjacent to all three Sylow theorem
branches. The examples show that the APIs compose under a finite group and a prime. They do not
freeze the canonical combined target, audit proof bodies, or prove a repo-local THM-M-0062 wrapper.
-/

open MulAction

#check Sylow
#check IsPGroup.exists_le_sylow
#check Sylow.nonempty
#check Sylow.exists_subgroup_card_pow_prime
#check Sylow.card_eq_multiplicity
#check Sylow.isPretransitive_of_finite
#check MulAction.exists_smul_eq
#check card_sylow_modEq_one
#check Sylow.card_dvd_index
#check Sylow.card_eq_index_normalizer

#print axioms Sylow.exists_subgroup_card_pow_prime
#print axioms Sylow.isPretransitive_of_finite
#print axioms card_sylow_modEq_one
#print axioms Sylow.card_dvd_index
#print axioms Sylow.card_eq_multiplicity

section

variable {G : Type*} [Group G] [Finite G] (p : Nat) [Fact p.Prime]

example : Nonempty (Sylow p G) := Sylow.nonempty

example (P Q : Sylow p G) : ∃ g : G, g • P = Q :=
  MulAction.exists_smul_eq G P Q

example : Nat.card (Sylow p G) ≡ 1 [MOD p] :=
  card_sylow_modEq_one p G

example (P : Sylow p G) : Nat.card (Sylow p G) ∣ P.index :=
  P.card_dvd_index

example (P : Sylow p G) :
    Nat.card (Sylow p G) = (Subgroup.normalizer (P : Set G)).index :=
  P.card_eq_index_normalizer

example (P : Sylow p G) :
    Nat.card P = p ^ (Nat.card G).factorization p :=
  P.card_eq_multiplicity

end
