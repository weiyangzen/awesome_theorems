import Mathlib.Computability.Halting

/-!
# THM-M-0707 obligation composition

This module exposes the checked child-to-parent composition selected by the
frozen obligation registry. The imported mathlib theorem remains an explicit
terminal premise of `root_of_fixed_input_anchor`.
-/

namespace Stage1Instances.THM_M_0707

open Nat.Partrec

/-- The exact canonical proposition, repeated here so this narrowly elaborated
module does not depend on an unbuilt local OLean artifact. -/
def HaltingProblemUndecidable : Prop :=
  ¬ComputablePred fun p : Code × Nat => (Code.eval p.1 p.2).Dom

/-- The computable embedding used to restrict a pair decider to input zero. -/
theorem codePairZero_computable :
    Computable (fun c : Code => (c, 0)) := by
  exact Computable.id.pair (Computable.const 0)

/-- A uniform pair decider would decide the fixed-input halting predicate. -/
theorem fixedInputDecider_of_pairDecider
    (hpair : ComputablePred (fun p : Code × Nat => (Code.eval p.1 p.2).Dom)) :
    ComputablePred (fun c : Code => (Code.eval c 0).Dom) := by
  obtain ⟨pairDecidable, pairComputable⟩ := hpair
  let fixedDecidable : DecidablePred (fun c : Code => (Code.eval c 0).Dom) :=
    fun c => pairDecidable (c, 0)
  refine ⟨fixedDecidable, ?_⟩
  simpa [fixedDecidable] using pairComputable.comp codePairZero_computable

/-- Checked composition certificate from the fixed-input terminal theorem to
the exact canonical proposition. -/
theorem root_of_fixed_input_anchor
    (fixedInputAnchor : ¬ComputablePred (fun c : Code => (Code.eval c 0).Dom)) :
    HaltingProblemUndecidable := by
  intro hpair
  exact fixedInputAnchor (fixedInputDecider_of_pairDecider hpair)

/-- The composition instantiated with the pinned mathlib terminal anchor. -/
theorem haltingProblemUndecidable_via_obligation_tree :
    HaltingProblemUndecidable := by
  exact root_of_fixed_input_anchor (ComputablePred.halting_problem 0)

end Stage1Instances.THM_M_0707

#print axioms Stage1Instances.THM_M_0707.codePairZero_computable
#print axioms Stage1Instances.THM_M_0707.fixedInputDecider_of_pairDecider
#print axioms Stage1Instances.THM_M_0707.root_of_fixed_input_anchor
#print axioms Stage1Instances.THM_M_0707.haltingProblemUndecidable_via_obligation_tree
