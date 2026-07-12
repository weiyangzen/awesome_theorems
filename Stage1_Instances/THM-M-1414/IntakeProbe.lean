import Mathlib.Dynamics.Flow
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.Dynamics.Transitive

/-! Bounded API checks only; this file states no spectral-decomposition theorem. -/

#check IsInvariant
#check Function.periodicPts
#check Dense
#check MulAction.IsTopologicallyTransitive
#check AddAction.IsTopologicallyTransitive
#check Flow
#check Flow.fromIter
#check Flow.restrict
