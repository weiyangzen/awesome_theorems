import Statement

/-!
# THM-M-0707 proof execution

This module proves the exact arbitrary-program/arbitrary-input target frozen in
`Statement.lean`.  A hypothetical pair decider is restricted computably to
input zero and contradicted by mathlib's pinned fixed-input halting theorem.
-/

namespace Stage1Instances.THM_M_0707.Proof

open Nat.Partrec
open Stage1Instances.THM_M_0707

/-- Pairing an arbitrary code with the fixed input zero is computable. -/
theorem codePairZero_computable :
    Computable (fun c : Code => (c, 0)) := by
  exact Computable.id.pair (Computable.const 0)

/-- Restrict a uniform code/input halting decider to input zero. -/
theorem fixedInputDecider_of_pairDecider
    (hpair : ComputablePred Halts) :
    ComputablePred (fun c : Code => (Code.eval c 0).Dom) := by
  obtain ⟨pairDecidable, pairComputable⟩ := hpair
  let fixedDecidable : DecidablePred (fun c : Code => (Code.eval c 0).Dom) :=
    fun c => pairDecidable (c, 0)
  refine ⟨fixedDecidable, ?_⟩
  simpa [Halts, fixedDecidable] using
    pairComputable.comp codePairZero_computable

/-- The exact frozen halting-problem target. -/
theorem haltingProblemUndecidable : HaltingProblemUndecidable := by
  intro hpair
  exact ComputablePred.halting_problem 0
    (fixedInputDecider_of_pairDecider hpair)

#print axioms codePairZero_computable
#print axioms fixedInputDecider_of_pairDecider
#print axioms haltingProblemUndecidable

end Stage1Instances.THM_M_0707.Proof
