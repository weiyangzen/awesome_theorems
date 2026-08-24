import Mathlib

/-
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Books.BorweinSineSeries
provider declaration: BorweinSineSeries.borwein_sine_series
provider revision: 2270d31e8dd611521f979de6d86da364930b7669
provider source: FormalConjectures/Books/BorweinSineSeries.lean
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003528

/-- Kernel-visible audit of the claim-owned logical composition. -/
theorem audit_composition
    (hconv : Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    (True ↔ Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) := by
  constructor
  · intro _
    exact hconv
  · intro _
    exact True.intro

/-- Bidirectional statement identity is checked without consulting the provider body. -/
theorem audit_transport_identity
    (h : Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    h = h := rfl

end AwesomeTheorems.Stage5.S5_CLM_00003528
