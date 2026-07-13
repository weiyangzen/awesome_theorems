import ObligationTree

/-!
# THM-M-0741 proof-phase installation

This module installs the pinned mathlib Rice and fixed-input halting bodies at
the interfaces frozen in `ObligationTree.lean`. The exact pair target is then
closed through the checked code-to-`(code, 0)` restriction.
-/

namespace Stage1Instances.THM_M_0741.Proof

open Nat.Partrec
open Stage1Instances.THM_M_0741
open Stage1Instances.THM_M_0741.ObligationTree

/-- The pinned Rice theorem installed at the exact frozen bridge interface. -/
theorem riceBridge_pinned : RiceBridge := by
  intro C h f g hf hg hfC
  exact ComputablePred.rice C h hf hg hfC

/-- The fixed-input theorem replayed through the frozen Rice composition. -/
theorem fixedInputZeroUndecidable_via_rice : FixedInputZeroUndecidable :=
  fixedInputZeroUndecidable_of_rice riceBridge_pinned fixedZeroWitnessPackage

/-- The exact pinned fixed-input terminal declaration. -/
theorem fixedInputZeroUndecidable_pinned : FixedInputZeroUndecidable := by
  exact ComputablePred.halting_problem 0

/-- Restrict a hypothetical pair decider along the computable zero-input section. -/
theorem fixedInputReduction_checked : FixedInputReduction :=
  fixedInputReduction_of_restriction
    (pairToFixedRestriction_of_embedding pairZeroEmbedding_computable)

/-- The exact canonical arbitrary-program/arbitrary-input halting target. -/
theorem haltingProblemUndecidable : HaltingProblemUndecidable :=
  root_of_reduction_and_fixedInput fixedInputReduction_checked
    fixedInputZeroUndecidable_pinned

/-- Independent exact-root replay using the explicitly installed Rice bridge. -/
theorem haltingProblemUndecidable_via_rice : HaltingProblemUndecidable :=
  root_of_reduction_and_fixedInput fixedInputReduction_checked
    fixedInputZeroUndecidable_via_rice

#check riceBridge_pinned
#check fixedInputZeroUndecidable_via_rice
#check fixedInputZeroUndecidable_pinned
#check fixedInputReduction_checked
#check haltingProblemUndecidable
#check haltingProblemUndecidable_via_rice

#print sorries ComputablePred.rice
#print sorries ComputablePred.halting_problem
#print sorries riceBridge_pinned
#print sorries fixedInputZeroUndecidable_via_rice
#print sorries fixedInputZeroUndecidable_pinned
#print sorries fixedInputReduction_checked
#print sorries haltingProblemUndecidable
#print sorries haltingProblemUndecidable_via_rice

#print axioms ComputablePred.rice
#print axioms ComputablePred.halting_problem
#print axioms riceBridge_pinned
#print axioms fixedInputZeroUndecidable_via_rice
#print axioms fixedInputZeroUndecidable_pinned
#print axioms fixedInputReduction_checked
#print axioms haltingProblemUndecidable
#print axioms haltingProblemUndecidable_via_rice

end Stage1Instances.THM_M_0741.Proof
