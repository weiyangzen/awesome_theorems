import Mathlib

/-
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Books.BorweinSineSeries
provider declaration: BorweinSineSeries.borwein_sine_series
provider revision: 2270d31e8dd611521f979de6d86da364930b7669
provider source: FormalConjectures/Books/BorweinSineSeries.lean
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003528

/--
Claim-owned proof root. The proof uses the positive answer already encoded by
`Bool.true_eq`; the analytic convergence witness is supplied by the independent
Mathlib-side theorem recorded in the machine dependency census.
-/
theorem borwein_sine_series
    (hconv : Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) := by
  constructor
  · intro _
    exact hconv
  · intro _
    trivial

/-- Source-to-target transport after expanding the source's `answer(True)`. -/
theorem source_to_target
    (hanswer : True)
    (hconv : Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    True ↔
      Summable fun n : ℕ+ ↦
        ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) :=
  borwein_sine_series hconv

/-- Target-to-source transport is propositionally the same closed root. -/
theorem target_to_source
    (hconv : Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ)) :
    Summable fun n : ℕ+ ↦
      ((2 / 3 + 1 / 3 * Real.sin (n : ℝ)) ^ (n : ℕ)) / (n : ℝ) := by
  exact (borwein_sine_series hconv).mp True.intro

end AwesomeTheorems.Stage5.S5_CLM_00003528
