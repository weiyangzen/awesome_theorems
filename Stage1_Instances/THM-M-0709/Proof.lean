import Mathlib.Computability.Reduce
import Statement

/-!
# THM-M-0709 proof-phase bodies

This module checks the pinned halting source and the terminal computability
argument for the frozen binary-PCP target. The actual halting-to-PCP reduction
is not available in the pinned dependency closure and remains an explicit
premise of the final assembly theorem.
-/

namespace Stage1Instances.THM_M_0709

/-- The fixed-input halting predicate used as the source problem. -/
def HaltingPredicate (input : Nat) (code : Nat.Partrec.Code) : Prop :=
  (Nat.Partrec.Code.eval code input).Dom

/-- Computable many-one reducibility pulls a target decider back to a source
decider, so a noncomputable source makes the target noncomputable. -/
theorem not_computablePred_of_manyOneReducible
    {alpha beta : Type*} [Primcodable alpha] [Primcodable beta]
    {source : alpha -> Prop} {target : beta -> Prop}
    (hsource : ¬ ComputablePred source) (hred : source ≤₀ target) :
    ¬ ComputablePred target := by
  intro htarget
  exact hsource (ComputablePred.computable_of_manyOneReducible hred htarget)

/-- The pinned mathlib halting theorem in the selected source-predicate shape. -/
theorem haltingPredicate_not_computable (input : Nat) :
    ¬ ComputablePred (HaltingPredicate input) := by
  exact ComputablePred.halting_problem input

/-- Exact-root assembly from the still-open halting-to-binary-PCP reduction.
The premise exposes rather than assumes the missing construction. -/
theorem postCorrespondenceUndecidable_of_haltingReduction
    (input : Nat)
    (hred : HaltingPredicate input ≤₀ HasSolution) :
    PostCorrespondenceUndecidable := by
  exact not_computablePred_of_manyOneReducible
    (haltingPredicate_not_computable input) hred

#check not_computablePred_of_manyOneReducible
#check haltingPredicate_not_computable
#check postCorrespondenceUndecidable_of_haltingReduction
#print sorries not_computablePred_of_manyOneReducible
#print sorries haltingPredicate_not_computable
#print sorries postCorrespondenceUndecidable_of_haltingReduction
#print sorries ComputablePred.computable_of_manyOneReducible
#print sorries ComputablePred.halting_problem
#print axioms not_computablePred_of_manyOneReducible
#print axioms haltingPredicate_not_computable
#print axioms postCorrespondenceUndecidable_of_haltingReduction
#print axioms ComputablePred.computable_of_manyOneReducible
#print axioms ComputablePred.halting_problem

end Stage1Instances.THM_M_0709
