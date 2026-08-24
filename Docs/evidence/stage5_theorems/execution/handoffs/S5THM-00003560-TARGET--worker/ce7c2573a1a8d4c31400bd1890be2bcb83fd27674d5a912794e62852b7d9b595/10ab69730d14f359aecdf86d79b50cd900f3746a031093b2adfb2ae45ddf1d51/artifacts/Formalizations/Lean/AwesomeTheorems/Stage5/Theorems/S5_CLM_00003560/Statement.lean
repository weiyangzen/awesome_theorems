/- Exact frozen provider module (the numeric component is recorded verbatim for
the semantic validator; the canonical Lean project currently exposes Mathlib):
import FormalConjectures.ErdosProblems.1004
Erdos1004.erdos_1004.variants.le_of_isDistinctTotientRun
-/
import Mathlib

open Filter Real Nat

namespace AwesomeTheorems.Stage5.S5_CLM_00003560

/-- Claim-local expansion of the complete frozen proposition. -/
theorem statement
    (h : True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ))) :
    True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ)) := h

/-- Forward identity transport for the expanded source type. -/
theorem source_to_target
    (h : True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ))) :
    True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ)) := h

/-- Reverse identity transport for the expanded target type. -/
theorem target_to_source
    (h : True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ))) :
    True ↔ ∃ (c : ℝ) (hc : c > 0),
      ∀ᶠ n in atTop, ∀ (K : ℕ),
        (Set.Icc (n + 1) (n + K)).InjOn Nat.totient →
        (K : ℝ) ≤ (n : ℝ) / Real.exp (c * (Real.log n) ^ (1/3 : ℝ)) := h

end AwesomeTheorems.Stage5.S5_CLM_00003560
