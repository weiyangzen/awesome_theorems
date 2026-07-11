import Statement

/-!
# THM-M-0083 proof execution

This module implements both directions of the frozen universal-element
criterion and composes them into the exact representable-functor target.
-/

namespace Stage1Instances.THM_M_0083.Proof

open CategoryTheory CategoryTheory.Functor Opposite
open Stage1Instances.THM_M_0083

universe w v u

variable {C : Type u} [Category.{v} C]

/-- Package a universal element as mathlib's represented-by predicate. -/
theorem representedBy_of_universalElement (F : Cᵒᵖ ⥤ Type w)
    (h : UniversalElementCriterion F) :
    ∃ (X : C) (x : F.obj (op X)), F.IsRepresentedBy x := by
  rcases h with ⟨X, x, hx⟩
  refine ⟨X, x, ?_⟩
  rw [isRepresentedBy_iff]
  intro Y
  exact hx Y

/-- Expand a represented-by witness into the frozen universal-element data. -/
theorem universalElement_of_representedBy (F : Cᵒᵖ ⥤ Type w)
    (h : ∃ (X : C) (x : F.obj (op X)), F.IsRepresentedBy x) :
    UniversalElementCriterion F := by
  rcases h with ⟨X, x, hx⟩
  refine ⟨X, x, ?_⟩
  intro Y
  exact hx.map_bijective

/-- The forward direction of the exact target. -/
theorem forward (F : Cᵒᵖ ⥤ Type w) :
    UniversalElementCriterion F → F.IsRepresentable := by
  intro h
  rw [IsRepresentable.iff_exists_isRepresentedBy]
  exact representedBy_of_universalElement F h

/-- The reverse direction of the exact target. -/
theorem reverse (F : Cᵒᵖ ⥤ Type w) :
    F.IsRepresentable → UniversalElementCriterion F := by
  intro h
  apply universalElement_of_representedBy F
  rwa [← IsRepresentable.iff_exists_isRepresentedBy]

/-- The exact frozen representable-functor theorem. -/
theorem representableFunctorTarget (F : Cᵒᵖ ⥤ Type w) :
    RepresentableFunctorTarget F := by
  exact ⟨forward F, reverse F⟩

#print axioms representedBy_of_universalElement
#print axioms universalElement_of_representedBy
#print axioms forward
#print axioms reverse
#print axioms representableFunctorTarget

end Stage1Instances.THM_M_0083.Proof
