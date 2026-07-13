import Mathlib.Analysis.Fourier.AddCircle
import Mathlib.MeasureTheory.Function.LpSeminorm.ChebyshevMarkov

/-!
# THM-M-0247 discovery-only intake probe

These checks authenticate adjacent pinned measure, additive-circle, Fourier, and distribution-bound
interfaces. They do not define the periodic conjugate operator or state/prove Kolmogorov's
weak-`(1,1)` theorem.
-/

#check AddCircle
#check @AddCircle.haarAddCircle
#check MeasureTheory.Integrable
#check MeasureTheory.Lp
#check MeasureTheory.eLpNorm
#check fourierCoeff
#check MeasureTheory.mul_meas_ge_le_pow_eLpNorm'
#check MeasureTheory.Lp.meas_ge_le_mul_pow_enorm
#check MeasureTheory.Measure.real
