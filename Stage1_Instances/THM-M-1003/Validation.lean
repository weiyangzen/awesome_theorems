import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1003 exact-root validation probe

This module rechecks the proof-phase root at the exact frozen type. It adds no
mathematical proof route: this is a same-worker import/type/trust probe, not an
independent proof or a distinct-runner attestation.
-/

noncomputable section

namespace Stage1Instances.THM_M_1003.Validation

universe u

/-- Exact-type probe for the proof-phase Lp martingale convergence root. -/
theorem exactRootTypeProbe :
    Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget.{u} :=
  Stage1Instances.THM_M_1003.Proof.target

#check exactRootTypeProbe
assert_no_sorry Stage1Instances.THM_M_1003.Proof.target
assert_no_sorry exactRootTypeProbe
#print sorries Stage1Instances.THM_M_1003.Proof.target
#print sorries exactRootTypeProbe
#print axioms Stage1Instances.THM_M_1003.Proof.target
#print axioms exactRootTypeProbe

end Stage1Instances.THM_M_1003.Validation
