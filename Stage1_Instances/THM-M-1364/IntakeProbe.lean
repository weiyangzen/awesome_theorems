import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.Dynamics.OmegaLimit

/-!
# THM-M-1364 discovery-only intake probe

These checks authenticate pinned generic interfaces adjacent to possible Lorenz-system encodings.
They neither define the Lorenz equations or a chaos predicate nor state or prove any part of
THM-M-1364.
-/

#check IsIntegralCurve
#check IsIntegralCurveOn
#check Flow
#check Flow.orbit
#check omegaLimit
#check Flow.isInvariant_omegaLimit
#check Function.IsFixedPt
#check IsInvariant
#check HasFDerivAt
#check IsCompact
