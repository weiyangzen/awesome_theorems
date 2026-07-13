import Mathlib.Analysis.InnerProductSpace.Rayleigh
import Mathlib.Analysis.InnerProductSpace.Spectrum
import Mathlib.Analysis.Matrix.Spectrum

/-!
# THM-M-0055 discovery-only intake probe

These checks authenticate adjacent pinned Rayleigh-quotient, extremal-eigenvalue, Hermitian-matrix,
and ordered-spectrum interfaces. They do not choose an extremal or indexed source proposition,
declare the target, check a matrix-to-operator theorem wrapper, or prove THM-M-0055.
-/

#check ContinuousLinearMap.rayleighQuotient
#check ContinuousLinearMap.iSup_rayleigh_eq_iSup_rayleigh_sphere
#check ContinuousLinearMap.iInf_rayleigh_eq_iInf_rayleigh_sphere
#check IsSelfAdjoint.hasEigenvector_of_isMaxOn
#check IsSelfAdjoint.hasEigenvector_of_isMinOn
#check LinearMap.IsSymmetric.hasEigenvalue_iSup_of_finiteDimensional
#check LinearMap.IsSymmetric.hasEigenvalue_iInf_of_finiteDimensional
#check Matrix.isHermitian_iff_isSymmetric
#check Matrix.IsHermitian.eigenvalues
#check Matrix.IsHermitian.eigenvalues₀_antitone
#check LinearMap.IsSymmetric.eigenvalues
#check LinearMap.IsSymmetric.eigenvalues_antitone
