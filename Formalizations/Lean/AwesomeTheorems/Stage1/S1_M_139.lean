import Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems
import Mathlib.CategoryTheory.Adjunction.PartialAdjoint
import Mathlib.CategoryTheory.Abelian.Injective.Basic
import Mathlib.CategoryTheory.Abelian.LeftDerived
import Mathlib.CategoryTheory.Abelian.Projective.Basic
import Mathlib.CategoryTheory.Abelian.RightDerived
import Mathlib.CategoryTheory.Abelian.ShortExact
import Mathlib.CategoryTheory.RepresentedBy
import Mathlib.Algebra.Homology.HomologySequenceLemmas

/-!
# S1-M-139 / THM-M-0083: Representable functor theorem

This Stage1 artifact records the category-level statement shape that mathlib
currently supports directly: a presheaf is representable exactly when it has a
universal element whose induced maps from hom-sets are bijective.  The dual
corepresentability package is also exposed as a wrapper around mathlib's
`CorepresentableBy` and `IsCorepresentable` API.

This file deliberately does not claim a terminal proof of a stronger
representability theorem such as Brown representability or a Freyd adjoint
functor theorem consequence.  The homological branch below records checked
mathlib API boundaries for preadditive Yoneda exactness, projective/injective
objects, short exact sequences, derived functors, and homology long-exact
sequence segments; it is still not a terminal homological representability
theorem.
-/

noncomputable section

universe w v u vD uD

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_139

open CategoryTheory
open CategoryTheory.Functor
open CategoryTheory.Limits
open Opposite

variable {C : Type u} [Category.{v} C]

/--
Universal-element criterion for representability of a presheaf.

For a presheaf `F : Cᵒᵖ ⥤ Type w`, the data are a representing object `X`, a
universal element `x : F.obj (op X)`, and bijectivity of the induced maps
`(Y ⟶ X) -> F.obj (op Y)` for every test object `Y`.
-/
def UniversalElementCriterion (F : Cᵒᵖ ⥤ Type w) : Prop :=
  ∃ (X : C) (x : F.obj (op X)),
    ∀ Y : C, Function.Bijective (fun f : Y ⟶ X => F.map f.op x)

/--
Stage1 statement-shape candidate for the representable functor theorem.

This is the precise category-level boundary checked in this file.  It is
equivalent to mathlib's `F.IsRepresentable`.
-/
def StatementShape (F : Cᵒᵖ ⥤ Type w) : Prop :=
  UniversalElementCriterion F

/-- Checked mathlib equivalence between the universal-element criterion and representability. -/
theorem statementShape_iff_isRepresentable (F : Cᵒᵖ ⥤ Type w) :
    StatementShape F ↔ F.IsRepresentable := by
  constructor
  · rintro ⟨X, x, hx⟩
    exact (IsRepresentable.iff_exists_isRepresentedBy (F := F)).mpr
      ⟨X, x, ⟨fun {Y} => hx Y⟩⟩
  · intro hF
    rcases (IsRepresentable.iff_exists_isRepresentedBy (F := F)).mp hF with
      ⟨X, x, hx⟩
    exact ⟨X, x, fun Y => hx.map_bijective (Y := Y)⟩

/-- Forward wrapper: a universal element makes the presheaf representable. -/
theorem isRepresentable_of_statementShape {F : Cᵒᵖ ⥤ Type w}
    (hF : StatementShape F) : F.IsRepresentable :=
  (statementShape_iff_isRepresentable F).mp hF

/-- Reverse wrapper: mathlib representability supplies the universal-element criterion. -/
theorem statementShape_of_isRepresentable {F : Cᵒᵖ ⥤ Type w}
    (hF : F.IsRepresentable) : StatementShape F :=
  (statementShape_iff_isRepresentable F).mpr hF

/--
Equivalent bundled criterion: a presheaf is representable iff it has an explicit
`RepresentableBy` witness.
-/
theorem isRepresentable_iff_exists_representableBy (F : Cᵒᵖ ⥤ Type w) :
    F.IsRepresentable ↔ ∃ X : C, Nonempty (F.RepresentableBy X) := by
  constructor
  · intro hF
    rcases (IsRepresentable.iff_exists_isRepresentedBy (F := F)).mp hF with
      ⟨X, _x, hx⟩
    exact ⟨X, ⟨hx.representableBy⟩⟩
  · rintro ⟨_X, ⟨R⟩⟩
    exact R.isRepresentable

