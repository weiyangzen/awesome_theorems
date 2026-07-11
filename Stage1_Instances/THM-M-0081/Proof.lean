import Mathlib.CategoryTheory.Yoneda

/-!
# THM-M-0081 proof execution

This module closes the frozen object-detection formulation of the Yoneda lemma.  The reflection
direction uses the fully faithful Yoneda embedding to recover an isomorphism of objects; the
preservation direction maps an object isomorphism through the Yoneda functor.
-/

open CategoryTheory

universe v u

namespace Stage1Instances.THM_M_0081.Proof

/-- A natural isomorphism between contravariant representables reflects to an object isomorphism. -/
theorem reflection {C : Type u} [Category.{v} C] (X Y : C) :
    Nonempty (yoneda.obj X ≅ yoneda.obj Y) → Nonempty (X ≅ Y) := by
  rintro ⟨e⟩
  exact ⟨Yoneda.fullyFaithful.preimageIso e⟩

/-- An object isomorphism is preserved by the Yoneda functor. -/
theorem preservation {C : Type u} [Category.{v} C] (X Y : C) :
    Nonempty (X ≅ Y) → Nonempty (yoneda.obj X ≅ yoneda.obj Y) := by
  rintro ⟨e⟩
  exact ⟨yoneda.mapIso e⟩

/--
The exact frozen target: two objects are isomorphic exactly when their contravariant representable
functors are naturally isomorphic.
-/
theorem yonedaObjectDetection {C : Type u} [Category.{v} C] (X Y : C) :
    Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y) :=
  ⟨reflection X Y, preservation X Y⟩

#print axioms reflection
#print axioms preservation
#print axioms yonedaObjectDetection

end Stage1Instances.THM_M_0081.Proof
