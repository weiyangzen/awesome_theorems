import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1057 validation probe

This module checks the exact proof declarations and selected upstream terminals
through Lean's transitive sorry and axiom collectors. It deliberately adds no
mathematical proof content. Importing `Proof` is necessary because the target's
almost-everywhere cocycle hypotheses require the target-specific strictification
implemented there; a short proof-free wrapper around the upstream theorem would
silently strengthen the frozen target.

This is a same-worker trust probe, not an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_1057.Validation

#check Stage1Instances.THM_M_1057.KingmanTarget
#check Stage1Instances.THM_M_1057.root_of_pointwiseLimitPackage
#check ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#check ErgodicTheory.tendsto_birkhoffAverage_ae
#check ErgodicTheory.tendsto_kingman
#check ErgodicTheory.tendsto_kingman_ergodic
#check ErgodicTheory.tendsto_kingman_ergodic_means
#check Stage1Instances.THM_M_1057.pointwiseLimitPackage
#check Stage1Instances.THM_M_1057.kingmanTarget

assert_no_sorry Stage1Instances.THM_M_1057.root_of_pointwiseLimitPackage
assert_no_sorry ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
assert_no_sorry ErgodicTheory.tendsto_birkhoffAverage_ae
assert_no_sorry ErgodicTheory.tendsto_kingman
assert_no_sorry ErgodicTheory.tendsto_kingman_ergodic
assert_no_sorry ErgodicTheory.tendsto_kingman_ergodic_means
assert_no_sorry Stage1Instances.THM_M_1057.pointwiseLimitPackage
assert_no_sorry Stage1Instances.THM_M_1057.kingmanTarget

#print sorries Stage1Instances.THM_M_1057.root_of_pointwiseLimitPackage
#print sorries ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae
#print sorries ErgodicTheory.tendsto_kingman
#print sorries ErgodicTheory.tendsto_kingman_ergodic
#print sorries ErgodicTheory.tendsto_kingman_ergodic_means
#print sorries Stage1Instances.THM_M_1057.pointwiseLimitPackage
#print sorries Stage1Instances.THM_M_1057.kingmanTarget

#print axioms Stage1Instances.THM_M_1057.root_of_pointwiseLimitPackage
#print axioms ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae
#print axioms ErgodicTheory.tendsto_kingman
#print axioms ErgodicTheory.tendsto_kingman_ergodic
#print axioms ErgodicTheory.tendsto_kingman_ergodic_means
#print axioms Stage1Instances.THM_M_1057.pointwiseLimitPackage
#print axioms Stage1Instances.THM_M_1057.kingmanTarget

end Stage1Instances.THM_M_1057.Validation
