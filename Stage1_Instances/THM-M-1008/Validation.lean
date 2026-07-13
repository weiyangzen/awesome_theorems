import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1008 exact-root validation probe

This module rechecks the proof-phase root at the exact frozen type. It deliberately adds no
mathematical proof route: this is an import/type/trust probe in the same worker and dependency
closure, not an independently implemented proof or a distinct-runner attestation.
-/

noncomputable section

namespace Stage1Instances.THM_M_1008.Validation

universe u v

/-- Exact-type probe for the proof-phase Hewitt-Savage root. -/
theorem exactRootTypeProbe :
    Stage1Instances.THM_M_1008.HewittSavageZeroOneTarget.{u, v} :=
  Stage1Instances.THM_M_1008.hewittSavageZeroOneTarget

#check exactRootTypeProbe
assert_no_sorry Stage1Instances.THM_M_1008.hewittSavageZeroOneTarget
assert_no_sorry exactRootTypeProbe
#print sorries Stage1Instances.THM_M_1008.hewittSavageZeroOneTarget
#print sorries exactRootTypeProbe
#print axioms Stage1Instances.THM_M_1008.hewittSavageZeroOneTarget
#print axioms exactRootTypeProbe

end Stage1Instances.THM_M_1008.Validation