/-- Representing objects are unique up to isomorphism. -/
def representingObjectUniqueUpToIso {F : Cᵒᵖ ⥤ Type w} {X Y : C}
    (RX : F.RepresentableBy X) (RY : F.RepresentableBy Y) : X ≅ Y :=
  RX.uniqueUpToIso RY

/-- The Yoneda presheaf is represented by its indexing object. -/
def yonedaRepresentableBy (X : C) : (yoneda.obj X).RepresentableBy X :=
  RepresentableBy.yoneda X

/--
Naturality of the Yoneda universal element in the same-universe case.  This is
the checked naturality square that later theorem-tree branches can use as the
category-level normalization for maps between representing objects.
-/
theorem yoneda_universalElement_naturality {F : Cᵒᵖ ⥤ Type v}
    {X Y : C} (α : yoneda.obj X ⟶ F) (g : Y ⟶ X) :
    F.map g.op (yonedaEquiv α) = yonedaEquiv (yoneda.map g ≫ α) :=
  yonedaEquiv_naturality α g

/-- Dual Stage1 statement shape for corepresentability of a copresheaf. -/
def CorepresentableStatementShape (F : C ⥤ Type w) : Prop :=
  ∃ X : C, Nonempty (F.CorepresentableBy X)

/-- Checked equivalence with mathlib's `IsCorepresentable` class. -/
theorem corepresentableStatementShape_iff_isCorepresentable (F : C ⥤ Type w) :
    CorepresentableStatementShape F ↔ F.IsCorepresentable := by
  constructor
  · intro hF
    exact ⟨hF⟩
  · intro hF
    exact hF.has_corepresentation

/-- A `CorepresentableBy` witness makes a functor corepresentable. -/
theorem isCorepresentable_of_corepresentableBy {F : C ⥤ Type w} {X : C}
    (R : F.CorepresentableBy X) : F.IsCorepresentable :=
  R.isCorepresentable

/-- Corepresenting objects are unique up to isomorphism. -/
def corepresentingObjectUniqueUpToIso {F : C ⥤ Type w} {X Y : C}
    (RX : F.CorepresentableBy X) (RY : F.CorepresentableBy Y) : X ≅ Y :=
  RX.uniqueUpToIso RY

/-- The coyoneda copresheaf is corepresented by its indexing object. -/
def coyonedaCorepresentableBy (X : Cᵒᵖ) :
    (coyoneda.obj X).CorepresentableBy X.unop :=
  CorepresentableBy.coyoneda X

section PartialAdjointBridge

variable {D : Type uD} [Category.{vD} D]

/--
Partial-adjoint bridge: the objectwise domain of a right adjoint to `F` is
exactly the predicate that the hom functor `F.op ⋙ yoneda.obj Y` is
representable.
-/
theorem rightAdjointObjIsDefined_iff_representable
    (F : C ⥤ D) (Y : D) :
    F.rightAdjointObjIsDefined Y ↔ (F.op ⋙ yoneda.obj Y).IsRepresentable :=
  F.rightAdjointObjIsDefined_iff Y

/--
Partial-adjoint bridge: `F` is a left adjoint precisely when every objectwise
right-adjoint representing functor is defined.
-/
theorem isLeftAdjoint_iff_all_rightAdjoint_objects_representable
    (F : C ⥤ D) :
    F.IsLeftAdjoint ↔ ∀ Y : D, (F.op ⋙ yoneda.obj Y).IsRepresentable := by
  rw [F.isLeftAdjoint_iff_rightAdjointObjIsDefined_eq_top]
  constructor
  · intro h Y
    exact (F.rightAdjointObjIsDefined_iff Y).mp (by simp [h])
  · intro h
    ext Y
    exact (F.rightAdjointObjIsDefined_iff Y).trans (iff_true_intro (h Y))

