import Mathlib.Geometry.Euclidean.Angle.Sphere

/-!
# THM-M-0194 discovery-only intake probe

These commands authenticate pinned inscribed-angle and semicircle/right-angle interfaces. They do
not choose the catalogue's angle or arc convention, establish a source-to-Lean transport, or prove
the unfrozen target.
-/

#check Orientation.oangle_eq_two_zsmul_oangle_sub_of_norm_eq
#check Orientation.oangle_eq_two_zsmul_oangle_sub_of_norm_eq_real
#check EuclideanGeometry.Sphere.oangle_center_eq_two_zsmul_oangle
#check EuclideanGeometry.Sphere.angle_eq_pi_div_two_iff_mem_sphere_of_isDiameter
#check EuclideanGeometry.Sphere.angle_eq_pi_div_two_iff_mem_sphere_ofDiameter
#check EuclideanGeometry.Sphere.thales_theorem

#print axioms EuclideanGeometry.Sphere.oangle_center_eq_two_zsmul_oangle
#print axioms EuclideanGeometry.Sphere.thales_theorem
