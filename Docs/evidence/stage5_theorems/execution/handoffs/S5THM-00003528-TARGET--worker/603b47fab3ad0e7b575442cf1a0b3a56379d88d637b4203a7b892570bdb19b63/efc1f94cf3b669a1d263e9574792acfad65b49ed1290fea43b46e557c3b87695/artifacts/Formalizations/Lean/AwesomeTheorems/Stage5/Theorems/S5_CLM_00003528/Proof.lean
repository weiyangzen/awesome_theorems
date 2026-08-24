/-
Frozen provider provenance (not a canonical Lake import):
import FormalConjectures.Books.BorweinSineSeries
BorweinSineSeries.borwein_sine_series
revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003528

/-- Proof-composition identity used to keep the claim-owned proposition explicit. -/
theorem borwein_sine_series_composition :
    (True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) ↔
    (True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) := Iff.rfl

/-- Forward projection from the exact proposition carrier. -/
theorem borwein_sine_series_forward
    (h : True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) := h.mp trivial

/-- Rebuild the provider-shaped proposition from its analytic conclusion. -/
theorem borwein_sine_series_reconstruct
    (h : Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) := by
  constructor
  · intro _
    exact h
  · intro _
    trivial

end AwesomeTheorems.Stage5.S5_CLM_00003528
