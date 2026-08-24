import Mathlib

/- Exact frozen provider-module binding; the provider declaration below is
used for statement identity only and is excluded from the proof dependency
graph because its pinned body is not kernel-closed:
import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Bugeaud06.furstenberg_two_three
-/

/-!
# Machine closure for S5-CLM-00003536

This file records the typed composition boundary independently of the open
provider body.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003536

open Filter

/-- Applying a closed root proof to the frozen theorem inputs. -/
theorem furstenberg_two_three_root_application
    (root : ∀ (ξ : ℝ), Irrational ξ →
      Dense {x : AddCircle (1 : ℝ) |
        ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))})
    (ξ : ℝ) (hξ : Irrational ξ) :
    Dense {x : AddCircle (1 : ℝ) |
      ∃ m n : ℕ, 0 < m ∧ 0 < n ∧ x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact root ξ hξ

end AwesomeTheorems.Stage5.S5_CLM_00003536
