import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.LinearAlgebra.UnitaryGroup

/-!
# THM-M-1448 discovery-only intake probe

These checks authenticate pinned Gram-Schmidt, triangular-matrix, and unitary-matrix interfaces.
They do not select a canonical QR statement, construct a QR factorization, audit terminal proof-body
provenance, or prove the catalog claim.
-/

#check InnerProductSpace.gramSchmidt
#check InnerProductSpace.gramSchmidt_orthogonal
#check InnerProductSpace.gramSchmidt_triangular
#check InnerProductSpace.gramSchmidtNormed_orthonormal
#check InnerProductSpace.gramSchmidtOrthonormalBasis
#check InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular
#check OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary
#check Matrix.mem_unitaryGroup_iff
#check Matrix.BlockTriangular
#check Matrix.det_of_upperTriangular

#print axioms InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular
#print axioms Matrix.mem_unitaryGroup_iff
