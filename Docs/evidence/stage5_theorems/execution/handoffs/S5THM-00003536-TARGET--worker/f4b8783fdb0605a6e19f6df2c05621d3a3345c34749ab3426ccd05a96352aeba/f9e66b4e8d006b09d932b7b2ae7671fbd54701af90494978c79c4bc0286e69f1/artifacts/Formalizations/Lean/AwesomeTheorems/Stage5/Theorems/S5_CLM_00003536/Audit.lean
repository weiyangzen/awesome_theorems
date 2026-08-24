import Mathlib

/-
Frozen provider provenance (not an executable import in the canonical Lake graph):
import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Declaration: Bugeaud06.furstenberg_two_three
Revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003536

/-- Exact-type audit: the proof surface consumes and returns precisely the frozen
proposition, with no local definitions, aliases, notation, or parser extensions. -/
theorem exact_type_audit
    (root : ∀ ξ : ℝ, Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
          x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))}) :
    ∀ ξ : ℝ, Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
          x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact root

/-- Terminal audit application at an arbitrary irrational input. -/
theorem terminal_root_audit
    (root : ∀ ξ : ℝ, Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
          x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))})
    (ξ : ℝ) (hξ : Irrational ξ) :
    Dense {x : AddCircle (1 : ℝ) |
      ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
        x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact root ξ hξ

end AwesomeTheorems.Stage5.S5_CLM_00003536
