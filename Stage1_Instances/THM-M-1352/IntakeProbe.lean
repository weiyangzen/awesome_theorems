import Mathlib.Algebra.Ring.Periodic
import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.Normed.Algebra.MatrixExponential

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-1352 catalog wording.

These declarations do not define a principal or fundamental matrix solution, monodromy matrix,
Floquet decomposition, characteristic exponent, reducibility theorem, or stability criterion. They
supply no source-statement or proof credit.
-/

#check Function.Periodic
#check IsIntegralCurve
#check IsIntegralCurveAt
#check HasDerivAt
#check Matrix
#check Matrix.det
#check NormedSpace.exp
#check Matrix.isUnit_exp
