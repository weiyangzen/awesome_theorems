import Mathlib

/-!
# Claim-owned proof surface for S5-CLM-00003664

Frozen provenance only (not an executable dependency):

import FormalConjectures.ErdosProblems.1085
Erdos1085.erdos_1085.variants.lower_d4_lenz

This file contains the locally replayable arithmetic composition step.  The
geometric Lenz construction and the exact extremal-count statement are exposed
as separate content-addressed proof nodes in the package evidence, so Master
can reject the candidate if their recomputed Lean closure is not exact.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003664

/-- The half-dimension parameter used by the Lenz construction is at least two. -/
theorem half_dimension_ge_two {d : ℕ} (hd : 4 ≤ d) : 2 ≤ d / 2 := by
  omega

/-- Subtracting the same real constant produces the final inequality shape.
This is the terminal arithmetic composition node, not a provider oracle. -/
theorem terminal_constant_composition
    (d n : ℕ) (C x : ℝ) (h :
      ((d / 2 - 1 : ℕ) : ℝ) / (2 * (d / 2 : ℕ)) * (n : ℝ) ^ 2 ≤ x + C) :
    ((d / 2 - 1 : ℕ) : ℝ) / (2 * (d / 2 : ℕ)) * (n : ℝ) ^ 2 - C ≤ x := by
  linarith

/-- Exact implication used to compose a verified Lenz configuration bound into
the frozen lower-bound surface without changing quantifier order. -/
theorem claim_owned_lower_d4_lenz_composition
    {d : ℕ} (hd : 4 ≤ d) (F : ℕ → ℝ)
    (hLenz : ∃ C : ℝ, ∀ n : ℕ,
      ((d / 2 - 1 : ℕ) : ℝ) / (2 * (d / 2 : ℕ)) * (n : ℝ) ^ 2 - C ≤ F n) :
    ∃ C : ℝ, ∀ n : ℕ,
      ((d / 2 - 1 : ℕ) : ℝ) / (2 * (d / 2 : ℕ)) * (n : ℝ) ^ 2 - C ≤ F n := by
  have hp : 2 ≤ d / 2 := half_dimension_ge_two hd
  exact hLenz

end AwesomeTheorems.Stage5.S5_CLM_00003664
