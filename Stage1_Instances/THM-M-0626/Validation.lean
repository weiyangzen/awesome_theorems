import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0626 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It separately checks the
exact frozen global-continuity target through the pinned `IsConnected.image` theorem. This is a
same-worker differential wrapper, not a distinct proof body or independent-runner attestation.
-/

namespace Stage1Instances.THM_M_0626.Validation

universe u v

/-- A separately written exact-type route from the pinned local theorem to the frozen global root. -/
theorem differentialConnectedImage :
    Stage1Instances.THM_M_0626.ConnectedImageTarget.{u, v} := by
  intro alpha beta _ _ s hs f hf
  exact hs.image f hf.continuousOn

assert_no_sorry IsPreconnected.image
assert_no_sorry IsConnected.image
assert_no_sorry differentialConnectedImage

#print sorries IsPreconnected.image
#print sorries IsConnected.image
#print sorries differentialConnectedImage
#print axioms IsPreconnected.image
#print axioms IsConnected.image
#print axioms differentialConnectedImage

end Stage1Instances.THM_M_0626.Validation
