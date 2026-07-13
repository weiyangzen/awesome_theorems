import Mathlib.GroupTheory.Focal

/-!
# THM-M-0073 discovery-only intake probe

These checks authenticate pinned finite-group conjugacy, Sylow, transfer, and focal-subgroup
interfaces adjacent to classical fusion arguments. They do not define a fusion system or an
essential subgroup, select an exact Goldschmidt theorem, declare a canonical target, or claim
proof credit.
-/

#check IsConj
#check isConj_iff
#check Sylow
#check Sylow.smul_eq_iff_mem_normalizer
#check Sylow.conj_eq_normalizer_conj_of_mem
#check Subgroup.normalizerMonoidHom
#check MonoidHom.transfer
#check Subgroup.focalSubgroup
#check Subgroup.transferFocal
#check Subgroup.commutator_inf_eq_focalSubgroup

#print axioms Sylow.conj_eq_normalizer_conj_of_mem
#print axioms Subgroup.commutator_inf_eq_focalSubgroup

section AdjacentFiniteGroupBoundary

variable {G : Type*} [Group G] {p : ℕ} [Fact p.Prime]

example {x y : G} (h : IsConj x y) : IsConj y x :=
  h.symm

example (P : Sylow p G) {g : G} :
    g • P = P ↔ g ∈ Subgroup.normalizer (P : Subgroup G) :=
  Sylow.smul_eq_iff_mem_normalizer

end AdjacentFiniteGroupBoundary
