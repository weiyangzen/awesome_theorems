import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Analysis.Complex.UpperHalfPlane.Metric
import Mathlib.Geometry.Euclidean.Triangle

/-!
# THM-M-0215 discovery-only intake probe

These checks authenticate pinned hyperbolic-function, upper-half-plane distance, and Euclidean
triangle APIs. They do not define a hyperbolic triangle or angle, select a canonical target, or
prove the hyperbolic law of cosines.
-/

#check Real.sinh
#check Real.cosh
#check Real.cosh_sub
#check Real.cosh_sq_sub_sinh_sq
#check UpperHalfPlane
#check UpperHalfPlane.dist_eq
#check UpperHalfPlane.cosh_dist
#check InnerProductGeometry.norm_sub_sq_eq_norm_sq_add_norm_sq_sub_two_mul_norm_mul_norm_mul_cos_angle
