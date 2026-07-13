import Mathlib.Analysis.Fourier.AddCircle

/-!
Discovery-only API probe for THM-M-0293. This file declares no canonical target or proof.
-/

#check AddCircle
#check AddCircle.haarAddCircle
#check fourier
#check fourierCoeff
#check hasSum_sq_fourierCoeff
#check tsum_sq_fourierCoeff
#check hasSum_fourier_series_of_summable
#check has_pointwise_sum_fourier_series_of_summable

-- Specialize the pinned coefficient interface to Hurwitz's historical period without selecting a
-- source theorem, coefficient normalization transport, or target conclusion.
noncomputable example (f : AddCircle (2 * Real.pi) → ℂ) (n : ℤ) : ℂ :=
  haveI : Fact (0 < 2 * Real.pi) := ⟨mul_pos two_pos Real.pi_pos⟩
  fourierCoeff f n

#print axioms hasSum_sq_fourierCoeff
#print axioms hasSum_fourier_series_of_summable
