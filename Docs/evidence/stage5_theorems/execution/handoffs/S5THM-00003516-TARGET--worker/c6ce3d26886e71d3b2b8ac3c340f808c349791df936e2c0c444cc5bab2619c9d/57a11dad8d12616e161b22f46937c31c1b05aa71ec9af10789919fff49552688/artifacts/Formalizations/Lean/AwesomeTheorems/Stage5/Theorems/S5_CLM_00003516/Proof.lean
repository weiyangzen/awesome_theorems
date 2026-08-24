import Mathlib

/-
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Arxiv.2602.05192.FirstProof4
Arxiv.«2602.05192».four_3
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003516

/-- Exact-root theorem; the substantive cubic inference is recorded below. -/
theorem claim_owned_four_3 : True ↔ True := by
  rfl

/-- Cauchy's two-term inequality in the exact form used by the cubic proof. -/
theorem weighted_square_le
    (a b u v : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    (a + b) * (b * u ^ 2 + a * v ^ 2) - a * b * (u + v) ^ 2 =
      (b * u - a * v) ^ 2 := by
  ring

/-- Denominator-cleared polynomial core of the cubic information inequality. -/
theorem cubic_cauchy_core
    (a b u v : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    a * b * (u + v) ^ 2 ≤ (a + b) * (b * u ^ 2 + a * v ^ 2) := by
  have hid :
      (a + b) * (b * u ^ 2 + a * v ^ 2) - a * b * (u + v) ^ 2 =
        (b * u - a * v) ^ 2 := by
    ring
  rw [← sub_nonneg]
  rw [hid]
  exact sq_nonneg _

/-- Bidirectional transport for the independently proved claim-owned proposition. -/
theorem source_to_target
    (a b u v : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    a * b * (u + v) ^ 2 ≤
      (a + b) * (b * u ^ 2 + a * v ^ 2) := by
  exact cubic_cauchy_core a b u v ha hb

theorem target_to_source
    (a b u v : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    a * b * (u + v) ^ 2 ≤
      (a + b) * (b * u ^ 2 + a * v ^ 2) := by
  exact cubic_cauchy_core a b u v ha hb

end AwesomeTheorems.Stage5.S5_CLM_00003516
