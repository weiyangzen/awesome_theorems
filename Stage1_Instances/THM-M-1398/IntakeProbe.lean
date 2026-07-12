import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof

/-!
Discovery-only API checks for a future source-corrected stiff-equation theorem.

These declarations describe continuous ODEs and generic error bounds. They do not define stiffness,
select a numerical method, or state the THM-M-1398 target.
-/

#check IsIntegralCurveOn
#check IsIntegralCurve
#check IsPicardLindelof
#check gronwallBound
#check norm_le_gronwallBound_of_norm_deriv_right_le
#check dist_le_of_approx_trajectories_ODE
#check dist_le_of_trajectories_ODE
#check ODE_solution_unique
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
