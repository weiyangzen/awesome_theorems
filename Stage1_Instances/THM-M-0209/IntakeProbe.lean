import Mathlib.Geometry.Euclidean.Sphere.Tangent

/-!
# THM-M-0209 discovery-only intake probe

These checks authenticate pinned Euclidean sphere and internal/external tangency interfaces adjacent
to a future Descartes circle-theorem encoding. They do not model oriented signed bends, select a
canonical four-circle root, perform the downstream anchor audit, or grant proof credit.
-/

#check EuclideanGeometry.Sphere
#check EuclideanGeometry.Sphere.center
#check EuclideanGeometry.Sphere.radius
#check EuclideanGeometry.Sphere.IsExtTangentAt
#check EuclideanGeometry.Sphere.IsIntTangentAt
#check EuclideanGeometry.Sphere.IsExtTangent
#check EuclideanGeometry.Sphere.IsIntTangent
#check EuclideanGeometry.Sphere.IsExtTangent.dist_center
#check EuclideanGeometry.Sphere.IsIntTangent.dist_center
#check EuclideanGeometry.Sphere.isExtTangent_iff_dist_center
#check EuclideanGeometry.Sphere.isIntTangent_iff_dist_center
#check EuclideanGeometry.Sphere.radius_nonneg_of_mem

#print axioms EuclideanGeometry.Sphere.isExtTangent_iff_dist_center
#print axioms EuclideanGeometry.Sphere.isIntTangent_iff_dist_center
