import Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four

/-!
# THM-M-0002: exact five lemma statement

This module freezes the conventional category-theoretic five lemma selected by
the intake scope map. It elaborates a proposition only; it does not prove it.
-/

noncomputable section

open CategoryTheory CategoryTheory.ComposableArrows

universe u v

namespace Stage1Instances.THM_M_0002

variable {C : Type u} [Category.{v} C] [Abelian C]

/-- Two exact rows of five objects and a morphism between them, with the
standard epi/iso/iso/mono hypotheses, have an isomorphism in the middle. -/
def FiveLemmaTarget : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact →
      R₂.Exact →
        Epi (app' phi 0) →
          IsIso (app' phi 1) →
            IsIso (app' phi 3) →
              Mono (app' phi 4) →
                IsIso (app' phi 2)

/-- Direct expansion of the statement shape in the historical discovery
module. Kept separate so the relationship is checked rather than asserted. -/
def PinnedCandidateSourceShape : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact → R₂.Exact → Epi (app' phi 0) →
      IsIso (app' phi 1) → IsIso (app' phi 3) →
        Mono (app' phi 4) → IsIso (app' phi 2)

/-- The frozen target is definitionally the historical candidate shape. -/
theorem fiveLemmaTarget_iff_pinnedCandidateSourceShape :
    FiveLemmaTarget (C := C) ↔ PinnedCandidateSourceShape (C := C) :=
  Iff.rfl

-- Structural mutations separately elaborated and distinguished by the checker.
def mutationRemovedLowerExactness : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact → Epi (app' phi 0) → IsIso (app' phi 1) →
      IsIso (app' phi 3) → Mono (app' phi 4) → IsIso (app' phi 2)

def mutationStrengthenedFirstVertical : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact → R₂.Exact → IsIso (app' phi 0) →
      IsIso (app' phi 1) → IsIso (app' phi 3) →
        Mono (app' phi 4) → IsIso (app' phi 2)

def mutationStrengthenedLastVertical : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact → R₂.Exact → Epi (app' phi 0) →
      IsIso (app' phi 1) → IsIso (app' phi 3) →
        IsIso (app' phi 4) → IsIso (app' phi 2)

def mutationChangedConclusionIndex : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (phi : R₁ ⟶ R₂),
    R₁.Exact → R₂.Exact → Epi (app' phi 0) →
      IsIso (app' phi 1) → IsIso (app' phi 3) →
        Mono (app' phi 4) → IsIso (app' phi 1)

end Stage1Instances.THM_M_0002

set_option pp.explicit true in
#print Stage1Instances.THM_M_0002.FiveLemmaTarget
