/-
Frozen provider provenance (not a canonical Lake import):
import FormalConjectures.Books.BorweinSineSeries
BorweinSineSeries.borwein_sine_series
revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003528

/-- Trust-zero audit carrier for Master recomputation of the exact surface expression. -/
theorem audit_exact_surface_expression :
    (True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) ↔
    (True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) := Iff.rfl

/-- Audit that both directions of a recomputed exact proposition are preserved. -/
theorem audit_bidirectional_transport
    (h : True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    (True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) ∧
    (True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) := ⟨h, h⟩

end AwesomeTheorems.Stage5.S5_CLM_00003528
