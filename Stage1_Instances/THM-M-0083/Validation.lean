import Statement

/-!
# THM-M-0083 independent validation probe

This module reconstructs the exact frozen target directly from the pinned
mathlib predicates. It does not import the proof-phase or obligation-tree
modules.
-/

namespace Stage1Instances.THM_M_0083.Validation

open CategoryTheory CategoryTheory.Functor Opposite
open Stage1Instances.THM_M_0083

universe w v u

variable {C : Type u} [Category.{v} C]

/-- Independent exact-root reconstruction through the pinned mathlib API. -/
theorem independentRepresentableFunctorTarget (F : Cᵒᵖ ⥤ Type w) :
    RepresentableFunctorTarget F := by
  constructor
  · rintro ⟨X, x, hx⟩
    rw [IsRepresentable.iff_exists_isRepresentedBy]
    refine ⟨X, x, ?_⟩
    rw [isRepresentedBy_iff]
    intro Y
    exact hx Y
  · rw [IsRepresentable.iff_exists_isRepresentedBy]
    rintro ⟨X, x, hx⟩
    refine ⟨X, x, ?_⟩
    intro Y
    exact hx.map_bijective

#check independentRepresentableFunctorTarget
#print axioms independentRepresentableFunctorTarget

end Stage1Instances.THM_M_0083.Validation
