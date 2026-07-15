import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0819 validation probe

This module asks Lean to inspect the existing exact Dilworth root and the two
finite partition theorems used by its proof. It deliberately introduces no
theorem or proof body. Reimplementing Dilworth's argument during validation
would cross the validation-only boundary rather than establish independent
runner evidence.

This is a same-worker trust probe, not an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_0819.Validation

#check Stage1Instances.THM_M_0819.DilworthPrimaryTarget
#check minAntichainPartition_eq_chainHeight
#check minChainPartition_eq_antichainWidth
#check Stage1Instances.THM_M_0819_Proof.dilworthPrimary

assert_no_sorry minAntichainPartition_eq_chainHeight
assert_no_sorry minChainPartition_eq_antichainWidth
assert_no_sorry Stage1Instances.THM_M_0819_Proof.dilworthPrimary

#print sorries minAntichainPartition_eq_chainHeight
#print sorries minChainPartition_eq_antichainWidth
#print sorries Stage1Instances.THM_M_0819_Proof.dilworthPrimary

#print axioms minAntichainPartition_eq_chainHeight
#print axioms minChainPartition_eq_antichainWidth
#print axioms Stage1Instances.THM_M_0819_Proof.dilworthPrimary

end Stage1Instances.THM_M_0819.Validation
