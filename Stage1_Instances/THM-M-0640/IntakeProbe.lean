import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Dynamics.FixedPoints.Basic

/-!
Discovery-only checks for APIs adjacent to the ambiguous THM-M-0640 catalog wording.

These declarations expose finite Euclidean spaces, metric closed balls, continuity, self-map, and
fixed-point vocabulary. They do not select the meaning of n-dimensional ball, state Brouwer's
fixed-point theorem, or supply source-fidelity or proof credit.
-/

#check EuclideanSpace
#check Metric.closedBall
#check Metric.mem_closedBall
#check Continuous
#check ContinuousOn
#check Set.MapsTo
#check Function.IsFixedPt
#check Function.fixedPoints
