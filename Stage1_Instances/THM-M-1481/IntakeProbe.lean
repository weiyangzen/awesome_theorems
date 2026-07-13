import Mathlib.Data.Finset.Max
import Mathlib.Probability.Kernel.Invariance
import Mathlib.Probability.Kernel.Irreducible

/-!
# THM-M-1481 discovery-only intake probe

These checks authenticate pinned finite-minimum and Markov-kernel interfaces adjacent to possible
future simulated-annealing statements. They do not define an annealing transition, select a cooling
schedule or convergence mode, or prove the catalog claim.
-/

#check ProbabilityTheory.Kernel
#check ProbabilityTheory.IsMarkovKernel
#check ProbabilityTheory.Kernel.Invariant
#check ProbabilityTheory.Kernel.IsReversible
#check ProbabilityTheory.Kernel.IsReversible.invariant
#check ProbabilityTheory.Kernel.IsIrreducible
#check Finset.exists_min_image

#print axioms ProbabilityTheory.Kernel.IsReversible.invariant
#print axioms Finset.exists_min_image
