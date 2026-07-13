import Mathlib.Analysis.InnerProductSpace.Rayleigh
import Mathlib.Analysis.Matrix.Spectrum

/-!
# THM-M-0056 discovery-only intake probe

These checks authenticate adjacent pinned Hermitian-matrix eigenvalue, spectral-theorem, and
Rayleigh-quotient APIs. They do not select a Weyl inequality variant or prove THM-M-0056.
-/

#check Matrix.IsHermitian.eigenvalues₀
#check Matrix.IsHermitian.eigenvalues₀_antitone
#check Matrix.IsHermitian.eigenvalues
#check Matrix.IsHermitian.mulVec_eigenvectorBasis
#check Matrix.IsHermitian.spectral_theorem
#check Matrix.IsHermitian.spectrum_real_eq_range_eigenvalues
#check ContinuousLinearMap.rayleighQuotient_add
#check ContinuousLinearMap.rayleighQuotient_le_norm
#check ContinuousLinearMap.norm_eq_iSup_rayleighQuotient
