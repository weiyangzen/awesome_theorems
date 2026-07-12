import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.MeasureTheory.Function.AEEqOfIntegral
import Mathlib.Analysis.Distribution.AEEqOfIntegralContDiff
import Mathlib.Analysis.Calculus.LocalExtr.Basic

/-!
# THM-M-1518 mathlib anchor probes

These probes freeze the nearby APIs found by the anchor audit. None is a
terminal proof of the stationary-action-to-Euler-Lagrange target.
-/

#check intervalIntegral.integral_eq_sub_of_hasDerivAt
#check intervalIntegral.integral_deriv_eq_sub
#check intervalIntegral.integral_mul_deriv_eq_deriv_mul
#check intervalIntegral.integral_smul_deriv_eq_deriv_smul
#check MeasureTheory.Integrable.ae_eq_zero_of_forall_setIntegral_eq_zero
#check ae_eq_zero_of_integral_contDiff_smul_eq_zero
#check IsLocalMin.fderiv_eq_zero
#check IsLocalExtr.fderiv_eq_zero
