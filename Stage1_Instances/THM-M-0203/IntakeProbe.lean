import Mathlib.Geometry.Euclidean.Triangle

/-!
# THM-M-0203 discovery-only intake probe

These checks authenticate pinned Euclidean triangle, angle, distance, square-root, and algebraic
interfaces used by the separately elaborated Archive candidate. They do not define an area,
select a canonical target, import the optional Archive theorem, or prove the repository target.
-/

#check EuclideanGeometry.dist_sq_eq_dist_sq_add_dist_sq_sub_two_mul_dist_mul_dist_mul_cos_angle
#check EuclideanGeometry.sin_angle_mul_dist_eq_sin_angle_mul_dist
#check InnerProductGeometry.sin_angle_mul_norm_eq_sin_angle_mul_norm
#check Real.sin_eq_sqrt_one_sub_cos_sq
#check Real.sqrt_div
#check Real.sqrt_mul'
#check Real.sqrt_sq
