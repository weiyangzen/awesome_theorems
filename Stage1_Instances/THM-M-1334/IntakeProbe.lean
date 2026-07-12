import Mathlib.Analysis.Analytic.Basic
import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-! Bounded API checks only; this file states no Cauchy-Kovalevskaya theorem. -/

#check IsIntegralCurveAt
#check isIntegralCurveAt_iff_exists_pos
#check AnalyticAt
#check AnalyticOnNhd
#check IsPicardLindelof
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check ODE.contDiffOn_enat_Icc_of_hasDerivWithinAt
#check EuclideanSpace
