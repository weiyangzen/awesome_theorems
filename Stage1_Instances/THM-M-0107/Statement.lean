import Mathlib.AlgebraicGeometry.ZariskisMainTheorem

/-!
# THM-M-0107: Zariski's Main Theorem statement boundary

This module freezes the quasi-finite separated factorization form selected at
intake. It does not prove that statement.
-/

open CategoryTheory

namespace Stage1Instances.THM_M_0107

open AlgebraicGeometry

universe u

/-- The intake-selected factorization form of Zariski's Main Theorem. -/
def ZariskiMainFactorizationTarget : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
    ∃ (Xbar : Scheme.{u}) (j : X ⟶ Xbar) (g : Xbar ⟶ Y),
      IsOpenImmersion j ∧ IsFinite g ∧ j ≫ g = f

/-- The canonical relative-normalization factorization supplied by the pinned API. -/
def RelativeNormalizationFactorizationTarget : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
    IsOpenImmersion f.toNormalization ∧ IsFinite f.fromNormalization ∧
      f.toNormalization ≫ f.fromNormalization = f

/-- The relative-normalization encoding is definitionally a witness for the
existential factorization target. This checks the direction needed to prevent
the canonical API encoding from silently replacing the selected root. -/
theorem relativeNormalization_implies_factorization :
    RelativeNormalizationFactorizationTarget.{u} →
      ZariskiMainFactorizationTarget.{u} := by
  intro h X Y f _ _ _ _
  exact ⟨f.normalization, f.toNormalization, f.fromNormalization, h f⟩

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedQuasiCompact : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f],
    ∃ (Xbar : Scheme.{u}) (j : X ⟶ Xbar) (g : Xbar ⟶ Y),
      IsOpenImmersion j ∧ IsFinite g ∧ j ≫ g = f

def mutationRemovedSeparated : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyQuasiFinite f] [LocallyOfFiniteType f] [QuasiCompact f],
    ∃ (Xbar : Scheme.{u}) (j : X ⟶ Xbar) (g : Xbar ⟶ Y),
      IsOpenImmersion j ∧ IsFinite g ∧ j ≫ g = f

def mutationRemovedLocallyQuasiFinite : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
    ∃ (Xbar : Scheme.{u}) (j : X ⟶ Xbar) (g : Xbar ⟶ Y),
      IsOpenImmersion j ∧ IsFinite g ∧ j ≫ g = f

def mutationFiniteFirstFactor : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
    ∃ (Xbar : Scheme.{u}) (j : X ⟶ Xbar) (g : Xbar ⟶ Y),
      IsFinite j ∧ IsOpenImmersion g ∧ j ≫ g = f

end Stage1Instances.THM_M_0107

set_option pp.explicit true in
#print Stage1Instances.THM_M_0107.ZariskiMainFactorizationTarget
