import Mathlib.Analysis.ODE.Gronwall
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts

/-! Discovery-only checks for APIs adjacent to a future exact Bihari-LaSalle statement. -/

#check gronwallBound
#check le_gronwallBound_of_liminf_deriv_right_le
#check norm_le_gronwallBound_of_norm_deriv_right_le
#check intervalIntegral.integral_mono_on
#check intervalIntegral.integral_nonneg
#check intervalIntegral.integral_comp_mul_deriv
