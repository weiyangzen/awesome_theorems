import Mathlib.AlgebraicGeometry.Geometrically.Basic
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic
import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.Topology.Sheaves.Abelian

/-!
# THM-M-0122: Faltings' theorem statement

This module freezes the Mordell-conjecture form selected at intake. Smoothness,
relative dimension, geometric connectedness, projective space, closed
immersions, structure-sheaf cohomology, and rational points use concrete
pinned mathlib objects.

For the selected smooth projective curve class, geometric genus is represented
by the standard cohomological characterization: the underlying additive group
of `H^1(X, O_X)` is additively equivalent to `K^n`. Over a number field,
additive maps are rational-linear and the finite rational dimension of `K`
forces this `n` to be the usual `K`-dimension of `H^1(X, O_X)`. Thus the
strict bound is derived from the actual scheme rather than supplied as curve
data.

This file states and mutation-tests the target only. It does not prove
Faltings' theorem.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u

namespace Stage1Instances.THMM0122

/-- The base scheme of a commutative ring. -/
abbrev SpecOf (K : Type u) [CommRing K] : Scheme.{u} :=
  Spec (CommRingCat.of K)

/-- Projective `n`-space over `K`, built from the standard homogeneous grading. -/
def ProjectiveSpace (K : Type u) [Field K] (n : Nat) : Scheme.{u} := by
  letI : GradedAlgebra
      (MvPolynomial.homogeneousSubmodule (Fin (n + 1)) K) :=
    MvPolynomial.gradedAlgebra
  exact Proj (MvPolynomial.homogeneousSubmodule (Fin (n + 1)) K)

/-- The constants map into the degree-zero part of the homogeneous grading. -/
def constantsToDegreeZero (K : Type u) [Field K] (n : Nat) :
    K →+* MvPolynomial.homogeneousSubmodule (Fin (n + 1)) K 0 := by
  let A := MvPolynomial.homogeneousSubmodule (Fin (n + 1)) K
  letI : GradedAlgebra A := MvPolynomial.gradedAlgebra
  exact algebraMap K (A 0)

/-- The canonical structure morphism from projective space to `Spec K`. -/
def projectiveSpaceToBase (K : Type u) [Field K] (n : Nat) :
    ProjectiveSpace K n ⟶ SpecOf K := by
  letI : GradedAlgebra
      (MvPolynomial.homogeneousSubmodule (Fin (n + 1)) K) :=
    MvPolynomial.gradedAlgebra
  exact Proj.toSpecZero (MvPolynomial.homogeneousSubmodule (Fin (n + 1)) K) ≫
    Spec.map (CommRingCat.ofHom (constantsToDegreeZero K n))

/-- Projectivity over a field via a closed immersion into finite projective space. -/
def IsProjectiveOver {K : Type u} [Field K] {X : Scheme.{u}}
    (structureMap : X ⟶ SpecOf K) : Prop :=
  ∃ n : Nat, ∃ i : X ⟶ ProjectiveSpace K n,
    IsClosedImmersion i ∧ i ≫ projectiveSpaceToBase K n = structureMap

/-- Geometric connectedness through every field-valued base change. -/
def IsGeometricallyConnected {K : Type u} [Field K] {X : Scheme.{u}}
    (structureMap : X ⟶ SpecOf K) : Prop :=
  geometrically (fun Y : Scheme.{u} => ConnectedSpace Y) structureMap

/-- The concrete pinned sheaf-cohomology group `H^1(X, O_X)`. -/
abbrev StructureSheafH1 (X : Scheme.{u}) : Type u :=
  ((SheafOfModules.toSheaf X.ringCatSheaf).obj
    (SheafOfModules.unit X.ringCatSheaf)).H 1

/--
The structure-sheaf cohomology of `X` has dimension `n` over the number
field `K`, expressed on underlying additive groups.
-/
def HasGeometricGenus (K : Type u) [Field K]
    (X : Scheme.{u}) (n : Nat) : Prop :=
  Nonempty (StructureSheafH1 X ≃+ (Fin n → K))

/-- The cohomological geometric genus of `X` is strictly greater than one. -/
def GeometricGenusGreaterThanOne (K : Type u) [Field K]
    (X : Scheme.{u}) : Prop :=
  ∃ n : Nat, 1 < n ∧ HasGeometricGenus K X n

/-- The boundary mutation allowing every positive cohomological genus. -/
def GeometricGenusPositive (K : Type u) [Field K]
    (X : Scheme.{u}) : Prop :=
  ∃ n : Nat, 0 < n ∧ HasGeometricGenus K X n

/-- A scheme over `K` with its structure morphism; genus is derived from `scheme`. -/
structure CurveOver (K : Type u) [Field K] where
  scheme : Scheme.{u}
  structureMap : scheme ⟶ SpecOf K

