import Mathlib.Computability.TuringMachine.Computable

/-!
# THM-M-0729 pinned anchor probes

These checks cover the machine, polynomial-time, logarithm, and finite-counting
infrastructure used by the frozen PCP statement. None is an NP/PCP class
definition or a proof of the PCP theorem.
-/

#check Turing.FinTM2
#check Turing.TM2ComputableInPolyTime
#check Turing.TM2ComputableInPolyTime.toTM2ComputableInTime
#check Polynomial.eval
#check Nat.log2
#check List.ofFn
#check Finset.card_filter_le_iff

