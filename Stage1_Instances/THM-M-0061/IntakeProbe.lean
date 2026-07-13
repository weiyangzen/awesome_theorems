import Mathlib.GroupTheory.Coset.Card

/-!
# THM-M-0061 discovery-only intake probe

These checks authenticate the pinned Lagrange declaration and show that it applies while the
catalog's finite-group premise remains explicit. They do not freeze the canonical root, audit the
terminal proof body, or create an accepted THM-M-0061 proof declaration.
-/

#check @Subgroup.card_subgroup_dvd_card
#check @Subgroup.card_eq_card_quotient_mul_card_subgroup
#print axioms Subgroup.card_subgroup_dvd_card

universe u

section

variable {G : Type u} [Group G] [Finite G]

example (H : Subgroup G) : Nat.card H ∣ Nat.card G :=
  H.card_subgroup_dvd_card

example : Nat.card (⊥ : Subgroup G) ∣ Nat.card G :=
  Subgroup.card_subgroup_dvd_card ⊥

example : Nat.card (⊤ : Subgroup G) ∣ Nat.card G :=
  Subgroup.card_subgroup_dvd_card ⊤

end
