import Mathlib

/-
Frozen provider provenance (text only; the numeric module is not a canonical import):
import FormalConjectures.ErdosProblems.107
Erdos107.variants.ersz_bounds
Provider revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003643

/-- Bidirectional audit of the curried surface used by the frozen declaration. -/
theorem erdosSzekeresBounds_audit_roundtrip (f : ℕ → ℕ) :
    (∀ n ≥ 3,
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1) ↔
    (∀ n : ℕ, 3 ≤ n →
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1) := by
  constructor
  · intro h n hn
    exact h n hn
  · intro h n hn
    exact h n hn

/-- Recomposition after both audited projections is lossless. -/
theorem erdosSzekeresBounds_audit_recompose
    (f : ℕ → ℕ)
    (h : ∀ n ≥ 3,
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1) :
    ∀ n ≥ 3,
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1 := by
  intro n hn
  exact ⟨(h n hn).1, (h n hn).2⟩

end AwesomeTheorems.Stage5.S5_CLM_00003643
