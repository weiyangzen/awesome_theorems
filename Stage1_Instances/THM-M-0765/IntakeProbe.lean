import Mathlib.Computability.TuringMachine.ToPartrec

/-!
Discovery-only checks for pinned computability and Turing-machine interfaces adjacent to the
catalog target. No declaration below selects or proves a source-identical theorem.
-/

open Nat.Partrec

#check REPred
#check Partrec.dom_re
#check ComputablePred.to_re
#check Code
#check Code.eval
#check Code.exists_code
#check Turing.PartrecToTM2.tr
#check Turing.PartrecToTM2.init
#check Turing.PartrecToTM2.tr_eval
#check Turing.PartrecToTM2.tr_supports
