import Mathlib.Probability.Moments.Variance
import Mathlib.Probability.StrongLaw

/-!
# THM-M-1479 discovery-only intake probe

These checks authenticate pinned expectation, independence, identical-distribution, variance,
Chebyshev-bound, and strong-law interfaces adjacent to possible Monte Carlo theorems. They do not
select a sampling model, estimator, convergence or error claim, source proposition, or proof of
THM-M-1479.
-/

#check MeasureTheory.Integrable
#check ProbabilityTheory.IndepFun
#check ProbabilityTheory.IdentDistrib
#check ProbabilityTheory.variance
#check ProbabilityTheory.IndepFun.variance_sum
#check ProbabilityTheory.meas_ge_le_variance_div_sq
#check ProbabilityTheory.strong_law_ae_real
#check ProbabilityTheory.strong_law_ae

#print axioms ProbabilityTheory.IndepFun.variance_sum
#print axioms ProbabilityTheory.meas_ge_le_variance_div_sq
#print axioms ProbabilityTheory.strong_law_ae
