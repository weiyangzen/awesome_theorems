import Statement

/-!
# THM-M-0322 differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the frozen root directly from the pinned mathlib declaration so
the validation run is not merely replaying the local proof adapter.
-/

namespace Stage1Instances.THM_M_0322.Validation

open Set

universe u

/-- Same-worker differential reconstruction of the exact frozen target. -/
theorem kreinMilmanTarget_direct : KreinMilmanTarget.{u} := by
  intro E _ _ _ _ _ _ _ s hscomp hconv
  exact closure_convexHull_extremePoints hscomp hconv

#print axioms kreinMilmanTarget_direct

end Stage1Instances.THM_M_0322.Validation
