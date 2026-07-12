import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.Martingale.OptionalSampling

/-!
# THM-M-1042 statement substrate probe

This file checks only nearby interfaces in the pinned dependency snapshot. It
is not the canonical Dynkin-formula statement: the source-exact stopped-process
variant and a concrete continuous-time Markov generator model remain unfrozen.
-/

open MeasureTheory ProbabilityTheory

#check Kernel
#check IsMarkovKernel
#check Filtration
#check IsStoppingTime
#check stoppedProcess
#check Martingale
#check intervalIntegral
#check HasDerivWithinAt

