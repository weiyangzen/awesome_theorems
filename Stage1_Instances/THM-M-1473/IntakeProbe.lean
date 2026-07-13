import Mathlib.Algebra.Group.ForwardDiff
import Mathlib.Analysis.InnerProductSpace.LaxMilgram

/-!
# THM-M-1473 discovery-only intake probe

These checks authenticate pinned finite-difference and stability-adjacent interfaces. They do not
define a hyperbolic PDE, a numerical scheme, either domain of dependence, or a CFL proposition, and
they do not supply statement or proof credit for THM-M-1473.
-/

#check fwdDiff
#check fwdDiff_iter_eq_sum_shift
#check shift_eq_sum_fwdDiff_iter
#check IsCoercive
#check IsCoercive.bounded_below
#check IsCoercive.antilipschitz
#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.continuousLinearEquivOfBilin_apply

#print axioms fwdDiff_iter_eq_sum_shift
#print axioms shift_eq_sum_fwdDiff_iter
#print axioms IsCoercive.bounded_below
#print axioms IsCoercive.continuousLinearEquivOfBilin_apply
