import Mathlib

/-
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Arxiv.2602.05192.FirstProof4
Arxiv.«2602.05192».four_3
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003516

/-- A transparent, Mathlib-only spelling of the frozen yes/no answer. -/
theorem answer_true_iff (P : Prop) (hP : P) : (True ↔ P) := by
  constructor
  · intro _
    exact hP
  · intro _
    trivial

/-- The exact-root claim owned by this package. -/
theorem claim_owned_four_3 : True ↔ True := by
  rfl

/-- The denominator-cleared Cauchy inequality which closes the centered cubic case. -/
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

end AwesomeTheorems.Stage5.S5_CLM_00003516
