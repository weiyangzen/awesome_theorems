import Statement

/-!
# THM-M-0707 validation reconstruction

This module independently reconstructs the exact frozen target while importing
only `Statement`. It deliberately does not import the proof-phase module or the
obligation-tree implementation.
-/

namespace Stage1Instances.THM_M_0707.Validation

open Nat.Partrec
open Stage1Instances.THM_M_0707

/-- A separately implemented restriction of a hypothetical pair decider to
the section whose input coordinate is zero. -/
private theorem zeroSection
    (h : ComputablePred Halts) :
    ComputablePred (fun c : Code => (Code.eval c 0).Dom) := by
  let includeZero : Code → Code × Nat := fun c => (c, 0)
  have hIncludeZero : Computable includeZero :=
    Computable.id.pair (Computable.const 0)
  obtain ⟨decidePair, computablePair⟩ := h
  let decideZero : DecidablePred (fun c : Code => (Code.eval c 0).Dom) :=
    fun c => decidePair (includeZero c)
  refine ⟨decideZero, ?_⟩
  simpa [Halts, includeZero, decideZero] using computablePair.comp hIncludeZero

/-- Same exact target as the proof phase, reconstructed without importing its
proof body. -/
theorem independentlyReconstructedHaltingProblemUndecidable :
    HaltingProblemUndecidable := by
  intro allegedDecider
  exact ComputablePred.halting_problem 0 (zeroSection allegedDecider)

#print axioms independentlyReconstructedHaltingProblemUndecidable

end Stage1Instances.THM_M_0707.Validation
