import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.InnerProductSpace.Laplacian

/-!
# THM-M-1289 anchor probes

These checks pin the closest analytic infrastructure in the installed mathlib.
None proves positivity, smoothness, the critical PDE, integrability, or sharp
Sobolev equality for the dossier's explicit Aubin-Talenti bubble.
-/

#check MeasureTheory.lintegral_pow_le_pow_lintegral_fderiv
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis

