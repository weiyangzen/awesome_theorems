import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0557 conditional obligation composition

This module checks the interfaces and final composition frozen by the
obligation registry.  It deliberately takes the two structure branches as
premises; integrating their pinned implementations belongs to the proof node.
-/

namespace Stage1Instances.THM_M_0557.ObligationTree

universe u

def GroupStructureBranch : Prop :=
  forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
    Nonempty (Group (HomotopyGroup.Pi (n + 1) X x))

def CommutativeStructureBranch : Prop :=
  forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
    Nonempty (CommGroup (HomotopyGroup.Pi (n + 2) X x))

def ExactTarget : Prop :=
  forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
    Nonempty (Group (HomotopyGroup.Pi (n + 1) X x)) /\
      Nonempty (CommGroup (HomotopyGroup.Pi (n + 2) X x))

/-- Checked child-to-parent composition; neither premise is discharged here. -/
theorem exactTarget_of_branches
    (groupBranch : GroupStructureBranch.{u})
    (commBranch : CommutativeStructureBranch.{u}) : ExactTarget.{u} := by
  intro X _ x n
  exact ⟨groupBranch X x n, commBranch X x n⟩

#check HomotopyGroup.group
#check homotopyGroupEquivFundamentalGroup
#check HomotopyGroup.commGroup
#check HomotopyGroup.isUnital_auxGroup
#check HomotopyGroup.auxGroup_indep
#check GenLoop.transAt_distrib
#print axioms exactTarget_of_branches

end Stage1Instances.THM_M_0557.ObligationTree
