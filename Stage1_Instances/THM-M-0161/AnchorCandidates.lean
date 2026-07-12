import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.LinearAlgebra.CrossProduct

/-!
# THM-M-0161 anchor-candidate elaboration

This file checks the pinned mathlib declarations identified by the anchor
audit. They are supporting ingredients, not a proof of the target theorem.
-/

#check crossProduct
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check ODE_solution_unique_of_mem_Ioo
#check ODE_solution_unique_univ

