import Mathlib.Algebra.Ring.Periodic
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.ODE.Basic
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic

/-!
# THM-M-1353 discovery-only intake probe

These checks authenticate adjacent pinned periodicity, ODE, matrix-exponential, and invertible-
matrix interfaces that could support a later source-selected Floquet statement. They do not define
a fundamental matrix, select a Floquet theorem variant, state THM-M-1353, or prove it.
-/

#check Function.Periodic
#check IsIntegralCurve
#check IsIntegralCurveAt
#check NormedSpace.exp
#check Matrix.isUnit_exp
#check Matrix.GeneralLinearGroup
