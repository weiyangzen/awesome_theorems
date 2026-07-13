import Mathlib.Geometry.Euclidean.NinePointCircle

/-!
# THM-M-0196 discovery-only intake probe

These checks authenticate pinned nine-point-circle definitions and the separate membership bodies
for side midpoints, vertex-orthocenter midpoints, and altitude feet. They do not select a canonical
root, establish source fidelity, perform the downstream anchor audit, or install proof credit.
-/

#check Affine.Simplex.ninePointCircle
#check Affine.Simplex.faceOppositeCentroid_mem_ninePointCircle
#check Affine.Simplex.eulerPoint_mem_ninePointCircle
#check Affine.Triangle.eulerPoint_eq_midpoint
#check Affine.Triangle.altitudeFoot_mem_ninePointCircle
#check Affine.Simplex.ninePointCircle_eq_circumsphere_medial

#print axioms Affine.Simplex.faceOppositeCentroid_mem_ninePointCircle
#print axioms Affine.Simplex.eulerPoint_mem_ninePointCircle
#print axioms Affine.Triangle.altitudeFoot_mem_ninePointCircle
