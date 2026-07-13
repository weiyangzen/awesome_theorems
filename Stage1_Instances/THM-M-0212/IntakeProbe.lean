import Mathlib.LinearAlgebra.Projectivization.Constructions
import Mathlib.LinearAlgebra.Projectivization.Independence
import Mathlib.LinearAlgebra.Projectivization.Subspace
import Mathlib.LinearAlgebra.QuadraticForm.Basic

/-!
# THM-M-0212 discovery-only intake probe

These checks authenticate pinned projective point, subspace, homogeneous incidence, dependence,
quadratic-form, and polar-form interfaces adjacent to Brianchon's theorem. They do not define a
source-selected conic, tangent or polarity relation, projective concurrency predicate, canonical
target, or proof. In particular, coordinate `Projectivization.orthogonal` is not credited as an
arbitrary conic polarity.
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
#check Projectivization.Dependent
#check Projectivization.dependent_iff
#check QuadraticForm
#check QuadraticMap.polarBilin
