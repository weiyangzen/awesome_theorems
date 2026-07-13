import Mathlib.LinearAlgebra.AffineSpace.Ceva
import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional

/-!
# THM-M-0199 discovery-only intake probe

These checks authenticate pinned affine-triangle, side-line, interpolation, and collinearity APIs.
The checked Ceva declaration is an explicitly distinct neighboring theorem. Nothing here selects a
signed-ratio convention, states Menelaus's theorem, or supplies proof credit for the target.
-/

open scoped Affine

#check Affine.Triangle
#check Affine.Simplex.points
#check Affine.Simplex.independent
#check AffineMap.lineMap
#check AffineMap.lineMap_apply
#check AffineMap.lineMap_apply_one_sub
#check mem_affineSpan_pair_iff_exists_lineMap_eq
#check Collinear
#check affineIndependent_iff_not_collinear_set
#check Collinear.mem_affineSpan_of_mem_of_ne
#check Affine.Triangle.prod_eq_prod_one_sub_of_mem_line_point_lineMap
