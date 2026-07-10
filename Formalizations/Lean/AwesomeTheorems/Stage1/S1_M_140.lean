import Mathlib.CategoryTheory.Monad.Monadicity

/-!
# S1-M-140 / THM-M-0085: Beck's monadicity theorem

This Stage1 file records repo-local wrappers around mathlib's pinned Lean 4
formalization of Beck's monadicity theorem.

The theorem is already present in mathlib as several monadicity criteria for a
right adjoint `G`, formulated through the comparison functor from `D` to the
Eilenberg-Moore category of the monad induced by an adjunction `F ⊣ G`.  The
declarations below keep the Stage1 surface small and explicit: they expose the
comparison-functor statement shape and wrap the four checked mathlib variants
without adding proof placeholders.

Boundary: `upstream theorem closure: yes / repo-local checked dependency closure: yes / repo-local vendored proof-body copy: no`.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

universe v u₁ u₂

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_140

variable {C : Type u₁} {D : Type u₂}
variable [Category.{v} C] [Category.{v} D]
variable {F : C ⥤ D} {G : D ⥤ C}

/-- The monad on `C` induced by an adjunction `F ⊣ G`. -/
abbrev InducedMonad (adj : F ⊣ G) : Monad C :=
  adj.toMonad

/--
The Eilenberg-Moore comparison functor associated to an adjunction `F ⊣ G`.

Beck monadicity identifies the right adjoint `G` as monadic when this functor is
an equivalence under the appropriate split-coequalizer hypotheses.
-/
abbrev ComparisonFunctor (adj : F ⊣ G) : D ⥤ (InducedMonad adj).Algebra :=
  CategoryTheory.Monad.comparison adj

/-- The forgetful functor from algebras composed with the comparison functor is `G`. -/
abbrev comparisonForgetIso (adj : F ⊣ G) :
    ComparisonFunctor adj ⋙ CategoryTheory.Monad.forget (InducedMonad adj) ≅ G :=
  CategoryTheory.Monad.comparisonForget adj

/--
Stage1 normalized statement shape for Beck monadicity.

`MonadicRightAdjoint G` packages a left adjoint for `G`, the induced monad, and
the assertion that the comparison functor to Eilenberg-Moore algebras is an
equivalence.  The concrete Beck criteria below provide checked constructors for
this shape from mathlib's split-coequalizer hypotheses.
-/
def StatementShape (G : D ⥤ C) : Prop :=
  Nonempty (CategoryTheory.MonadicRightAdjoint G)

/-- The statement-shape definition unfolds to nonemptiness of mathlib's monadicity class. -/
theorem statementShape_iff_nonempty (G : D ⥤ C) :
    StatementShape G ↔ Nonempty (CategoryTheory.MonadicRightAdjoint G) :=
  Iff.rfl

/--
Beck monadicity, mathlib's has/preserves/reflects `G`-split coequalizer form.
-/
@[implicit_reducible]
def beckMonadicity_of_has_preserves_reflects_GSplitCoequalizers (adj : F ⊣ G)
    [CategoryTheory.Monad.HasCoequalizerOfIsSplitPair G]
    [CategoryTheory.Monad.PreservesColimitOfIsSplitPair G]
    [CategoryTheory.Monad.ReflectsColimitOfIsSplitPair G] :
    CategoryTheory.MonadicRightAdjoint G :=
  CategoryTheory.Monad.monadicOfHasPreservesReflectsGSplitCoequalizers adj

/--
Beck monadicity, mathlib's creates-`G`-split-coequalizers form.
-/
@[implicit_reducible]
def beckMonadicity_of_creates_GSplitCoequalizers (adj : F ⊣ G)
    [CategoryTheory.Monad.CreatesColimitOfIsSplitPair G] :
    CategoryTheory.MonadicRightAdjoint G :=
  CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers adj

