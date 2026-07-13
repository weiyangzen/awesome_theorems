import Mathlib.Algebra.Group.Action.End
import Mathlib.Algebra.Group.Subgroup.Ker

/-!
# THM-M-0063 canonical Lean statement

This module freezes Cayley's theorem as the left-regular permutation representation of an
arbitrary group. It contains a checked transport to the literal permutation-subgroup wording and
statement-identity tests, but no proof of the canonical target.
-/

namespace Stage1Instances.THM_M_0063

universe u

/-- Every group is isomorphic to the image subgroup of its left-regular permutation action. -/
def CayleyTheoremTarget : Prop :=
  forall (G : Type u) [Group G],
    Nonempty (G ≃* (MulAction.toPermHom G G).range)

/-- Literal "some permutation group" consequence on the underlying carrier of `G`. -/
def PermutationSubgroupExistenceTarget : Prop :=
  forall (G : Type u) [Group G],
    exists K : Subgroup (Equiv.Perm G), Nonempty (G ≃* K)

/-- The canonical range formulation implies the catalog's existential subgroup wording. -/
theorem cayleyTheoremTarget_implies_permutationSubgroupExistenceTarget :
    CayleyTheoremTarget.{u} -> PermutationSubgroupExistenceTarget.{u} := by
  intro h G _
  exact ⟨(MulAction.toPermHom G G).range, h G⟩

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

/-- Mutation: restrict the carrier from arbitrary groups to commutative groups. -/
def mutationChangedDomain : Prop :=
  forall (G : Type u) [CommGroup G],
    Nonempty (G ≃* (MulAction.toPermHom G G).range)

/-- Mutation: change the universal group binder to an existential binder. -/
def mutationChangedBinderScope : Prop :=
  exists (G : Type u) (_ : Group G),
    Nonempty (G ≃* (MulAction.toPermHom G G).range)

/-- Mutation: exclude the trivial group boundary. -/
def mutationExcludedTrivialBoundary : Prop :=
  forall (G : Type u) [Group G] [Nontrivial G],
    Nonempty (G ≃* (MulAction.toPermHom G G).range)

/-! Removing `[Group G]` is not even an elaborable proposition in this vocabulary. -/
#check_failure (fun (G : Type u) =>
  show Prop from Nonempty (G ≃* (MulAction.toPermHom G G).range))

variable
  (hDomain : mutationChangedDomain.{u})
  (hScope : mutationChangedBinderScope.{u})
  (hBoundary : mutationExcludedTrivialBoundary.{u})

#check_failure (show CayleyTheoremTarget.{u} from hDomain)
#check_failure (show CayleyTheoremTarget.{u} from hScope)
#check_failure (show CayleyTheoremTarget.{u} from hBoundary)

/-! These specializations confirm that no finite, nontrivial, or countability premise is hidden. -/

/-- The exact conclusion elaborates for the trivial permutation group on the empty set. -/
def trivialGroupBoundary : Prop :=
  Nonempty ((Equiv.Perm Empty) ≃*
    (MulAction.toPermHom (Equiv.Perm Empty) (Equiv.Perm Empty)).range)

/-- The exact conclusion also elaborates for the permutation group on an infinite carrier. -/
def infiniteCarrierBoundary : Prop :=
  Nonempty ((Equiv.Perm Nat) ≃*
    (MulAction.toPermHom (Equiv.Perm Nat) (Equiv.Perm Nat)).range)

#check cayleyTheoremTarget_implies_permutationSubgroupExistenceTarget
#check trivialGroupBoundary
#check infiniteCarrierBoundary

/-! The proof-bearing Cayley anchor is deliberately outside this statement-only import closure. -/
#check_failure Equiv.Perm.subgroupOfMulAction

#print axioms cayleyTheoremTarget_implies_permutationSubgroupExistenceTarget

set_option pp.universes true in
set_option pp.explicit true in
#print CayleyTheoremTarget

end Stage1Instances.THM_M_0063