/--
Dual partial-adjoint bridge: the objectwise domain of a left adjoint to `G` is
exactly the predicate that `G ⋙ coyoneda.obj (op X)` is corepresentable.
-/
theorem leftAdjointObjIsDefined_iff_corepresentable
    (G : D ⥤ C) (X : C) :
    G.leftAdjointObjIsDefined X ↔ (G ⋙ coyoneda.obj (op X)).IsCorepresentable :=
  G.leftAdjointObjIsDefined_iff X

/--
Dual partial-adjoint bridge: `G` is a right adjoint precisely when every
objectwise left-adjoint corepresenting functor is defined.
-/
theorem isRightAdjoint_iff_all_leftAdjoint_objects_corepresentable
    (G : D ⥤ C) :
    G.IsRightAdjoint ↔ ∀ X : C, (G ⋙ coyoneda.obj (op X)).IsCorepresentable := by
  rw [G.isRightAdjoint_iff_leftAdjointObjIsDefined_eq_top]
  constructor
  · intro h X
    exact (G.leftAdjointObjIsDefined_iff X).mp (by simp [h])
  · intro h
    ext X
    exact (G.leftAdjointObjIsDefined_iff X).trans (iff_true_intro (h X))

end PartialAdjointBridge

section AdjointFunctorTheoremAudit

variable {D : Type uD} [Category.{vD} D]

/--
General adjoint-functor-theorem branch audited for this Stage1 slot.

For a functor `G : D ⥤ C`, mathlib's general AFT produces right-adjointness
from completeness of `D`, preservation of small limits by `G`, and the
solution-set condition.  This is the general branch to use only if the selected
public representability statement keeps an explicit `SolutionSetCondition`.
-/
theorem generalAFT_isRightAdjoint_of_solutionSetCondition
    (G : D ⥤ C) [HasLimits D] [PreservesLimitsOfSize.{vD, vD} G]
    (hG : SolutionSetCondition.{vD} G) : G.IsRightAdjoint :=
  isRightAdjoint_of_preservesLimits_of_solutionSetCondition (G := G) hG

/--
Corepresentability consequence of the general AFT branch.

This keeps the branch boundary explicit: mathlib's general AFT first proves
`G.IsRightAdjoint`; the partial-adjoint bridge then identifies the resulting
objectwise left-adjoint predicates with corepresentability.
-/
theorem all_leftAdjoint_objects_corepresentable_of_generalAFT
    (G : D ⥤ C) [HasLimits D] [PreservesLimitsOfSize.{vD, vD} G]
    (hG : SolutionSetCondition.{vD} G) :
    ∀ X : C, (G ⋙ coyoneda.obj (op X)).IsCorepresentable :=
  (isRightAdjoint_iff_all_leftAdjoint_objects_corepresentable G).mp
    (generalAFT_isRightAdjoint_of_solutionSetCondition G hG)

section SameHomUniverse

variable {D' : Type uD} [Category.{v} D']

