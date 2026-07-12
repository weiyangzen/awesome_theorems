import Mathlib.Dynamics.Flow
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.Dynamics.TopologicalEntropy.CoverEntropy
import Mathlib.Dynamics.Transitive

/-!
# THM-M-1363 discovery-only intake probe

These checks authenticate pinned interfaces adjacent to possible future chaos encodings. They do
not choose a definition of chaos, select a deterministic system, state the catalog target, or prove
any part of THM-M-1363.
-/

#check Flow
#check Flow.fromIter
#check IsInvariant
#check Function.IsPeriodicPt
#check Function.periodicPts
#check MulAction.IsTopologicallyTransitive
#check AddAction.IsTopologicallyTransitive
#check Dynamics.coverEntropy