/--
Beck monadicity, mathlib's reflects-isomorphisms plus has/preserves
`G`-split-coequalizers form.
-/
@[implicit_reducible]
def beckMonadicity_of_has_preserves_GSplitCoequalizers_reflectsIsomorphisms
    (adj : F ⊣ G) [G.ReflectsIsomorphisms]
    [CategoryTheory.Monad.HasCoequalizerOfIsSplitPair G]
    [CategoryTheory.Monad.PreservesColimitOfIsSplitPair G] :
    CategoryTheory.MonadicRightAdjoint G :=
  CategoryTheory.Monad.monadicOfHasPreservesGSplitCoequalizersOfReflectsIsomorphisms adj

/--
The reflexive, or crude, monadicity theorem from mathlib.
-/
@[implicit_reducible]
def beckMonadicity_of_reflexiveCoequalizers_reflectsIsomorphisms
    (adj : F ⊣ G) [HasReflexiveCoequalizers D] [G.ReflectsIsomorphisms]
    [CategoryTheory.Monad.PreservesColimitOfIsReflexivePair G] :
    CategoryTheory.MonadicRightAdjoint G :=
  CategoryTheory.Monad.monadicOfHasPreservesReflexiveCoequalizersOfReflectsIsomorphisms adj

/--
The converse direction recorded in mathlib: a monadic right adjoint creates
colimits of `G`-split pairs.
-/
@[implicit_reducible]
def creates_GSplitCoequalizers_of_monadic (G : D ⥤ C)
    [CategoryTheory.MonadicRightAdjoint G] ⦃A B : D⦄ (f g : A ⟶ B)
    [G.IsSplitPair f g] :
    CreatesColimit (parallelPair f g) G :=
  CategoryTheory.Monad.createsGSplitCoequalizersOfMonadic G f g

/-- The Beck cofork of a monad algebra is a split coequalizer in mathlib. -/
def beckSplitCoequalizer {T : Monad C} (X : T.Algebra) :
    IsSplitCoequalizer (T.map X.a) (T.μ.app _) X.a :=
  CategoryTheory.Monad.beckSplitCoequalizer X

/-- The Beck cofork of a monad algebra is a coequalizer in mathlib. -/
def beckCoequalizer {T : Monad C} (X : T.Algebra) :
    IsColimit (CategoryTheory.Monad.beckCofork X) :=
  CategoryTheory.Monad.beckCoequalizer X

/-- mathlib modules checked and imported as anchors for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Monad.Adjunction",
  "Mathlib.CategoryTheory.Monad.Algebra",
  "Mathlib.CategoryTheory.Monad.Coequalizer",
  "Mathlib.CategoryTheory.Monad.Limits",
  "Mathlib.CategoryTheory.Monad.Monadicity",
  "Mathlib.CategoryTheory.Monad.Comonadicity"
]

/-- Pinned theorem and definition names used or audited for Beck monadicity. -/
def mathlibAnchorNames : List String := [
  "CategoryTheory.MonadicRightAdjoint",
  "CategoryTheory.Monad.comparison",
  "CategoryTheory.Monad.comparisonForget",
  "CategoryTheory.Monad.beckSplitCoequalizer",
  "CategoryTheory.Monad.beckCoequalizer",
  "CategoryTheory.Monad.createsGSplitCoequalizersOfMonadic",
  "CategoryTheory.Monad.monadicOfHasPreservesReflectsGSplitCoequalizers",
  "CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers",
  "CategoryTheory.Monad.monadicOfHasPreservesGSplitCoequalizersOfReflectsIsomorphisms",
  "CategoryTheory.Monad.monadicOfHasPreservesReflexiveCoequalizersOfReflectsIsomorphisms"
]

/-- Search terms used to check for nearby or alternate terminal anchors. -/
def anchorSearchTerms : List String := [
  "Beck",
  "monadicity",
  "MonadicRightAdjoint",
  "comparison",
  "GSplitCoequalizers",
  "CreatesColimitOfIsSplitPair",
  "PreservesColimitOfIsSplitPair",
  "ReflectsColimitOfIsSplitPair"
]

end S1_M_140
end Stage1
end AwesomeTheorems
