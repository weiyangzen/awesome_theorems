import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# THM-M-1454 discovery-only intake probe

These checks authenticate pinned matrix-vector, Gram-Schmidt, span, orthogonal-projection, and
norm-isometry APIs adjacent to a future GMRES encoding. They do not select the catalog's exact
statement, define a GMRES iteration, or prove THM-M-1454.
-/

#check Matrix.mulVec
#check Matrix.mulVecLin
#check Matrix.mulVecLin_apply
#check InnerProductSpace.gramSchmidt
#check InnerProductSpace.gramSchmidt_orthogonal
#check InnerProductSpace.span_gramSchmidt
#check Submodule.orthogonalProjection
#check Submodule.orthogonalProjection_mem_subspace_eq_self
#check LinearIsometry.norm_map
#check dotProduct
