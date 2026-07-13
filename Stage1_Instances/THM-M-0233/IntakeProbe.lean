import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Analysis.Complex.JensenFormula
import Mathlib.Analysis.SpecialFunctions.Complex.LogDeriv

/-!
# THM-M-0233 discovery-only intake probe

These checks authenticate adjacent pinned meromorphic-order, divisor, logarithmic-derivative,
circle-integral, and Jensen-formula APIs. They do not select a canonical contour or statement and
do not prove the argument principle.
-/

#check meromorphicOrderAt
#check MeromorphicOn.divisor
#check MeromorphicOn.divisor_apply
#check logDeriv
#check MeromorphicOn.logDeriv
#check circleIntegral
#check circleIntegral.integral_sub_inv_of_mem_ball
#check MeromorphicOn.circleAverage_log_norm
