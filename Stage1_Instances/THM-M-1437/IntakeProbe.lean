import Mathlib.Dynamics.FixedPoints.Topology
import Mathlib.Dynamics.PeriodicPts.Lemmas

/-!
# THM-M-1437 discovery-only intake probe

These checks authenticate adjacent pinned iteration, periodic-point, fixed-point, semiconjugacy,
and limit APIs. They neither define Feigenbaum universality nor select or prove a target theorem.
-/

#check Function.iterate_succ_apply
#check Function.IsPeriodicPt
#check Function.minimalPeriod
#check Function.isPeriodicPt_minimalPeriod
#check Function.IsPeriodicPt.minimalPeriod_dvd
#check Function.IsFixedPt
#check isFixedPt_of_tendsto_iterate
#check Function.Semiconj
#check Function.Semiconj.iterate_right
#check Filter.Tendsto
