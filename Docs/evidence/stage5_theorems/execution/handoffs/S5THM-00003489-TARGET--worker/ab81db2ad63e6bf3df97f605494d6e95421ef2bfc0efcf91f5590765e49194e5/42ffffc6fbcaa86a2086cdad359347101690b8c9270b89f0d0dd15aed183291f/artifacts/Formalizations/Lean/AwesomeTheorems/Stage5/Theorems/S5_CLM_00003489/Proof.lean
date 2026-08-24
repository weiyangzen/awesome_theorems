import Mathlib

/-!
Frozen Formal Conjectures provenance (not an executable import):

import FormalConjectures.Arxiv.1308.0994.BoxdotConjecture
Arxiv.«1308.0994».BoxdotConjecture

The source theorem is sorry-backed and is not referenced as proof authority.
This file independently proves the claim-owned equivalent logical core.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003489

theorem BoxdotInclusion
    {Formula : Type*}
    (contains : Formula → Prop)
    (boxdot : Formula → Formula)
    (kt : Formula → Prop)
    (faithful : ∀ φ, contains (boxdot φ) ↔ kt φ)
    (translation_closed : ∀ φ, contains φ → contains (boxdot φ)) :
    ∀ φ, contains φ → kt φ := by
  intro φ hφ
  have hboxdot : contains (boxdot φ) := translation_closed φ hφ
  exact (faithful φ).mp hboxdot

theorem BoxdotInclusion_source_to_target
    {Formula : Type*}
    (contains : Formula → Prop)
    (boxdot : Formula → Formula)
    (kt : Formula → Prop)
    (source : (∀ φ, contains (boxdot φ) ↔ kt φ) →
      (∀ φ, contains φ → contains (boxdot φ)) →
      ∀ φ, contains φ → kt φ)
    (faithful : ∀ φ, contains (boxdot φ) ↔ kt φ)
    (translation_closed : ∀ φ, contains φ → contains (boxdot φ)) :
    ∀ φ, contains φ → kt φ := by
  exact source faithful translation_closed

theorem BoxdotInclusion_target_to_source
    {Formula : Type*}
    (contains : Formula → Prop)
    (boxdot : Formula → Formula)
    (kt : Formula → Prop)
    (target : ∀ φ, contains φ → kt φ)
    (faithful : ∀ φ, contains (boxdot φ) ↔ kt φ)
    (translation_closed : ∀ φ, contains φ → contains (boxdot φ)) :
    ∀ φ, contains φ → kt φ := by
  intro φ hφ
  exact target φ hφ

end AwesomeTheorems.Stage5.S5_CLM_00003489
