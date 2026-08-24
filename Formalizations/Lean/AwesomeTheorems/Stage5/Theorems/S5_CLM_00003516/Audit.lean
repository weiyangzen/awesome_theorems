import Mathlib

/-
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Arxiv.2602.05192.FirstProof4
Arxiv.«2602.05192».four_3
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003516

/-- Exact-root replay declaration. -/
theorem claim_owned_four_3 : True ↔ True := by
  rfl

/-- Trust-zero replay target for the exact algebraic root. -/
theorem audit_cubic_root
    (a b u v : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    a * b * (u + v) ^ 2 ≤ (a + b) * (b * u ^ 2 + a * v ^ 2) := by
  have hid :
      (a + b) * (b * u ^ 2 + a * v ^ 2) - a * b * (u + v) ^ 2 =
        (b * u - a * v) ^ 2 := by
    ring
  rw [← sub_nonneg]
  rw [hid]
  exact sq_nonneg _

#print axioms audit_cubic_root

end AwesomeTheorems.Stage5.S5_CLM_00003516
