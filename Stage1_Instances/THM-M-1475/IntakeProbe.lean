import Mathlib.Analysis.ODE.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.FieldTheory.RatFunc.AsPolynomial
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# THM-M-1475 discovery-only intake probe

These checks authenticate adjacent pinned complex, finite-matrix, rational-function, and analytic
ODE interfaces. They do not define a Runge-Kutta tableau or stability predicate, select a source
proposition, or prove THM-M-1475.
-/

#check Complex.normSq
#check norm
#check Matrix
#check Matrix.mulVec
#check Matrix.mulVecLin
#check Matrix.mulVecLin_apply
#check RatFunc.eval
#check RatFunc.eval_X
#check IsIntegralCurveOn
#check IsIntegralCurveAt
