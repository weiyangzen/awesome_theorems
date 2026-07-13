import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof

/-!
# THM-M-1476 discovery-only intake probe

These checks authenticate adjacent pinned continuous-ODE, trajectory-error, and complex-decay
interfaces. They do not define stiffness, a numerical scheme, or stiff stability, select a source
proposition, or prove THM-M-1476.
-/

#check IsIntegralCurveOn
#check IsIntegralCurve
#check IsPicardLindelof
#check gronwallBound
#check dist_le_of_approx_trajectories_ODE
#check dist_le_of_trajectories_ODE
#check ODE_solution_unique
#check Complex.exp
#check Complex.norm_exp

#print axioms dist_le_of_approx_trajectories_ODE
#print axioms ODE_solution_unique
#print axioms Complex.norm_exp