/--
Special adjoint-functor-theorem branch using a small coseparating object
property.  This branch proves right-adjointness of a limit-preserving functor.
-/
theorem specialAFT_isRightAdjoint_of_coseparating
    [HasLimits D'] [WellPowered.{v} D']
    {P : ObjectProperty D'} [ObjectProperty.Small.{v} P]
    (hP : P.IsCoseparating) (G : D' ⥤ C) [PreservesLimits G] :
    G.IsRightAdjoint :=
  isRightAdjoint_of_preservesLimits_of_isCoseparating hP G

/--
Dual special adjoint-functor-theorem branch using a small separating object
property.  This is the branch that directly feeds the checked objectwise
representability bridge for `F : C ⥤ D'`.
-/
theorem specialAFT_isLeftAdjoint_of_separating
    [HasColimits C] [WellPowered.{v} Cᵒᵖ]
    {P : ObjectProperty C} [ObjectProperty.Small.{v} P]
    (hP : P.IsSeparating) (F : C ⥤ D') [PreservesColimits F] :
    F.IsLeftAdjoint :=
  isLeftAdjoint_of_preservesColimits_of_isSeparating hP F

/--
Representability consequence of the dual special AFT branch.

If the chosen public statement is an adjoint-functor-theorem consequence for
`F : C ⥤ D'`, this is the exact repo-local checked branch: special AFT gives
`F.IsLeftAdjoint`, then the partial-adjoint bridge turns that into
representability of every presheaf `F.op ⋙ yoneda.obj Y`.
-/
theorem all_rightAdjoint_objects_representable_of_specialAFT
    [HasColimits C] [WellPowered.{v} Cᵒᵖ]
    {P : ObjectProperty C} [ObjectProperty.Small.{v} P]
    (hP : P.IsSeparating) (F : C ⥤ D') [PreservesColimits F] :
    ∀ Y : D', (F.op ⋙ yoneda.obj Y).IsRepresentable :=
  (isLeftAdjoint_iff_all_rightAdjoint_objects_representable F).mp
    (specialAFT_isLeftAdjoint_of_separating hP F)

/--
Corepresentability consequence of the special AFT branch.

This is the dual branch for a limit-preserving `G : D' ⥤ C`: special AFT gives
`G.IsRightAdjoint`, then the dual partial-adjoint bridge turns that into
corepresentability of every copresheaf `G ⋙ coyoneda.obj (op X)`.
-/
theorem all_leftAdjoint_objects_corepresentable_of_specialAFT
    [HasLimits D'] [WellPowered.{v} D']
    {P : ObjectProperty D'} [ObjectProperty.Small.{v} P]
    (hP : P.IsCoseparating) (G : D' ⥤ C) [PreservesLimits G] :
    ∀ X : C, (G ⋙ coyoneda.obj (op X)).IsCorepresentable :=
  (isRightAdjoint_iff_all_leftAdjoint_objects_corepresentable G).mp
    (specialAFT_isRightAdjoint_of_coseparating hP G)

end SameHomUniverse

end AdjointFunctorTheoremAudit

section HomologicalBranch

variable [Preadditive C]

/-- Preadditive Yoneda preserves all limits; this is the exactness anchor for left-exact use. -/
theorem preadditiveYonedaObj_preservesLimits (X : C) :
    PreservesLimits (preadditiveYonedaObj X) :=
  inferInstance

/-- Preadditive co-Yoneda preserves all limits; this is the dual left-exact anchor. -/
theorem preadditiveCoyonedaObj_preservesLimits (X : C) :
    PreservesLimits (preadditiveCoyonedaObj X) :=
  inferInstance

/-- Projective objects are detected by preservation of epimorphisms by preadditive co-Yoneda. -/
theorem projective_iff_preadditiveCoyonedaObj_preservesEpimorphisms (P : C) :
    Projective P ↔ (preadditiveCoyonedaObj P).PreservesEpimorphisms :=
  Projective.projective_iff_preservesEpimorphisms_preadditiveCoyonedaObj P

/-- Injective objects are detected by preservation of epimorphisms by preadditive Yoneda. -/
theorem injective_iff_preadditiveYonedaObj_preservesEpimorphisms (J : C) :
    Injective J ↔ (preadditiveYonedaObj J).PreservesEpimorphisms :=
  Injective.injective_iff_preservesEpimorphisms_preadditive_yoneda_obj' J

end HomologicalBranch

section AbelianHomologicalBranch

variable [Abelian C]

/-- A projective object makes preadditive co-Yoneda preserve homology. -/
theorem preadditiveCoyonedaObj_preservesHomology_of_projective
    (P : C) [Projective P] :
    (preadditiveCoyonedaObj P).PreservesHomology :=
  preservesHomology_preadditiveCoyonedaObj_of_projective P

/-- A projective object makes preadditive co-Yoneda preserve finite colimits. -/
theorem preadditiveCoyonedaObj_preservesFiniteColimits_of_projective
    (P : C) [Projective P] :
    PreservesFiniteColimits (preadditiveCoyonedaObj P) :=
  preservesFiniteColimits_preadditiveCoyonedaObj_of_projective P

/-- Finite-colimit preservation by preadditive co-Yoneda recovers projectivity. -/
theorem projective_of_preadditiveCoyonedaObj_preservesFiniteColimits
    (P : C) [PreservesFiniteColimits (preadditiveCoyonedaObj P)] :
    Projective P :=
  projective_of_preservesFiniteColimits_preadditiveCoyonedaObj P

/-- An injective object makes preadditive Yoneda preserve homology. -/
theorem preadditiveYonedaObj_preservesHomology_of_injective
    (J : C) [Injective J] :
    (preadditiveYonedaObj J).PreservesHomology :=
  preservesHomology_preadditiveYonedaObj_of_injective J

/-- An injective object makes preadditive Yoneda preserve finite colimits. -/
theorem preadditiveYonedaObj_preservesFiniteColimits_of_injective
    (J : C) [Injective J] :
    PreservesFiniteColimits (preadditiveYonedaObj J) :=
  preservesFiniteColimits_preadditiveYonedaObj_of_injective J

/-- Finite-colimit preservation by preadditive Yoneda recovers injectivity. -/
theorem injective_of_preadditiveYonedaObj_preservesFiniteColimits
    (J : C) [PreservesFiniteColimits (preadditiveYonedaObj J)] :
    Injective J :=
  injective_of_preservesFiniteColimits_preadditiveYonedaObj J

section ShortExactFunctorBridge

variable {D : Type uD} [Category.{vD} D] [Abelian D]
    (F : C ⥤ D) [F.PreservesZeroMorphisms] [F.Faithful]
    {S : ShortComplex C}

/-- Faithful exact-target functors reflect short exactness. -/
theorem shortExact_reflects_of_faithful
    (hS : (S.map F).ShortExact) : S.ShortExact :=
  CategoryTheory.ShortExact.reflects_shortExact_of_faithful F hS

/-- A faithful functor preserving finite limits and colimits preserves and reflects short exactness. -/
theorem shortExact_map_iff_of_faithful_exact
    [PreservesFiniteColimits F] [PreservesFiniteLimits F] :
    (S.map F).ShortExact ↔ S.ShortExact :=
  CategoryTheory.ShortExact.shortExact_map_iff F

end ShortExactFunctorBridge

section HomologySequenceBranch

variable {ι : Type w} {c : ComplexShape ι}
    {S : ShortComplex (HomologicalComplex C c)}

/-- Connecting morphism in the homology sequence of a short exact sequence of complexes. -/
def homologySequenceConnectingHom
    (hS : S.ShortExact) {i j : ι} (hij : c.Rel i j) :
    S.X₃.homology i ⟶ S.X₁.homology j :=
  hS.δ i j hij

/-- The same-degree three-term homology sequence associated to a short exact complex is exact. -/
theorem homologySequence_two_term_exact
    (hS : S.ShortExact) (i : ι) :
    (HomologicalComplex.HomologySequence.composableArrows₂ S i).Exact :=
  HomologicalComplex.HomologySequence.composableArrows₂_exact hS i

/-- A checked five-term segment of the long exact homology sequence. -/
theorem homologySequence_five_term_exact
    (hS : S.ShortExact) (i j : ι) (hij : c.Rel i j) :
    (HomologicalComplex.HomologySequence.composableArrows₅ hS i j hij).Exact :=
  HomologicalComplex.HomologySequence.composableArrows₅_exact hS i j hij

end HomologySequenceBranch

section DerivedFunctorBranch

variable {D : Type uD} [Category.{vD} D] [Abelian D]

/-- Higher left-derived functors vanish on projective objects. -/
theorem isZero_leftDerived_obj_projective_succ
    [HasProjectiveResolutions C] (F : C ⥤ D) [F.Additive]
    (n : ℕ) (X : C) [Projective X] :
    IsZero ((F.leftDerived (n + 1)).obj X) :=
  Functor.isZero_leftDerived_obj_projective_succ F n X

/-- Higher right-derived functors vanish on injective objects. -/
theorem isZero_rightDerived_obj_injective_succ
    [HasInjectiveResolutions C] (F : C ⥤ D) [F.Additive]
    (n : ℕ) (X : C) [Injective X] :
    IsZero ((F.rightDerived (n + 1)).obj X) :=
  Functor.isZero_rightDerived_obj_injective_succ F n X

end DerivedFunctorBranch

end AbelianHomologicalBranch

/-- Pinned mathlib modules audited for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Yoneda",
  "Mathlib.CategoryTheory.RepresentedBy",
  "Mathlib.CategoryTheory.Adjunction.PartialAdjoint",
  "Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Basic",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Limits",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Projective",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Injective",
  "Mathlib.CategoryTheory.Abelian.Projective.Basic",
  "Mathlib.CategoryTheory.Abelian.Injective.Basic",
  "Mathlib.CategoryTheory.Abelian.ShortExact",
  "Mathlib.CategoryTheory.Abelian.LeftDerived",
  "Mathlib.CategoryTheory.Abelian.RightDerived",
  "Mathlib.Algebra.Homology.HomologySequence",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas"
]

/-- Pinned theorem and declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorTheorems : List String := [
  "CategoryTheory.yoneda",
  "CategoryTheory.coyoneda",
  "CategoryTheory.yonedaEquiv",
  "CategoryTheory.yonedaEquiv_naturality",
  "CategoryTheory.Functor.RepresentableBy",
  "CategoryTheory.Functor.CorepresentableBy",
  "CategoryTheory.Functor.IsRepresentable",
  "CategoryTheory.Functor.IsRepresentedBy",
  "CategoryTheory.Functor.IsRepresentable.iff_exists_isRepresentedBy",
  "CategoryTheory.Functor.IsRepresentedBy.iff_exists_representableBy",
  "CategoryTheory.Functor.RepresentableBy.isRepresentedBy",
  "CategoryTheory.Functor.RepresentableBy.isRepresentable",
  "CategoryTheory.Functor.RepresentableBy.uniqueUpToIso",
  "CategoryTheory.Functor.IsCorepresentable",
  "CategoryTheory.Functor.CorepresentableBy.isCorepresentable",
  "CategoryTheory.Functor.CorepresentableBy.uniqueUpToIso",
  "CategoryTheory.Functor.RepresentableBy.yoneda",
  "CategoryTheory.Functor.CorepresentableBy.coyoneda",
  "CategoryTheory.Functor.rightAdjointObjIsDefined_iff",
  "CategoryTheory.Functor.isLeftAdjoint_iff_rightAdjointObjIsDefined_eq_top",
  "CategoryTheory.Functor.leftAdjointObjIsDefined_iff",
  "CategoryTheory.Functor.isRightAdjoint_iff_leftAdjointObjIsDefined_eq_top",
  "CategoryTheory.SolutionSetCondition",
  "CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition",
  "CategoryTheory.isRightAdjoint_of_preservesLimits_of_isCoseparating",
  "CategoryTheory.isLeftAdjoint_of_preservesColimits_of_isSeparating",
  "CategoryTheory.preadditiveYonedaObj",
  "CategoryTheory.preadditiveCoyonedaObj",
  "CategoryTheory.preadditiveYoneda",
  "CategoryTheory.preadditiveCoyoneda",
  "CategoryTheory.preservesLimits_preadditiveYonedaObj",
  "CategoryTheory.preservesLimits_preadditiveCoyonedaObj",
  "CategoryTheory.Projective.projective_iff_preservesEpimorphisms_preadditiveCoyonedaObj",
  "CategoryTheory.Injective.injective_iff_preservesEpimorphisms_preadditive_yoneda_obj'",
  "CategoryTheory.preservesHomology_preadditiveCoyonedaObj_of_projective",
  "CategoryTheory.preservesFiniteColimits_preadditiveCoyonedaObj_of_projective",
  "CategoryTheory.projective_of_preservesFiniteColimits_preadditiveCoyonedaObj",
  "CategoryTheory.preservesHomology_preadditiveYonedaObj_of_injective",
  "CategoryTheory.preservesFiniteColimits_preadditiveYonedaObj_of_injective",
  "CategoryTheory.injective_of_preservesFiniteColimits_preadditiveYonedaObj",
  "CategoryTheory.ShortExact.reflects_shortExact_of_faithful",
  "CategoryTheory.ShortExact.shortExact_map_iff",
  "HomologicalComplex.HomologySequence.composableArrows₂",
  "HomologicalComplex.HomologySequence.composableArrows₂_exact",
  "HomologicalComplex.HomologySequence.composableArrows₅",
  "HomologicalComplex.HomologySequence.composableArrows₅_exact",
  "HomologicalComplex.HomologySequence.δ_naturality",
  "CategoryTheory.Functor.leftDerived",
  "CategoryTheory.Functor.isZero_leftDerived_obj_projective_succ",
  "CategoryTheory.Functor.rightDerived",
  "CategoryTheory.Functor.isZero_rightDerived_obj_injective_succ",
  "AwesomeTheorems.Stage1.S1_M_139.generalAFT_isRightAdjoint_of_solutionSetCondition",
  "AwesomeTheorems.Stage1.S1_M_139.all_leftAdjoint_objects_corepresentable_of_generalAFT",
  "AwesomeTheorems.Stage1.S1_M_139.specialAFT_isRightAdjoint_of_coseparating",
  "AwesomeTheorems.Stage1.S1_M_139.specialAFT_isLeftAdjoint_of_separating",
  "AwesomeTheorems.Stage1.S1_M_139.all_rightAdjoint_objects_representable_of_specialAFT",
  "AwesomeTheorems.Stage1.S1_M_139.all_leftAdjoint_objects_corepresentable_of_specialAFT",
  "AwesomeTheorems.Stage1.S1_M_139.preadditiveYonedaObj_preservesLimits",
  "AwesomeTheorems.Stage1.S1_M_139.preadditiveCoyonedaObj_preservesLimits",
  "AwesomeTheorems.Stage1.S1_M_139.projective_iff_preadditiveCoyonedaObj_preservesEpimorphisms",
  "AwesomeTheorems.Stage1.S1_M_139.injective_iff_preadditiveYonedaObj_preservesEpimorphisms",
  "AwesomeTheorems.Stage1.S1_M_139.preadditiveCoyonedaObj_preservesHomology_of_projective",
  "AwesomeTheorems.Stage1.S1_M_139.preadditiveCoyonedaObj_preservesFiniteColimits_of_projective",
  "AwesomeTheorems.Stage1.S1_M_139.projective_of_preadditiveCoyonedaObj_preservesFiniteColimits",
  "AwesomeTheorems.Stage1.S1_M_139.preadditiveYonedaObj_preservesHomology_of_injective",
  "AwesomeTheorems.Stage1.S1_M_139.preadditiveYonedaObj_preservesFiniteColimits_of_injective",
  "AwesomeTheorems.Stage1.S1_M_139.injective_of_preadditiveYonedaObj_preservesFiniteColimits",
  "AwesomeTheorems.Stage1.S1_M_139.shortExact_reflects_of_faithful",
  "AwesomeTheorems.Stage1.S1_M_139.shortExact_map_iff_of_faithful_exact",
  "AwesomeTheorems.Stage1.S1_M_139.homologySequenceConnectingHom",
  "AwesomeTheorems.Stage1.S1_M_139.homologySequence_two_term_exact",
  "AwesomeTheorems.Stage1.S1_M_139.homologySequence_five_term_exact",
  "AwesomeTheorems.Stage1.S1_M_139.isZero_leftDerived_obj_projective_succ",
  "AwesomeTheorems.Stage1.S1_M_139.isZero_rightDerived_obj_injective_succ"
]

#check StatementShape
#check statementShape_iff_isRepresentable
#check CorepresentableStatementShape
#check corepresentableStatementShape_iff_isCorepresentable
#check rightAdjointObjIsDefined_iff_representable
#check generalAFT_isRightAdjoint_of_solutionSetCondition
#check all_leftAdjoint_objects_corepresentable_of_generalAFT
#check specialAFT_isLeftAdjoint_of_separating
#check all_rightAdjoint_objects_representable_of_specialAFT
#check preadditiveYonedaObj_preservesLimits
#check projective_iff_preadditiveCoyonedaObj_preservesEpimorphisms
#check injective_iff_preadditiveYonedaObj_preservesEpimorphisms
#check shortExact_map_iff_of_faithful_exact
#check homologySequenceConnectingHom
#check homologySequence_five_term_exact
#check isZero_leftDerived_obj_projective_succ
#check isZero_rightDerived_obj_injective_succ

end S1_M_139
end Stage1
end AwesomeTheorems
