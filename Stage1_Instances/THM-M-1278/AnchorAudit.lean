import Mathlib.Geometry.Manifold.Instances.Sphere
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.MeasureTheory.Measure.Hausdorff

/-!
# THM-M-1278: pinned anchor probes

These declarations are geometric and measure-theoretic infrastructure for the
canonical Onofri statement. None states or proves the Onofri inequality.
-/

#check Metric.sphere
#check Metric.sphere_zero
#check stereographic
#check stereographic_source
#check stereographic_target
#check contMDiff_coe_sphere
#check range_mfderiv_coe_sphere
#check gradient
#check MeasureTheory.Measure.hausdorffMeasure
#check Isometry.hausdorffMeasure_image
#check IsometryEquiv.measurePreserving_hausdorffMeasure

#print axioms stereographic_source
#print axioms stereographic_target
#print axioms contMDiff_coe_sphere
#print axioms range_mfderiv_coe_sphere
#print axioms Isometry.hausdorffMeasure_image
#print axioms IsometryEquiv.measurePreserving_hausdorffMeasure
