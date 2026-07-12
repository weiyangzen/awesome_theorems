import Mathlib.Algebra.Group.ForwardDiff
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.ODE.Basic

/-!
# THM-M-1395 discovery-only intake probe

These checks authenticate pinned forward-difference, exact-ODE, and Taylor-remainder interfaces
adjacent to the ambiguous catalog wording. They do not define a numerical ODE scheme, select a
source proposition, or prove consistency, stability, convergence, solvability, or an error bound.
-/

#check fwdDiff
#check fwdDiff_iter_eq_sum_shift
#check shift_eq_sum_fwdDiff_iter
#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check IsIntegralCurveAt.hasDerivAt
#check IsIntegralCurve
#check exists_taylor_mean_remainder_bound
