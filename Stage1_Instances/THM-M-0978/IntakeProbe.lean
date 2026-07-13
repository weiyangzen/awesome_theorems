import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0978 discovery-only intake probe

These checks authenticate pinned exact-topic Hoeffding and sub-Gaussian interfaces. They do not
select a source proposition, allocate the duplicate Hoeffding catalog records, declare a target,
or provide proof credit for THM-M-0978.
-/

open MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal ProbabilityTheory

#check ProbabilityTheory.HasSubgaussianMGF
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun
#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero
#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc
#check ProbabilityTheory.mgf
#check ProbabilityTheory.cgf

#print axioms ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#print axioms ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc
