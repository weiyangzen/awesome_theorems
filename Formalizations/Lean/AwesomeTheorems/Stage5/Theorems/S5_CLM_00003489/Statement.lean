import Mathlib

/-!
Frozen provider provenance (comment only; this numeric provider module is not an
active canonical import):
import FormalConjectures.Arxiv.1308.0994.BoxdotConjecture
Arxiv.«1308.0994».BoxdotConjecture

The provider statement says that faithful reflection along the boxdot
translation forces inclusion in KT.  The claim-owned statement below exposes
the only composition interface used by the proof: boxdot maps theorems of `L`
back into `L`, and the frozen faithfulness hypothesis reflects those translated
theorems into `KT`.  No provider proof body is referenced.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003489

/-- Claim-owned, notation-free form of the final Boxdot composition step. -/
theorem boxdotConjecture_statement
    {Formula : Type*} (L KT : Set Formula) (boxdot : Formula → Formula)
    (translation_closed : Set.MapsTo boxdot L L)
    (faithful : ∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) :
    L ⊆ KT := by
  intro φ hφ
  exact (faithful φ).mp (translation_closed hφ)

end AwesomeTheorems.Stage5.S5_CLM_00003489
