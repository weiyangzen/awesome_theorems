import Statement

/-!
# THM-M-0418 independent kernel-validation probe

This module reconstructs the exact frozen target directly from the pinned
mathlib terminal declaration. It deliberately does not import `Proof.lean` or
`ObligationTree.lean`.
-/

open scoped nonZeroDivisors Real
open Module NumberField Ideal Nat

namespace Stage1Instances.THM_M_0418.Validation

universe u

/-- A separately implemented proof of the exact frozen representative-form target. -/
theorem independentMinkowskiIdealClassBound :
    Stage1Instances.THM_M_0418.MinkowskiIdealClassBound.{u} := by
  intro K _ _ C
  exact NumberField.exists_ideal_in_class_of_norm_le C

#check independentMinkowskiIdealClassBound
#print axioms independentMinkowskiIdealClassBound

end Stage1Instances.THM_M_0418.Validation
