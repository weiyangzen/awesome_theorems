import Statement

/-!
# THM-M-0415 checked obligation interfaces

This module checks the final `Fintype`-to-`Finite` composition and the pinned
mathlib instance interface.  The obligation registry separately exposes the
substantive class-number construction hidden behind that instance.
-/

open scoped NumberField

namespace Stage1Instances.THM_M_0415.ObligationTree

universe u

/-- The data-bearing child needed by the final wrapper. -/
theorem fintypePresentation_mathlib : FintypePresentation.{u} := by
  intro K _ _
  exact ⟨NumberField.RingOfIntegers.instFintypeClassGroup K⟩

/-- Checked child-to-parent composition, kept independent of the child body. -/
theorem finiteTarget_of_fintypePresentation
    (h : FintypePresentation.{u}) : IdealClassGroupFiniteTarget.{u} :=
  idealClassGroupFiniteTarget_iff_fintypePresentation.mpr h

/-- Exact root wrapper over the pinned mathlib class-number construction. -/
theorem idealClassGroupFinite_mathlib : IdealClassGroupFiniteTarget.{u} :=
  finiteTarget_of_fintypePresentation fintypePresentation_mathlib

#print axioms fintypePresentation_mathlib
#print axioms finiteTarget_of_fintypePresentation
#print axioms idealClassGroupFinite_mathlib

end Stage1Instances.THM_M_0415.ObligationTree
