import Mathlib.Analysis.ODE.Basic
import Mathlib.LinearAlgebra.Lagrange
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic

/-!
# THM-M-1397 discovery-only intake probe

These checks authenticate pinned interpolation, integration, ODE, and finite-sum interfaces
adjacent to possible Adams-method encodings. They do not select an Adams-Bashforth, Adams-Moulton,
error, convergence, or stability proposition and do not prove THM-M-1397.
-/

#check Lagrange.interpolate
#check Lagrange.eval_interpolate_at_node
#check intervalIntegral
#check IsIntegralCurve
#check Finset.sum
