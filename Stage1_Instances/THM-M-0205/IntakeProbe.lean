import Mathlib.Geometry.Euclidean.Congruence
import Mathlib.Geometry.Euclidean.Triangle
import Mathlib.Analysis.Normed.Affine.Simplex

/-!
# THM-M-0205 discovery-only intake probe

These checks authenticate adjacent pinned Euclidean angle, triangle, distance, collinearity, and
congruence interfaces. They do not define internal side-adjacent trisectors, construct their
intersections, choose an equilateral encoding, declare a canonical target, or prove Morley's
theorem.
-/

#check EuclideanGeometry.angle
#check EuclideanGeometry.angle_add_angle_add_angle_eq_pi
#check EuclideanGeometry.sin_angle_mul_dist_eq_sin_angle_mul_dist
#check EuclideanGeometry.angle_eq_angle_of_dist_eq
#check EuclideanGeometry.dist_eq_of_angle_eq_angle_of_angle_ne_pi
#check EuclideanGeometry.oangle_add_oangle_add_oangle_eq_pi
#check Collinear
#check Wbtw
#check EuclideanGeometry.side_side_side
#check EuclideanGeometry.triangle_congruent_iff_dist_eq
#check Affine.Simplex.Equilateral
#check Affine.Simplex.interior
#check Affine.Triangle.equilateral_iff_dist_01_eq_02_and_dist_01_eq_12
