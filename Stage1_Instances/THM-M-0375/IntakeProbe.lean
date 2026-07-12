import Mathlib.Analysis.Fourier.FourierTransform
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic

/-! Discovery-only API checks for a later exact Fourier-restriction statement. -/

open MeasureTheory Metric
open scoped FourierTransform ENNReal

#check VectorFourier.fourierIntegral
#check FourierTransform.fourier
#check Measure.toSphere
#check sphere
#check eLpNorm
#check Measure.map
#check Measure.restrict
