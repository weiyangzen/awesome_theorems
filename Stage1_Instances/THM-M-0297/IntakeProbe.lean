import Mathlib.MeasureTheory.Function.LpSeminorm.ChebyshevMarkov
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-0297 discovery-only intake probe

These checks authenticate adjacent pinned Lp and superlevel-measure interfaces. They do not choose
a weak-type convention, define the source-selected operator contract, state an interpolation
theorem, or prove THM-M-0297.
-/

#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
#check MeasureTheory.Lp
#check MeasureTheory.eLpNorm_eq_lintegral_rpow_enorm_toReal
#check MeasureTheory.mul_meas_ge_le_pow_eLpNorm'
#check MeasureTheory.meas_ge_le_mul_pow_eLpNorm_enorm
