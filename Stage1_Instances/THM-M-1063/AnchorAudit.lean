import Mathlib.Probability.CentralLimitTheorem
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric

/-!
This module checks the types and axiom provenance of the closest declarations found by the
THM-M-1063 anchor audit. None of them has the continuous-path Donsker conclusion.
-/

#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check ProbabilityTheory.IsGaussianProcess
#check MeasureTheory.TendstoInDistribution
#check MeasureTheory.LevyProkhorov.eq_convergenceInDistribution

#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#print axioms MeasureTheory.LevyProkhorov.eq_convergenceInDistribution
