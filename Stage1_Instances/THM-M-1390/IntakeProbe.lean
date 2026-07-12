import Mathlib.Analysis.InnerProductSpace.Rayleigh
import Mathlib.Analysis.InnerProductSpace.Spectrum

/-!
# THM-M-1390 discovery-only intake probe

These checks authenticate adjacent pinned Rayleigh-quotient and finite-dimensional spectral APIs.
They do not choose a matrix, compact-operator, Sturm-Liouville, or elliptic-PDE version of the
Courant min-max principle, and they do not prove THM-M-1390.
-/

#check ContinuousLinearMap.rayleighQuotient
#check ContinuousLinearMap.iSup_rayleigh_eq_iSup_rayleigh_sphere
#check ContinuousLinearMap.iInf_rayleigh_eq_iInf_rayleigh_sphere
#check IsSelfAdjoint.hasEigenvector_of_isMaxOn
#check IsSelfAdjoint.hasEigenvector_of_isMinOn
#check LinearMap.IsSymmetric.hasEigenvalue_iSup_of_finiteDimensional
#check LinearMap.IsSymmetric.hasEigenvalue_iInf_of_finiteDimensional
#check LinearMap.IsSymmetric.eigenvalues
#check LinearMap.IsSymmetric.eigenvalues_antitone
