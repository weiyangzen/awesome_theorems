import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
# THM-M-1246 anchor audit

This module asks Lean to resolve the nearest pinned mathlib candidates. The
exact target is separately checked by `check_statement.py`. This file
deliberately provides no proof or transport: the
Sobolev results below have different integrands, exponents, and constants.
-/

open MeasureTheory

#check MeasureTheory.lintegral_pow_le_pow_lintegral_fderiv_aux
#check MeasureTheory.lintegral_pow_le_pow_lintegral_fderiv
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner
