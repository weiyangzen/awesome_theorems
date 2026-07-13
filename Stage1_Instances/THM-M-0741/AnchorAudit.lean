import Mathlib.Computability.Halting

/-!
# THM-M-0741 anchor-audit probe

This module checks a pinned mathlib terminal theorem and an exact audit-local adapter to the
frozen arbitrary-program/arbitrary-input target. It is candidate evidence for the anchor-audit
phase only; it is not an accepted proof-phase declaration.
-/

namespace Stage1Instances.THM_M_0741_AnchorAudit

open Nat.Partrec

/-- Literal audit copy of the frozen target, kept independent of another target's state. -/
def ExactTarget : Prop :=
  Not (ComputablePred fun programInput : Code × Nat =>
    (Code.eval programInput.1 programInput.2).Dom)

/-- Restrict a hypothetical pair decider to the computable section `code |-> (code, 0)`. -/
theorem exactTarget_of_pinnedMathlibAnchor : ExactTarget := by
  intro pairDecider
  apply ComputablePred.halting_problem 0
  obtain ⟨pairDecidable, pairComputable⟩ := pairDecider
  let fixedDecidable : DecidablePred (fun code : Code => (Code.eval code 0).Dom) :=
    fun code => pairDecidable (code, 0)
  refine ⟨fixedDecidable, ?_⟩
  simpa [fixedDecidable] using
    pairComputable.comp (Computable.id.pair (Computable.const 0))

#check ComputablePred.halting_problem
#check ComputablePred.halting_problem_re
#check ComputablePred.halting_problem_not_re
#check ComputablePred.rice
#print ComputablePred.halting_problem
#print axioms ComputablePred.halting_problem
#print axioms exactTarget_of_pinnedMathlibAnchor

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0741_AnchorAudit
