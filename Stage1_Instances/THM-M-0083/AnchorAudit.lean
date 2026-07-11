import Mathlib.CategoryTheory.RepresentedBy

/-!
# THM-M-0083 immutable mathlib anchor

This module checks the exact universal-element equivalence against the pinned
mathlib declaration. It is candidate evidence for the anchor-audit phase only.
-/

namespace Stage1Instances.THM_M_0083_AnchorAudit

open CategoryTheory CategoryTheory.Functor Opposite

universe w v u

variable {C : Type u} [Category.{v} C]

/-- Literal copy of the frozen target, kept independent of the statement file
so this audit checks the upstream bridge rather than importing a local proof. -/
def ExactTarget (F : Cᵒᵖ ⥤ Type w) : Prop :=
  (∃ (X : C) (x : F.obj (op X)),
    ∀ Y : C, Function.Bijective (fun f : Y ⟶ X => F.map f.op x)) ↔
      F.IsRepresentable

/-- Exact wrapper over the pinned mathlib representation criterion. -/
theorem exactTarget_mathlib_candidate (F : Cᵒᵖ ⥤ Type w) : ExactTarget F := by
  rw [ExactTarget, IsRepresentable.iff_exists_isRepresentedBy]
  simp only [isRepresentedBy_iff]

#check CategoryTheory.Functor.IsRepresentable.iff_exists_isRepresentedBy
#check CategoryTheory.Functor.isRepresentedBy_iff
#print axioms CategoryTheory.Functor.IsRepresentable.iff_exists_isRepresentedBy
#print axioms exactTarget_mathlib_candidate

end Stage1Instances.THM_M_0083_AnchorAudit
