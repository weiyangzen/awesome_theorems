import Statement
import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0276 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It separately specializes
the pinned Banach open-mapping theorem to the exact frozen real-and-complex target. This is a
same-worker differential wrapper, not a distinct proof body or independent-runner attestation.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0276.Validation

open Stage1Instances.THM_M_0276

universe u v

/-- A separately written exact-type route from the pinned terminal to both scalar branches. -/
theorem differentialBanachOpenMapping : BanachOpenMappingTarget.{u, v} := by
  constructor
  · intro E F _ _ _ _ _ _ f surj
    exact ContinuousLinearMap.isOpenMap f surj
  · intro E F _ _ _ _ _ _ f surj
    exact ContinuousLinearMap.isOpenMap f surj

assert_no_sorry ContinuousLinearMap.exists_approx_preimage_norm_le
assert_no_sorry ContinuousLinearMap.exists_preimage_norm_le
assert_no_sorry ContinuousLinearMap.isOpenMap
assert_no_sorry differentialBanachOpenMapping

#print sorries ContinuousLinearMap.exists_approx_preimage_norm_le
#print sorries ContinuousLinearMap.exists_preimage_norm_le
#print sorries ContinuousLinearMap.isOpenMap
#print sorries differentialBanachOpenMapping

#print axioms ContinuousLinearMap.exists_approx_preimage_norm_le
#print axioms ContinuousLinearMap.exists_preimage_norm_le
#print axioms ContinuousLinearMap.isOpenMap
#print axioms differentialBanachOpenMapping

end Stage1Instances.THM_M_0276.Validation
