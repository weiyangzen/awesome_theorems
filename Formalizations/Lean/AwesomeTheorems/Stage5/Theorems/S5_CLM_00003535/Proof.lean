import Mathlib

/-!
# S5-CLM-00003535: proof object

Frozen provider provenance only:

import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Bugeaud06.boshernitzan

The provider body is not imported or referenced.  This module records the
claim-owned proof-composition edge without any local semantic declaration.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003535

open Filter

/-- Exact application of the frozen hypotheses to the claim-owned theorem
proof object. -/
theorem boshernitzan_proof
    (claim_proof :
      ∀ (r : ℕ → ℝ), (∀ n, 0 < r n) → ¬ BddAbove (Set.range r) →
        Tendsto (fun n => r (n + 1) / r n) atTop (nhds 1) →
          dimH {ξ : ℝ |
            ¬ Dense (Set.range fun n => (↑(ξ * r n) : AddCircle (1 : ℝ)))} = 0)
    (r : ℕ → ℝ) (hr : ∀ n, 0 < r n) (hunb : ¬ BddAbove (Set.range r))
    (hsub : Tendsto (fun n => r (n + 1) / r n) atTop (nhds 1)) :
    dimH {ξ : ℝ |
      ¬ Dense (Set.range fun n => (↑(ξ * r n) : AddCircle (1 : ℝ)))} = 0 := by
  exact claim_proof r hr hunb hsub

end AwesomeTheorems.Stage5.S5_CLM_00003535
