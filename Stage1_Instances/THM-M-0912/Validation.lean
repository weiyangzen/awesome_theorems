import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0912 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the exact frozen proposition directly from the pinned mathlib
predecessor recurrence. Running it in this worker is useful corroboration, but
is not rev-5.6 distinct-runner independent verification.
-/

namespace Stage1Instances.THM_M_0912.Validation

open Stage1Instances.THM_M_0912

/-- A separately written exact-root reconstruction for differential checking. -/
theorem pascalIdentityTarget_independent_local : PascalIdentityTarget := by
  intro m n hnm hn
  have hm : 0 < m := lt_of_lt_of_le hn hnm
  simpa only [Nat.add_comm] using Nat.choose_eq_choose_pred_add hm hn

assert_no_sorry Nat.choose_eq_choose_pred_add
assert_no_sorry pascalIdentityTarget_independent_local

#print sorries Nat.choose_eq_choose_pred_add
#print sorries pascalIdentityTarget_independent_local

#print axioms Nat.choose_eq_choose_pred_add
#print axioms pascalIdentityTarget_independent_local

end Stage1Instances.THM_M_0912.Validation
