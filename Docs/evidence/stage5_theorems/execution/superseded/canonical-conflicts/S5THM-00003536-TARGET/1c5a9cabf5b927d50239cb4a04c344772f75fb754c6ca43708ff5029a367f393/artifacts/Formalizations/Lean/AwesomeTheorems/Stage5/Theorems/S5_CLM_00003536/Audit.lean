import Mathlib

/- Exact frozen provider-module binding checked against the task-local source
record.  The named declaration is not used as proof authority:
import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Bugeaud06.furstenberg_two_three
-/

/-!
# Kernel audit surface for S5-CLM-00003536

The source declaration is named explicitly so the exact provider binding is
visible to elaboration and to the semantic-substitution checks.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003536

open Filter

/-- Re-elaboration witness for the exact unconditional root type. -/
theorem audit_exact_root_type
    (h : ∀ (ξ : ℝ), Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))}) :
    ∀ (ξ : ℝ), Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003536
