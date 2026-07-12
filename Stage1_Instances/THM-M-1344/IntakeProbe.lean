import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.LinearAlgebra.Eigenspace.Basic

/-!
# THM-M-1344 discovery-only intake probe

These checks authenticate adjacent pinned ODE, derivative, and spectral APIs. They do not define
stability, choose a finite- or infinite-dimensional indirect-method statement, or supply target
statement or proof credit.
-/

#check IsIntegralCurve
#check IsIntegralCurveAt
#check IsPicardLindelof
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check ODE_solution_unique_univ
#check HasFDerivAt
#check fderiv
#check spectrum
#check Module.End.hasEigenvalue_iff_mem_spectrum
