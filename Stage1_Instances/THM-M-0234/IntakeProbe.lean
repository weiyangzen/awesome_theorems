import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Analysis.Analytic.Order
import Mathlib.Analysis.Meromorphic.Divisor

/-!
# THM-M-0234 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for analytic order, isolated zeros, and
meromorphic divisors. They do not select a boundary or zero-count convention, state Rouche's
theorem, reconcile the duplicate catalog target, or supply proof credit.
-/

#check analyticOrderAt
#check analyticOrderNatAt
#check AnalyticAt.analyticOrderAt_eq_natCast
#check AnalyticAt.eventually_eq_zero_or_eventually_ne_zero
#check AnalyticOnNhd.eqOn_zero_or_eventually_ne_zero_of_preconnected
#check MeromorphicOn.divisor
#check MeromorphicOn.divisor_apply
#check MeromorphicOn.AnalyticOnNhd.divisor_nonneg
