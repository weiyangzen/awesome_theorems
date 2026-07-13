import Mathlib.MeasureTheory.Integral.Average
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# THM-M-0254 discovery-only intake probe

These checks authenticate adjacent pinned set-average, centering, and Euclidean box-volume APIs.
They do not define BMO, select a characterization, state a John-Nirenberg inequality, or prove
THM-M-0254.
-/

#check MeasureTheory.average
#check MeasureTheory.setAverage_eq
#check MeasureTheory.average_congr
#check MeasureTheory.setAverage_sub_setAverage
#check Real.volume_Icc_pi
#check Real.volume_pi_Ioo

#print axioms MeasureTheory.setAverage_eq
#print axioms MeasureTheory.setAverage_sub_setAverage
#print axioms Real.volume_Icc_pi
