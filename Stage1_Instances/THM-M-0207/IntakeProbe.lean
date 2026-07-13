import Mathlib.Geometry.Euclidean.Simplex

/-!
# THM-M-0207 discovery-only intake probe

The catalog does not define the outward construction, center convention, or exact conclusion of
Napoleon's theorem. These checks authenticate adjacent pinned triangle, equilateral, and centroid
interfaces only. They do not construct the three external triangles, select a canonical statement,
or prove the repository target.
-/

#check Affine.Triangle
#check Affine.Simplex.Equilateral
#check Affine.Simplex.Equilateral.dist_eq
#check Affine.Triangle.equilateral_iff_dist_eq_and_dist_eq
#check Affine.Triangle.equilateral_iff_dist_01_eq_02_and_dist_01_eq_12
#check Affine.Simplex.centroid
#check Affine.Simplex.centroid_vsub_eq
#check Affine.Simplex.Equilateral.angle_eq_pi_div_three

#print axioms Affine.Simplex.Equilateral.dist_eq
#print axioms Affine.Triangle.equilateral_iff_dist_01_eq_02_and_dist_01_eq_12
#print axioms Affine.Simplex.Equilateral.angle_eq_pi_div_three
