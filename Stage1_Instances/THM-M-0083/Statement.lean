import Mathlib.CategoryTheory.RepresentedBy

/-!
# THM-M-0083: exact representable-functor statement

This module freezes and tests the universal-element criterion selected at
intake. It does not claim a new proof of a representability theorem.
-/

namespace Stage1Instances.THM_M_0083

open CategoryTheory
open CategoryTheory.Functor
open Opposite

universe w v u

variable {C : Type u} [Category.{v} C]

/-- A Type-valued presheaf has a universal element: evaluation at that
element is bijective on every hom-set. -/
def UniversalElementCriterion (F : Cᵒᵖ ⥤ Type w) : Prop :=
  ∃ (X : C) (x : F.obj (op X)),
    ∀ Y : C, Function.Bijective (fun f : Y ⟶ X => F.map f.op x)

/-- The exact target selected at intake. -/
def RepresentableFunctorTarget (F : Cᵒᵖ ⥤ Type w) : Prop :=
  UniversalElementCriterion F ↔ F.IsRepresentable

/-- A direct expansion using mathlib's universal-element predicate. -/
def PinnedMathlibSourceShape (F : Cᵒᵖ ⥤ Type w) : Prop :=
  (∃ (X : C) (x : F.obj (op X)), F.IsRepresentedBy x) ↔ F.IsRepresentable

/-- Checked transport from the explicit intake wording to the pinned mathlib
statement shape. -/
theorem representableFunctorTarget_iff_pinnedMathlibSourceShape
    (F : Cᵒᵖ ⥤ Type w) :
    RepresentableFunctorTarget F ↔ PinnedMathlibSourceShape F := by
  simp only [RepresentableFunctorTarget, UniversalElementCriterion,
    PinnedMathlibSourceShape, isRepresentedBy_iff]

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationInjectiveOnly (F : Cᵒᵖ ⥤ Type w) : Prop :=
  (∃ (X : C) (x : F.obj (op X)),
    ∀ Y : C, Function.Injective (fun f : Y ⟶ X => F.map f.op x)) ↔
      F.IsRepresentable

def mutationSurjectiveOnly (F : Cᵒᵖ ⥤ Type w) : Prop :=
  (∃ (X : C) (x : F.obj (op X)),
    ∀ Y : C, Function.Surjective (fun f : Y ⟶ X => F.map f.op x)) ↔
      F.IsRepresentable

def mutationExistsTestObject (F : Cᵒᵖ ⥤ Type w) : Prop :=
  (∃ (X : C) (x : F.obj (op X)) (Y : C),
    Function.Bijective (fun f : Y ⟶ X => F.map f.op x)) ↔
      F.IsRepresentable

def mutationReverseDirectionOnly (F : Cᵒᵖ ⥤ Type w) : Prop :=
  F.IsRepresentable → UniversalElementCriterion F

/-- Empty categories remain in scope; both sides of the selected equivalence
are false rather than being excluded by a nonemptiness hypothesis. -/
theorem empty_category_boundary (F : (Discrete Empty)ᵒᵖ ⥤ Type w) :
    ¬ UniversalElementCriterion F ∧ ¬ F.IsRepresentable := by
  constructor
  · rintro ⟨X, _x, _h⟩
    exact Empty.elim X.as
  · rw [IsRepresentable.iff_exists_isRepresentedBy]
    rintro ⟨X, _x, _h⟩
    exact Empty.elim X.as

end Stage1Instances.THM_M_0083

set_option pp.explicit true in
#print Stage1Instances.THM_M_0083.RepresentableFunctorTarget
