import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.Calculus.ParametricIntervalIntegral
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts

/-!
# THM-M-1378 discovery-only intake probe

These checks authenticate pinned variational-calculus substrate adjacent to a future
source-selected Euler-Lagrange encoding. They do not select the catalog proposition, define an
action or admissible variation space, or prove THM-M-1378.
-/

#check IsLocalMin.fderiv_eq_zero
#check IsLocalMax.fderiv_eq_zero
#check IsLocalExtr.fderiv_eq_zero
#check IsLocalMin.deriv_eq_zero
#check intervalIntegral.integral_deriv_smul_eq_sub_of_hasDeriv_right
#check intervalIntegral.integral_smul_deriv_eq_deriv_smul_of_hasDerivAt
#check integral_bilinear_hasFDerivAt_right_eq_neg_left_of_integrable
#check integral_bilinear_fderiv_right_eq_neg_left_of_integrable
