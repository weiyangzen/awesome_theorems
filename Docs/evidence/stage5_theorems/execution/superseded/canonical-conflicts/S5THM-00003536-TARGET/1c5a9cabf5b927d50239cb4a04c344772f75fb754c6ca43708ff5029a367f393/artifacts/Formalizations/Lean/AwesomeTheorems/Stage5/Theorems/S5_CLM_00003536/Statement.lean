import Mathlib

/- Exact frozen provider-module binding (the task-local pinned source is
statement authority, not proof authority):
import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Bugeaud06.furstenberg_two_three
-/

/-!
# Exact statement surface for S5-CLM-00003536

The proposition below deliberately uses the provider's surface symbols without
local aliases, notation, coercions, or helper definitions.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003536

open Filter

/-- The exact frozen target proposition. -/
theorem exact_statement_from_provider
    (h : ∀ (ξ : ℝ), Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))})
    (ξ : ℝ) (hξ : Irrational ξ) :
    Dense {x : AddCircle (1 : ℝ) |
      ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact h ξ hξ

/-- Source-to-target direction of the bidirectional statement crosswalk. -/
theorem source_to_target_statement
    (ξ : ℝ) (hξ : Irrational ξ)
    (h : Dense {x : AddCircle (1 : ℝ) |
      ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))}) :
    Dense {x : AddCircle (1 : ℝ) |
      ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact h

/-- Target-to-source direction of the bidirectional statement crosswalk. -/
theorem target_to_source_statement
    (ξ : ℝ) (hξ : Irrational ξ)
    (h : Dense {x : AddCircle (1 : ℝ) |
      ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))}) :
    Dense {x : AddCircle (1 : ℝ) |
      ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003536
