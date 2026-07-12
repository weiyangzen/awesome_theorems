import Mathlib.Analysis.Fourier.Inversion
import Mathlib.MeasureTheory.Measure.IntegralCharFun

/-!
# THM-M-1018 anchor audit

Kernel checks for the strongest nearby declarations in pinned mathlib. None of
these declarations is asserted to prove `LevyInversionTarget`.
-/

open MeasureTheory

#check charFun_apply_real
#check intervalIntegrable_charFun
#check integral_charFun_Icc
#check measureReal_abs_gt_le_integral_charFun
#check Measure.ext_of_charFun
#check MeasureTheory.Integrable.fourierInv_fourier_eq
#check Continuous.fourierInv_fourier_eq
