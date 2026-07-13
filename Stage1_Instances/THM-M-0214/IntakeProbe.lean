import Mathlib.Geometry.Euclidean.Angle.Sphere
import Mathlib.Geometry.Euclidean.Triangle

/-!
# THM-M-0214 discovery-only intake probe

These checks authenticate adjacent pinned sphere, angle, inner-product, and Euclidean-triangle
APIs. The sphere APIs use ambient Euclidean geometry, and `law_cos` is Euclidean. This file neither
defines intrinsic spherical distance nor states or proves a spherical-triangle cosine law.
-/

#check EuclideanGeometry.Sphere
#check EuclideanGeometry.mem_sphere
#check EuclideanGeometry.Sphere.oangle_center_eq_two_zsmul_oangle
#check InnerProductGeometry.angle
#check InnerProductGeometry.cos_angle
#check InnerProductGeometry.inner_eq_cos_angle_of_norm_eq_one
#check EuclideanGeometry.angle
#check EuclideanGeometry.law_cos
#check Real.sin
#check Real.cos
