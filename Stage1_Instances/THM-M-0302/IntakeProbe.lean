import Mathlib.MeasureTheory.Integral.Average
import Mathlib.MeasureTheory.Integral.Lebesgue.Markov
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# THM-M-0302 discovery-only intake probe

These checks authenticate adjacent pinned set-average, Euclidean box-volume, exponential-integral,
and Markov-inequality APIs. They do not define BMO, state a John-Nirenberg inequality, elaborate a
canonical target for THM-M-0302, or supply proof credit.
-/

#check MeasureTheory.average
#check MeasureTheory.setAverage_eq
#check MeasureTheory.average_congr
#check MeasureTheory.setAverage_sub_setAverage
#check Real.volume_Icc_pi
#check Real.volume_pi_Ioo
#check MeasureTheory.mul_meas_ge_le_lintegral₀
#check MeasureTheory.meas_ge_le_lintegral_div
#check MeasureTheory.mul_meas_ge_le_integral_of_nonneg
#check MeasureTheory.integral_exp_pos

#print axioms MeasureTheory.setAverage_sub_setAverage
#print axioms MeasureTheory.mul_meas_ge_le_lintegral₀
#print axioms MeasureTheory.integral_exp_pos
