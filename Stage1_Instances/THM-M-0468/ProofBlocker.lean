import Statement

/-!
# THM-M-0468 proof-phase blocker

The frozen `BogomolovTarget` quantifies over arbitrary semantic data without
requiring its operations and predicates to model abelian geometry.  This file
gives a kernel-checked countermodel.  Consequently no proof body for the exact
frozen target can be implemented consistently; the statement phase must first
strengthen the structure's laws or use concrete mathematical definitions.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0468

universe uPoint uSubvariety uAbelianSubvariety uLineBundle

/-- In this countermodel every required ambient hypothesis and every density
claim is true, while no point is torsion. -/
def counterexampleData :
    BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle} where
  Point := ULift.{uPoint} Unit
  Subvariety := ULift.{uSubvariety} Unit
  AbelianSubvariety := ULift.{uAbelianSubvariety} Unit
  LineBundle := ULift.{uLineBundle} Unit
  add := fun _ _ => ULift.up ()
  pointMem := fun _ _ => True
  pointMemAbelianSubvariety := fun _ _ => True
  isAbelianVarietyOverNumberField := True
  isClosedGeometricallyIntegral := fun _ => True
  isAbelianSubvariety := fun _ => True
  isAmple := fun _ => True
  isSymmetric := fun _ => True
  canonicalHeight := fun _ _ => 0
  isTorsionPoint := fun _ => False
  isZariskiDenseIn := fun _ _ => True

/-- The exact frozen target is refutable because its semantic surface carries
no compatibility laws. -/
theorem not_bogomolovTarget :
    Not BogomolovTarget.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle} := by
  intro h
  let D := counterexampleData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle}
  let L : D.LineBundle := ULift.up ()
  let X : D.Subvariety := ULift.up ()
  have hEquiv := h D L X
    True.intro True.intro True.intro True.intro
  have hDense : forall epsilon : Real, 0 < epsilon ->
      D.isZariskiDenseIn (smallPoints D L X epsilon) X := by
    intro _ _
    exact True.intro
  rcases hEquiv.mp hDense with ⟨_, _, _, hTorsion, _⟩
  exact hTorsion

#print axioms not_bogomolovTarget

end Stage1Instances.THM_M_0468
