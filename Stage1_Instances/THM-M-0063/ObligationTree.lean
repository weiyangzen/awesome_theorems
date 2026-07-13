import Statement

/-!
# THM-M-0063 conditional obligation composition

This module checks the interfaces and child-to-parent composition selected by
the frozen Cayley architecture. The pointwise-faithfulness and range-equivalence
packages remain explicit premises, so this module does not install the audited
mathlib candidate or prove the unconditional theorem.
-/

namespace Stage1Instances.THM_M_0063.ObligationTree

universe u v

/-- The faithful-action principle needed to make the permutation homomorphism injective. -/
def PointwiseFaithfulness : Prop :=
  forall (G : Type u) (H : Type v) [Group G] [MulAction G H] [FaithfulSMul G H]
    (g h : G), (forall x : H, g • x = h • x) -> g = h

/-- The left-regular action is faithful for every group. -/
def RegularFaithfulness : Prop :=
  forall (G : Type u) [Group G], FaithfulSMul G G

/-- The exact action homomorphism construction, separated from later properties. -/
def PermutationHomConstructor : Prop :=
  forall (G : Type u) (H : Type v) [Group G] [MulAction G H],
    Nonempty { f : G →* Equiv.Perm H // f = MulAction.toPermHom G H }

/-- Injectivity of the permutation representation for every faithful action. -/
def GenericToPermInjectivity : Prop :=
  forall (G : Type u) (H : Type v) [Group G] [MulAction G H] [FaithfulSMul G H],
    Function.Injective (MulAction.toPermHom G H)

/-- Generic construction of a chosen left inverse from injectivity. -/
def LeftInverseConstructor : Prop :=
  forall (G : Type u) (K : Type v) [Group G] [Group K] (f : G →* K),
    Function.Injective f -> Nonempty { g : K -> G // Function.LeftInverse g f }

/-- Exact constructor used in the audited body; its codomain is `MonoidHom.mrange`. -/
def MRangeEquivFromLeftInverse : Prop :=
  forall (G : Type u) (K : Type v) [Group G] [Group K] (f : G →* K) (g : K -> G),
    Function.LeftInverse g f -> Nonempty (G ≃* MonoidHom.mrange f)

/-- Representation transport from the monoid range to the subgroup range for group homomorphisms. -/
def MRangeToRangeTransport : Prop :=
  forall (G : Type u) (K : Type v) [Group G] [Group K] (f : G →* K),
    Nonempty (G ≃* MonoidHom.mrange f) -> Nonempty (G ≃* f.range)

/-- The monoid-range and subgroup-range carriers are definitionally aligned for group homs. -/
theorem mrangeToRangeTransport : MRangeToRangeTransport.{u, v} := by
  intro G K _ _ f h
  exact h

/-- The generalized faithful-action package before regular-action specialization. -/
def GeneralFaithfulActionPackage : Prop :=
  forall (G : Type u) (H : Type v) [Group G] [MulAction G H] [FaithfulSMul G H],
    Nonempty (G ≃* (MulAction.toPermHom G H).range)

/-- The typed specialization interface, kept separate from its package input. -/
def RegularSpecialization : Prop :=
  GeneralFaithfulActionPackage.{u, u} -> Stage1Instances.THM_M_0063.CayleyTheoremTarget.{u}

/-- The exact assembled conclusion before its identity composition into the root. -/
def ExactAssembly : Prop := Stage1Instances.THM_M_0063.CayleyTheoremTarget.{u}

/-- Checked composition from pointwise faithfulness to injectivity of `toPermHom`. -/
theorem genericInjectivity_of_pointwiseFaithfulness
    (faithfulness : PointwiseFaithfulness.{u, v}) :
    GenericToPermInjectivity.{u, v} := by
  intro G H _ _ _ g h heq
  apply faithfulness G H g h
  intro x
  exact congrArg (fun p : Equiv.Perm H => p x) heq

/-- Checked composition of injectivity and the range constructor. -/
theorem generalPackage_of_components
    (permHom : PermutationHomConstructor.{u, v})
    (injectivity : GenericToPermInjectivity.{u, v})
    (leftInverse : LeftInverseConstructor.{u, v})
    (mrangeEquiv : MRangeEquivFromLeftInverse.{u, v})
    (toRange : MRangeToRangeTransport.{u, v}) :
    GeneralFaithfulActionPackage.{u, v} := by
  intro G H _ _ _
  exact (permHom G H).map fun ⟨f, hf⟩ => by
    subst f
    have witness := leftInverse G (Equiv.Perm H) (MulAction.toPermHom G H) (injectivity G H)
    exact witness.map (fun ⟨g, hg⟩ =>
      (toRange G (Equiv.Perm H) (MulAction.toPermHom G H)
        (mrangeEquiv G (Equiv.Perm H) (MulAction.toPermHom G H) g hg)).some) |>.some

/-- Checked specialization of a faithful action package to the left-regular action. -/
theorem exactTarget_of_generalFaithfulAction
    (regularFaithful : RegularFaithfulness.{u}) : RegularSpecialization.{u} := by
  intro package G _
  letI : FaithfulSMul G G := regularFaithful G
  exact package G G

/-- Assemble the regular-specialization map and the generalized package. -/
theorem exactAssembly_of_components
    (specialize : RegularSpecialization.{u})
    (package : GeneralFaithfulActionPackage.{u, u}) : ExactAssembly.{u} :=
  specialize package

/-- Exact child-to-root identity composition; `assembled` remains an explicit premise. -/
theorem root_of_exactAssembly (assembled : ExactAssembly.{u}) :
    Stage1Instances.THM_M_0063.CayleyTheoremTarget.{u} :=
  assembled

#print axioms genericInjectivity_of_pointwiseFaithfulness
#print axioms mrangeToRangeTransport
#print axioms generalPackage_of_components
#print axioms exactTarget_of_generalFaithfulAction
#print axioms exactAssembly_of_components
#print axioms root_of_exactAssembly

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0063.CayleyTheoremTarget

end Stage1Instances.THM_M_0063.ObligationTree
