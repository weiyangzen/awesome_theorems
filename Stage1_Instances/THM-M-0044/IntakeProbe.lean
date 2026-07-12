import Mathlib.Analysis.InnerProductSpace.SingularValues
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.UnitaryGroup

/-!
# THM-M-0044 discovery-only intake probe

These checks authenticate pinned singular-value, spectral, diagonal, star, and unitary interfaces.
They do not state or prove an SVD, construct its factors, freeze a canonical target, audit terminal
proof-body provenance, or promote any declaration to the theorem root.
-/

#check LinearMap.singularValues
#check LinearMap.singularValues_nonneg
#check LinearMap.sq_singularValues_fin
#check LinearMap.hasEigenvalue_adjoint_comp_self_sq_singularValues
#check LinearMap.support_singularValues
#check LinearMap.IsSymmetric.eigenvectorBasis
#check Matrix.IsHermitian.eigenvectorUnitary
#check Matrix.IsHermitian.spectral_theorem
#check Matrix.diagonal
#check Matrix.conjTranspose
#check Matrix.unitaryGroup
#check Matrix.mem_unitaryGroup_iff

#print axioms LinearMap.support_singularValues
#print axioms Matrix.IsHermitian.spectral_theorem
