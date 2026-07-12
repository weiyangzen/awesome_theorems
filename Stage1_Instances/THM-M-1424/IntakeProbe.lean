import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Kernel.Basic
import Mathlib.Dynamics.Ergodic.MeasurePreserving
import Mathlib.Dynamics.Flow

/-!
# THM-M-1424 discovery-only intake probe

These checks authenticate adjacent pinned APIs. They neither define a random dynamical system nor
state or prove a theorem connecting stochastic differential equations to one.
-/

open MeasureTheory

#check Filtration
#check Adapted
#check StronglyAdapted
#check ProbabilityTheory.Kernel
#check ProbabilityTheory.IsMarkovKernel
#check MeasurePreserving
#check Flow
#check Flow.map_add
