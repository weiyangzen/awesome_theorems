import Mathlib.Computability.Halting

/-!
# THM-M-0707: exact halting-problem statement

This module freezes the arbitrary-program/arbitrary-input halting predicate for
mathlib's universal partial-recursive-code model. It elaborates the statement
boundary only and contains no proof of undecidability.
-/

namespace Stage1Instances.THM_M_0707

open Nat.Partrec

/-- A code halts on an input exactly when its partial evaluation is defined. -/
def Halts (p : Code × Nat) : Prop :=
  (Code.eval p.1 p.2).Dom

/-- No total partial-recursive Boolean procedure decides halting uniformly for
every program code and every natural-number input. -/
def HaltingProblemUndecidable : Prop :=
  ¬ComputablePred Halts

/-- The canonical target expanded without the local predicate name. -/
def PinnedMathlibSourceShape : Prop :=
  ¬ComputablePred fun p : Code × Nat => (Code.eval p.1 p.2).Dom

/-- Checked identity with the expanded pinned mathlib source shape. -/
theorem haltingProblemUndecidable_iff_pinnedMathlibSourceShape :
    HaltingProblemUndecidable ↔ PinnedMathlibSourceShape :=
  Iff.rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationFixedInput : Prop :=
  ∀ n : Nat, ¬ComputablePred fun c : Code => (Code.eval c n).Dom

def mutationSelfInput : Prop :=
  ¬ComputablePred fun c : Code => (Code.eval c c.encodeCode).Dom

def mutationDroppedEffectivity : Prop :=
  ¬∃ d : Code × Nat → Bool,
    ∀ p, d p = true ↔ Halts p

def mutationSemidecidability : Prop :=
  ¬REPred Halts

/-- The zero code terminates on every input. -/
theorem zero_halts (n : Nat) : Halts (Code.zero, n) := by
  exact Part.some_dom 0

/-- Searching for a zero of the constant-one function diverges. -/
theorem rfind_succ_does_not_halt (n : Nat) : ¬Halts (Code.rfind' Code.succ, n) := by
  simp [Halts, Code.eval]

end Stage1Instances.THM_M_0707

set_option pp.explicit true in
#print Stage1Instances.THM_M_0707.HaltingProblemUndecidable
