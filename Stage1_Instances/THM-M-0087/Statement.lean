import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu

/-!
# THM-M-0087: Gabriel-Popescu theorem statement

This file freezes the formulation proved by the pinned mathlib module: for a
separator `G` of a Grothendieck abelian category, `Hom(G, -)` is fully faithful
and has an exact left adjoint. In an abelian setting, exactness of this left
adjoint is represented by preservation of finite limits; preservation of
colimits follows from the displayed adjunction.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

universe v u

namespace Stage1Instances.THM_M_0087

variable (C : Type u) [Category.{v} C] [Abelian C]
  [IsGrothendieckAbelian.{v} C]

/--
The exact Lean target for the Gabriel-Popescu theorem.

All categorical data and universe levels are explicit in the surrounding
binders. The target fixes mathlib's module convention
`ModuleCat (End G)ᵐᵒᵖ` through `preadditiveCoyonedaObj G` and `tensorObj G`.
-/
def Statement : Prop :=
  ∀ G : C, IsSeparator G →
    (preadditiveCoyonedaObj G).Full ∧
    (preadditiveCoyonedaObj G).Faithful ∧
    Nonempty
      (IsGrothendieckAbelian.tensorObj G ⊣ preadditiveCoyonedaObj G) ∧
    PreservesFiniteLimits (IsGrothendieckAbelian.tensorObj G)

#check Statement
#print Statement

end Stage1Instances.THM_M_0087
