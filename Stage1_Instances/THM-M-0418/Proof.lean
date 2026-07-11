import Statement

/-!
# THM-M-0418 proof execution

This module closes the frozen representative-form target by applying the
audited theorem in the repository's pinned mathlib dependency.
-/

open scoped nonZeroDivisors Real

open Module NumberField Ideal Nat

namespace Stage1Instances.THM_M_0418

universe u

/-- Kernel-checked proof of the exact proposition frozen in `Statement.lean`.
The terminal body is the pinned mathlib declaration
`NumberField.exists_ideal_in_class_of_norm_le`; this declaration is the exact
repo-local adapter and receives no duplicate proof-body credit. -/
theorem minkowskiIdealClassBound_proof : MinkowskiIdealClassBound.{u} := by
  intro K _ _ C
  exact NumberField.exists_ideal_in_class_of_norm_le C

/-- Checked composition from the proof declaration to the literal source
shape used by the anchor audit. -/
theorem pinnedMathlibSourceShape_proof : PinnedMathlibSourceShape.{u} :=
  minkowskiIdealClassBound_iff_pinnedMathlibSourceShape.mp
    minkowskiIdealClassBound_proof

#print axioms NumberField.exists_ideal_in_class_of_norm_le
#print axioms minkowskiIdealClassBound_proof
#print axioms pinnedMathlibSourceShape_proof

end Stage1Instances.THM_M_0418
