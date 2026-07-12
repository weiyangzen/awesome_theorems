import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.Geometry.Manifold.IntegralCurve.Basic
import Mathlib.Geometry.Manifold.MFDeriv.Basic

/-!
# THM-M-1368 discovery-only intake probe

These checks authenticate adjacent pinned ODE, flow, invariant-set, periodic-point, manifold
integral-curve, and tangent-derivative interfaces. They do not define hyperbolicity, stable or
unstable manifolds, transversality, Morse-Smale systems, or structural stability, and they do not
select or prove THM-M-1368.
-/

#check IsIntegralCurve
#check IsMIntegralCurve
#check Flow
#check Flow.orbit
#check IsInvariant
#check Function.IsFixedPt
#check Function.IsPeriodicPt
#check mfderiv
#check tangentMap
