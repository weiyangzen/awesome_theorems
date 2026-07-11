import Mathlib.AlgebraicGeometry.ZariskisMainTheorem

/-! Conditional composition for the frozen THM-M-0107 obligation architecture. -/

open CategoryTheory

namespace Stage1Instances.THM_M_0107.ObligationTree

open AlgebraicGeometry

universe u

set_option maxHeartbeats 800000

def Root : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
    ∃ (Xbar : Scheme.{u}) (j : X ⟶ Xbar) (g : Xbar ⟶ Y),
      IsOpenImmersion j ∧ IsFinite g ∧ j ≫ g = f

/-- This certificate consumes each of the three normalization-property children.
It checks their exact composition but deliberately does not prove them. -/
theorem root_compose
    (openFactor : ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
      [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
      IsOpenImmersion f.toNormalization)
    (finiteFactor : ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
      [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
      IsFinite f.fromNormalization)
    (factorEquation : ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
      [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
      f.toNormalization ≫ f.fromNormalization = f) :
    Root.{u} := by
  intro X Y f _ _ _ _
  exact ⟨f.normalization, f.toNormalization, f.fromNormalization,
    openFactor f, finiteFactor f, factorEquation f⟩

theorem root_exact_type :
    Root.{u} =
      (∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
        [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
        ∃ (Xbar : Scheme.{u}) (j : X ⟶ Xbar) (g : Xbar ⟶ Y),
          IsOpenImmersion j ∧ IsFinite g ∧ j ≫ g = f) :=
  rfl

#print root_compose
#print axioms root_compose

end Stage1Instances.THM_M_0107.ObligationTree
