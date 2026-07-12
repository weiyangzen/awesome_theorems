import Mathlib.Data.Real.Basic

/-!
# THM-M-0468: Bogomolov theorem statement boundary

This module freezes the Ullmo--Zhang formulation selected at intake. Mathlib
does not currently provide an abelian-variety, Neron--Tate-height, or
subvariety API, so those notions are exposed as typed semantic data rather
than replaced by a different theorem. No field below asserts the conclusion.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0468

universe uPoint uSubvariety uAbelianSubvariety uLineBundle

/-- Typed semantic surface needed to state the Bogomolov theorem. The carrier
represents geometric points of one abelian variety over a number field. -/
structure BogomolovData where
  Point : Type uPoint
  Subvariety : Type uSubvariety
  AbelianSubvariety : Type uAbelianSubvariety
  LineBundle : Type uLineBundle
  add : Point -> Point -> Point
  pointMem : Subvariety -> Point -> Prop
  pointMemAbelianSubvariety : AbelianSubvariety -> Point -> Prop
  isAbelianVarietyOverNumberField : Prop
  isClosedGeometricallyIntegral : Subvariety -> Prop
  isAbelianSubvariety : AbelianSubvariety -> Prop
  isAmple : LineBundle -> Prop
  isSymmetric : LineBundle -> Prop
  canonicalHeight : LineBundle -> Point -> Real
  isTorsionPoint : Point -> Prop
  isZariskiDenseIn : Set Point -> Subvariety -> Prop

/-- Points of `X` whose canonical height is at most a positive threshold. -/
def smallPoints (D : BogomolovData) (L : D.LineBundle)
    (X : D.Subvariety) (epsilon : Real) : Set D.Point :=
  {x | D.pointMem X x /\ D.canonicalHeight L x <= epsilon}

/-- A subvariety is special when its geometric points are exactly a translate
of an abelian subvariety by a torsion point. -/
def IsSpecial (D : BogomolovData) (X : D.Subvariety) : Prop :=
  exists (B : D.AbelianSubvariety) (t : D.Point),
    D.isAbelianSubvariety B /\ D.isTorsionPoint t /\
      {x | D.pointMem X x} =
        {x | exists b, D.pointMemAbelianSubvariety B b /\ x = D.add t b}

/-- Exact Ullmo--Zhang target: for every valid ambient abelian variety, ample
symmetric height, and closed geometrically integral subvariety, arbitrarily
small points are Zariski dense exactly when the subvariety is special. -/
def BogomolovTarget : Prop :=
  forall (D : BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle})
    (L : D.LineBundle) (X : D.Subvariety),
    D.isAbelianVarietyOverNumberField ->
    D.isAmple L -> D.isSymmetric L ->
    D.isClosedGeometricallyIntegral X ->
      ((forall epsilon : Real, 0 < epsilon ->
          D.isZariskiDenseIn (smallPoints D L X epsilon) X) <->
        IsSpecial D X)

/-- Binder-explicit expansion used to kernel-check the frozen target. -/
theorem bogomolovTarget_exact_type :
    BogomolovTarget.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle} <->
      (forall (D : BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle})
        (L : D.LineBundle) (X : D.Subvariety),
        D.isAbelianVarietyOverNumberField ->
        D.isAmple L -> D.isSymmetric L ->
        D.isClosedGeometricallyIntegral X ->
          ((forall epsilon : Real, 0 < epsilon ->
              D.isZariskiDenseIn (smallPoints D L X epsilon) X) <->
            IsSpecial D X)) :=
  Iff.rfl

-- Structural mutations are elaborated separately and compared by the checker.
def mutationRemovedAmpleness : Prop :=
  forall (D : BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle})
    (L : D.LineBundle) (X : D.Subvariety),
    D.isAbelianVarietyOverNumberField -> D.isSymmetric L ->
    D.isClosedGeometricallyIntegral X ->
      ((forall epsilon : Real, 0 < epsilon ->
          D.isZariskiDenseIn (smallPoints D L X epsilon) X) <-> IsSpecial D X)

def mutationRemovedSymmetry : Prop :=
  forall (D : BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle})
    (L : D.LineBundle) (X : D.Subvariety),
    D.isAbelianVarietyOverNumberField -> D.isAmple L ->
    D.isClosedGeometricallyIntegral X ->
      ((forall epsilon : Real, 0 < epsilon ->
          D.isZariskiDenseIn (smallPoints D L X epsilon) X) <-> IsSpecial D X)

def mutationRemovedGeometricIntegrality : Prop :=
  forall (D : BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle})
    (L : D.LineBundle) (X : D.Subvariety),
    D.isAbelianVarietyOverNumberField -> D.isAmple L -> D.isSymmetric L ->
      ((forall epsilon : Real, 0 < epsilon ->
          D.isZariskiDenseIn (smallPoints D L X epsilon) X) <-> IsSpecial D X)

def mutationRemovedTorsion : Prop :=
  forall (D : BogomolovData.{uPoint, uSubvariety, uAbelianSubvariety, uLineBundle})
    (L : D.LineBundle) (X : D.Subvariety),
    D.isAbelianVarietyOverNumberField -> D.isAmple L -> D.isSymmetric L ->
    D.isClosedGeometricallyIntegral X ->
      ((forall epsilon : Real, 0 < epsilon ->
          D.isZariskiDenseIn (smallPoints D L X epsilon) X) <->
        exists (B : D.AbelianSubvariety) (t : D.Point),
          D.isAbelianSubvariety B /\
            {x | D.pointMem X x} =
              {x | exists b, D.pointMemAbelianSubvariety B b /\ x = D.add t b})

end Stage1Instances.THM_M_0468

set_option pp.explicit true in
#print Stage1Instances.THM_M_0468.BogomolovTarget
