import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0557 proof integration

This module discharges the two frozen structure branches using the pinned
mathlib instances and composes them into the literal canonical target.
-/

namespace Stage1Instances.THM_M_0557.Proof

universe u

/-- The pinned positive-dimensional homotopy-group construction closes
`M0557-GROUP` (with its transfer dependency `M0557-GROUP-TRANSFER`). -/
theorem groupStructureBranch :
    forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
      Nonempty (Group (HomotopyGroup.Pi (n + 1) X x)) := by
  intro X _ x n
  exact ⟨inferInstance⟩

/-- The pinned Eckmann-Hilton construction closes `M0557-COMM`, including the
frozen `M0557-EH` and `M0557-DISTRIB` dependencies represented by its terminal
mathlib body. -/
theorem commutativeStructureBranch :
    forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
      Nonempty (CommGroup (HomotopyGroup.Pi (n + 2) X x)) := by
  intro X _ x n
  exact ⟨inferInstance⟩

/-- Exact proof body for the proposition frozen in `Statement.lean`. -/
theorem homotopyGroupStructureTarget :
    forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
      Nonempty (Group (HomotopyGroup.Pi (n + 1) X x)) /\
        Nonempty (CommGroup (HomotopyGroup.Pi (n + 2) X x)) := by
  intro X _ x n
  exact ⟨groupStructureBranch X x n, commutativeStructureBranch X x n⟩

#print axioms groupStructureBranch
#print axioms commutativeStructureBranch
#print axioms homotopyGroupStructureTarget

end Stage1Instances.THM_M_0557.Proof
