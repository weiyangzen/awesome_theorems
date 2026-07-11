import Mathlib.CategoryTheory.Yoneda

/-!
# THM-M-0081 independent validation probe

This module reconstructs the exact frozen target without importing `Proof.lean`.  It uses the
Yoneda embedding's isomorphism equivalence rather than the proof module's separate `preimageIso`
and `mapIso` calls.
-/

open CategoryTheory

universe v u

namespace Stage1Instances.THM_M_0081.Validation

/-- Independent reconstruction of the exact object-detection formulation of Yoneda. -/
theorem independentYonedaObjectDetection {C : Type u} [Category.{v} C] (X Y : C) :
    Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y) := by
  constructor
  · rintro ⟨e⟩
    exact ⟨Yoneda.fullyFaithful.isoEquiv.symm e⟩
  · rintro ⟨e⟩
    exact ⟨Yoneda.fullyFaithful.isoEquiv e⟩

#print axioms independentYonedaObjectDetection

end Stage1Instances.THM_M_0081.Validation
