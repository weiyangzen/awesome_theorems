import ObligationTree

/-!
# THM-M-0079 proof-phase installation

This module installs the exact pinned mathlib Nielsen-Schreier theorem at both the frozen direct
root and the registered quotient-action composition interfaces. The substantive proof bodies are
upstream in the pinned mathlib dependency; these local declarations are exact wrappers and checked
composition, not independent reconstructions.
-/

noncomputable section

open CategoryTheory CategoryTheory.ActionCategory

universe u

namespace Stage1Instances.THM_M_0079.Proof

open Stage1Instances.THM_M_0079
open Stage1Instances.THM_M_0079.ObligationTree

/-- The quotient action is pretransitive at the frozen leaf interface. -/
theorem quotientActionPretransitive : QuotientActionPretransitive.{u} := by
  intro G _ H
  exact MulAction.isPretransitive_quotient G H

/-- The identity coset supplies the frozen nonempty quotient interface. -/
theorem quotientNonempty : QuotientNonempty.{u} := by
  intro G _ H
  exact Nonempty.intro ((1 : G) : G ⧸ H)

/-- The pinned action-groupoid construction installed at its frozen interface. -/
def actionGroupoidFreeConstructor : ActionGroupoidFreeConstructor.{u} := by
  intro G A _ _ _
  exact IsFreeGroupoid.actionGroupoidIsFree

/-- The pinned connected-free vertex-group theorem installed at its frozen interface. -/
theorem connectedFreeEndConstructor : ConnectedFreeEndConstructor.{u} := by
  intro C _ _ _ r
  exact IsFreeGroupoid.endIsFreeOfConnectedFree r

/-- The action-category stabilizer/end equivalence installed at its frozen interface. -/
def stabilizerEndConstructor : StabilizerEndConstructor.{u} := by
  intro G _ H
  exact ActionCategory.stabilizerIsoEnd G ((1 : G) : G ⧸ H)

/-- The quotient stabilizer identity installed at its frozen interface. -/
theorem quotientStabilizerIdentification : QuotientStabilizerIdentification.{u} := by
  intro G _ H
  exact MulAction.stabilizer_quotient H

/-- Freeness transported along an arbitrary multiplicative equivalence. -/
theorem mulEquivFreenessTransport : MulEquivFreenessTransport.{u} := by
  intro A B _ _ _ e
  exact IsFreeGroup.ofMulEquiv e

/-- Quotient-action connectedness through the frozen two-child composer. -/
theorem quotientActionConnected : QuotientActionConnected.{u} :=
  quotientActionConnected_of_components quotientActionPretransitive quotientNonempty

/-- The exact end-group/subgroup equivalence through the frozen two-child composer. -/
def endSubgroupEquivConstructor : EndSubgroupEquivConstructor.{u} :=
  endSubgroupEquiv_of_components stabilizerEndConstructor quotientStabilizerIdentification

/-- The selected quotient vertex end group is free through the frozen three-child composer. -/
theorem quotientVertexEndFree : QuotientVertexEndFree.{u} :=
  quotientVertexEndFree_of_components actionGroupoidFreeConstructor connectedFreeEndConstructor
    quotientActionConnected

/-- The registered end-group route assembled at the exact canonical interface. -/
theorem exactAssembly : ExactAssembly.{u} :=
  exactAssembly_of_end_packages quotientVertexEndFree endSubgroupEquivConstructor
    mulEquivFreenessTransport

/-- Exact canonical root obtained from the frozen composition route. -/
theorem nielsenSchreier_via_frozen_composition : NielsenSchreierTarget.{u} :=
  root_of_exactAssembly exactAssembly

/-- Direct exact-root wrapper over the same deduplicated pinned terminal declaration. -/
theorem nielsenSchreier_direct : NielsenSchreierTarget.{u} := by
  intro G _ _ H
  exact subgroupIsFreeOfIsFree H

#check (nielsenSchreier_via_frozen_composition : NielsenSchreierTarget.{u})
#check (nielsenSchreier_direct : NielsenSchreierTarget.{u})

#print sorries subgroupIsFreeOfIsFree
#print sorries quotientActionPretransitive
#print sorries quotientNonempty
#print sorries actionGroupoidFreeConstructor
#print sorries connectedFreeEndConstructor
#print sorries stabilizerEndConstructor
#print sorries quotientStabilizerIdentification
#print sorries mulEquivFreenessTransport
#print sorries quotientActionConnected
#print sorries endSubgroupEquivConstructor
#print sorries quotientVertexEndFree
#print sorries exactAssembly
#print sorries nielsenSchreier_via_frozen_composition
#print sorries nielsenSchreier_direct

#print axioms subgroupIsFreeOfIsFree
#print axioms quotientActionPretransitive
#print axioms quotientNonempty
#print axioms actionGroupoidFreeConstructor
#print axioms connectedFreeEndConstructor
#print axioms stabilizerEndConstructor
#print axioms quotientStabilizerIdentification
#print axioms mulEquivFreenessTransport
#print axioms quotientActionConnected
#print axioms endSubgroupEquivConstructor
#print axioms quotientVertexEndFree
#print axioms exactAssembly
#print axioms nielsenSchreier_via_frozen_composition
#print axioms nielsenSchreier_direct

end Stage1Instances.THM_M_0079.Proof
