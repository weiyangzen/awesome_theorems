import Statement
import Mathlib.GroupTheory.Perm.Subgroup
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0063 same-worker differential validation probe

This module reconstructs the exact frozen Cayley target from pinned lower-level mathlib APIs. It
deliberately imports neither `Proof` nor `ObligationTree`. This is same-worker corroboration over
the same underlying route, not distinct-runner independent verification.
-/

namespace Stage1Instances.THM_M_0063.Validation

open Stage1Instances.THM_M_0063

universe u

/-- A separately written adapter from the pinned Cayley construction APIs to the frozen target. -/
theorem independentlyReconstructedTarget : CayleyTheoremTarget.{u} := by
  intro G _
  exact ⟨MulEquiv.ofLeftInverse' (MulAction.toPermHom G G)
    (Classical.choose_spec MulAction.toPerm_injective.hasLeftInverse)⟩

assert_no_sorry Equiv.Perm.subgroupOfMulAction
assert_no_sorry independentlyReconstructedTarget

#print sorries Equiv.Perm.subgroupOfMulAction
#print sorries independentlyReconstructedTarget
#print axioms Equiv.Perm.subgroupOfMulAction
#print axioms independentlyReconstructedTarget

end Stage1Instances.THM_M_0063.Validation
