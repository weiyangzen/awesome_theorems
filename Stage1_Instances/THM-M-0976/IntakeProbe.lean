import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.Moments.SubGaussian
import Mathlib.Logic.Function.Basic

/-!
# THM-M-0976 discovery-only intake probe

These commands authenticate pinned probability, independence, coordinate-update, integration,
finite-sum, and exponential interfaces adjacent to a future source-selected McDiarmid statement.
They do not select or declare the canonical target, establish a source transport, or prove
THM-M-0976.
-/

open MeasureTheory ProbabilityTheory Real

#check ProbabilityTheory.iIndepFun
#check MeasureTheory.IsProbabilityMeasure
#check MeasureTheory.Measure.real
#check MeasureTheory.integral
#check Function.update
#check Finset.sum
#check Real.exp
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun

#print axioms ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
