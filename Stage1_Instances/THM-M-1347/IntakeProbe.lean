import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.Algebra.Module.Submodule.Invariant
import Mathlib.Dynamics.Flow

/-!
# THM-M-1347 discovery-only intake probe

These checks authenticate adjacent pinned ODE, smoothness, linear-operator, spectral, and invariant
set/submodule APIs. They do not define a center manifold, select the catalog's exact statement, or
prove THM-M-1347.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check IsInvariant
#check ContDiff
#check HasFDerivAt
#check ContinuousLinearMap
#check Module.End.invtSubmodule
#check Module.End.mem_invtSubmodule_iff_mapsTo
#check spectrum
