import Mathlib.Probability.Distributions.Gaussian.Multivariate

/-!
# THM-M-0996 anchor audit

These checks pin the declarations found by the anchor audit.  They are useful
infrastructure for the selected statement, but none states the Gaussian
isoperimetric comparison.
-/

#check ProbabilityTheory.stdGaussian
#check ProbabilityTheory.isProbabilityMeasure_stdGaussian
#check ProbabilityTheory.variance_dual_stdGaussian
#check ProbabilityTheory.stdGaussian_map
#check ProbabilityTheory.map_pi_eq_stdGaussian
#check ProbabilityTheory.stdGaussian_eq_map_pi_orthonormalBasis
#check ProbabilityTheory.gaussianReal
#check ProbabilityTheory.noAtoms_gaussianReal
#check Metric.isOpen_thickening
#check Metric.thickening_of_nonpos
#check Metric.self_subset_thickening
#check MeasureTheory.measure_mono
