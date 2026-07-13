import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional
import Mathlib.LinearAlgebra.Projectivization.Constructions
import Mathlib.LinearAlgebra.Projectivization.Subspace

/-!
# THM-M-0210 discovery-only intake probe

These checks authenticate adjacent pinned affine-collinearity and projective-space interfaces.
They do not choose an affine or projective form of Desargues's theorem, define perspective
triangles or corresponding-side intersections, declare the target, or supply proof credit.
-/

open scoped LinearAlgebra.Projectivization

#check Collinear
#check collinear_iff_rank_le_one
#check collinear_pair
#check affineIndependent_iff_not_collinear_set
#check Collinear.mem_affineSpan_of_mem_of_ne
#check Projectivization
#check Projectivization.submodule
#check Projectivization.Subspace
#check Projectivization.Subspace.span
#check Projectivization.cross
#check Projectivization.cross_orthogonal_left
