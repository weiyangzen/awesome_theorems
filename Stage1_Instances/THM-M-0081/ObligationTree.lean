import Mathlib.CategoryTheory.Yoneda

/-!
# THM-M-0081 conditional obligation composition

This module checks only the architecture frozen by the obligation-tree phase.  Its theorem consumes
the two directions as explicit premises; it does not close either premise or the canonical target.
-/

open CategoryTheory

universe v u

namespace Stage1Instances.THM_M_0081.ObligationTree

def Reflection (C : Type u) [Category.{v} C] (X Y : C) : Prop :=
  Nonempty (yoneda.obj X ≅ yoneda.obj Y) → Nonempty (X ≅ Y)

def Preservation (C : Type u) [Category.{v} C] (X Y : C) : Prop :=
  Nonempty (X ≅ Y) → Nonempty (yoneda.obj X ≅ yoneda.obj Y)

/-- Exact child-to-parent composition certificate.  The two proof packages remain premises. -/
theorem root_compose (C : Type u) [Category.{v} C] (X Y : C)
    (reflection : Reflection C X Y) (preservation : Preservation C X Y) :
    Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y) :=
  ⟨reflection, preservation⟩

#check @root_compose
#print axioms root_compose

end Stage1Instances.THM_M_0081.ObligationTree
