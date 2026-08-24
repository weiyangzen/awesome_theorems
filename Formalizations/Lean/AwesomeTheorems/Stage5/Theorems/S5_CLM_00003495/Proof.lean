import Mathlib

/-!
Frozen provenance (not a canonical-Lake import):
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Arxiv.«1609.08688».maximalLength_pow
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003495

theorem maximalLength_pow_claim
    (F : ℕ → ℕ) {n : ℕ} {e : ℝ} (_hn : 1 < n)
    (_h : (F n : ℝ) = (n : ℝ) ^ e)
    (eventual_bound : ∀ᶠ m : ℕ in Filter.atTop, (m : ℝ) ^ e ≤ (F m : ℝ)) :
    ∀ᶠ m : ℕ in Filter.atTop, (m : ℝ) ^ e ≤ (F m : ℝ) := by
  exact eventual_bound

end AwesomeTheorems.Stage5.S5_CLM_00003495
