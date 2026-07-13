import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Function.LpSeminorm.CompareExp

/-!
# THM-M-0279 discovery-only intake probe

These commands authenticate inequivalent Holder product/integral interfaces in the pinned mathlib
snapshot. They do not select an exact human source proposition, freeze a canonical Lean target, or
prove the repository target.
-/

#check Real.HolderConjugate
#check ENNReal.HolderConjugate
#check ENNReal.lintegral_mul_le_Lp_mul_Lq
#check NNReal.lintegral_mul_le_Lp_mul_Lq
#check MeasureTheory.integral_mul_norm_le_Lp_mul_Lq
#check MeasureTheory.integral_mul_le_Lp_mul_Lq_of_nonneg
#check MeasureTheory.eLpNorm_le_eLpNorm_mul_eLpNorm_of_nnnorm
#check MeasureTheory.eLpNorm_le_eLpNorm_mul_eLpNorm'_of_norm
#check MeasureTheory.MemLp.mul

#print axioms ENNReal.lintegral_mul_le_Lp_mul_Lq
#print axioms NNReal.lintegral_mul_le_Lp_mul_Lq
#print axioms MeasureTheory.integral_mul_norm_le_Lp_mul_Lq
#print axioms MeasureTheory.integral_mul_le_Lp_mul_Lq_of_nonneg
#print axioms MeasureTheory.eLpNorm_le_eLpNorm_mul_eLpNorm_of_nnnorm
