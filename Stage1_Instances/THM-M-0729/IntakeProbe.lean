import Mathlib.Analysis.Asymptotics.Defs
import Mathlib.Computability.Language
import Mathlib.Computability.TuringMachine.Computable
import Mathlib.Probability.ProbabilityMassFunction.Monad

/- Discovery-only checks for ingredients of a future exact PCP encoding. -/
#check Language
#check Turing.TM2OutputsInTime
#check Turing.TM2ComputableInPolyTime
#check PMF
#check PMF.pure
#check PMF.bind
#check Asymptotics.IsBigO
