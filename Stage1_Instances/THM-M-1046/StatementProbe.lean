import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Predictable

/-!
Elaboration probe for the THM-M-1046 exact-statement blocker.

The pinned environment provides the general filtration, martingale, stopping,
and predictable-process substrate checked below. It does not provide the
continuous-local-martingale, quadratic-variation, stochastic-integration, or
stochastic-exponential objects needed to state Novikov's condition exactly.
Consequently this file deliberately does not declare a canonical target.
-/

open MeasureTheory ProbabilityTheory

#check Filtration
#check Martingale
#check IsStoppingTime
#check stoppedProcess
#check IsPredictable

