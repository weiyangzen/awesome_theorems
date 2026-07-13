import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1188 validation probe

This module checks the exact canonical target through separately elaborated
wrappers around the proof-phase root and its frozen composition route. It is
same-worker corroboration, not a separate proof body, an independently
implemented verifier, or an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_1188.Validation

/-- Exact-type validation adapter for the canonical statement. -/
theorem exactCanonicalRoot :
    Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget :=
  Stage1Instances.THM_M_1188.Proof.heatEquationWeakMaximumPrinciple

/-- Exact-type validation adapter for the frozen child-to-root composition. -/
theorem exactComposedRoot :
    Stage1Instances.THM_M_1188.ObligationTree.Root :=
  Stage1Instances.THM_M_1188.Proof.assembledObligationRoot

#check exactCanonicalRoot
#check exactComposedRoot
assert_no_sorry exactCanonicalRoot
assert_no_sorry exactComposedRoot
#print sorries exactCanonicalRoot
#print sorries exactComposedRoot
#print axioms exactCanonicalRoot
#print axioms exactComposedRoot

end Stage1Instances.THM_M_1188.Validation
