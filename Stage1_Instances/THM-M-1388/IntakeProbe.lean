import Mathlib.Analysis.InnerProductSpace.Rayleigh
import Mathlib.Analysis.InnerProductSpace.Spectrum
import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Analysis.ODE.Basic

/-!
# THM-M-1388 discovery-only intake probe

These checks authenticate adjacent pinned derivative, ODE, eigenvalue, symmetric-operator,
compact-operator, spectral, and Rayleigh-quotient interfaces. They do not define a
Sturm-Liouville differential expression, weighted space, operator domain, boundary conditions,
eigenvalue problem, or spectral theorem. No target theorem or proof body is declared here.
-/

#check HasDerivAt
#check deriv
#check IsIntegralCurve
#check LinearPMap
#check IsSelfAdjoint
#check Module.End.HasEigenvalue
#check Module.End.HasEigenvalue.mem_spectrum
#check LinearMap.IsSymmetric
#check IsCompactOperator
#check IsCompactOperator.hasEigenvalue_iff_mem_spectrum
#check ContinuousLinearMap.orthogonalComplement_iSup_eigenspaces_eq_bot
#check LinearMap.IsSymmetric.hasEigenvalue_iSup_of_finiteDimensional
#check LinearMap.IsSymmetric.hasEigenvalue_iInf_of_finiteDimensional
