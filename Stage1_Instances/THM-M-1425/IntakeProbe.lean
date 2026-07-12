import Mathlib.Dynamics.Flow
import Mathlib.Dynamics.OmegaLimit
import Mathlib.Topology.MetricSpace.HausdorffDistance
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic

/-! Discovery-only API checks for a later source-corrected random-attractor statement. -/

#check Flow
#check IsInvariant
#check IsForwardInvariant
#check omegaLimit
#check Flow.isInvariant_omegaLimit
#check IsCompact
#check Metric.hausdorffDist
#check Measurable
#check Filter.Tendsto
