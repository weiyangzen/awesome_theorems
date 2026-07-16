import Mathlib.AlgebraicGeometry.Geometrically.Basic
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.Topology.Sheaves.Abelian

/-!
# THM-M-0123: Mordell conjecture statement

This module freezes the intake-selected proper-curve form. The geometric genus
condition is derived from the concrete pinned structure-sheaf cohomology
`H^1(X, O_X)`: its underlying additive group must be equivalent to `K^n` for
some `n >= 2`. No genus proposition or natural-number field is supplied by the
caller, and this file does not prove Faltings' theorem.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u

namespace Stage1Instances.THM_M_0123

/-- The base scheme of a commutative ring. -/
abbrev SpecOf (K : Type u) [CommRing K] : Scheme.{u} :=
  Spec (CommRingCat.of K)

/-- Geometric connectedness through every field-valued base change. -/
def IsGeometricallyConnected {K : Type u} [Field K] {X : Scheme.{u}}
    (structureMap : X ⟶ SpecOf K) : Prop :=
  geometrically (fun Y : Scheme.{u} => ConnectedSpace Y) structureMap

/-- The concrete pinned sheaf-cohomology group `H^1(X, O_X)`. -/
abbrev StructureSheafH1 (X : Scheme.{u}) : Type u :=
  ((SheafOfModules.toSheaf X.ringCatSheaf).obj
    (SheafOfModules.unit X.ringCatSheaf)).H 1

/-- The cohomological geometric genus of `X` is at least two. -/
def GeometricGenusAtLeastTwo (K : Type u) [Field K]
    (X : Scheme.{u}) : Prop :=
  ∃ n : Nat, 2 ≤ n ∧ Nonempty (StructureSheafH1 X ≃+ (Fin n → K))

/-- The boundary mutation also permits cohomological genus one. -/
def GeometricGenusAtLeastOne (K : Type u) [Field K]
    (X : Scheme.{u}) : Prop :=
  ∃ n : Nat, 1 ≤ n ∧ Nonempty (StructureSheafH1 X ≃+ (Fin n → K))

/-- A scheme over `K` and its structure morphism. -/
structure CurveOver (K : Type u) [Field K] where
  scheme : Scheme.{u}
  structureMap : scheme ⟶ SpecOf K

/-- A `K`-rational point represented as a section of the structure morphism. -/
abbrev RationalPoint {K : Type u} [Field K] (C : CurveOver.{u} K) : Type u :=
  { point : SpecOf K ⟶ C.scheme // point ≫ C.structureMap = 𝟙 (SpecOf K) }

/-- The equivalent slice-category representation of a rational point. -/
abbrev OverRationalPoint {K : Type u} [Field K] (C : CurveOver.{u} K) : Type u :=
  Over.mk (𝟙 (SpecOf K)) ⟶ Over.mk C.structureMap

/-- Checked equivalence between section and slice-category point encodings. -/
def rationalPointEquivOver {K : Type u} [Field K] (C : CurveOver.{u} K) :
    RationalPoint C ≃ OverRationalPoint C where
  toFun p := Over.homMk p.1 p.2
  invFun p := ⟨p.left, by simpa using Over.w p⟩
  left_inv p := by cases p; rfl
  right_inv p := by ext; rfl

namespace CurveOver

variable {K : Type u} [Field K]

/-- Every geometric hypothesis in the selected proper-curve statement. -/
def Hypotheses (C : CurveOver.{u} K) : Prop :=
  SmoothOfRelativeDimension 1 C.structureMap ∧
    IsProper C.structureMap ∧
      IsGeometricallyConnected C.structureMap ∧
        GeometricGenusAtLeastTwo K C.scheme

end CurveOver

/--
The normalized Mordell target: rational points on every smooth, proper,
geometrically connected curve of genus at least two over a number field form
a finite type.
-/
def MordellTarget : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
    SmoothOfRelativeDimension 1 C.structureMap ∧
        IsProper C.structureMap ∧
          IsGeometricallyConnected C.structureMap ∧
            (∃ n : Nat, 2 ≤ n ∧
              Nonempty (StructureSheafH1 C.scheme ≃+ (Fin n → K))) →
      Finite (RationalPoint C)

/-- Checked expansion fixing every ordered binder and geometric hypothesis. -/
theorem mordellTarget_iff_expanded :
    MordellTarget.{u} ↔
      ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
        C.Hypotheses → Finite (RationalPoint C) :=
  Iff.rfl

/-- Checked transport of point finiteness to the slice-category encoding. -/
theorem finite_rationalPoint_iff_finite_over
    {K : Type u} [Field K] (C : CurveOver.{u} K) :
    Finite (RationalPoint C) ↔ Finite (OverRationalPoint C) :=
  (rationalPointEquivOver C).finite_iff

/-- Checked target-level transport to slice-category rational points. -/
theorem mordellTarget_iff_over :
    MordellTarget.{u} ↔
      ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
        C.Hypotheses → Finite (OverRationalPoint C) := by
  constructor
  · intro h K _ _ C hC
    exact (finite_rationalPoint_iff_finite_over C).mp (h K C hC)
  · intro h K _ _ C hC
    exact (finite_rationalPoint_iff_finite_over C).mpr (h K C hC)

/-! Structural mutations elaborate independently and receive no identity credit. -/

def MutationRemovedGenusHypothesis : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
    SmoothOfRelativeDimension 1 C.structureMap ∧
        IsProper C.structureMap ∧
          IsGeometricallyConnected C.structureMap →
      Finite (RationalPoint C)

def MutationRemovedNumberField : Prop :=
  ∀ (K : Type u) [Field K] (C : CurveOver.{u} K),
    C.Hypotheses → Finite (RationalPoint C)

def MutationChangedCurveBinderScope : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K], ∃ C : CurveOver.{u} K,
    C.Hypotheses → Finite (RationalPoint C)

def MutationIncludesGenusOne : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
    SmoothOfRelativeDimension 1 C.structureMap ∧
        IsProper C.structureMap ∧
          IsGeometricallyConnected C.structureMap ∧
            GeometricGenusAtLeastOne K C.scheme →
      Finite (RationalPoint C)

variable
  (hRemoved : MutationRemovedGenusHypothesis.{u})
  (hDomain : MutationRemovedNumberField.{u})
  (hScope : MutationChangedCurveBinderScope.{u})
  (hBoundary : MutationIncludesGenusOne.{u})

#check_failure (show MordellTarget.{u} from hRemoved)
#check_failure (show MordellTarget.{u} from hDomain)
#check_failure (show MordellTarget.{u} from hScope)
#check_failure (show MordellTarget.{u} from hBoundary)

#check mordellTarget_iff_expanded
#check mordellTarget_iff_over
#print axioms mordellTarget_iff_expanded
#print axioms mordellTarget_iff_over

set_option pp.universes true in
set_option pp.explicit true in
#print MordellTarget

end Stage1Instances.THM_M_0123
