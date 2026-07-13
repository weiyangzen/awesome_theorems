import Mathlib.GroupTheory.FreeGroup.NielsenSchreier

/-!
# THM-M-0079 discovery-only intake probe

These checks authenticate the pinned free-group vocabulary and the unusually close mathlib
candidate. They do not freeze the repository's canonical expression, perform the downstream anchor
audit, install an accepted wrapper, or prove theorem completion.
-/

#check FreeGroupBasis
#check IsFreeGroup
#check FreeGroupBasis.isFreeGroup
#check subgroupIsFreeOfIsFree

#print axioms subgroupIsFreeOfIsFree

section

universe u

variable {G : Type u} [Group G] [IsFreeGroup G]

/-- Candidate proposition shape and application, validated only for intake feasibility. -/
example (H : Subgroup G) : IsFreeGroup H :=
  subgroupIsFreeOfIsFree H

/-- The literal-carrier encoding is an alternate candidate, not the canonical target. -/
example (X : Type u) (H : Subgroup (FreeGroup X)) : IsFreeGroup H :=
  subgroupIsFreeOfIsFree H

end
