import Statement
import Mathlib.Topology.Connected.TotallyDisconnected

/-!
# THM-M-0112 proof-phase blocker witness

This module does not prove the Lefschetz hyperplane theorem. It kernel-checks
that the exact frozen target has a countermodel: its opaque geometric
propositions do not constrain the supplied map on homotopy groups.
-/

noncomputable section

open scoped Topology
open unitInterval

namespace Stage1Instances.THMM0112.Proof

private theorem not_joined_false_true : Not (Joined false true) := by
  rintro ⟨path⟩
  have endpoints_equal : path (0 : unitInterval) = path (1 : unitInterval) :=
    PreconnectedSpace.constant (by infer_instance) path.continuous
  simp at endpoints_equal

private theorem zeroth_false_ne_true :
    (⟦false⟧ : ZerothHomotopy Bool) ≠ (⟦true⟧ : ZerothHomotopy Bool) := by
  intro equality
  exact not_joined_false_true (Quotient.exact equality)

private def counterexampleData : LefschetzHyperplaneData PUnit Bool where
  complexDimension := 2
  inclusion := ContinuousMap.const _ PUnit.unit
  basePoint := false
  ambientConnected := by
    rw [show (Set.univ : Set PUnit) = {PUnit.unit} by ext x; simp]
    exact isConnected_singleton
  ambientSmoothOverComplex := True
  ambientProjectiveOverComplex := True
  sectionIsSmooth := True
  sectionIsHyperplaneForInclusion := True
  piMap := fun _ _ => default
  piMapIsInducedByInclusion := True

/-- The exact frozen proposition is false: at complex dimension two it would
make a constant map from the two path components of discrete `Bool` injective
in degree zero. This is a blocker certificate, not theorem closure. -/
theorem not_weakTopologicalLefschetzTarget :
    Not WeakTopologicalLefschetzTarget.{0, 0} := by
  intro target
  have conclusion := target PUnit Bool counterexampleData
    True.intro True.intro True.intro True.intro True.intro
  have injectivePiZero := (conclusion.1 0 (by norm_num [counterexampleData])).1
  let equivalence :=
    HomotopyGroup.pi0EquivZerothHomotopy (X := Bool) (x := false)
  let falseClass : HomotopyGroup.Pi 0 Bool false :=
    equivalence.symm (⟦false⟧ : ZerothHomotopy Bool)
  let trueClass : HomotopyGroup.Pi 0 Bool false :=
    equivalence.symm (⟦true⟧ : ZerothHomotopy Bool)
  have classesEqual : falseClass = trueClass := by
    apply injectivePiZero (a₁ := falseClass) (a₂ := trueClass)
    rfl
  apply zeroth_false_ne_true
  simpa [falseClass, trueClass] using congrArg equivalence classesEqual

#print not_weakTopologicalLefschetzTarget
#print axioms not_weakTopologicalLefschetzTarget

end Stage1Instances.THMM0112.Proof
