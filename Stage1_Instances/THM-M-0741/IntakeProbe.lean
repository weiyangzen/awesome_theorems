import Mathlib.Computability.Halting

/-!
Discovery-only checks for pinned computability interfaces adjacent to the halting-problem target.
No declaration below freezes or proves the source-identical theorem.
-/

open Nat.Partrec

#check Code
#check Code.eval
#check Part.Dom
#check ComputablePred
#check REPred
#check ComputablePred.halting_problem_re
#check ComputablePred.halting_problem
#check ComputablePred.halting_problem_not_re

-- Prospective arbitrary-program/arbitrary-input shape only, not the canonical target.
#check (fun p : Code × Nat => (Code.eval p.1 p.2).Dom)
#check (Not (ComputablePred fun p : Code × Nat => (Code.eval p.1 p.2).Dom))
