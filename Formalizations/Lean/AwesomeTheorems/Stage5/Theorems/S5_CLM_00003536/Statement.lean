import Mathlib

/-
Frozen provider provenance (not an executable import in the canonical Lake graph):
import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Declaration: Bugeaud06.furstenberg_two_three
Revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003536

/-- The exact frozen proposition, exposed as a bidirectional identity transport.
The argument is explicit so this statement-only module introduces no proof oracle. -/
theorem source_to_target_theorem
    (h : ∀ ξ : ℝ, Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
          x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))}) :
    ∀ ξ : ℝ, Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
          x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact h

/-- Reverse half of the exact proposition transport. -/
theorem target_to_source_theorem
    (h : ∀ ξ : ℝ, Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
          x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))}) :
    ∀ ξ : ℝ, Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
          x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003536
