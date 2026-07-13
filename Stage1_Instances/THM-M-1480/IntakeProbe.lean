import Mathlib.Analysis.BoxIntegral.Basic
import Mathlib.MeasureTheory.Integral.Average
import Mathlib.MeasureTheory.Integral.Bochner.SumMeasure
import Mathlib.Probability.Distributions.Uniform

/-!
# THM-M-1480 discovery-only intake probe

These checks authenticate adjacent pinned integration, finite-sample, uniform-distribution, and
box-integral interfaces. They do not define discrepancy or low discrepancy, choose a quasi-Monte
Carlo theorem, state the Koksma-Hlawka inequality, or prove THM-M-1480.
-/

#check MeasureTheory.average
#check MeasureTheory.average_eq_integral
#check MeasureTheory.integral_sum_dirac
#check MeasureTheory.integral_sum_dirac_eq_tsum
#check MeasureTheory.pdf.IsUniform
#check MeasureTheory.pdf.IsUniform.integral_eq
#check BoxIntegral.Integrable.tendsto_integralSum_sum_integral

#print axioms MeasureTheory.average_eq_integral
#print axioms MeasureTheory.integral_sum_dirac
#print axioms BoxIntegral.Integrable.tendsto_integralSum_sum_integral
