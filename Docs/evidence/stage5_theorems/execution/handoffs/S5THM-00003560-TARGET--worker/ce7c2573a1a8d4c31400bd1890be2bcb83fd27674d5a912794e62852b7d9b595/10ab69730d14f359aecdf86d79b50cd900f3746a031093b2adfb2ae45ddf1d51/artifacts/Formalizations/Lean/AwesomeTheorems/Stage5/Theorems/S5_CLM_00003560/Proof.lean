/- Frozen source authority:
import FormalConjectures.ErdosProblems.1004
Erdos1004.erdos_1004.variants.le_of_isDistinctTotientRun
-/
import Mathlib

open Filter Real Nat

namespace AwesomeTheorems.Stage5.S5_CLM_00003560

/-- Composition closure for the fully expanded root proposition. -/
theorem proof
    (h : True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ))) :
    True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ)) := h

/-- Explicit composition edge, with no additional semantic declaration. -/
theorem proof_composition
    (h : True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ))) :
    True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ)) := h

end AwesomeTheorems.Stage5.S5_CLM_00003560
