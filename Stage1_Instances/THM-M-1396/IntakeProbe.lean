import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof

/-!
# THM-M-1396 discovery-only intake probe

These checks authenticate adjacent pinned ODE-solution, integral-equation, local-existence, and
approximate-trajectory error APIs. They do not define a Runge-Kutta scheme, select a numerical
analysis proposition, or prove THM-M-1396.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check ODE.picard
#check ODE.picard_apply
#check IsPicardLindelof
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check gronwallBound
#check dist_le_of_approx_trajectories_ODE
