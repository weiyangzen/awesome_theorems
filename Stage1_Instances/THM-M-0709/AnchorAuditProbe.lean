import Mathlib.Computability.Halting

/-!
Type-check the repo-local statement against the only relevant declarations found in the pinned
mathlib computability surface. None of these declarations is a PCP theorem or a reduction to PCP.
-/

namespace Stage1Instances.THM_M_0709.AnchorAudit

#check @ComputablePred
#check ComputablePred.computable_iff
#check ComputablePred.to_re
#check ComputablePred.rice
#check ComputablePred.halting_problem

end Stage1Instances.THM_M_0709.AnchorAudit
