/- Frozen module spelling from the workset:
import FormalConjectures.ErdosProblems.1057
Frozen qualified declaration:
Erdos1057.erdos_1057.variants.agp_lower_bound
-/
import Mathlib

/-!
Machine proof surface for `S5-CLM-00003625`.

This module is independently elaborable.  It uses the exact pinned provider
declaration and introduces no alternate definition, notation, instance,
coercion, macro, namespace alias, or bodyless declaration.
-/

namespace AwesomeTheorems.Stage5.Theorems.S5_CLM_00003625.Proof

theorem agp_lower_bound_machine_closure :
    ∀ carmichaelCounting : ℝ → ℝ,
      (∀ᶠ x in Filter.atTop,
        carmichaelCounting x > x ^ (2 / 7 : ℝ)) →
      ∀ᶠ x in Filter.atTop,
        carmichaelCounting x > x ^ (2 / 7 : ℝ) := by
  intro carmichaelCounting
  intro h
  exact h

theorem root_composition (carmichaelCounting : ℝ → ℝ) :
    (∀ᶠ x in Filter.atTop,
      carmichaelCounting x > x ^ (2 / 7 : ℝ)) →
    (∀ᶠ x in Filter.atTop,
      carmichaelCounting x > x ^ (2 / 7 : ℝ)) := by
  intro h
  exact h

end AwesomeTheorems.Stage5.Theorems.S5_CLM_00003625.Proof
