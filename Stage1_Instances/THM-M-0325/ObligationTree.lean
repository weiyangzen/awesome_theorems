import Statement

/-!
# THM-M-0325 conditional root composition

This file checks only the final interface. `GrothendieckProofPackage` is an
explicit premise for the open analytic proof tree, not a proof of that package.
-/

namespace Stage1Instances.THM_M_0325

universe u

/-- The exact result that the analytic and rounding obligations must deliver. -/
def GrothendieckProofPackage : Prop :=
  GrothendieckInequalityTarget.{u}

/-- Checked child-to-parent composition, conditional on the open package. -/
theorem target_of_proofPackage
    (package : GrothendieckProofPackage.{u}) : GrothendieckInequalityTarget.{u} := by
  exact package

#print axioms target_of_proofPackage

end Stage1Instances.THM_M_0325
