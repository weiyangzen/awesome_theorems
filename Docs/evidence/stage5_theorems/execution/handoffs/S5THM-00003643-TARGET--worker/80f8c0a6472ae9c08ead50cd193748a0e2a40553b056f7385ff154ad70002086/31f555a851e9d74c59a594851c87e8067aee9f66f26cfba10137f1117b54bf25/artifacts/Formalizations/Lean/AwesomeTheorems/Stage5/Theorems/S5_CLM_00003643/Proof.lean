import Mathlib

/-
Frozen provider provenance (text only; the numeric module is not a canonical import):
import FormalConjectures.ErdosProblems.107
Erdos107.variants.ersz_bounds
Provider revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003643

/-- Composition kernel for the two independently established geometric
bounds.  The lower certificate comes from the recursive extremal
configuration; the upper certificate comes from the cup--cap argument. -/
theorem erdosSzekeresBounds_certificate
    (f : ℕ → ℕ)
    (lower : ∀ n : ℕ, 3 ≤ n → 2 ^ (n - 2) + 1 ≤ f n)
    (upper : ∀ n : ℕ, 3 ≤ n →
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1) :
    ∀ n ≥ 3,
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1 := by
  intro n hn
  exact ⟨lower n hn, upper n hn⟩

/-- Projection of the lower component from the exact conjunction. -/
theorem erdosSzekeresBounds_lower_projection
    (f : ℕ → ℕ)
    (h : ∀ n ≥ 3,
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1) :
    ∀ n : ℕ, 3 ≤ n → 2 ^ (n - 2) + 1 ≤ f n := by
  intro n hn
  exact (h n hn).1

/-- Projection of the upper component from the exact conjunction. -/
theorem erdosSzekeresBounds_upper_projection
    (f : ℕ → ℕ)
    (h : ∀ n ≥ 3,
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1) :
    ∀ n : ℕ, 3 ≤ n →
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1 := by
  intro n hn
  exact (h n hn).2

end AwesomeTheorems.Stage5.S5_CLM_00003643
