import Statement
import ObligationTree
import Proof

/-!
# THM-M-1080 exact proof root

This module binds the proof bodies to both threshold-package interfaces in the frozen obligation
tree, composes those packages through the frozen parent theorem, and checks the result against the
canonical statement declaration.
-/

noncomputable section

namespace Stage1Instances.THM_M_1080.ExactRoot

universe u

/-- The implemented positive-threshold body has the frozen package type. -/
theorem positiveThresholdPackage :
    ObligationTree.PositiveThresholdPackage.{u} := by
  simpa only [
    ObligationTree.PositiveThresholdPackage,
    ObligationTree.squaredBoundSum,
    Proof.squaredBoundSum
  ] using Proof.positiveThreshold

/-- The implemented zero-threshold body has the frozen package type. -/
theorem zeroThresholdPackage :
    ObligationTree.ZeroThresholdPackage.{u} := by
  simpa only [
    ObligationTree.ZeroThresholdPackage,
    ObligationTree.squaredBoundSum,
    Proof.squaredBoundSum
  ] using Proof.zeroThreshold

/-- Exact canonical root, obtained through the frozen threshold-package composition theorem. -/
theorem azumaUpperTail_exact :
    Stage1Instances.THM_M_1080.Statement.{u} := by
  simpa only [
    Stage1Instances.THM_M_1080.Statement,
    Stage1Instances.THM_M_1080.AzumaUpperTail,
    Stage1Instances.THM_M_1080.squaredBoundSum,
    ObligationTree.squaredBoundSum
  ] using
    (ObligationTree.azumaUpperTail_of_threshold_packages
      positiveThresholdPackage zeroThresholdPackage)

#print axioms positiveThresholdPackage
#print axioms zeroThresholdPackage
#print axioms azumaUpperTail_exact

end Stage1Instances.THM_M_1080.ExactRoot
