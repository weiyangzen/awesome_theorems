import Statement

/-!
# THM-M-0072 conditional obligation composition

This module checks the terminal child-to-root shape selected by the frozen Thompson-transfer
architecture. The outside-maximal transfer conclusion remains an explicit premise. The local
inside-maximal branch is proved directly, but this file neither constructs the transfer argument
nor proves the unconditional root.
-/

namespace Stage1Instances.THM_M_0072.ObligationTree

open Stage1Instances.THM_M_0072

universe u

/-- The nontrivial branch of the source proof, with the involution outside the maximal subgroup. -/
def TransferOutsideTarget : Prop := OutsideMaximalTarget.{u}

/-- The complementary boundary branch, where self-conjugacy supplies the witness in `M`. -/
def InsideMaximalTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) -> NoIndexTwoSubgroup G ->
      forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
        forall u : S, u ∈ M -> orderOf u = 2 ->
          exists m : M, IsConj (u : G) ((m : S) : G)

/-- The exact two branches consumed by the terminal root composition. -/
def RootAssemblyTarget : Prop := TransferOutsideTarget.{u} /\ InsideMaximalTarget.{u}

/-- The inside-maximal boundary is closed by the element itself. -/
theorem insideMaximalConclusion : InsideMaximalTarget.{u} := by
  intro G _ _ _ _ S M _ u hu _
  exact insideMaximal_hasConjugate M u hu

/-- Pair the open transfer branch with the checked boundary branch. -/
theorem assembly_of_outside_and_inside
    (outside : TransferOutsideTarget.{u})
    (inside : InsideMaximalTarget.{u}) : RootAssemblyTarget.{u} :=
  ⟨outside, inside⟩

/-- Checked branch merge into the exact printed universal target. Both children are consumed. -/
theorem root_of_assembly (assembly : RootAssemblyTarget.{u}) :
    ThompsonTransferLemmaTarget.{u} := by
  intro G _ _ hEven hIndex S M hM u hu
  by_cases hum : u ∈ M
  · exact assembly.2 G hEven hIndex S M hM u hum hu
  · exact assembly.1 G hEven hIndex S M hM u hum hu

/-- Combined conditional harness; the transfer theorem remains the explicit open premise. -/
theorem root_of_outsideTransfer
    (outside : TransferOutsideTarget.{u}) : ThompsonTransferLemmaTarget.{u} :=
  root_of_assembly (assembly_of_outside_and_inside outside insideMaximalConclusion)

#check (insideMaximalConclusion : InsideMaximalTarget.{u})
#check (assembly_of_outside_and_inside :
  TransferOutsideTarget.{u} -> InsideMaximalTarget.{u} -> RootAssemblyTarget.{u})
#check (root_of_assembly : RootAssemblyTarget.{u} -> ThompsonTransferLemmaTarget.{u})
#check (root_of_outsideTransfer :
  TransferOutsideTarget.{u} -> ThompsonTransferLemmaTarget.{u})

#print axioms insideMaximalConclusion
#print axioms assembly_of_outside_and_inside
#print axioms root_of_assembly
#print axioms root_of_outsideTransfer

set_option pp.universes true in
set_option pp.explicit true in
#print ThompsonTransferLemmaTarget

end Stage1Instances.THM_M_0072.ObligationTree
