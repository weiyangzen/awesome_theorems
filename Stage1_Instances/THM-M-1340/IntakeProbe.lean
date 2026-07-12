import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.Calculus.FDeriv.Basic

/-! Discovery-only checks for APIs adjacent to a future exact parameter-dependence statement. -/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check IsPicardLindelof
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check HasFDerivAt
#check HasFDerivWithinAt
#check DifferentiableAt
#check DifferentiableWithinAt
