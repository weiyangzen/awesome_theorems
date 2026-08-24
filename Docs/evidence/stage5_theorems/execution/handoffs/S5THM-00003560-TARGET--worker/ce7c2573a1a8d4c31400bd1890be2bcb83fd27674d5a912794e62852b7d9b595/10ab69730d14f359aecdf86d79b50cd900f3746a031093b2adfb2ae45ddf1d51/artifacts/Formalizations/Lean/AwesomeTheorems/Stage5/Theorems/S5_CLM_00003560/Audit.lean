/- Frozen source authority:
import FormalConjectures.ErdosProblems.1004
Erdos1004.erdos_1004.variants.le_of_isDistinctTotientRun
-/
import Mathlib

open Filter Real Nat

namespace AwesomeTheorems.Stage5.S5_CLM_00003560

/-- Re-elaboration witness for the complete expanded expression. -/
theorem audit_source_expression
    (h : True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ))) :
    True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ)) := h

/-- Reverse audit transport for the complete expanded expression. -/
theorem audit_target_to_source
    (h : True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ))) :
    True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ)) := h

end AwesomeTheorems.Stage5.S5_CLM_00003560
