import Mathlib.Computability.Halting

/-!
# THM-M-0707 pinned anchor audit

The pinned fixed-input theorem closes the arbitrary-pair target: a hypothetical
decider for pairs can be restricted computably to pairs `(c, 0)`.
-/

namespace Stage1Instances.THM_M_0707

open Nat.Partrec

#check ComputablePred.halting_problem
#check ComputablePred.halting_problem_re
#check ComputablePred.rice

/-- Exact checked transport from mathlib's fixed-input halting theorem to the
canonical arbitrary-program/arbitrary-input target. -/
theorem haltingProblemUndecidable_of_pinnedMathlibAnchor :
    ¬ComputablePred (fun p : Code × Nat => (Code.eval p.1 p.2).Dom) := by
  intro hpair
  apply ComputablePred.halting_problem 0
  obtain ⟨pairDecidable, pairComputable⟩ := hpair
  let fixedDecidable : DecidablePred (fun c : Code => (Code.eval c 0).Dom) :=
    fun c => pairDecidable (c, 0)
  refine ⟨fixedDecidable, ?_⟩
  simpa [fixedDecidable] using
    pairComputable.comp (Computable.id.pair (Computable.const 0))

end Stage1Instances.THM_M_0707

#print axioms ComputablePred.halting_problem
#print axioms Stage1Instances.THM_M_0707.haltingProblemUndecidable_of_pinnedMathlibAnchor
