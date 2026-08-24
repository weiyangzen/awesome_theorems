import Mathlib

/-
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Books.BorweinSineSeries
provider declaration: BorweinSineSeries.borwein_sine_series
provider revision: 2270d31e8dd611521f979de6d86da364930b7669
provider source: FormalConjectures/Books/BorweinSineSeries.lean

The provider theorem is sorry-backed and is never used as proof authority here.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003528

/-- The exact mathematical proposition carried by the frozen source record. -/
theorem statement_transport_forward
    (h : Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) := h

/-- Reverse half of the identity transport used by the crosswalk. -/
theorem statement_transport_reverse
    (h : Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) := h

end AwesomeTheorems.Stage5.S5_CLM_00003528
