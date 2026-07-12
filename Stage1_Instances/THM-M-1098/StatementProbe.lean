import Mathlib.Probability.Kernel.Irreducible
import Mathlib.Probability.Kernel.Invariance
import Mathlib.Probability.Kernel.MeasurableIntegral

/-!
This file probes only the pinned mathlib substrate relevant to drift conditions. It is not the
canonical THM-M-1098 statement: the repository source does not identify a unique proposition.
-/

open MeasureTheory

open scoped ProbabilityTheory

namespace Stage1.THM_M_1098.StatementProbe

#check ProbabilityTheory.Kernel
#check ProbabilityTheory.Kernel.IsIrreducible
#check ProbabilityTheory.Kernel.Invariant
#check MeasureTheory.StronglyMeasurable.integral_kernel

end Stage1.THM_M_1098.StatementProbe
