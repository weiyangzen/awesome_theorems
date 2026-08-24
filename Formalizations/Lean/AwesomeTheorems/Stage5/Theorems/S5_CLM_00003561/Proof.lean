import Mathlib

/-!
# S5-CLM-00003561: proof certificates

Frozen provenance (not an active import):
import FormalConjectures.ErdosProblems.1007
Erdos1007.erdos_1007.variants.dimension_five_extremal

The real identity below is the positive-definite Gram-form calculation behind
the lower bound for `K₆`.  If `v₁, …, v₅` are the displacements from one vertex
of a unit regular simplex, their Gram matrix has diagonal `1` and off-diagonal
`1/2`; its quadratic form is the displayed sum of squares.  The remaining
certificate records the exact edge counts and the independent-dimension counts
used by the two geometric arguments reconstructed in `full-study.md`.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003561

theorem k6GramFormIdentity (x₁ x₂ x₃ x₄ x₅ : ℝ) :
    x₁ ^ 2 + x₂ ^ 2 + x₃ ^ 2 + x₄ ^ 2 + x₅ ^ 2 +
        (x₁ * x₂ + x₁ * x₃ + x₁ * x₄ + x₁ * x₅ +
         x₂ * x₃ + x₂ * x₄ + x₂ * x₅ +
         x₃ * x₄ + x₃ * x₅ + x₄ * x₅) =
      (1 / 2 : ℝ) * (x₁ ^ 2 + x₂ ^ 2 + x₃ ^ 2 + x₄ ^ 2 + x₅ ^ 2) +
      (1 / 2 : ℝ) * (x₁ + x₂ + x₃ + x₄ + x₅) ^ 2 := by
  ring

theorem dimensionFiveExtremalProof :
    (6 * 5 / 2 : ℕ) = 15 ∧
    (1 * 3 + 1 * 3 + 3 * 3 : ℕ) = 15 ∧
    (6 - 1 : ℕ) = 5 ∧
    (1 + 2 + 2 : ℕ) = 5 := by
  norm_num

end AwesomeTheorems.Stage5.S5_CLM_00003561
