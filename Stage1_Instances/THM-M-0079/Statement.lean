import Mathlib.GroupTheory.FreeGroup.IsFreeGroup

/-!
# THM-M-0079 canonical Lean statement

This module freezes the unrestricted Nielsen-Schreier statement and its boundary. It contains a
checked specialization to a literal `FreeGroup` carrier, but no proof of the canonical target.
-/

namespace Stage1Instances.THM_M_0079

universe u

/-- Every subgroup of every group equipped with a free-group basis is free. -/
def NielsenSchreierTarget : Prop :=
  forall (G : Type u) [Group G] [IsFreeGroup G],
    forall H : Subgroup G, IsFreeGroup H

/-- The common literal-carrier specialization of Nielsen-Schreier. -/
def LiteralFreeGroupTarget : Prop :=
  forall (X : Type u) (H : Subgroup (FreeGroup X)), IsFreeGroup H

/-- The definition-level expansion of freeness for each subgroup. -/
def BasisExistenceTarget : Prop :=
  forall (G : Type u) [Group G] [IsFreeGroup G] (H : Subgroup G),
    exists ι : Type u, Nonempty (FreeGroupBasis ι H)

/-- The generic basis-based target implies the literal `FreeGroup` formulation. -/
theorem nielsenSchreierTarget_implies_literalFreeGroupTarget :
    NielsenSchreierTarget.{u} -> LiteralFreeGroupTarget.{u} := by
  intro h X H
  exact h (FreeGroup X) H

/-- A literal free-group result transports back to every group carrying a free basis. -/
theorem literalFreeGroupTarget_implies_nielsenSchreierTarget :
    LiteralFreeGroupTarget.{u} -> NielsenSchreierTarget.{u} := by
  intro h G _ _ H
  let K : Subgroup (FreeGroup (IsFreeGroup.Generators G)) :=
    H.map (IsFreeGroup.mulEquiv G).symm.toMonoidHom
  let hK : IsFreeGroup K := h (IsFreeGroup.Generators G) K
  exact @IsFreeGroup.ofMulEquiv K inferInstance hK H inferInstance
    ((IsFreeGroup.mulEquiv G).symm.subgroupMap H).symm

/-- The generic and literal-carrier formulations are equivalent. -/
theorem nielsenSchreierTarget_iff_literalFreeGroupTarget :
    NielsenSchreierTarget.{u} ↔ LiteralFreeGroupTarget.{u} :=
  ⟨nielsenSchreierTarget_implies_literalFreeGroupTarget,
    literalFreeGroupTarget_implies_nielsenSchreierTarget⟩

/-- The canonical target is equivalent to expanding the definition of `IsFreeGroup` at `H`. -/
theorem nielsenSchreierTarget_iff_basisExistenceTarget :
    NielsenSchreierTarget.{u} ↔ BasisExistenceTarget.{u} := by
  constructor
  · intro h G _ _ H
    letI : IsFreeGroup H := h G H
    exact IsFreeGroup.nonempty_basis
  · intro h G _ _ H
    exact ⟨h G H⟩

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

/-- Mutation: remove the premise that the ambient group is free. -/
def mutationRemovedAmbientFreeness : Prop :=
  forall (G : Type u) [Group G],
    forall H : Subgroup G, IsFreeGroup H

/-- Mutation: restrict the arbitrary ambient group to a commutative group. -/
def mutationChangedDomain : Prop :=
  forall (G : Type u) [CommGroup G] [IsFreeGroup G],
    forall H : Subgroup G, IsFreeGroup H

/-- Mutation: weaken the universal subgroup binder to existence of one free subgroup. -/
def mutationChangedBinderScope : Prop :=
  forall (G : Type u) [Group G] [IsFreeGroup G],
    exists H : Subgroup G, IsFreeGroup H

/-- Mutation: exclude the bottom subgroup from the conclusion. -/
def mutationExcludedBottomBoundary : Prop :=
  forall (G : Type u) [Group G] [IsFreeGroup G],
    forall H : Subgroup G, H ≠ ⊥ -> IsFreeGroup H

variable
  (hRemoved : mutationRemovedAmbientFreeness.{u})
  (hDomain : mutationChangedDomain.{u})
  (hScope : mutationChangedBinderScope.{u})
  (hBoundary : mutationExcludedBottomBoundary.{u})

#check_failure (show NielsenSchreierTarget.{u} from hRemoved)
#check_failure (show NielsenSchreierTarget.{u} from hDomain)
#check_failure (show NielsenSchreierTarget.{u} from hScope)
#check_failure (show NielsenSchreierTarget.{u} from hBoundary)

/-! These surfaces confirm that no nontriviality, rank, or finiteness condition is hidden. -/

/-- The target specializes to the bottom subgroup of the free group on no generators. -/
theorem trivialAmbientBottomBoundary (h : NielsenSchreierTarget.{0}) :
    IsFreeGroup (⊥ : Subgroup (FreeGroup Empty)) :=
  h (FreeGroup Empty) ⊥

/-- The target specializes to the top subgroup of a generic free group. -/
theorem genericTopBoundary (h : NielsenSchreierTarget.{u})
    (G : Type u) [Group G] [IsFreeGroup G] : IsFreeGroup (⊤ : Subgroup G) :=
  h G ⊤

/-- The target specializes to any subgroup of an infinitely generated literal free group. -/
theorem infiniteRankBoundary (h : NielsenSchreierTarget.{0})
    (H : Subgroup (FreeGroup Nat)) : IsFreeGroup H :=
  h (FreeGroup Nat) H

#check nielsenSchreierTarget_implies_literalFreeGroupTarget
#check literalFreeGroupTarget_implies_nielsenSchreierTarget
#check nielsenSchreierTarget_iff_literalFreeGroupTarget
#check nielsenSchreierTarget_iff_basisExistenceTarget
#check trivialAmbientBottomBoundary
#check genericTopBoundary
#check infiniteRankBoundary

/-! The proof-bearing Nielsen-Schreier declaration is deliberately outside this import closure. -/
#check_failure subgroupIsFreeOfIsFree

#print axioms nielsenSchreierTarget_implies_literalFreeGroupTarget
#print axioms nielsenSchreierTarget_iff_literalFreeGroupTarget
#print axioms nielsenSchreierTarget_iff_basisExistenceTarget

set_option pp.universes true in
set_option pp.explicit true in
#print NielsenSchreierTarget

end Stage1Instances.THM_M_0079
