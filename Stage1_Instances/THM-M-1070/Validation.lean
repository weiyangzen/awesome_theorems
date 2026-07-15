import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1070 validation probe

This module adds no mathematical proof content. It applies Lean's transitive placeholder and
trust collectors to the four proof-phase declarations. The specialized zero-process witness and the
zero-measure countermodel are checked only at their exact types; neither closes the frozen
arbitrary-`P`, arbitrary-`X` root.

This is a same-worker trust probe, not independent-runner evidence.
-/

namespace Stage1Instances.THM_M_1070.Validation

#check Stage1Instances.THM_M_1070.isLevyProcess_iff_expandedSourceShape
#check Stage1Instances.THM_M_1070.isLevyProcess_of_clauses
#check Stage1Instances.THM_M_1070.clauses_of_isLevyProcess
#check Stage1Instances.THM_M_1070.isLevyProcess_zero
#check Stage1Instances.THM_M_1070.zeroMeasure_not_isLevyProcess

assert_no_sorry Stage1Instances.THM_M_1070.isLevyProcess_iff_expandedSourceShape
assert_no_sorry Stage1Instances.THM_M_1070.isLevyProcess_of_clauses
assert_no_sorry Stage1Instances.THM_M_1070.clauses_of_isLevyProcess
assert_no_sorry Stage1Instances.THM_M_1070.isLevyProcess_zero
assert_no_sorry Stage1Instances.THM_M_1070.zeroMeasure_not_isLevyProcess

#print sorries Stage1Instances.THM_M_1070.isLevyProcess_iff_expandedSourceShape
#print sorries Stage1Instances.THM_M_1070.isLevyProcess_of_clauses
#print sorries Stage1Instances.THM_M_1070.clauses_of_isLevyProcess
#print sorries Stage1Instances.THM_M_1070.isLevyProcess_zero
#print sorries Stage1Instances.THM_M_1070.zeroMeasure_not_isLevyProcess

#print axioms Stage1Instances.THM_M_1070.isLevyProcess_iff_expandedSourceShape
#print axioms Stage1Instances.THM_M_1070.isLevyProcess_of_clauses
#print axioms Stage1Instances.THM_M_1070.clauses_of_isLevyProcess
#print axioms Stage1Instances.THM_M_1070.isLevyProcess_zero
#print axioms Stage1Instances.THM_M_1070.zeroMeasure_not_isLevyProcess

end Stage1Instances.THM_M_1070.Validation
