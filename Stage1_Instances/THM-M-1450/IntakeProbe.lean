import Mathlib.Analysis.InnerProductSpace.Spectrum
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# THM-M-1450 discovery-only intake probe

These checks authenticate pinned eigenspace, spectral-decomposition, matrix-action, and operator-
power interfaces that could support a future power-iteration statement. They do not define the
iteration, select a canonical convergence theorem, or provide proof credit for the catalog claim.
-/

#check Module.End.HasEigenvector
#check Module.End.HasEigenvalue
#check Module.End.HasEigenvector.apply_eq_smul
#check Module.End.HasEigenvector.pow_apply
#check Module.End.HasEigenvalue.pow
#check Matrix.mulVec
#check Matrix.mulVecLin
#check Matrix.mulVecLin_mul
#check LinearMap.IsSymmetric.eigenvalues
#check LinearMap.IsSymmetric.eigenvalues_antitone
#check LinearMap.IsSymmetric.hasEigenvector_eigenvectorBasis
#check LinearMap.IsSymmetric.eigenvectorBasis_apply_self_apply

#print axioms Module.End.HasEigenvector.pow_apply
#print axioms LinearMap.IsSymmetric.eigenvectorBasis_apply_self_apply
