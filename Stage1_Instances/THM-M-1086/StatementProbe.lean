import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic
import Mathlib.Topology.MetricSpace.CoveringNumbers

/-!
# THM-M-1086 statement infrastructure probe

This is not the canonical Sudakov-minoration target. It checks only that the pinned environment
contains the Gaussian-law and metric packing/covering primitives needed after a source statement
has fixed the missing conventions.
-/

#check ProbabilityTheory.HasGaussianLaw
#check MeasureTheory.integral
#check Metric.coveringNumber
#check Metric.packingNumber
#check Metric.IsSeparated

