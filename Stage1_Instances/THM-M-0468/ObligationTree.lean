import Statement

/-!
# THM-M-0468 conditional obligation composition

This module checks only the final composition selected by the frozen
architecture.  The two mathematical directions remain explicit premises.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0468

universe uPoint uSubvariety uAbelianSubvariety uLineBundle

/-- The dense-small-points side of the frozen equivalence. -/
def DenseSmallPoints (D : BogomolovData) (L : D.LineBundle)
    (X : D.Subvariety) : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    D.isZariskiDenseIn (smallPoints D L X epsilon) X

/-- The difficult Ullmo--Zhang implication, kept as an explicit package. -/
def DenseSmallPointsImplySpecial : Prop :=
  forall (D : BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle})
    (L : D.LineBundle) (X : D.Subvariety),
    D.isAbelianVarietyOverNumberField -> D.isAmple L -> D.isSymmetric L ->
    D.isClosedGeometricallyIntegral X ->
    DenseSmallPoints D L X -> IsSpecial D X

/-- The torsion-translate converse, also kept as an explicit package. -/
def SpecialImplyDenseSmallPoints : Prop :=
  forall (D : BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle})
    (L : D.LineBundle) (X : D.Subvariety),
    D.isAbelianVarietyOverNumberField -> D.isAmple L -> D.isSymmetric L ->
    D.isClosedGeometricallyIntegral X ->
    IsSpecial D X -> DenseSmallPoints D L X

/-- Checked composition of the two open implication packages into the exact root. -/
theorem root_of_direction_packages
    (forward : DenseSmallPointsImplySpecial.{uPoint, uSubvariety,
      uAbelianSubvariety, uLineBundle})
    (converse : SpecialImplyDenseSmallPoints.{uPoint, uSubvariety,
      uAbelianSubvariety, uLineBundle}) :
    BogomolovTarget.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle} := by
  intro D L X hA hAmp hSym hX
  exact ⟨forward D L X hA hAmp hSym hX,
    converse D L X hA hAmp hSym hX⟩

#print axioms root_of_direction_packages

end Stage1Instances.THM_M_0468
