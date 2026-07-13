import Statement
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0741 differential validation reconstruction

This module imports only the frozen statement. It deliberately does not import
the proof-phase module or its obligation-tree implementation. The route below
uses input one rather than the proof phase's input-zero route so that validation
reconstructs the exact pair target through a distinct local reduction term.
-/

namespace Stage1Instances.THM_M_0741.Validation

open Nat.Partrec
open Stage1Instances.THM_M_0741

/-- A separately written reconstruction of the exact frozen target. This is a
same-worker differential check, not an independent-runner attestation. -/
theorem independentlyReconstructedHaltingProblemUndecidable :
    HaltingProblemUndecidable := by
  intro allegedPairDecider
  apply ComputablePred.halting_problem 1
  obtain ⟨pairDecidable, pairComputable⟩ := allegedPairDecider
  let fixedDecidable : DecidablePred (fun code : Code =>
      (Code.eval code 1).Dom) :=
    fun code => pairDecidable (code, 1)
  refine ⟨fixedDecidable, ?_⟩
  simpa [fixedDecidable, Halts] using
    pairComputable.comp (Computable.id.pair (Computable.const 1))

#check independentlyReconstructedHaltingProblemUndecidable
assert_no_sorry ComputablePred.halting_problem
assert_no_sorry independentlyReconstructedHaltingProblemUndecidable
#print sorries independentlyReconstructedHaltingProblemUndecidable
#print sorries ComputablePred.halting_problem
#print axioms independentlyReconstructedHaltingProblemUndecidable
#print axioms ComputablePred.halting_problem

end Stage1Instances.THM_M_0741.Validation
