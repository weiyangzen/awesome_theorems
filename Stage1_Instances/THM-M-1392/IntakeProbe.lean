import Mathlib.Analysis.ODE.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-!
# THM-M-1392 discovery-only intake probe

These checks authenticate adjacent pinned ODE, derivative, and interval-integral APIs. They do not
define a boundary-value problem or Green kernel, select a canonical statement, or supply proof
credit for the catalog claim.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check IsIntegralCurve
#check HasDerivAt
#check intervalIntegral
#check intervalIntegral.integral_eq_sub_of_hasDerivAt
