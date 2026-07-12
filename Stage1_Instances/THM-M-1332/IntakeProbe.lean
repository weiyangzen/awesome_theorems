import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.ODE.Gronwall

/-! Discovery-only checks for pinned Picard-Lindelof existence and ODE uniqueness interfaces. -/

#check IsPicardLindelof
#check ODE.picard
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt₀
#check IsPicardLindelof.exists_forall_mem_closedBall_eq_forall_mem_Icc_hasDerivWithinAt
#check ODE_solution_unique_of_mem_Icc
#check ODE_solution_unique_of_mem_Ioo
#check ODE_solution_unique_of_eventually
#check ODE_solution_unique
#check ODE_solution_unique_univ
