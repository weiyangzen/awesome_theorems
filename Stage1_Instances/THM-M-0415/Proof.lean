import ObligationTree

/-!
# THM-M-0415 proof execution

This module pins the existing mathlib class-number construction and checks a
direct wrapper at the exact frozen target. The terminal proof body remains in
the pinned mathlib dependency; it is not duplicated by this wrapper.
-/

open scoped NumberField

namespace Stage1Instances.THM_M_0415.Proof

universe u

/-- The exact ideal-class-group finiteness target, discharged by the pinned
mathlib `Fintype` instance for the ring of integers of a number field. -/
theorem idealClassGroupFinite :
    IdealClassGroupFiniteTarget.{u} := by
  intro K _ _
  letI : Fintype (ClassGroup (NumberField.RingOfIntegers K)) :=
    NumberField.RingOfIntegers.instFintypeClassGroup K
  exact Finite.of_fintype (ClassGroup (NumberField.RingOfIntegers K))

/-- Exact-type composition through the already checked frozen obligation
interfaces. This independently checks that the pinned data-bearing child
closes the canonical root rather than a nearby proposition. -/
theorem idealClassGroupFinite_via_frozen_composition :
    IdealClassGroupFiniteTarget.{u} :=
  ObligationTree.finiteTarget_of_fintypePresentation
    ObligationTree.fintypePresentation_mathlib

#print axioms idealClassGroupFinite
#print axioms idealClassGroupFinite_via_frozen_composition
#print axioms NumberField.RingOfIntegers.instFintypeClassGroup
#print axioms ClassGroup.fintypeOfAdmissibleOfFinite
#print axioms ClassGroup.fintypeOfAdmissibleOfAlgebraic
#print axioms ClassGroup.mkMMem_surjective

end Stage1Instances.THM_M_0415.Proof
