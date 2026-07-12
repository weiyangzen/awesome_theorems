import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof

/-!
# THM-M-1335 discovery-only intake probe

These checks authenticate adjacent pinned integral-curve, local-existence, and uniqueness APIs.
They do not define a partial solution, an extension order, a maximal interval, or a continuation
theorem, and they supply no target-statement or proof credit.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check isIntegralCurveAt_iff_exists_mem_nhds
#check IsPicardLindelof
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt₀
#check ContDiffAt.exists_forall_mem_closedBall_exists_eq_forall_mem_Ioo_hasDerivAt₀
#check ODE_solution_unique_of_mem_Ioo
#check ODE_solution_unique_of_eventually
