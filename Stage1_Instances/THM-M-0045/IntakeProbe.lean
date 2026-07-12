import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.LinearAlgebra.Eigenspace.Triangularizable

/-!
# THM-M-0045 discovery-only intake probe

These checks authenticate pinned eigenvalue, generalized-eigenspace, Gram-Schmidt,
upper-triangular, orthonormal-basis, unitary, and matrix-representation APIs. They do not combine
those ingredients into Schur triangularization, select a canonical target, or prove the theorem.
-/

#check Module.End.exists_eigenvalue
#check Module.End.iSup_maxGenEigenspace_eq_top
#check Matrix.BlockTriangular
#check InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular
#check OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary
#check Matrix.unitaryGroup
#check Matrix.mem_unitaryGroup_iff
#check LinearMap.toMatrix

#print axioms InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular
#print axioms OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary
