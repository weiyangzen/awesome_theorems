import Mathlib.Algebra.Homology.HomologySequenceLemmas
import Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four

/-!
# S1-M-097 / THM-M-0002: the five lemma

This Stage1 file records a checked Lean 4/mathlib anchor for the five lemma:
in a commutative diagram of exact rows in an abelian category, the middle
vertical morphism is an isomorphism under the standard epi/iso/iso/mono
hypotheses on the other vertical morphisms.

The terminal category-level statement is already present in the pinned mathlib
snapshot as `CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono`.
The local declarations below only freeze the Stage1 statement shape and provide
repo-local wrappers around the checked mathlib theorem and the adjacent
homological-complex consequence.  They contain no proof placeholders.
-/

noncomputable section

open CategoryTheory CategoryTheory.ComposableArrows

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_097

variable {C : Type u} [Category.{v} C] [Abelian C]

/--
Stage1 statement-shape candidate for the five lemma.

`ComposableArrows C 4` encodes a row with five objects and four arrows.  A
morphism `φ : R₁ ⟶ R₂` is the commutative diagram between two such rows.  The
mathlib theorem assumes both rows are exact, the first vertical map is epi, the
second and fourth are isomorphisms, and the fifth is mono; it concludes that the
middle vertical map is an isomorphism.
-/
def StatementShape : Prop :=
  ∀ (R₁ R₂ : ComposableArrows C 4) (φ : R₁ ⟶ R₂),
    R₁.Exact →
      R₂.Exact →
        Epi (app' φ 0) →
          IsIso (app' φ 1) →
            IsIso (app' φ 3) →
              Mono (app' φ 4) →
                IsIso (app' φ 2)

/-- Checked wrapper around mathlib's category-theoretic five lemma. -/
theorem fiveLemma_isIso_middle
    {R₁ R₂ : ComposableArrows C 4} (φ : R₁ ⟶ R₂)
    (hR₁ : R₁.Exact) (hR₂ : R₂.Exact)
    (h₀ : Epi (app' φ 0)) (h₁ : IsIso (app' φ 1))
    (h₃ : IsIso (app' φ 3)) (h₄ : Mono (app' φ 4)) :
    IsIso (app' φ 2) :=
  CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono hR₁ hR₂ φ h₀ h₁ h₃ h₄

/-- The Stage1 statement shape is satisfied by the pinned mathlib five lemma. -/
theorem statementShape_holds : StatementShape (C := C) := by
  intro R₁ R₂ φ hR₁ hR₂ h₀ h₁ h₃ h₄
  exact fiveLemma_isIso_middle φ hR₁ hR₂ h₀ h₁ h₃ h₄

namespace HomologySequenceWrapper

open HomologicalComplex

variable {ι : Type*} {c : ComplexShape ι}
  {S₁ S₂ : ShortComplex (HomologicalComplex C c)} (φ : S₁ ⟶ S₂)
  (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)

/--
Checked wrapper around the homology-sequence consequence that mathlib derives
from the four/five-lemma infrastructure.

This is not a separate proof of the five lemma; it records the nearby
homological-algebra API that uses the diagram-lemma package to prove that the
third map in a short exact sequence of complexes induces an isomorphism on
homology under the displayed neighboring-degree hypotheses.
-/
theorem isIso_homologyMap_tau3
    (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (i : ι)
    (h₁ : Epi (homologyMap φ.τ₁ i))
    (h₂ : IsIso (homologyMap φ.τ₂ i))
    (h₃ : ∀ j, c.Rel i j → IsIso (homologyMap φ.τ₁ j))
    (h₄ : ∀ j, c.Rel i j → Mono (homologyMap φ.τ₂ j)) :
    IsIso (homologyMap φ.τ₃ i) :=
  HomologicalComplex.HomologySequence.isIso_homologyMap_τ₃ φ hS₁ hS₂ i h₁ h₂ h₃ h₄

end HomologySequenceWrapper

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas",
  "Mathlib.Algebra.Homology.HomologySequence",
  "Mathlib.Algebra.Homology.ShortComplex.ShortExact",
  "Mathlib.Algebra.Homology.ShortComplex.QuasiIso",
  "Mathlib.Algebra.Homology.ExactSequence",
  "Mathlib.CategoryTheory.Abelian.CommSq",
  "Mathlib.CategoryTheory.Abelian.Exact",
  "Mathlib.CategoryTheory.Triangulated.Pretriangulated"
]

/-- Primary theorem names checked in the pinned mathlib source. -/
def mathlibAnchorTheorems : List String := [
  "CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono",
  "CategoryTheory.Abelian.mono_of_epi_of_mono_of_mono",
  "CategoryTheory.Abelian.epi_of_epi_of_epi_of_mono",
  "HomologicalComplex.HomologySequence.isIso_homologyMap_τ₃",
  "HomologicalComplex.HomologySequence.quasiIso_τ₃",
  "ShortComplex.quasiIso_of_epi_of_isIso_of_mono",
  "ShortComplex.exact_iff_of_epi_of_isIso_of_mono",
  "CategoryTheory.Triangle.isIso_of_isIsos",
  "CategoryTheory.Triangulated.isIso₂_of_isIso₁₃"
]

/-- Pinned mathlib revision used by this repository's Lake manifest. -/
def mathlibPinnedRevision : String :=
  "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Primary mathlib source file for the category-level five-lemma anchor. -/
def mathlibPrimarySourceFile : String :=
  "Mathlib/CategoryTheory/Abelian/DiagramLemmas/Four.lean"

/--
Source file for the checked homological-algebra downstream consequence.

This branch is recorded as a consequence of the diagram-lemma infrastructure,
not as a replacement statement for the category-level five lemma.
-/
def mathlibHomologyConsequenceSourceFile : String :=
  "Mathlib/Algebra/Homology/HomologySequenceLemmas.lean"

/-- Audit role of the homology-sequence branch relative to the five lemma. -/
def homologyConsequenceRole : String :=
  "downstream_consequence_not_replacement"

/-- M0387 machine-anchor status for this Stage1 artifact. -/
def machineAnchorStatus : String :=
  "local_wrapper_upstream_mathlib"

/--
Exact public-surface scope wording for this wrapper.

The local Lean artifact proves only this category-level `ComposableArrows`
statement.  Module, abelian-group, triangulated-category, and derived-category
variants should be added only as separate wrappers if later passes need them.
-/
def publicScopeWording : String :=
  "category-level five lemma for exact `ComposableArrows` in an abelian category"

/-! ## Audit probes -/

#check StatementShape
#check fiveLemma_isIso_middle
#check HomologySequenceWrapper.isIso_homologyMap_tau3
#check CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono
#check HomologicalComplex.HomologySequence.isIso_homologyMap_τ₃
#check mathlibPinnedRevision
#check mathlibPrimarySourceFile
#check mathlibHomologyConsequenceSourceFile
#check homologyConsequenceRole
#check machineAnchorStatus
#check publicScopeWording

end S1_M_097
end Stage1
end AwesomeTheorems