/-- A `K`-rational point represented as a section of the structure morphism. -/
abbrev RationalPoint {K : Type u} [Field K] (X : Scheme.{u})
    (structureMap : X ⟶ SpecOf K) : Type u :=
  { point : SpecOf K ⟶ X // point ≫ structureMap = 𝟙 (SpecOf K) }

/-- The equivalent slice-category representation of a rational point. -/
abbrev OverRationalPoint {K : Type u} [Field K] (X : Scheme.{u})
    (structureMap : X ⟶ SpecOf K) : Type u :=
  Over.mk (𝟙 (SpecOf K)) ⟶ Over.mk structureMap

/-- Checked equivalence between section and slice-category point encodings. -/
def rationalPointEquivOver {K : Type u} [Field K] {X : Scheme.{u}}
    {structureMap : X ⟶ SpecOf K} :
    RationalPoint X structureMap ≃ OverRationalPoint X structureMap where
  toFun p := Over.homMk p.1 p.2
  invFun p := ⟨p.left, by simpa using Over.w p⟩
  left_inv p := by cases p; rfl
  right_inv p := by ext; rfl

namespace CurveOver

variable {K : Type u} [Field K]

/-- Every geometric hypothesis in the selected Faltings statement. -/
def Hypotheses (C : CurveOver.{u} K) : Prop :=
  SmoothOfRelativeDimension 1 C.structureMap ∧
    IsProjectiveOver C.structureMap ∧
      IsGeometricallyConnected C.structureMap ∧
        GeometricGenusGreaterThanOne K C.scheme

end CurveOver

/--
The exact normalized Mordell target: rational points on every smooth,
projective, geometrically connected curve of genus greater than one over a
number field form a finite type.
-/
def FaltingsTarget : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
    SmoothOfRelativeDimension 1 C.structureMap ∧
        IsProjectiveOver C.structureMap ∧
          IsGeometricallyConnected C.structureMap ∧
            (∃ n : Nat, 1 < n ∧
              Nonempty (StructureSheafH1 C.scheme ≃+ (Fin n → K))) →
      Finite (RationalPoint C.scheme C.structureMap)

/-- Checked expansion fixing every ordered binder and geometric hypothesis. -/
theorem faltingsTarget_iff_expanded :
    FaltingsTarget.{u} ↔
      ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
        SmoothOfRelativeDimension 1 C.structureMap ∧
            IsProjectiveOver C.structureMap ∧
              IsGeometricallyConnected C.structureMap ∧
                (∃ n : Nat, 1 < n ∧
                  Nonempty (StructureSheafH1 C.scheme ≃+ (Fin n → K))) →
          Finite (RationalPoint C.scheme C.structureMap) :=
  Iff.rfl

/-- Checked transport of point finiteness to the slice-category encoding. -/
theorem finite_rationalPoint_iff_finite_over
    {K : Type u} [Field K] (C : CurveOver.{u} K) :
    Finite (RationalPoint C.scheme C.structureMap) ↔
      Finite (OverRationalPoint C.scheme C.structureMap) :=
  rationalPointEquivOver.finite_iff

/-- Checked target-level transport to the slice-category point encoding. -/
theorem faltingsTarget_iff_over :
    FaltingsTarget.{u} ↔
      ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
        C.Hypotheses → Finite (OverRationalPoint C.scheme C.structureMap) := by
  constructor
  · intro h K _ _ C hC
    exact (finite_rationalPoint_iff_finite_over C).mp (h K C hC)
  · intro h K _ _ C hC
    exact (finite_rationalPoint_iff_finite_over C).mpr (h K C hC)

/-! Structural mutations elaborate independently and receive no identity credit. -/

def MutationRemovedGenusHypothesis : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
    SmoothOfRelativeDimension 1 C.structureMap ∧
        IsProjectiveOver C.structureMap ∧
          IsGeometricallyConnected C.structureMap →
      Finite (RationalPoint C.scheme C.structureMap)

def MutationRemovedNumberField : Prop :=
  ∀ (K : Type u) [Field K] (C : CurveOver.{u} K),
    C.Hypotheses → Finite (RationalPoint C.scheme C.structureMap)

def MutationChangedCurveBinderScope : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K], ∃ C : CurveOver.{u} K,
    C.Hypotheses → Finite (RationalPoint C.scheme C.structureMap)

def MutationIncludesGenusOne : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver.{u} K),
    SmoothOfRelativeDimension 1 C.structureMap ∧
        IsProjectiveOver C.structureMap ∧
          IsGeometricallyConnected C.structureMap ∧
            GeometricGenusPositive K C.scheme →
      Finite (RationalPoint C.scheme C.structureMap)

variable
  (hRemoved : MutationRemovedGenusHypothesis.{u})
  (hDomain : MutationRemovedNumberField.{u})
  (hScope : MutationChangedCurveBinderScope.{u})
  (hBoundary : MutationIncludesGenusOne.{u})

#check_failure (show FaltingsTarget.{u} from hRemoved)
#check_failure (show FaltingsTarget.{u} from hDomain)
#check_failure (show FaltingsTarget.{u} from hScope)
#check_failure (show FaltingsTarget.{u} from hBoundary)

#check faltingsTarget_iff_expanded
#check faltingsTarget_iff_over
#print axioms faltingsTarget_iff_expanded
#print axioms faltingsTarget_iff_over

set_option pp.universes true in
set_option pp.explicit true in
#print FaltingsTarget

end Stage1Instances.THMM0122
