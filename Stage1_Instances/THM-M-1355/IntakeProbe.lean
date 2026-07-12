import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.Analysis.ODE.Basic

/-!
# THM-M-1355 discovery-only intake probe

These checks authenticate adjacent pinned matrix-exponential, spectral, and integral-curve APIs.
They do not define stability, select a continuous or discrete linear-system criterion, or supply
target statement or proof credit.
-/

#check NormedSpace.exp
#check Matrix.exp_diagonal
#check Matrix.exp_conj
#check Matrix.exp_neg
#check Matrix.isUnit_exp
#check Module.End.HasEigenvalue
#check Module.End.HasEigenvalue.mem_spectrum
#check Module.End.hasEigenvalue_iff_mem_spectrum
#check IsIntegralCurve
#check IsIntegralCurveAt
