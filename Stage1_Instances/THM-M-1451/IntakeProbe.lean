import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.LinearAlgebra.Matrix.Charpoly.Eigs
import Mathlib.LinearAlgebra.UnitaryGroup

/-!
# THM-M-1451 discovery-only intake probe

These checks authenticate pinned QR-factor, unitary-matrix, characteristic-polynomial, spectrum,
and triangular-matrix interfaces adjacent to QR iteration. They do not define an iteration, choose
between one-step invariance and convergence, or prove the catalog claim.
-/

#check InnerProductSpace.gramSchmidtOrthonormalBasis
#check InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular
#check OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary
#check Matrix.mem_unitaryGroup_iff
#check Matrix.BlockTriangular
#check Matrix.charpoly_mul_comm
#check Matrix.charpoly_units_conj
#check Matrix.mem_spectrum_iff_isRoot_charpoly
#check Matrix.charpoly_of_upperTriangular

#print axioms Matrix.charpoly_mul_comm
#print axioms Matrix.mem_spectrum_iff_isRoot_charpoly
