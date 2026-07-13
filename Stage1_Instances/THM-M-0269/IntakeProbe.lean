import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.Lebesgue.Add

/-!
# THM-M-0269 discovery-only intake probe

These commands authenticate monotone-convergence interfaces in the pinned mathlib snapshot. They
do not select an exact source proposition, establish statement identity, or prove the repository
target.
-/

#check MeasureTheory.lintegral_iSup
#check MeasureTheory.lintegral_iSup'
#check MeasureTheory.lintegral_tendsto_of_tendsto_of_monotone
#check MeasureTheory.lintegral_iSup_ae
#check MeasureTheory.lintegral_iSup_directed_of_measurable
#check MeasureTheory.lintegral_iSup_directed
#check MeasureTheory.integral_tendsto_of_tendsto_of_monotone

#print axioms MeasureTheory.lintegral_iSup
#print axioms MeasureTheory.lintegral_iSup'
#print axioms MeasureTheory.lintegral_tendsto_of_tendsto_of_monotone
#print axioms MeasureTheory.integral_tendsto_of_tendsto_of_monotone
