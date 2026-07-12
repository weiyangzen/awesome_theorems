import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.LinearAlgebra.Lagrange

/-!
# THM-M-1399 discovery-only intake probe

These checks authenticate pinned interfaces adjacent to a possible future backward-differentiation
formula encoding. They do not define a BDF method, select a catalog proposition, or prove
THM-M-1399.
-/

#check HasDerivAt
#check IsIntegralCurve
#check IsPicardLindelof
#check Lagrange.interpolate
#check Lagrange.iterate_derivative_interpolate
