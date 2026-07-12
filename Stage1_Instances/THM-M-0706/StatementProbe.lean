import Mathlib.Computability.TuringMachine.ToPartrec

/-!
This probe checks only that the pinned environment exposes a formal simulation result relating
partial-recursive code evaluation to a Turing-machine evaluator. It is not the canonical target
for the Church-Turing thesis and receives no statement or proof credit.
-/

#check Turing.PartrecToTM2.tr_eval
