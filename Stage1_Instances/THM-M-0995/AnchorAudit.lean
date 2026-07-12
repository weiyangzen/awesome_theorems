import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0995 anchor-audit probes

This module checks the pinned mathlib declarations relevant to a future
Bernstein proof. None has the exact type of `StatementShape`.
-/

noncomputable section

open Finset MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0995.AnchorAudit

/-- Immutable mathlib revision inspected by this audit. -/
def mathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Immutable external HighDimProb revision inspected by this audit. -/
def highDimProbRevision : String :=
  "8d4eec8bc06d80e8436ab3505000fca999b46546"

theorem mathlibRevision_frozen :
    mathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" := by
  rfl

theorem highDimProbRevision_frozen :
    highDimProbRevision = "8d4eec8bc06d80e8436ab3505000fca999b46546" := by
  rfl

end Stage1Instances.THM_M_0995.AnchorAudit

#check ProbabilityTheory.measure_ge_le_exp_mul_mgf
#check ProbabilityTheory.measure_ge_le_exp_cgf
#check ProbabilityTheory.HasSubgaussianMGF.measure_ge_le
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun
#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero
#check ProbabilityTheory.IndepFun.variance_sum

#print axioms ProbabilityTheory.measure_ge_le_exp_mul_mgf
#print axioms ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#print axioms ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero
#print axioms ProbabilityTheory.IndepFun.variance_sum
