import Mathlib.Analysis.Fourier.LpSpace

/-!
Discovery-only API probe for THM-M-0294. This file does not declare the canonical target or a proof.
-/

open MeasureTheory
open scoped FourierTransform

#check MeasureTheory.Lp.fourierTransformₗᵢ
#check MeasureTheory.Lp.norm_fourier_eq
#check MeasureTheory.Lp.inner_fourier_eq

-- Specialize the candidate norm interface without choosing it as the source-mapped root.
example (n : ℕ) (f : Lp (α := EuclideanSpace ℝ (Fin n)) ℂ 2) :
    ‖𝓕 f‖ = ‖f‖ :=
  MeasureTheory.Lp.norm_fourier_eq f
