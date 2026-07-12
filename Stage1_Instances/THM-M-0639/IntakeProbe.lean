import Mathlib.Analysis.InnerProductSpace.EuclideanDist
import Mathlib.Topology.Semicontinuity.Hemicontinuity

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0639 catalog wording.

These declarations can encode candidate ingredients. They neither select a canonical source
statement nor state or prove Kakutani's fixed-point theorem.
-/

#check EuclideanSpace
#check Set.Nonempty
#check IsClosed
#check Bornology.IsBounded
#check IsCompact
#check Convex
#check UpperHemicontinuousOn
#check upperHemicontinuousOn_iff_forall_isOpen
#check Metric.isCompact_of_isClosed_isBounded
