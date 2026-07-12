import Mathlib.GroupTheory.SchurZassenhaus
import Mathlib.GroupTheory.Solvable
import Mathlib.GroupTheory.SpecificGroups.ZGroup

/-!
# THM-M-0077 discovery-only intake probe

These checks authenticate the pinned solvability vocabulary and three Hall-adjacent special facts.
They do not define a Hall `pi`-subgroup, state the existence theorem for arbitrary finite solvable
groups, or prove a repository-local THM-M-0077 declaration.
-/

#check IsSolvable
#check isSolvable_def
#check Sylow.card_coprime_index
#check IsZGroup.coprime_commutator_index
#check Subgroup.exists_right_complement'_of_coprime

#print axioms Sylow.card_coprime_index
#print axioms IsZGroup.coprime_commutator_index
#print axioms Subgroup.exists_right_complement'_of_coprime

section

variable {G : Type*} [Group G] [Finite G]

example (p : Nat) [Fact p.Prime] (P : Sylow p G) :
    (Nat.card P).Coprime P.index :=
  P.card_coprime_index

example [IsZGroup G] :
    (Nat.card (commutator G)).Coprime (commutator G).index :=
  IsZGroup.coprime_commutator_index G

example (N : Subgroup G) [N.Normal]
    (hN : Nat.Coprime (Nat.card N) N.index) :
    exists H : Subgroup G, N.IsComplement' H :=
  Subgroup.exists_right_complement'_of_coprime hN

end
