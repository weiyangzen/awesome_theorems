import Mathlib.Geometry.Euclidean.Altitude
import Mathlib.Geometry.Euclidean.SignedDist
import Mathlib.Geometry.Euclidean.Simplex

/-!
# THM-M-0208 discovery-only intake probe

These checks authenticate pinned simplex, equilateral-triangle, interior, height, and signed
face-distance interfaces relevant to a future Viviani statement. They do not select a
source-faithful root, state the sum-of-distances theorem, or credit a proof.
-/

#check Affine.Triangle
#check Affine.Simplex.Equilateral
#check Affine.Simplex.Equilateral.dist_eq
#check Affine.Simplex.interior
#check Affine.Simplex.closedInterior
#check Affine.Simplex.interior_subset_closedInterior
#check Affine.Simplex.closedInterior_subset_affineSpan
#check Affine.Simplex.signedInfDist
#check Affine.Simplex.signedInfDist_affineCombination
#check Affine.Simplex.abs_signedInfDist_eq_dist_of_mem_affineSpan_range
#check Affine.Simplex.altitudeFoot
#check Affine.Simplex.height
#check Affine.Simplex.height_pos

#print axioms Affine.Simplex.signedInfDist_affineCombination
#print axioms Affine.Simplex.abs_signedInfDist_eq_dist_of_mem_affineSpan_range
