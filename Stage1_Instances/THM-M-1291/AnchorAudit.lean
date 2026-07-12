import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.MeasureTheory.Integral.MeanInequalities
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic

/-!
# THM-M-1291: pinned anchor probes

These declarations are useful measure-theory and `L^p` infrastructure. None
states the Brezis-Lieb splitting conclusion frozen in `Statement.lean`.
-/

#check MeasureTheory.tendsto_integral_of_dominated_convergence
#check MeasureTheory.tendsto_integral_filter_of_dominated_convergence
#check ENNReal.lintegral_rpow_add_lt_top_of_lintegral_rpow_lt_top
#check MeasureTheory.lintegral_rpow_enorm_lt_top_of_eLpNorm_lt_top
#check MeasureTheory.eLpNorm_lt_top_iff_lintegral_rpow_enorm_lt_top
