import Mathlib.Geometry.Euclidean.Circumcenter
import Mathlib.Geometry.Euclidean.Projection
import Mathlib.Geometry.Euclidean.Sphere.Basic

/-!
# THM-M-0198 discovery-only intake probe

These checks authenticate pinned interfaces that could express a Euclidean triangle, its
circumsphere, projections onto the affine spans of its side faces, and collinearity. They do not
select a canonical statement, assert the Simson line theorem, or add a proof body.
-/

#check Affine.Triangle
#check Affine.Simplex.faceOpposite
#check Affine.Simplex.circumsphere
#check Affine.Simplex.mem_circumsphere
#check Affine.Simplex.orthogonalProjectionSpan
#check EuclideanGeometry.orthogonalProjection_mem
#check EuclideanGeometry.Concyclic
#check Collinear
