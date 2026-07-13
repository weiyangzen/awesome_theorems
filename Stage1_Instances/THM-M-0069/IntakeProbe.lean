import Mathlib.GroupTheory.SpecificGroups.ZGroup
import Mathlib.GroupTheory.Transfer

/-!
# THM-M-0069 discovery-only intake probe

These checks authenticate pinned solvability, prime-power, Sylow, transfer, and Z-group APIs.
They do not freeze the catalog's missing parameters, prove that a p-alpha q-beta group is a
Z-group, or declare a repo-local THM-M-0069 root theorem.
-/

#check IsSolvable
#check isSolvable_def
#check IsPGroup.of_card
#check IsPGroup.iff_card
#check Sylow.exists_subgroup_card_pow_prime
#check MonoidHom.ker_transferSylow_isComplement'
#check IsZGroup
#check IsZGroup.of_squarefree

#print axioms isSolvable_def
#print axioms IsPGroup.of_card
#print axioms Sylow.exists_subgroup_card_pow_prime
#print axioms MonoidHom.ker_transferSylow_isComplement'

section

variable {G : Type*} [Group G]

example : IsSolvable G ↔ ∃ n : Nat, derivedSeries G n = ⊥ :=
  isSolvable_def G

example [Finite G] [IsZGroup G] : IsSolvable G :=
  inferInstance

end
