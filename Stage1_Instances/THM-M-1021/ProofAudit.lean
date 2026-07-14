import «Stage1_Instances».«THM-M-1021».Proof
import Mathlib.Util.AssertNoSorry

open MeasureTheory

namespace AwesomeTheorems.Stage1.THM_M_1021.ProofAudit

#check @bochner_theorem
#check AwesomeTheorems.Stage1.THM_M_1021.bochner_forward
#check AwesomeTheorems.Stage1.THM_M_1021.bochner_reverse
#check AwesomeTheorems.Stage1.THM_M_1021.bochner_exact

assert_no_sorry bochner_theorem
assert_no_sorry AwesomeTheorems.Stage1.THM_M_1021.bochner_forward
assert_no_sorry AwesomeTheorems.Stage1.THM_M_1021.bochner_reverse
assert_no_sorry AwesomeTheorems.Stage1.THM_M_1021.bochner_exact

#print sorries bochner_theorem
#print sorries AwesomeTheorems.Stage1.THM_M_1021.bochner_forward
#print sorries AwesomeTheorems.Stage1.THM_M_1021.bochner_reverse
#print sorries AwesomeTheorems.Stage1.THM_M_1021.bochner_exact

#print axioms bochner_theorem
#print axioms AwesomeTheorems.Stage1.THM_M_1021.bochner_forward
#print axioms AwesomeTheorems.Stage1.THM_M_1021.bochner_reverse
#print axioms AwesomeTheorems.Stage1.THM_M_1021.bochner_exact

end AwesomeTheorems.Stage1.THM_M_1021.ProofAudit
