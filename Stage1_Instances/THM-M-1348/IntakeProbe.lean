import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.OmegaLimit
import Mathlib.Dynamics.PeriodicPts.Defs

/-!
# THM-M-1348 discovery-only intake probe

These checks authenticate pinned integral-curve, flow, omega-limit, invariance, and discrete
periodic-point interfaces adjacent to a future Poincare-Bendixson encoding. They do not select the
catalog's exact statement, define a planar periodic orbit, or prove THM-M-1348.
-/

#check IsIntegralCurve
#check Flow
#check Flow.orbit
#check Flow.forwardOrbit
#check omegaLimit
#check isClosed_omegaLimit
#check Flow.isInvariant_omegaLimit
#check mem_omegaLimit_singleton_iff_map_cluster_point
#check nonempty_omegaLimit_of_isCompact_absorbing
#check Function.IsFixedPt
#check Function.IsPeriodicPt
