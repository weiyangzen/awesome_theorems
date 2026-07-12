import Mathlib.Analysis.Convex.Topology
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Geometry.Euclidean.Triangle
import Mathlib.Topology.Order.Compact

/-!
Discovery-only checks for pinned interfaces adjacent to the ambiguous THM-M-0197 catalog wording.

These declarations can help encode distances, a closed triangular region, vertex angles, and a
minimum after a source selects the exact theorem. They neither state nor prove the Fermat point
theorem, and the imports are not certified minimal for a target that has not been selected.
-/

#check dist
#check convexHull
#check Set.Finite.isCompact_convexHull
#check InnerProductGeometry.angle
#check EuclideanGeometry.angle
#check IsMinOn
#check IsCompact.exists_isMinOn
#check convexOn_dist
