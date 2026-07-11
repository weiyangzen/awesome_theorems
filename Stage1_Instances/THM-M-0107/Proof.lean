import Statement

/-!
# THM-M-0107 proof execution

This module pins the normalization proof bodies available in the configured
mathlib revision and checks exact-root assembly conditional on the remaining
finite-factor obligation.
-/

open CategoryTheory

namespace Stage1Instances.THM_M_0107.Proof

open AlgebraicGeometry

universe u

/-- The pinned Zariski main theorem instance supplies the open first factor. -/
theorem normalization_open {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f] :
    IsOpenImmersion f.toNormalization := by
  infer_instance

/-- Relative normalization composes back to the original morphism. -/
theorem normalization_equation {X Y : Scheme.{u}} (f : X ⟶ Y)
    [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f] :
    f.toNormalization ≫ f.fromNormalization = f :=
  f.toNormalization_fromNormalization

/-- Exact assembly of the frozen existential target from the one proof body
not present in the pinned closure: finiteness of the normalization envelope. -/
theorem exactTarget_of_normalization_finite
    (finiteFactor : ∀ {X Y : Scheme.{u}} (f : X ⟶ Y)
      [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f],
      IsFinite f.fromNormalization) :
    ZariskiMainFactorizationTarget.{u} := by
  intro X Y f _ _ _ _
  exact ⟨f.normalization, f.toNormalization, f.fromNormalization,
    normalization_open f, finiteFactor f, normalization_equation f⟩

#print axioms normalization_open
#print axioms normalization_equation
#print axioms exactTarget_of_normalization_finite

end Stage1Instances.THM_M_0107.Proof
