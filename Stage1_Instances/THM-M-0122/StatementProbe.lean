import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.CategoryTheory.Comma.Over.Basic
import Mathlib.NumberTheory.NumberField.Basic

/-!
Elaboration probe for `S56-M-0122-STATEMENT`.

This file checks only the part of the intended Faltings target represented by
the pinned mathlib API. It is not the canonical target: the pin has no native
predicate for projective scheme morphisms and no geometric-genus invariant for
smooth proper curves.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u

namespace Stage1Instances.THM_M_0122.StatementProbe

/-- A rational point represented as a section of the structure morphism. -/
structure RationalPoint (K : Type u) [Field K] (X : Scheme.{u})
    (structureMap : X ⟶ Spec (CommRingCat.of K)) where
  toSpecMap : Spec (CommRingCat.of K) ⟶ X
  over_base : toSpecMap ≫ structureMap = 𝟙 (Spec (CommRingCat.of K))

/-- The equivalent slice-category representation of a rational point. -/
abbrev OverRationalPoint (K : Type u) [Field K] (X : Scheme.{u})
    (structureMap : X ⟶ Spec (CommRingCat.of K)) : Type u :=
  Over.mk (𝟙 (Spec (CommRingCat.of K))) ⟶ Over.mk structureMap

/-- Checked transport between the section and slice-category encodings. -/
def rationalPointEquivOver {K : Type u} [Field K] {X : Scheme.{u}}
    {structureMap : X ⟶ Spec (CommRingCat.of K)} :
    RationalPoint K X structureMap ≃ OverRationalPoint K X structureMap where
  toFun p := Over.homMk p.toSpecMap p.over_base
  invFun p := ⟨p.left, by simpa using Over.w p⟩
  left_inv p := by cases p; rfl
  right_inv p := by ext; rfl

/-- The native curve boundary available in the pin. It deliberately does not
claim to encode projectivity or genus. -/
def AvailableCurveBoundary {K : Type u} [Field K] {X : Scheme.{u}}
    (structureMap : X ⟶ Spec (CommRingCat.of K)) : Prop :=
  SmoothOfRelativeDimension 1 structureMap ∧
    IsProper structureMap ∧
    GeometricallyIntegral structureMap

/-- The desired conclusion elaborates once a curve object is available. -/
def RationalPointFinitenessConclusion {K : Type u} [Field K]
    (X : Scheme.{u}) (structureMap : X ⟶ Spec (CommRingCat.of K)) : Prop :=
  Finite (RationalPoint K X structureMap)

#check NumberField
#check SmoothOfRelativeDimension
#check IsProper
#check GeometricallyIntegral
#check RationalPointFinitenessConclusion

end Stage1Instances.THM_M_0122.StatementProbe
