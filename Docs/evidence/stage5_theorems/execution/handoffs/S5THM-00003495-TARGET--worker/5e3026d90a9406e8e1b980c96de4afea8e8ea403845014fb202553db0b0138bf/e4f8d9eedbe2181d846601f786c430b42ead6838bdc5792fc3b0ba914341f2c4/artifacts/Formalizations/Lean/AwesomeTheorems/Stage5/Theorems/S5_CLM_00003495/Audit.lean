import Mathlib

/-!
Frozen provenance (not a canonical-Lake import):
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Arxiv.«1609.08688».maximalLength_pow
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003495

theorem source_to_target
    (F : ℕ → ℕ) {n : ℕ} {e : ℝ} (_hn : 1 < n)
    (_h : (F n : ℝ) = (n : ℝ) ^ e)
    (source : ∀ᶠ m : ℕ in Filter.atTop, (m : ℝ) ^ e ≤ (F m : ℝ)) :
    ∀ᶠ m : ℕ in Filter.atTop, (m : ℝ) ^ e ≤ (F m : ℝ) := by
  exact source

theorem target_to_source
    (F : ℕ → ℕ) {n : ℕ} {e : ℝ} (_hn : 1 < n)
    (_h : (F n : ℝ) = (n : ℝ) ^ e)
    (target : ∀ᶠ m : ℕ in Filter.atTop, (m : ℝ) ^ e ≤ (F m : ℝ)) :
    ∀ᶠ m : ℕ in Filter.atTop, (m : ℝ) ^ e ≤ (F m : ℝ) := by
  exact target

end AwesomeTheorems.Stage5.S5_CLM_00003495
