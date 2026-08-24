import Mathlib

/-!
# S5-CLM-00003535: semantic transport audit

Frozen provider provenance only:

import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Bugeaud06.boshernitzan

Both directions below use the same fully expanded proposition.  They do not
define, abbreviate, or reinterpret any provider symbol.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003535

open Filter

/-- Forward transport between textually separated copies of the exact root
proposition. -/
theorem boshernitzan_source_to_target
    (h :
      ∀ (r : ℕ → ℝ), (∀ n, 0 < r n) → ¬ BddAbove (Set.range r) →
        Tendsto (fun n => r (n + 1) / r n) atTop (nhds 1) →
          dimH {ξ : ℝ |
            ¬ Dense (Set.range fun n => (↑(ξ * r n) : AddCircle (1 : ℝ)))} = 0) :
    ∀ (r : ℕ → ℝ), (∀ n, 0 < r n) → ¬ BddAbove (Set.range r) →
      Tendsto (fun n => r (n + 1) / r n) atTop (nhds 1) →
        dimH {ξ : ℝ |
          ¬ Dense (Set.range fun n => (↑(ξ * r n) : AddCircle (1 : ℝ)))} = 0 := by
  exact h

/-- Reverse transport, used by Master to compare the target root to the frozen
provider root after elaboration. -/
theorem boshernitzan_target_to_source
    (h :
      ∀ (r : ℕ → ℝ), (∀ n, 0 < r n) → ¬ BddAbove (Set.range r) →
        Tendsto (fun n => r (n + 1) / r n) atTop (nhds 1) →
          dimH {ξ : ℝ |
            ¬ Dense (Set.range fun n => (↑(ξ * r n) : AddCircle (1 : ℝ)))} = 0) :
    ∀ (r : ℕ → ℝ), (∀ n, 0 < r n) → ¬ BddAbove (Set.range r) →
      Tendsto (fun n => r (n + 1) / r n) atTop (nhds 1) →
        dimH {ξ : ℝ |
          ¬ Dense (Set.range fun n => (↑(ξ * r n) : AddCircle (1 : ℝ)))} = 0 := by
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003535
