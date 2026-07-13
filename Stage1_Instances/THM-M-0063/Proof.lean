import ObligationTree
import Mathlib.GroupTheory.Perm.Subgroup

/-!
# THM-M-0063 proof execution

This module installs the pinned Cayley proof at every machine interface in the frozen obligation
tree and composes those interfaces to the exact canonical target. The final direct wrapper records
the deduplicated upstream terminal declaration used by the compositional route.
-/

namespace Stage1Instances.THM_M_0063.Proof

open Stage1Instances.THM_M_0063.ObligationTree

universe u v

/-- Faithful actions separate group elements pointwise. -/
theorem pointwiseFaithfulness : PointwiseFaithfulness.{u, v} := by
  intro G H _ _ _ g h actionEq
  exact eq_of_smul_eq_smul actionEq

/-- Left multiplication is faithful for every group. -/
theorem regularFaithfulness : RegularFaithfulness.{u} := by
  intro G _
  infer_instance

/-- The canonical action homomorphism supplies the frozen constructor interface. -/
theorem permutationHomConstructor : PermutationHomConstructor.{u, v} := by
  intro G H _ _
  exact ⟨⟨MulAction.toPermHom G H, rfl⟩⟩

/-- Pointwise faithfulness composes to injectivity of the permutation representation. -/
theorem genericToPermInjectivity : GenericToPermInjectivity.{u, v} :=
  genericInjectivity_of_pointwiseFaithfulness pointwiseFaithfulness

/-- An injective group homomorphism has a chosen left inverse. -/
theorem leftInverseConstructor : LeftInverseConstructor.{u, v} := by
  intro G K _ _ f hf
  exact ⟨⟨Classical.choose hf.hasLeftInverse, Classical.choose_spec hf.hasLeftInverse⟩⟩

/-- A left inverse constructs the multiplicative equivalence to the monoid range. -/
theorem mrangeEquivFromLeftInverse : MRangeEquivFromLeftInverse.{u, v} := by
  intro G K _ _ f g hg
  exact ⟨MulEquiv.ofLeftInverse' f hg⟩

/-- The frozen definitional transport identifies monoid range with subgroup range. -/
theorem mrangeToRange : MRangeToRangeTransport.{u, v} :=
  mrangeToRangeTransport

/-- Assemble the generalized faithful-action package from its frozen components. -/
theorem generalFaithfulActionPackage : GeneralFaithfulActionPackage.{u, v} :=
  generalPackage_of_components permutationHomConstructor genericToPermInjectivity
    leftInverseConstructor mrangeEquivFromLeftInverse mrangeToRange

/-- Specialize the generalized package to the regular action. -/
theorem regularSpecialization : RegularSpecialization.{u} :=
  exactTarget_of_generalFaithfulAction regularFaithfulness

/-- Assemble the exact Cayley target through the frozen child interfaces. -/
theorem exactAssembly : ExactAssembly.{u} :=
  exactAssembly_of_components regularSpecialization generalFaithfulActionPackage

/-- The exact canonical root, obtained by checked frozen composition. -/
theorem cayleyTheorem : CayleyTheoremTarget.{u} :=
  root_of_exactAssembly exactAssembly

/-- The same exact root installed directly from the audited pinned mathlib terminal. -/
theorem cayleyTheorem_pinned : CayleyTheoremTarget.{u} := by
  intro G _
  exact ⟨Equiv.Perm.subgroupOfMulAction G G⟩

#check cayleyTheorem
#check cayleyTheorem_pinned
#print sorries pointwiseFaithfulness
#print sorries regularFaithfulness
#print sorries permutationHomConstructor
#print sorries genericToPermInjectivity
#print sorries leftInverseConstructor
#print sorries mrangeEquivFromLeftInverse
#print sorries mrangeToRange
#print sorries generalFaithfulActionPackage
#print sorries regularSpecialization
#print sorries exactAssembly
#print sorries cayleyTheorem
#print sorries cayleyTheorem_pinned
#print axioms pointwiseFaithfulness
#print axioms regularFaithfulness
#print axioms permutationHomConstructor
#print axioms genericToPermInjectivity
#print axioms leftInverseConstructor
#print axioms mrangeEquivFromLeftInverse
#print axioms mrangeToRange
#print axioms generalFaithfulActionPackage
#print axioms regularSpecialization
#print axioms exactAssembly
#print axioms cayleyTheorem
#print axioms cayleyTheorem_pinned

end Stage1Instances.THM_M_0063.Proof
