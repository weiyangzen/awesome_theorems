import Statement
import Mathlib.SetTheory.Cardinal.Order

/-!
# THM-M-0771 independent validation probe

This module does not import `Proof.lean` or `ObligationTree.lean`. It reconstructs
the exact frozen root directly from the pinned mathlib well-order construction.
-/

universe u

namespace Stage1Instances.THM_M_0771.Validation

/-- Separately written reconstruction of the exact relation-level target. -/
theorem independentlyReconstructedRoot : WellOrderingTarget.{u} := by
  intro alpha
  exact IsWellOrder.subtype_nonempty

#print axioms independentlyReconstructedRoot
#print axioms IsWellOrder.subtype_nonempty

end Stage1Instances.THM_M_0771.Validation
