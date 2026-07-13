import Statement
import Mathlib.GroupTheory.FreeGroup.NielsenSchreier

/-!
# THM-M-0079 conditional obligation composition

This module checks the child-to-parent interfaces selected by the frozen Nielsen-Schreier
architecture. The quotient-action, connected free-end-group, and end-to-subgroup packages remain
explicit premises. Consequently this file does not install the audited mathlib candidate or close
the canonical theorem.
-/

noncomputable section

open CategoryTheory CategoryTheory.ActionCategory

universe u

namespace Stage1Instances.THM_M_0079.ObligationTree

/-- The transitivity input for the action of a group on its left-coset quotient. -/
def QuotientActionPretransitive : Prop :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    MulAction.IsPretransitive G (G ⧸ H)

/-- Every left-coset quotient has an object, represented by the identity coset. -/
def QuotientNonempty : Prop :=
  forall (G : Type u) [Group G] (H : Subgroup G), Nonempty (G ⧸ H)

/-- Construction of a free action groupoid over a free ambient group. -/
def ActionGroupoidFreeConstructor : Type (u + 1) :=
  forall (G A : Type u) [Group G] [IsFreeGroup G] [MulAction G A],
    IsFreeGroupoid (ActionCategory G A)

/-- The geodesic-spanning-tree package: a vertex group of a connected free groupoid is free. -/
def ConnectedFreeEndConstructor : Prop :=
  forall (C : Type u) [Groupoid.{u} C] [IsConnected C] [IsFreeGroupoid C] (r : C),
    IsFreeGroup (End r)

/-- The exact multiplicative equivalence between the chosen action-groupoid end group and `H`. -/
def EndSubgroupEquivConstructor : Type (u + 1) :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    End (objEquiv G (G ⧸ H) ↑(1 : G)) ≃* H

/-- Identify the quotient-action stabilizer with the corresponding vertex end group. -/
def StabilizerEndConstructor : Type (u + 1) :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    MulAction.stabilizerSubmonoid G ((1 : G) : G ⧸ H) ≃*
      End (objEquiv G (G ⧸ H) ↑(1 : G))

/-- Identify the stabilizer of the identity coset with the selected subgroup. -/
def QuotientStabilizerIdentification : Prop :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    MulAction.stabilizer G ((1 : G) : G ⧸ H) = H

/-- Transport freeness along a multiplicative equivalence. -/
def MulEquivFreenessTransport : Prop :=
  forall (A B : Type u) [Group A] [Group B] [IsFreeGroup A],
    A ≃* B → IsFreeGroup B

/-- Connectedness of the action groupoid for the quotient action. -/
def QuotientActionConnected : Prop :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    IsConnected (ActionCategory G (G ⧸ H))

/-- Freeness of the end group at the identity coset in the quotient action groupoid. -/
def QuotientVertexEndFree : Prop :=
  forall (G : Type u) [Group G] [IsFreeGroup G] (H : Subgroup G),
    @IsFreeGroup (End (objEquiv G (G ⧸ H) ↑(1 : G))) (End.group _)

/-- The exact canonical root, kept as a separate final assembly interface. -/
def ExactAssembly : Prop := Stage1Instances.THM_M_0079.NielsenSchreierTarget.{u}

/-- Compose quotient transitivity and nonemptiness into action-groupoid connectedness. -/
theorem quotientActionConnected_of_components
    (pretransitive : QuotientActionPretransitive.{u})
    (nonempty : QuotientNonempty.{u}) :
    QuotientActionConnected.{u} := by
  intro G _ H
  letI : MulAction.IsPretransitive G (G ⧸ H) := pretransitive G H
  letI : Nonempty (G ⧸ H) := nonempty G H
  exact inferInstance

/-- Compose the stabilizer/end equivalence with the exact quotient-stabilizer identity. -/
def endSubgroupEquiv_of_components
    (stabilizerEnd : StabilizerEndConstructor.{u})
    (quotientStabilizer : QuotientStabilizerIdentification.{u}) :
    EndSubgroupEquivConstructor.{u} := by
  intro G _ H
  exact MulEquiv.trans (stabilizerEnd G H).symm
    (MulEquiv.subgroupCongr (quotientStabilizer G H))

/-- Compose free-action, connectedness, and connected-free-end packages at the identity coset. -/
theorem quotientVertexEndFree_of_components
    (freeActionGroupoid : ActionGroupoidFreeConstructor.{u})
    (connectedFreeEnd : ConnectedFreeEndConstructor.{u})
    (connected : QuotientActionConnected.{u}) :
    QuotientVertexEndFree.{u} := by
  intro G _ _ H
  letI : IsFreeGroupoid (ActionCategory G (G ⧸ H)) :=
    freeActionGroupoid G (G ⧸ H)
  have hConnected : IsConnected (ActionCategory G (G ⧸ H)) := connected G H
  exact @connectedFreeEnd (ActionCategory G (G ⧸ H)) inferInstance hConnected
    inferInstance (objEquiv G (G ⧸ H) ↑(1 : G))

/-- Transport end-group freeness through the exact end-to-subgroup equivalence. -/
theorem exactAssembly_of_end_packages
    (endFree : QuotientVertexEndFree.{u})
    (endEquiv : EndSubgroupEquivConstructor.{u})
    (transport : MulEquivFreenessTransport.{u}) : ExactAssembly.{u} := by
  intro G _ _ H
  have h := endFree G H
  exact @transport (End (objEquiv G (G ⧸ H) ↑(1 : G))) H (End.group _)
    H.toGroup h (endEquiv G H)

/-- Final identity composition into the exact frozen declaration. -/
theorem root_of_exactAssembly (assembled : ExactAssembly.{u}) :
    Stage1Instances.THM_M_0079.NielsenSchreierTarget.{u} :=
  assembled

/- These ascriptions are the graph-to-Lean boundary. A change to a registered child wrapper or to
the parent result makes this module fail rather than leaving the relationship implicit in a name. -/
#check (quotientActionConnected_of_components :
  QuotientActionPretransitive.{u} → QuotientNonempty.{u} → QuotientActionConnected.{u}
  )
#check (endSubgroupEquiv_of_components :
  StabilizerEndConstructor.{u} → QuotientStabilizerIdentification.{u} →
    EndSubgroupEquivConstructor.{u}
  )
#check (quotientVertexEndFree_of_components :
  ActionGroupoidFreeConstructor.{u} → ConnectedFreeEndConstructor.{u} →
    QuotientActionConnected.{u} → QuotientVertexEndFree.{u}
  )
#check (exactAssembly_of_end_packages :
  QuotientVertexEndFree.{u} → EndSubgroupEquivConstructor.{u} →
    MulEquivFreenessTransport.{u} → ExactAssembly.{u}
  )
#check (root_of_exactAssembly :
  ExactAssembly.{u} → Stage1Instances.THM_M_0079.NielsenSchreierTarget.{u}
  )

#check subgroupIsFreeOfIsFree
#check IsFreeGroup.ofMulEquiv
#check CategoryTheory.ActionCategory.endMulEquivSubgroup
#check IsFreeGroupoid.actionGroupoidIsFree
#check IsFreeGroupoid.endIsFreeOfConnectedFree
#check IsFreeGroupoid.SpanningTree.endIsFree
#check Quiver.geodesicSubtree

#print axioms quotientActionConnected_of_components
#print axioms endSubgroupEquiv_of_components
#print axioms quotientVertexEndFree_of_components
#print axioms exactAssembly_of_end_packages
#print axioms root_of_exactAssembly

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0079.NielsenSchreierTarget

end Stage1Instances.THM_M_0079.ObligationTree
