import Proof

/-!
# THM-M-0452 validation probe

This module checks the exact public type of the quotient proof without adding
any canonical-height or polarization construction.  It intentionally imports
the proof module: this is a same-checkout kernel probe, not an independent
runner or an additional proof body.
-/

noncomputable section

open scoped WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0452.Validation

universe u

/-- Exact-type probe for the only unconditional proof-phase deliverable. -/
theorem quotient_branch_probe :
    Stage1Instances.THM_M_0452.QuotientPairingCoreTarget.{u} :=
  Stage1Instances.THM_M_0452.quotientPairingCoreTarget_of_polarization

#print axioms quotient_branch_probe

end Stage1Instances.THM_M_0452.Validation
