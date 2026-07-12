import Mathlib.Analysis.Calculus.ImplicitContDiff
import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.Dynamics.Flow

/-!
# THM-M-1359 discovery-only intake probe

These checks authenticate pinned generic interfaces adjacent to possible saddle-node encodings.
They do not select a scalar or multidimensional bifurcation statement, supply its nondegeneracy
hypotheses, or prove any part of THM-M-1359.
-/

#check IsIntegralCurve
#check Flow
#check Flow.orbit
#check Function.IsFixedPt
#check HasFDerivAt
#check HasStrictFDerivAt.implicitFunction
#check ImplicitFunctionData.implicitFunction
#check ContDiffAt.implicitFunction
#check ContDiffAt.eventually_apply_eq_iff_implicitFunction
