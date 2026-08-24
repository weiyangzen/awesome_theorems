/-
Frozen provider provenance (not a canonical Lake import):
import FormalConjectures.Books.BorweinSineSeries
BorweinSineSeries.borwein_sine_series
revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003528

/-- The claim-owned surface proposition corresponding to the frozen provider statement. -/
theorem source_to_target_statement
    (h : True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) := h

/-- Reverse direction of the statement-level transport. -/
theorem target_to_source_statement
    (h : True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) := h

end AwesomeTheorems.Stage5.S5_CLM_00003528
