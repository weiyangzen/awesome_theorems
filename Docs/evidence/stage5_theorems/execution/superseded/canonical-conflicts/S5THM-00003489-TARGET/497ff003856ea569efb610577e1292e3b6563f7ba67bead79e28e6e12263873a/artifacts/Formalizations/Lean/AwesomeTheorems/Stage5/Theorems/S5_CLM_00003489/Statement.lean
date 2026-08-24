import Mathlib

/-!
Frozen Formal Conjectures provenance (data only; the numeric module path is
not an import in this Lake environment):

import FormalConjectures.Arxiv.1308.0994.BoxdotConjecture
Arxiv.«1308.0994».BoxdotConjecture

Provider revision: 2270d31e8dd611521f979de6d86da364930b7669
Provider declaration type:
  (L : NormalModalLogic) (H : ∀ φ, L ⊢ ■ φ ↔ KT ⊢ φ) : L ⊆ KT

`ClaimOwnedBoxdotStatement` is the import-independent logical core used for
cold canonical replay. `contains` represents membership in a normal modal
logic, `boxdot` its translation, and `kt` membership in KT. The third field is
the claim-owned closure lemma whose provider derivation is independently
audited by the canonical Master; no provider proof body is used here.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003489

theorem ClaimOwnedBoxdotStatement
    {Formula : Type*}
    (contains : Formula → Prop)
    (boxdot : Formula → Formula)
    (kt : Formula → Prop)
    (faithful : ∀ φ, contains (boxdot φ) ↔ kt φ)
    (translation_closed : ∀ φ, contains φ → contains (boxdot φ)) :
    ∀ φ, contains φ → kt φ := by
  intro φ hφ
  exact (faithful φ).mp (translation_closed φ hφ)

end AwesomeTheorems.Stage5.S5_CLM_00003489
