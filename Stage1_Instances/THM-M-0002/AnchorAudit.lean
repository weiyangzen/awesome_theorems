import Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four

/-!
# THM-M-0002 anchor-audit probe

This module checks that the exact frozen statement can be discharged by the
five-lemma declaration in the repository's immutable mathlib dependency. It is
audit evidence only; the canonical proof wrapper and trust closure belong to
later rev-5.6 phases.
-/

noncomputable section

open CategoryTheory CategoryTheory.ComposableArrows

universe u v

namespace Stage1Instances.THM_M_0002.AnchorAudit

variable {C : Type u} [Category.{v} C] [Abelian C]

/-- Exact-type feasibility probe for the pinned mathlib anchor. -/
theorem pinnedMathlibAnchorFitsFrozenTarget :
    ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
      R₁.Exact → R₂.Exact → Epi (app' phi 0) →
        IsIso (app' phi 1) → IsIso (app' phi 3) →
          Mono (app' phi 4) → IsIso (app' phi 2) := by
  intro R₁ R₂ phi hR₁ hR₂ h₀ h₁ h₃ h₄
  exact CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono
    hR₁ hR₂ phi h₀ h₁ h₃ h₄

end Stage1Instances.THM_M_0002.AnchorAudit

#check CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono
#print axioms CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono
#print axioms Stage1Instances.THM_M_0002.AnchorAudit.pinnedMathlibAnchorFitsFrozenTarget
