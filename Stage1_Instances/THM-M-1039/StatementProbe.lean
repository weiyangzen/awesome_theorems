import Mathlib.Probability.Kernel.CondDistrib
import Mathlib.Probability.Process.Filtration

/-!
# THM-M-1039 statement substrate probe

This file checks the pinned mathlib types needed to express the Markov
conclusion already described by the intake. It is not a canonical SDE theorem
statement: the source record does not fix an exact theorem, and the pinned
dependency closure has no concrete SDE, Brownian-motion, or stochastic-integral
object model with which to encode its hypotheses.
-/

open MeasureTheory ProbabilityTheory

#check Filtration
#check Kernel
#check IsMarkovKernel
#check condDistrib
#check condExp
