import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-1026 pinned anchor probes

These checks bind the anchor audit to the pinned mathlib probability surface.
The declarations are useful infrastructure, or the ordinary Gaussian CLT, and
do not prove the stable-law/domain-of-attraction target.
-/

#check MeasureTheory.charFun_conv
#check MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun
#check MeasureTheory.ProbabilityMeasure.tendsto_of_tendsto_charFun
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub

#print axioms MeasureTheory.charFun_conv
#print axioms MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun
#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
