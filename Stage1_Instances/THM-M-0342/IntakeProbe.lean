import Mathlib.Analysis.Fourier.LpSpace

open MeasureTheory
open scoped FourierTransform

#check MeasureTheory.Lp.fourierTransformₗᵢ
#check MeasureTheory.Lp.norm_fourier_eq
#check MeasureTheory.Lp.inner_fourier_eq

-- This specializes the candidate API without declaring a canonical target or new theorem.
example (n : ℕ) (f : Lp (α := EuclideanSpace ℝ (Fin n)) ℂ 2) :
    ‖𝓕 f‖ = ‖f‖ :=
  MeasureTheory.Lp.norm_fourier_eq f
