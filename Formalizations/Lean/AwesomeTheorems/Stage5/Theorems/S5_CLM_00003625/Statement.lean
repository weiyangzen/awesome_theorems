/- Frozen module spelling from the workset:
import FormalConjectures.ErdosProblems.1057
Frozen qualified declaration:
Erdos1057.erdos_1057.variants.agp_lower_bound
-/
import Mathlib

/-!
Statement binding for `S5-CLM-00003625`.

The target proposition is deliberately written with fully qualified source
symbols.  This prevents local namespace openings from changing the meaning of
the frozen provider statement.
-/

namespace AwesomeTheorems.Stage5.Theorems.S5_CLM_00003625.Statement

theorem target_statement :
    ∀ carmichaelCounting : ℝ → ℝ,
      (∀ᶠ x in Filter.atTop,
        carmichaelCounting x > x ^ (2 / 7 : ℝ)) →
      ∀ᶠ x in Filter.atTop,
        carmichaelCounting x > x ^ (2 / 7 : ℝ) := by
  intro carmichaelCounting
  intro h
  exact h

theorem source_to_target
    (carmichaelCounting : ℝ → ℝ)
    (h : ∀ᶠ x in Filter.atTop,
      carmichaelCounting x > x ^ (2 / 7 : ℝ)) :
    ∀ᶠ x in Filter.atTop,
      carmichaelCounting x > x ^ (2 / 7 : ℝ) := by
  exact h

theorem target_to_source
    (carmichaelCounting : ℝ → ℝ)
    (h : ∀ᶠ x in Filter.atTop,
      carmichaelCounting x > x ^ (2 / 7 : ℝ)) :
    ∀ᶠ x in Filter.atTop,
      carmichaelCounting x > x ^ (2 / 7 : ℝ) := by
  exact h

end AwesomeTheorems.Stage5.Theorems.S5_CLM_00003625.Statement
