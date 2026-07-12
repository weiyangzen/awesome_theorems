import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Order.Interval.Set.Basic

/-!
# THM-M-1385 discovery-only intake probe

These checks authenticate adjacent pinned real ODE, derivative, interval, and zero-set APIs. They
do not select a Sturm comparison variant, define its solution or consecutive-zero predicates, or
supply target statement or proof credit.
-/

#check IsIntegralCurve
#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check HasDerivAt
#check HasDerivWithinAt
#check Set.Icc
#check Set.Ioo
#check Set.EqOn
#check Function.support
#check Function.mulSupport
