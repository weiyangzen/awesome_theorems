import Mathlib.Analysis.Complex.UpperHalfPlane.Measure
import Mathlib.Analysis.Complex.UpperHalfPlane.Metric
import Mathlib.Geometry.Euclidean.Angle.Unoriented.Affine

/-!
# THM-M-0220 discovery-only intake probe

These checks authenticate adjacent pinned hyperbolic-plane metric and measure interfaces together
with a Euclidean angle vocabulary. They do not define a hyperbolic geodesic triangle or its
interior angles, select a curvature normalization, state an area-defect formula, or supply proof
credit.
-/

open MeasureTheory
open scoped MatrixGroups

#check UpperHalfPlane
#check UpperHalfPlane.dist_eq
#check UpperHalfPlane.volume_def
#check EuclideanGeometry.angle
#check InnerProductGeometry.angle
#check Real.pi
#synth MetricSpace UpperHalfPlane
#synth MeasureSpace UpperHalfPlane
#synth SMulInvariantMeasure (GL (Fin 2) ℝ) UpperHalfPlane volume
