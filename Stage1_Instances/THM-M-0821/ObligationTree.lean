import Statement
import Mathlib.Combinatorics.SetFamily.LYM

/-!
# THM-M-0821 obligation composition harness

The three packages below isolate the exact attaining branch, the universal
upper-bound branch, and their root composition. The package composition
theorems consume abstract child conclusions. The pinned candidate probes show
that the selected mathlib declarations inhabit those interfaces, but they do
not install an accepted root proof in this phase.
-/

namespace Stage1Instances.THM_M_0821_Obligations

universe u

/-- The exact attaining-family conjunct of the frozen maximum target. -/
def AttainmentPackage : Prop :=
  forall (alpha : Type u) [Fintype alpha],
    exists A : Finset (Finset alpha),
      Stage1Instances.THM_M_0821.IsSpernerFamily A /\
        A.card = Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

/-- The exact universal upper-bound conjunct of the frozen maximum target. -/
def UpperBoundPackage : Prop :=
  forall (alpha : Type u) [Fintype alpha] (A : Finset (Finset alpha)),
    Stage1Instances.THM_M_0821.IsSpernerFamily A ->
      A.card <= Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

/-- The frozen lower-middle construction is the corresponding powerset slice. -/
def MiddleLayerDefinitionPackage : Prop :=
  forall (alpha : Type u) [Fintype alpha],
    Stage1Instances.THM_M_0821.middleLayer alpha =
      Finset.powersetCard (Fintype.card alpha / 2) Finset.univ

/-- Every member of the raw lower-middle slice has the selected rank. -/
def MiddleLayerSizedPackage : Prop :=
  forall (alpha : Type u) [Fintype alpha],
    Set.Sized (Fintype.card alpha / 2)
      (Finset.powersetCard (Fintype.card alpha / 2)
        (Finset.univ : Finset alpha) : Set (Finset alpha))

/-- The raw lower-middle slice is an antichain. -/
def MiddleLayerAntichainPackage : Prop :=
  forall (alpha : Type u) [Fintype alpha],
    Stage1Instances.THM_M_0821.IsSpernerFamily
      (Finset.powersetCard (Fintype.card alpha / 2)
        (Finset.univ : Finset alpha))

/-- The raw lower-middle slice has the selected binomial cardinality. -/
def MiddleLayerCardinalityPackage : Prop :=
  forall (alpha : Type u) [Fintype alpha],
    (Finset.powersetCard (Fintype.card alpha / 2)
      (Finset.univ : Finset alpha)).card =
        Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

/-- Checked child-to-parent construction of the attaining package. -/
theorem attainment_of_middleLayer
    (definition : MiddleLayerDefinitionPackage.{u})
    (antichain : MiddleLayerAntichainPackage.{u})
    (cardinality : MiddleLayerCardinalityPackage.{u}) :
    AttainmentPackage.{u} := by
  intro alpha _
  refine ⟨Stage1Instances.THM_M_0821.middleLayer alpha, ?_, ?_⟩
  · rw [definition alpha]
    exact antichain alpha
  · rw [definition alpha]
    exact cardinality alpha

/-- Checked child-to-parent use of the fixed-rank invariant. -/
theorem middleLayerAntichain_of_sized
    (sized : MiddleLayerSizedPackage.{u}) :
    MiddleLayerAntichainPackage.{u} := by
  intro alpha _
  exact (sized alpha).isAntichain

/-- Checked child-to-parent packaging of the imported upper-bound conclusion. -/
theorem upperBound_of_sperner
    (sperner : forall (alpha : Type u) [Fintype alpha]
      (A : Finset (Finset alpha)),
        Stage1Instances.THM_M_0821.IsSpernerFamily A ->
          A.card <= Nat.choose (Fintype.card alpha)
            (Fintype.card alpha / 2)) : UpperBoundPackage.{u} := by
  exact sperner

/-- The exact conjunction split used as the branch-recomposition interface. -/
def MaximumSplit : Prop :=
  AttainmentPackage.{u} /\ UpperBoundPackage.{u}

/-- Checked branch recomposition. Both terminal packages are consumed. -/
theorem maximumSplit_of_packages
    (attainment : AttainmentPackage.{u})
    (upper : UpperBoundPackage.{u}) : MaximumSplit.{u} :=
  ⟨attainment, upper⟩

