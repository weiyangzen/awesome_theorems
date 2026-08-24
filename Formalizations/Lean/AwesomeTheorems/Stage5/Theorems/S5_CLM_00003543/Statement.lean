import Mathlib

/-
import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_8
-/

/-!
The Stage 5 target statement surface for `S5-CLM-00003543`.

Frozen source reference:
`Bugeaud08.problem_10_8.variants.quadratic`.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003543

variable (distToNearestInt : ℝ → ℝ)

/-- Target-side proposition, with the unavailable provider surface explicit. -/
theorem statement (ξ : ℝ) (p : ℕ) (hp : p.Prime)
    (hξ : (minpoly ℚ ξ).natDegree = 2) :
    (sInf {x : ℝ | ∃ q : ℕ, 1 ≤ q ∧
      x = q * padicNorm p q * distToNearestInt (q * ξ)} = 0) →
    sInf {x : ℝ | ∃ q : ℕ, 1 ≤ q ∧
      x = q * padicNorm p q * distToNearestInt (q * ξ)} = 0 := by
  intro h
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003543
