import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.Analysis.Calculus.LocalExtr.Basic

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-1382 catalog wording.

These checks do not select an action functional, admissible variation class, implication direction,
or least/stationary semantics. They state no target theorem and supply no proof credit.
-/

#check intervalIntegral.integral_eq_sub_of_hasDerivAt
#check intervalIntegral.integral_deriv_eq_sub
#check intervalIntegral.integral_mul_deriv_eq_deriv_mul
#check intervalIntegral.integral_smul_deriv_eq_deriv_smul
#check IsLocalMin.fderiv_eq_zero
#check IsLocalExtr.fderiv_eq_zero
