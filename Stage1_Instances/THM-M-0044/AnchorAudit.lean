import Mathlib.Analysis.InnerProductSpace.SingularValues
import Mathlib.Analysis.Matrix.Spectrum

/-!
# THM-M-0044 immutable anchor-audit probes

These checks authenticate the strongest SVD prerequisites found in pinned
mathlib.  None of them constructs both unitary factors or proves the frozen
rectangular factorization, so this module deliberately contains no root
wrapper.
-/

set_option autoImplicit false

#check LinearMap.singularValues
#check LinearMap.singularValues_nonneg
#check LinearMap.sq_singularValues_fin
#check LinearMap.hasEigenvalue_adjoint_comp_self_sq_singularValues
#check LinearMap.support_singularValues

#check Matrix.isHermitian_conjTranspose_mul_self
#check Matrix.IsHermitian.eigenvectorUnitary
#check Matrix.IsHermitian.spectral_theorem

#check Orthonormal.exists_orthonormalBasis_extension_of_card_eq
#check LinearIsometryEquiv.toMatrix_mem_unitaryGroup
#check Matrix.toEuclideanLin_conjTranspose_eq_adjoint

#print axioms LinearMap.singularValues_nonneg
#print axioms LinearMap.sq_singularValues_fin
#print axioms LinearMap.hasEigenvalue_adjoint_comp_self_sq_singularValues
#print axioms LinearMap.support_singularValues
#print axioms Matrix.isHermitian_conjTranspose_mul_self
#print axioms Matrix.IsHermitian.eigenvectorUnitary
#print axioms Matrix.IsHermitian.spectral_theorem
#print axioms Orthonormal.exists_orthonormalBasis_extension_of_card_eq
#print axioms LinearIsometryEquiv.toMatrix_mem_unitaryGroup
#print axioms Matrix.toEuclideanLin_conjTranspose_eq_adjoint
