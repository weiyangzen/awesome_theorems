import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic

/-!
# THM-M-1343 discovery-only intake probe

These checks authenticate adjacent pinned ODE, derivative, continuity, and convergence APIs. They
do not select a Lyapunov direct-method proposition, define stability, or prove THM-M-1343.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check IsIntegralCurveAt.hasDerivAt
#check HasFDerivAt
#check ContinuousAt
#check Filter.Tendsto
