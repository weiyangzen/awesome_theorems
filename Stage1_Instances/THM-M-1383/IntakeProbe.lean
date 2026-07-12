import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.ODE.Basic

/-!
# THM-M-1383 discovery-only intake probe

These checks authenticate pinned interval, integral-curve, local initial-value existence, and
initial-value uniqueness interfaces adjacent to a possible future two-point boundary-value
encoding. They do not define a boundary-value problem, select the catalog proposition, establish a
second endpoint condition, or prove THM-M-1383.
-/

#check Set.Icc
#check IsIntegralCurveOn
#check HasDerivWithinAt
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check ODE_solution_unique_of_mem_Icc
#check Set.EqOn
