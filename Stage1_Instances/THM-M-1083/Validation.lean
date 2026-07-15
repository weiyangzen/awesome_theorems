import «Stage1_Instances».«THM-M-1083».Proof
import «Stage1_Instances».«THM-M-1083».ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1083 validation probe

This module adds no mathematical proof body. It checks the exact proof root, its external terminal,
the target-specific bridges, and the frozen conditional composition with Lean's transitive
placeholder and axiom collectors. This is a same-worker trust probe, not independent-runner evidence.
-/

namespace Stage1Instances.THM_M_1083.Validation

#check (Stage1Instances.THM_M_1083.Proof.canonicalProof :
  Stage1Instances.THM_M_1083.Statement)
#check ProbabilityTheory.exists_modification_holder
#check Stage1Instances.THM_M_1083.ObligationTree.kolmogorovContinuity_of_engine

assert_no_sorry ProbabilityTheory.exists_modification_holder
assert_no_sorry Stage1Instances.THM_M_1083.Proof.timeInterval_hasBoundedCoveringNumber
assert_no_sorry Stage1Instances.THM_M_1083.Proof.isKolmogorovProcess_of_increment
assert_no_sorry Stage1Instances.THM_M_1083.Proof.kolmogorovContinuity
assert_no_sorry Stage1Instances.THM_M_1083.Proof.canonicalProof
assert_no_sorry Stage1Instances.THM_M_1083.ObligationTree.kolmogorovContinuity_of_engine

#print sorries ProbabilityTheory.exists_modification_holder
  Stage1Instances.THM_M_1083.Proof.timeInterval_hasBoundedCoveringNumber
  Stage1Instances.THM_M_1083.Proof.isKolmogorovProcess_of_increment
  Stage1Instances.THM_M_1083.Proof.kolmogorovContinuity
  Stage1Instances.THM_M_1083.Proof.canonicalProof
  Stage1Instances.THM_M_1083.ObligationTree.kolmogorovContinuity_of_engine

#print axioms ProbabilityTheory.exists_modification_holder
#print axioms Stage1Instances.THM_M_1083.Proof.timeInterval_hasBoundedCoveringNumber
#print axioms Stage1Instances.THM_M_1083.Proof.isKolmogorovProcess_of_increment
#print axioms Stage1Instances.THM_M_1083.Proof.kolmogorovContinuity
#print axioms Stage1Instances.THM_M_1083.Proof.canonicalProof
#print axioms Stage1Instances.THM_M_1083.ObligationTree.kolmogorovContinuity_of_engine

end Stage1Instances.THM_M_1083.Validation
