import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.Analysis.Distribution.SchwartzSpace.Deriv

/-!
# THM-M-1171 anchor probes

These checks pin useful analytic infrastructure in the installed mathlib. None
of the declarations proves the target Calderon-Zygmund Hessian estimate.
-/

#check ContDiffAt.isSymmSndFDerivAt
#check bilinearIteratedFDerivTwo_eq_iteratedFDeriv
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis
#check SchwartzMap.laplacian_eq_sum
#check MeasureTheory.eLpNorm_mono
