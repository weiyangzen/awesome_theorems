import Mathlib.Geometry.Euclidean.Triangle

open scoped EuclideanGeometry Real

/-!
# THM-M-0204 discovery-only intake probe

The repository gloss names a median-length formula, while pinned mathlib provides both the
general cevian identity labeled Stewart's theorem and its midpoint specialization labeled
Apollonius's theorem. These checks authenticate those interfaces only. They do not select either
as the canonical target, establish source fidelity, or add a proof body for THM-M-0204.
-/

#check EuclideanGeometry.dist_sq_mul_dist_add_dist_sq_mul_dist
#check EuclideanGeometry.dist_sq_add_dist_sq_eq_two_mul_dist_midpoint_sq_add_half_dist_sq
#check EuclideanGeometry.angle_eq_pi_iff_sbtw
#check EuclideanGeometry.angle_midpoint_eq_pi
#check dist_left_midpoint
#check dist_right_midpoint

#print axioms EuclideanGeometry.dist_sq_mul_dist_add_dist_sq_mul_dist
#print axioms EuclideanGeometry.dist_sq_add_dist_sq_eq_two_mul_dist_midpoint_sq_add_half_dist_sq
