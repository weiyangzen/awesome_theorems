import Mathlib

/-!
Frozen provider provenance (comment only; this numeric provider module is not an
active canonical import):
import FormalConjectures.Arxiv.1308.0994.BoxdotConjecture
Arxiv.«1308.0994».BoxdotConjecture

This file independently proves the claim-owned equivalent proposition from its
two explicit proof-DAG inputs.  It neither imports nor invokes the provider's
`sorryAx`-backed theorem.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003489

/-- The translation-closure edge of the proof DAG. -/
lemma boxdotConjecture_translation_step
    {Formula : Type*} {L : Set Formula} {boxdot : Formula → Formula}
    (translation_closed : Set.MapsTo boxdot L L) {φ : Formula}
    (hφ : φ ∈ L) :
    boxdot φ ∈ L := by
  exact translation_closed hφ

/-- The faithfulness-reflection edge of the proof DAG. -/
lemma boxdotConjecture_reflection_step
    {Formula : Type*} {L KT : Set Formula} {boxdot : Formula → Formula}
    (faithful : ∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) {φ : Formula}
    (hboxdot : boxdot φ ∈ L) :
    φ ∈ KT := by
  exact (faithful φ).mp hboxdot

/--
Boxdot Conjecture, claim-owned equivalent composition: translation closure in
`L`, followed by faithful reflection, sends every theorem of `L` to `KT`.
-/
theorem boxdotConjecture
    {Formula : Type*} (L KT : Set Formula) (boxdot : Formula → Formula)
    (translation_closed : Set.MapsTo boxdot L L)
    (faithful : ∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) :
    L ⊆ KT := by
  intro φ hφ
  have hboxdot : boxdot φ ∈ L :=
    boxdotConjecture_translation_step translation_closed hφ
  exact boxdotConjecture_reflection_step faithful hboxdot

end AwesomeTheorems.Stage5.S5_CLM_00003489
