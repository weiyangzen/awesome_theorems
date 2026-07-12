import Mathlib.Probability.CentralLimitTheorem

/-!
# Pinned mathlib anchor check for THM-M-0989

This file checks the declarations found by the anchor audit.  None has the
triangular-array type frozen in `Statement.lean`; this is an inventory check,
not a proof or wrapper for that statement.
-/

open Filter MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory Real Topology

#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check ProbabilityMeasure.tendsto_iff_tendsto_charFun
#check ProbabilityTheory.charFun_gaussianReal

#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
