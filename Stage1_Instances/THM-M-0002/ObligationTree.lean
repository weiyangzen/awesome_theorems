import Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four

/-!
# THM-M-0002 conditional obligation composition

The mono and epi conclusions for the middle component are explicit premises.
This checks only their composition into the frozen five-lemma target.
-/

noncomputable section

open CategoryTheory CategoryTheory.ComposableArrows

universe u v

namespace Stage1Instances.THM_M_0002.ObligationTree

variable {C : Type u} [Category.{v} C] [Abelian C]

def Root : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact → R₂.Exact → Epi (app' phi 0) →
      IsIso (app' phi 1) → IsIso (app' phi 3) →
        Mono (app' phi 4) → IsIso (app' phi 2)

def MiddleMono : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact → R₂.Exact → Epi (app' phi 0) →
      IsIso (app' phi 1) → IsIso (app' phi 3) →
        Mono (app' phi 4) → Mono (app' phi 2)

def MiddleEpi : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact → R₂.Exact → Epi (app' phi 0) →
      IsIso (app' phi 1) → IsIso (app' phi 3) →
        Mono (app' phi 4) → Epi (app' phi 2)

/-- Exact child-to-root composition without invoking either four lemma. -/
theorem root_compose (monoMiddle : MiddleMono (C := C))
    (epiMiddle : MiddleEpi (C := C)) : Root (C := C) := by
  intro R₁ R₂ phi hR₁ hR₂ h₀ h₁ h₃ h₄
  letI : Mono (app' phi 2) := monoMiddle R₁ R₂ phi hR₁ hR₂ h₀ h₁ h₃ h₄
  letI : Epi (app' phi 2) := epiMiddle R₁ R₂ phi hR₁ hR₂ h₀ h₁ h₃ h₄
  apply isIso_of_mono_of_epi

#check CategoryTheory.Abelian.mono_of_epi_of_mono_of_mono
#check CategoryTheory.Abelian.epi_of_epi_of_epi_of_mono
#check CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono
#print axioms root_compose

end Stage1Instances.THM_M_0002.ObligationTree
