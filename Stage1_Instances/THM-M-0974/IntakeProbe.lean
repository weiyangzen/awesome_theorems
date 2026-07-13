/-
Pinned API probe for THM-M-0974 intake.

This file deliberately states no Talagrand concentration theorem. It only checks
nearby convexity, Lipschitz, product-measure, and sub-Gaussian interfaces that a
future source-approved statement may use.
-/

import Mathlib.Analysis.Convex.Function
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Probability.ProductMeasure
import Mathlib.Probability.Moments.SubGaussian

#check ConvexOn
#check LipschitzWith
#check MeasureTheory.Measure.pi
#check MeasureTheory.Measure.infinitePi
#check ProbabilityTheory.HasSubgaussianMGF
#check ProbabilityTheory.HasSubgaussianMGF.measure_ge_le
