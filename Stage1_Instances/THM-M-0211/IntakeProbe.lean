import Mathlib.LinearAlgebra.Projectivization.Constructions
import Mathlib.LinearAlgebra.Projectivization.Subspace
import Mathlib.LinearAlgebra.QuadraticForm.Basic
import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional

/-!
# THM-M-0211 discovery-only intake probe

These checks authenticate pinned projective point, projective subspace, homogeneous incidence,
quadratic-form, and affine-collinearity interfaces adjacent to Pascal's theorem. They do not define
a source-selected conic or projective collinearity predicate, select a canonical target, or prove
Pascal's theorem. In particular, affine `Collinear` is not credited as projective collinearity.
-/

open scoped LinearAlgebra.Projectivization

#check Projectivization
#check Projectivization.mk
#check Projectivization.Subspace
#check Projectivization.Subspace.span
#check Projectivization.cross
#check Projectivization.orthogonal
#check Projectivization.cross_orthogonal_left
#check Projectivization.cross_orthogonal_right
#check QuadraticForm
#check Collinear
