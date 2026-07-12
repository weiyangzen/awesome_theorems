import Mathlib.Analysis.InnerProductSpace.EuclideanDist
import Mathlib.Topology.Semicontinuity.Hemicontinuity

/-!
# THM-M-0320: pinned anchor probes

These checks freeze the mathlib APIs retained by the anchor audit. They are
supporting infrastructure, not a proof of Kakutani's fixed-point theorem.
-/

#check UpperHemicontinuousOn
#check UpperHemicontinuousOn.upperHemicontinuousWithinAt
#check UpperHemicontinuousAt.mem_of_tendsto
#check upperHemicontinuousOn_iff_forall_isOpen
#check Metric.isCompact_of_isClosed_isBounded
#check IsCompact.isSeqCompact
#check Convex

