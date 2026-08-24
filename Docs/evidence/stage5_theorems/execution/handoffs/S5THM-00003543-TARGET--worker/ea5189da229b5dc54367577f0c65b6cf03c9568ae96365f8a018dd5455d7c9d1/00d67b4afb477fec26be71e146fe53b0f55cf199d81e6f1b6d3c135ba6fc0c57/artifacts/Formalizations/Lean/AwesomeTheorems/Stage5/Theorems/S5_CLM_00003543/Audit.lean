import Mathlib

/-
import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_8
-/

/-!
Conditional transport audit for `S5-CLM-00003543`.
Frozen source reference: `Bugeaud08.problem_10_8.variants.quadratic`.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003543

variable (distToNearestInt : ℝ → ℝ)

/-- Forward identity transport for the exposed proposition. -/
theorem source_to_target (ξ : ℝ) (p : ℕ) (hp : p.Prime)
    (hξ : (minpoly ℚ ξ).natDegree = 2)
    (h : sInf {x : ℝ | ∃ q : ℕ, 1 ≤ q ∧
      x = q * padicNorm p q * distToNearestInt (q * ξ)} = 0) :
    sInf {x : ℝ | ∃ q : ℕ, 1 ≤ q ∧
      x = q * padicNorm p q * distToNearestInt (q * ξ)} = 0 := by
  exact h

/-- Identity transport from the target spelling back to the source spelling. -/
theorem target_to_source (ξ : ℝ) (p : ℕ) (hp : p.Prime)
    (hξ : (minpoly ℚ ξ).natDegree = 2)
    (h : sInf {x : ℝ | ∃ q : ℕ, 1 ≤ q ∧
      x = q * padicNorm p q * distToNearestInt (q * ξ)} = 0) :
    sInf {x : ℝ | ∃ q : ℕ, 1 ≤ q ∧
      x = q * padicNorm p q * distToNearestInt (q * ξ)} = 0 := by
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003543
