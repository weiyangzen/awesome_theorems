import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Topology.Order.IntermediateValue

/-!
# THM-M-1394 discovery-only intake probe

These checks authenticate adjacent pinned IVP trajectory, existence, uniqueness, error-bound, and
intermediate-value interfaces. They do not define a boundary residual or shooting algorithm,
select a source proposition, or prove a shooting-method theorem.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check IsIntegralCurve
#check IsPicardLindelof
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check dist_le_of_approx_trajectories_ODE
#check ODE_solution_unique
#check intermediate_value_Icc
