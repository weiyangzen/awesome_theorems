import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof

/-!
# THM-M-1331 discovery-only intake probe

These checks authenticate adjacent pinned existence and uniqueness APIs. They do not select a
canonical combined theorem, resolve the collision with THM-M-1332, or claim proof credit.
-/

#check IsPicardLindelof
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check IsPicardLindelof.exists_forall_mem_closedBall_eq_forall_mem_Icc_hasDerivWithinAt
#check ODE.picard
#check ODE_solution_unique_of_mem_Icc
#check ODE_solution_unique_of_eventually
#check ODE_solution_unique
#check ODE_solution_unique_univ
#check ContDiffAt.exists_forall_mem_closedBall_exists_eq_forall_mem_Ioo_hasDerivAt
