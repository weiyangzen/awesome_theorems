import Mathlib.Dynamics.FixedPoints.Topology
import Mathlib.Topology.Homotopy.Basic

/-!
# THM-M-0642 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for fixed points, continuous maps, and
homotopy. They do not define Nielsen fixed-point classes, select a canonical theorem, or provide a
proof body.
-/

#check Function.IsFixedPt
#check Function.fixedPoints
#check Function.mem_fixedPoints_iff
#check isClosed_fixedPoints
#check ContinuousMap
#check ContinuousMap.Homotopy
#check ContinuousMap.Homotopic
#check ContinuousMap.HomotopicRel
