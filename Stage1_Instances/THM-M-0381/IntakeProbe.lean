import Mathlib.Analysis.Fourier.LpSpace
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

open MeasureTheory

#check Measure
#check Measure.prod
#check MemLp
#check Lp
#check eLpNorm
#check MeasureTheory.Lp.fourierTransformₗᵢ

example {X E : Type*} (u : ℝ × X → E) (t : ℝ) : X → E :=
  fun x => u (t, x)
