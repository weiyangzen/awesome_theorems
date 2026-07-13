import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0975 discovery-only intake probe

These commands authenticate pinned conditional sub-Gaussian and Azuma-Hoeffding interfaces. They
do not select the catalog's exact statement, prove a bounded-increment bridge, or establish a
repo-local THM-M-0975 theorem.
-/

#check ProbabilityTheory.HasSubgaussianMGF
#check ProbabilityTheory.HasCondSubgaussianMGF
#check ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF
#check ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF
#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero
#check MeasureTheory.StronglyAdapted
#check MeasureTheory.Filtration

#print axioms ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF
#print axioms ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF
