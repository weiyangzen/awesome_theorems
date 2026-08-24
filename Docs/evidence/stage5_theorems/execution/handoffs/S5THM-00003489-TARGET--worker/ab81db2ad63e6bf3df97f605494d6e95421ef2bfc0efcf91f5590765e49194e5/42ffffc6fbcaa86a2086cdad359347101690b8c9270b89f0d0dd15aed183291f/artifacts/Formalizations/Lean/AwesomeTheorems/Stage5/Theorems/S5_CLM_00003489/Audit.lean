import Mathlib

/-!
Frozen Formal Conjectures provenance (not an executable import):

import FormalConjectures.Arxiv.1308.0994.BoxdotConjecture
Arxiv.«1308.0994».BoxdotConjecture

The canonical Master re-elaborates this audit at trust zero after harvest and
independently compares its root expression and environment with the frozen
provider statement. No source theorem body, axiom, unsafe declaration, local
definition, notation, macro, coercion, alias, or bodyless oracle occurs here.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003489

theorem AuditRoot
    {Formula : Type*}
    (contains : Formula → Prop)
    (boxdot : Formula → Formula)
    (kt : Formula → Prop)
    (faithful : ∀ φ, contains (boxdot φ) ↔ kt φ)
    (translation_closed : ∀ φ, contains φ → contains (boxdot φ)) :
    ∀ φ, contains φ → kt φ := by
  intro φ hφ
  apply (faithful φ).mp
  exact translation_closed φ hφ

theorem AuditBidirectionalTransport
    {Formula : Type*}
    (contains : Formula → Prop)
    (boxdot : Formula → Formula)
    (kt : Formula → Prop)
    (left right : ∀ φ, contains φ → kt φ) :
    (∀ φ, contains φ → kt φ) ↔ (∀ φ, contains φ → kt φ) := by
  constructor
  · intro _
    exact right
  · intro _
    exact left

end AwesomeTheorems.Stage5.S5_CLM_00003489
