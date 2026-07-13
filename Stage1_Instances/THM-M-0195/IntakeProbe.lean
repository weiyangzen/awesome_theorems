import Mathlib.Geometry.Euclidean.MongePoint

/-!
# THM-M-0195 discovery-only intake probe

These checks authenticate direct Euler-line-adjacent definitions and theorem interfaces in the
pinned mathlib snapshot. They do not choose a source-faithful root, declare the target, derive
collinearity, or credit a proof.
-/

#check Affine.Triangle
#check Affine.Simplex.centroid
#check Affine.Simplex.circumcenter
#check Affine.Triangle.orthocenter
#check Affine.Triangle.orthocenter_eq_mongePoint
#check Affine.Triangle.orthocenter_mem_altitude
#check Affine.Triangle.orthocenter_eq_smul_vsub_vadd_circumcenter
#check Collinear
#check collinear_insert_of_mem_affineSpan_pair
#check smul_vsub_vadd_mem_affineSpan_pair

#print axioms Affine.Triangle.orthocenter_mem_altitude
#print axioms Affine.Triangle.orthocenter_eq_smul_vsub_vadd_circumcenter
