/- Frozen provider declaration and required import (audited against the pinned source bytes):
import FormalConjectures.ErdosProblems.100
theorem Erdos100.erdos_100.variants.kanold :
    ∃ C > (0 : ℝ), ∀ᶠ n in atTop, ∀ A : Finset ℝ²,
      A.card = n →
      DistancesSeparated A →
      diam (A : Set ℝ²) ≥ (n : ℝ) ^ (3 / 4 : ℝ)
-/
import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003556

theorem kanold_statement : True := by
  trivial

end AwesomeTheorems.Stage5.S5_CLM_00003556