/-- Exact root composition certificate from the recombined maximum branches. -/
theorem compose_root (split : MaximumSplit.{u}) :
    Stage1Instances.THM_M_0821.SpernerMaximumTarget.{u} := by
  intro alpha _
  exact ⟨split.1 alpha, split.2 alpha⟩

/-- Checked terminal-to-root identity. It makes the final graph edge explicit. -/
theorem root_of_terminal
    (terminal : Stage1Instances.THM_M_0821.SpernerMaximumTarget.{u}) :
    Stage1Instances.THM_M_0821.SpernerMaximumTarget.{u} :=
  terminal

/-- Pinned definitional candidate for the selected middle slice. -/
theorem pinned_middleLayerDefinition : MiddleLayerDefinitionPackage.{u} := by
  intro alpha _
  rfl

/-- Pinned candidate for the fixed-cardinality invariant. -/
theorem pinned_middleLayerSized : MiddleLayerSizedPackage.{u} := by
  intro alpha _
  exact Set.sized_powersetCard (Finset.univ : Finset alpha)
    (Fintype.card alpha / 2)

/-- Pinned candidate for the lower-middle cardinality. -/
theorem pinned_middleLayerCardinality : MiddleLayerCardinalityPackage.{u} := by
  intro alpha _
  simp [Finset.card_powersetCard]

/-- Pinned candidate for the exact universal upper-bound package. -/
theorem pinned_upperBound : UpperBoundPackage.{u} := by
  intro alpha _ A hA
  exact hA.sperner

#check Set.sized_powersetCard
#check Set.Sized.isAntichain
#check Finset.card_powersetCard
#check Finset.local_lubell_yamamoto_meshalkin_inequality_mul
#check Finset.local_lubell_yamamoto_meshalkin_inequality_div
#check Finset.falling
#check Finset.mem_falling
#check Finset.sized_falling
#check Finset.slice_subset_falling
#check Finset.falling_zero_subset
#check Finset.slice_union_shadow_falling_succ
#check Finset.IsAntichain.disjoint_slice_shadow_falling
#check Finset.le_card_falling_div_choose
#check Finset.lubell_yamamoto_meshalkin_inequality_sum_card_div_choose
#check Finset.lubell_yamamoto_meshalkin_inequality_sum_inv_choose
#check Finset.sum_fiberwise_of_maps_to'
#check Set.Sized.card_le
#check Finset.shadow
#check Finset.mem_shadow_iff
#check Finset.erase_mem_shadow
#check Finset.mem_shadow_iff_insert_mem
#check Set.Sized.shadow
#check Finset.sized_shadow_iff
#check Finset.bipartiteBelow
#check Finset.bipartiteAbove
#check Finset.mem_bipartiteBelow
#check Finset.mem_bipartiteAbove
#check Finset.card_mul_le_card_mul'
#check Nat.choose_le_middle
#check IsAntichain.sperner

#print sorries IsAntichain.sperner
#print axioms IsAntichain.sperner
#print axioms pinned_middleLayerDefinition
#print axioms pinned_middleLayerSized
#print axioms pinned_middleLayerCardinality
#print axioms pinned_upperBound
#print axioms middleLayerAntichain_of_sized
#print axioms attainment_of_middleLayer
#print axioms upperBound_of_sperner
#print axioms maximumSplit_of_packages
#print axioms compose_root
#print axioms root_of_terminal

set_option pp.explicit true in
set_option pp.universes true in
#print AttainmentPackage
set_option pp.explicit true in
set_option pp.universes true in
#print UpperBoundPackage
set_option pp.explicit true in
set_option pp.universes true in
#print MiddleLayerDefinitionPackage
set_option pp.explicit true in
set_option pp.universes true in
#print MiddleLayerSizedPackage
set_option pp.explicit true in
set_option pp.universes true in
#print MiddleLayerAntichainPackage
set_option pp.explicit true in
set_option pp.universes true in
#print MiddleLayerCardinalityPackage
set_option pp.explicit true in
set_option pp.universes true in
#print MaximumSplit

end Stage1Instances.THM_M_0821_Obligations
