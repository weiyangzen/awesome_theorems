import Mathlib.Computability.Halting
import Mathlib.GroupTheory.PresentedGroup

namespace Stage1.THM_M_0711.AnchorAudit

-- These are the pinned mathlib declarations that are adjacent to the target.
#check PresentedGroup
#check PresentedGroup.mk
#check PresentedGroup.mk_eq_one_iff
#check ComputablePred
#check ComputablePred.halting_problem

-- The only local noncomputability theorem found by the audit concerns halting,
-- not equality to one in a finitely presented group.
#check (ComputablePred.halting_problem :
  (n : Nat) -> Not (ComputablePred fun c => (Nat.Partrec.Code.eval c n).Dom))

#print axioms PresentedGroup.mk_eq_one_iff
#print axioms ComputablePred.halting_problem

end Stage1.THM_M_0711.AnchorAudit
