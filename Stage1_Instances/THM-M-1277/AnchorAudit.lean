import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
Elaboration surface for the THM-M-1277 anchor audit.

The declarations below are the closest pinned mathlib results found by the
audit.  They are subcritical Gagliardo-Nirenberg-Sobolev inequalities, not the
two-dimensional endpoint exponential inequality or its sharpness clause.
-/

open MeasureTheory

#check lintegral_pow_le_pow_lintegral_fderiv
#check eLpNorm_le_eLpNorm_fderiv_one
#check eLpNorm_le_eLpNorm_fderiv_of_eq
#check eLpNorm_le_eLpNorm_fderiv_of_le

#print axioms lintegral_pow_le_pow_lintegral_fderiv
#print axioms eLpNorm_le_eLpNorm_fderiv_one
#print axioms eLpNorm_le_eLpNorm_fderiv_of_eq
#print axioms eLpNorm_le_eLpNorm_fderiv_of_le
