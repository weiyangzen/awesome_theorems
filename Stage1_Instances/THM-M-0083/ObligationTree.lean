import Statement

/-!
# THM-M-0083 obligation composition

This module checks the two directed universal-element packages and their exact
composition into the frozen target. The declarations expose the actual pinned
mathlib boundaries rather than treating the short wrapper as an atomic proof.
-/

namespace Stage1Instances.THM_M_0083

open CategoryTheory CategoryTheory.Functor Opposite

universe w v u

variable {C : Type u} [Category.{v} C]

/-- The universal-element-to-representability direction. -/
def ForwardPackage (F : Cᵒᵖ ⥤ Type w) : Prop :=
  UniversalElementCriterion F → F.IsRepresentable

/-- The representability-to-universal-element direction. -/
def ReversePackage (F : Cᵒᵖ ⥤ Type w) : Prop :=
  F.IsRepresentable → UniversalElementCriterion F

/-- Exact composition certificate: both directed children are consumed. -/
theorem root_of_direction_packages (F : Cᵒᵖ ⥤ Type w)
    (forward : ForwardPackage F) (reverse : ReversePackage F) :
    RepresentableFunctorTarget F := by
  exact ⟨forward, reverse⟩

/-- The forward package, exposing both pinned mathlib bridge declarations. -/
theorem forwardPackage_mathlib (F : Cᵒᵖ ⥤ Type w) : ForwardPackage F := by
  rintro ⟨X, x, h⟩
  rw [IsRepresentable.iff_exists_isRepresentedBy]
  refine ⟨X, x, ?_⟩
  rw [isRepresentedBy_iff]
  intro Y
  exact h Y

/-- The reverse package, exposing both pinned mathlib bridge declarations. -/
theorem reversePackage_mathlib (F : Cᵒᵖ ⥤ Type w) : ReversePackage F := by
  rw [ReversePackage, IsRepresentable.iff_exists_isRepresentedBy]
  rintro ⟨X, x, h⟩
  refine ⟨X, x, ?_⟩
  intro Y
  exact h.map_bijective

/-- Checked full composition over the frozen obligation cut set. -/
theorem representableFunctorTarget_mathlib (F : Cᵒᵖ ⥤ Type w) :
    RepresentableFunctorTarget F :=
  root_of_direction_packages F (forwardPackage_mathlib F)
    (reversePackage_mathlib F)

#print axioms root_of_direction_packages
#print axioms forwardPackage_mathlib
#print axioms reversePackage_mathlib
#print axioms representableFunctorTarget_mathlib

end Stage1Instances.THM_M_0083
