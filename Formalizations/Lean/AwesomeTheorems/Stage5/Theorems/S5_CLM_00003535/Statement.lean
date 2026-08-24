import Mathlib

/-!
# S5-CLM-00003535: frozen statement surface

The following two lines are provenance strings, not imports or proof authority.
They identify the immutable provider declaration at revision
`2270d31e8dd611521f979de6d86da364930b7669`.

import FormalConjectures.Books.BugeaudDistributionModuloOne.Problem10_6
Bugeaud06.boshernitzan

The claim-owned surface below spells out the provider proposition without
introducing definitions, notation, coercions, aliases, or parser rules.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003535

open Filter

/-- The frozen Boshernitzan proposition transported on an explicit proof term.
The TARGET proof module supplies the proof term; this statement module fixes
the complete binder and conclusion surface. -/
theorem boshernitzan_statement
    (source_theorem :
      ∀ (r : ℕ → ℝ), (∀ n, 0 < r n) → ¬ BddAbove (Set.range r) →
        Tendsto (fun n => r (n + 1) / r n) atTop (nhds 1) →
          dimH {ξ : ℝ |
            ¬ Dense (Set.range fun n => (↑(ξ * r n) : AddCircle (1 : ℝ)))} = 0)
    (r : ℕ → ℝ) (hr : ∀ n, 0 < r n) (hunb : ¬ BddAbove (Set.range r))
    (hsub : Tendsto (fun n => r (n + 1) / r n) atTop (nhds 1)) :
    dimH {ξ : ℝ |
      ¬ Dense (Set.range fun n => (↑(ξ * r n) : AddCircle (1 : ℝ)))} = 0 := by
  exact source_theorem r hr hunb hsub

end AwesomeTheorems.Stage5.S5_CLM_00003535
