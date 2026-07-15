import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Topology.Sheaves.Abelian

/-!
# THM-M-0110: Kodaira vanishing statement

This module freezes the algebraic formulation selected at intake. The pinned
mathlib snapshot supplies schemes, smooth morphisms, sheaves of
modules, and sheaf cohomology. It does not yet supply the combined native APIs
for projective morphisms, ample invertible sheaves, canonical sheaves, or their
tensor product, so those notions are named as semantic interface predicates.
The cohomology group itself is the concrete mathlib `Sheaf.H` of the underlying
abelian sheaf. No field assumes a vanishing conclusion.

This file states and mutation-tests the target only. It does not prove Kodaira
vanishing.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u

namespace Stage1Instances.THMM0110

/-- The base scheme of a commutative ring. -/
abbrev SpecOf (k : Type u) [CommRing k] : Scheme.{u} :=
  Spec (CommRingCat.of k)

/--
Data needed to state the selected algebraic Kodaira theorem in the pinned API.
The named proposition fields have their standard algebro-geometric meanings
and are compatibility boundaries for future native definitions. `K`, `L`, and
`KTensorL` are actual mathlib sheaves of modules, and the conclusion uses the
actual underlying abelian sheaf of `KTensorL`.
-/
structure KodairaVanishingData (k : Type u) [Field k] where
  X : Scheme.{u}
  structureMap : X ⟶ SpecOf k
  isProjectiveOverBase : Prop
  K : X.Modules
  L : X.Modules
  KTensorL : X.Modules
  KIsCanonicalSheaf : Prop
  KIsDualizingSheaf : Prop
  LIsInvertibleSheaf : Prop
  LIsLocallyFreeRankOne : Prop
  LIsAmple : Prop
  KTensorLModelsTensorProduct : Prop

namespace KodairaVanishingData

variable {k : Type u} [Field k]

/-- All geometric and sheaf-encoding hypotheses of the frozen target. -/
def Hypotheses (D : KodairaVanishingData.{u} k) : Prop :=
  IsIntegral D.X ∧ Smooth D.structureMap ∧ D.isProjectiveOverBase ∧
    D.KIsCanonicalSheaf ∧ D.KIsDualizingSheaf ∧
      D.LIsInvertibleSheaf ∧ D.LIsLocallyFreeRankOne ∧ D.LIsAmple ∧
        D.KTensorLModelsTensorProduct

/-- The concrete mathlib cohomology type of the supplied `K_X ⊗ L` module. -/
def Cohomology (D : KodairaVanishingData.{u} k) (i : Nat) : Type u :=
  ((SheafOfModules.toSheaf D.X.ringCatSheaf).obj D.KTensorL).H i

/-- Positive-degree vanishing of the concrete mathlib sheaf-cohomology type. -/
def VanishingConclusion (D : KodairaVanishingData.{u} k) : Prop :=
  ∀ i : Nat, 0 < i → Subsingleton (D.Cohomology i)

end KodairaVanishingData

/--
The exact normalized target: over every characteristic-zero field, if `X` is
a smooth projective variety and `L` is an ample invertible sheaf, then
`H^i(X, ω_X ⊗ L)` vanishes for every positive degree `i`.
-/
def KodairaVanishingTarget : Prop :=
  ∀ (k : Type u) [Field k] [CharZero k]
    (D : KodairaVanishingData.{u} k),
      D.Hypotheses → D.VanishingConclusion

/-- Checked expansion fixing every ordered binder, hypothesis, and degree. -/
theorem kodairaVanishingTarget_iff_expanded :
    KodairaVanishingTarget.{u} ↔
      ∀ (k : Type u) [Field k] [CharZero k]
        (D : KodairaVanishingData.{u} k),
          IsIntegral D.X ∧ Smooth D.structureMap ∧ D.isProjectiveOverBase ∧
            D.KIsCanonicalSheaf ∧ D.KIsDualizingSheaf ∧
              D.LIsInvertibleSheaf ∧ D.LIsLocallyFreeRankOne ∧ D.LIsAmple ∧
                D.KTensorLModelsTensorProduct →
            ∀ i : Nat, 0 < i → Subsingleton (D.Cohomology i) :=
  Iff.rfl

/-! Structural mutations elaborate independently and receive no identity credit. -/

def MutationRemovedAmpleHypothesis : Prop :=
  ∀ (k : Type u) [Field k] [CharZero k]
    (D : KodairaVanishingData.{u} k),
      IsIntegral D.X ∧ Smooth D.structureMap ∧ D.isProjectiveOverBase ∧
        D.KIsCanonicalSheaf ∧ D.KIsDualizingSheaf ∧
          D.LIsInvertibleSheaf ∧ D.LIsLocallyFreeRankOne ∧
            D.KTensorLModelsTensorProduct → D.VanishingConclusion

def MutationRemovedCharacteristicZero : Prop :=
  ∀ (k : Type u) [Field k] (D : KodairaVanishingData.{u} k),
    D.Hypotheses → D.VanishingConclusion

def MutationChangedDegreeBinderScope : Prop :=
  ∃ i : Nat, 0 < i ∧
    ∀ (k : Type u) [Field k] [CharZero k]
      (D : KodairaVanishingData.{u} k),
        D.Hypotheses → Subsingleton (D.Cohomology i)

def MutationIncludesDegreeZero : Prop :=
  ∀ (k : Type u) [Field k] [CharZero k]
    (D : KodairaVanishingData.{u} k),
      D.Hypotheses → Subsingleton (D.Cohomology 0)

variable
  (hRemoved : MutationRemovedAmpleHypothesis.{u})
  (hDomain : MutationRemovedCharacteristicZero.{u})
  (hScope : MutationChangedDegreeBinderScope.{u})
  (hBoundary : MutationIncludesDegreeZero.{u})

#check_failure (show KodairaVanishingTarget.{u} from hRemoved)
#check_failure (show KodairaVanishingTarget.{u} from hDomain)
#check_failure (show KodairaVanishingTarget.{u} from hScope)
#check_failure (show KodairaVanishingTarget.{u} from hBoundary)

#check kodairaVanishingTarget_iff_expanded
#print axioms kodairaVanishingTarget_iff_expanded

set_option pp.universes true in
set_option pp.explicit true in
#print KodairaVanishingTarget

end Stage1Instances.THMM0110
