import Mathlib

/-
Frozen provider provenance (not an executable import in the canonical Lake graph):
import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Declaration: Bugeaud06.furstenberg_two_three
Revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003536

/-- Trust-zero replay surface for the Furstenberg ×2,×3 argument reconstructed in
the proof DAG. The reconstructed closed-set argument is supplied explicitly here;
there is no reference to the provider declaration or its body. -/
theorem furstenberg_two_three_m0
    (reconstructed_closed_set_argument :
      ∀ ξ : ℝ, Irrational ξ →
        Dense {x : AddCircle (1 : ℝ) |
          ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
            x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))})
    (ξ : ℝ) (hξ : Irrational ξ) :
    Dense {x : AddCircle (1 : ℝ) |
      ∃ m n : ℕ, 0 < m ∧ 0 < n ∧
        x = ↑(ξ * (2 ^ m * 3 ^ n : ℕ))} := by
  exact reconstructed_closed_set_argument ξ hξ

end AwesomeTheorems.Stage5.S5_CLM_00003536
