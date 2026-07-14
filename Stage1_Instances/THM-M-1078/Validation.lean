import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1078 validation probe

This module adds no mathematical proof content. It rechecks the two proof-phase
declarations with Lean's transitive sorry and axiom collectors. In particular,
it does not claim that the horizon-local bridge proves the frozen all-future
interface or the exact martingale-transform root.

This is a same-worker trust probe, not independent-runner evidence.
-/

namespace Stage1Instances.THM_M_1078.Validation

#check Stage1Instances.THM_M_1078.Proof.memLp_condExp_of_one_lt
#check Stage1Instances.THM_M_1078.Proof.earlierMemLpUpTo

assert_no_sorry Stage1Instances.THM_M_1078.Proof.memLp_condExp_of_one_lt
assert_no_sorry Stage1Instances.THM_M_1078.Proof.earlierMemLpUpTo

#print sorries Stage1Instances.THM_M_1078.Proof.memLp_condExp_of_one_lt
#print sorries Stage1Instances.THM_M_1078.Proof.earlierMemLpUpTo

#print axioms Stage1Instances.THM_M_1078.Proof.memLp_condExp_of_one_lt
#print axioms Stage1Instances.THM_M_1078.Proof.earlierMemLpUpTo

end Stage1Instances.THM_M_1078.Validation
