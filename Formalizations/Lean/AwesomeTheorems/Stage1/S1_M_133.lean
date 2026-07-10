import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu
import Mathlib.CategoryTheory.Abelian.SerreClass.Localization
import Mathlib.CategoryTheory.Abelian.SerreClass.Bousfield

/-!
# S1-M-133 / THM-M-0087: Gabriel-Popescu theorem

This Stage1 file records a repo-local wrapper around the pinned mathlib
formalization of the Gabriel-Popescu theorem.

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the module
`Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu`
proves that for a Grothendieck abelian category `C` and a separator `G`, the
preadditive coyoneda functor `Hom(G, -)` is full and faithful and has a left
adjoint that preserves finite limits.  Since the left adjoint is a left adjoint,
it also has the expected colimit-preservation side of the usual "exact left
adjoint" formulation.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

universe v u v' u' v'' u''

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_133

variable {C : Type u} [Category.{v} C] [Abelian C]

/-- The Gabriel-Popescu embedding functor `X ↦ Hom(G, X)`. -/
abbrev gabrielPopescuEmbedding (G : C) :=
  preadditiveCoyonedaObj G

/-- mathlib proves faithfulness of the same functor from the separator property. -/
theorem embedding_faithful (G : C) (hG : IsSeparator G) :
    (gabrielPopescuEmbedding G).Faithful := by
  exact (isSeparator_iff_faithful_preadditiveCoyonedaObj G).1 hG

variable [IsGrothendieckAbelian.{v} C]

/-- The left adjoint to the Gabriel-Popescu embedding functor. -/
abbrev gabrielPopescuLeftAdjoint (G : C) :=
  IsGrothendieckAbelian.tensorObj G

/--
Checked data package for the Gabriel-Popescu embedding theorem.

The proof fields are filled below by the pinned mathlib theorem names, so this
is a genuine local wrapper rather than an anchor-only note.
-/
structure GabrielPopescuEmbeddingData (G : C) where
  embedding_full : (gabrielPopescuEmbedding G).Full
  embedding_faithful : (gabrielPopescuEmbedding G).Faithful
  embedding_preservesInjectiveObjects :
    (gabrielPopescuEmbedding G).PreservesInjectiveObjects
  leftAdjoint_adjunction :
    gabrielPopescuLeftAdjoint G ⊣ gabrielPopescuEmbedding G
  leftAdjoint_preservesFiniteLimits :
    PreservesFiniteLimits (gabrielPopescuLeftAdjoint G)
  embedding_isRightAdjoint : (gabrielPopescuEmbedding G).IsRightAdjoint
  leftAdjoint_isLeftAdjoint : (gabrielPopescuLeftAdjoint G).IsLeftAdjoint

/--
Normalized Stage1 statement-shape candidate for the Gabriel-Popescu theorem.

For every separator `G` in a Grothendieck abelian category, the Hom functor
`Hom(G, -)` has the full/faithful embedding and exact-left-adjoint data supplied
by mathlib.
-/
def StatementShape : Prop :=
  ∀ G : C, IsSeparator G → Nonempty (GabrielPopescuEmbeddingData G)

/--
Primary machine anchor for the full embedding half of the Gabriel-Popescu
formulation.
-/
theorem embedding_full (G : C) (hG : IsSeparator G) :
    (gabrielPopescuEmbedding G).Full := by
  exact IsGrothendieckAbelian.GabrielPopescu.full G hG

/--
The `map_surjective` component of the pinned mathlib proof of
`GabrielPopescu.full`.
-/
theorem embedding_full_map_surjective (G : C) (hG : IsSeparator G) {A B : C}
    (f : (gabrielPopescuEmbedding G).obj A ⟶ (gabrielPopescuEmbedding G).obj B) :
    ∃ g : A ⟶ B, (gabrielPopescuEmbedding G).map g = f := by
  exact (embedding_full G hG).map_surjective f

/--
Primary machine anchor for the injective-object preservation branch used by
mathlib's exactness proof.
-/
theorem embedding_preservesInjectiveObjects (G : C) (hG : IsSeparator G) :
    (gabrielPopescuEmbedding G).PreservesInjectiveObjects := by
  exact IsGrothendieckAbelian.GabrielPopescu.preservesInjectiveObjects G hG

/-- mathlib's tensor-Hom adjunction for the Gabriel-Popescu functor. -/
def leftAdjoint_adjunction (G : C) :
    gabrielPopescuLeftAdjoint G ⊣ gabrielPopescuEmbedding G := by
  exact IsGrothendieckAbelian.tensorObjPreadditiveCoyonedaObjAdjunction G

/--
Primary machine anchor for the finite-limit-preserving half of the exact
left-adjoint Gabriel-Popescu formulation.
-/
theorem leftAdjoint_preservesFiniteLimits (G : C) (hG : IsSeparator G) :
    PreservesFiniteLimits (gabrielPopescuLeftAdjoint G) := by
  exact IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits G hG

/--
Intermediate machine anchor from the upstream proof of
`GabrielPopescu.preservesFiniteLimits`: the left adjoint preserves homology once
the right adjoint preserves injective objects.
-/
theorem leftAdjoint_preservesHomology (G : C) (hG : IsSeparator G) :
    (gabrielPopescuLeftAdjoint G).PreservesHomology := by
  have := embedding_preservesInjectiveObjects G hG
  have : (gabrielPopescuLeftAdjoint G).PreservesMonomorphisms :=
    (gabrielPopescuLeftAdjoint G).preservesMonomorphisms_of_adjunction_of_preservesInjectiveObjects
      (leftAdjoint_adjunction G)
  have : PreservesBinaryBiproducts (gabrielPopescuLeftAdjoint G) :=
    preservesBinaryBiproducts_of_preservesBinaryCoproducts _
  have : (gabrielPopescuLeftAdjoint G).Additive :=
    Functor.additive_of_preservesBinaryBiproducts _
  exact (gabrielPopescuLeftAdjoint G).preservesHomology_of_preservesMonos_and_cokernels

/-- Repo-local data wrapper around the pinned mathlib Gabriel-Popescu theorem. -/
def gabrielPopescuEmbeddingData (G : C) (hG : IsSeparator G) :
    GabrielPopescuEmbeddingData G where
  embedding_full := embedding_full G hG
  embedding_faithful := embedding_faithful G hG
  embedding_preservesInjectiveObjects := embedding_preservesInjectiveObjects G hG
  leftAdjoint_adjunction := leftAdjoint_adjunction G
  leftAdjoint_preservesFiniteLimits := leftAdjoint_preservesFiniteLimits G hG
  embedding_isRightAdjoint := inferInstance
  leftAdjoint_isLeftAdjoint := inferInstance

/-- The normalized Stage1 statement shape is closed by pinned mathlib. -/
theorem statementShape : StatementShape (C := C) := by
  intro G hG
  exact ⟨gabrielPopescuEmbeddingData G hG⟩

/-- A compact theorem-form wrapper for downstream importers. -/
theorem gabrielPopescu_full_faithful_exactLeftAdjoint (G : C) (hG : IsSeparator G) :
    (gabrielPopescuEmbedding G).Full ∧
      (gabrielPopescuEmbedding G).Faithful ∧
      PreservesFiniteLimits (gabrielPopescuLeftAdjoint G) := by
  exact ⟨embedding_full G hG, embedding_faithful G hG, leftAdjoint_preservesFiniteLimits G hG⟩

/-- mathlib modules checked for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu",
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.Basic",
  "Mathlib.CategoryTheory.Generator.Preadditive",
  "Mathlib.CategoryTheory.Abelian.Yoneda",
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.Opposite",
  "Mathlib.Algebra.Category.ModuleCat.AB"
]

/-- Pinned theorem and definition names used by the local wrapper. -/
def mathlibAnchorNames : List String := [
  "CategoryTheory.IsGrothendieckAbelian",
  "CategoryTheory.IsGrothendieckAbelian.tensorObj",
  "CategoryTheory.IsGrothendieckAbelian.tensorObjPreadditiveCoyonedaObjAdjunction",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.full",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.preservesInjectiveObjects",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits",
  "CategoryTheory.isSeparator_iff_faithful_preadditiveCoyonedaObj",
  "CategoryTheory.preadditiveCoyonedaObj"
]

/-- Primary machine anchors for the embedding formulation requested by Stage1. -/
def primaryMachineAnchorNames : List String := [
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.full",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits"
]

/--
Machine-audit leaves for the upstream proof of
`CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.full`.

These are proof-tree metadata, not replacement proofs.  Each leaf points to a
specific source-level step in the pinned mathlib proof and is small enough for a
public `<=100`-step audit expansion.
-/
def gabrielPopescuFullAuditLeaves : List String := [
  "GP-full-01 context: fix A B in C and a module morphism f : Hom(G,A) -> Hom(G,B).",
  "GP-full-02 separator-epi: use (isSeparator_iff_epi G).1 hG A to make d (1_Hom(G,A)) an epimorphism.",
  "GP-full-03 kernel-vanishing: apply GabrielPopescuAux.kernel_ι_d_comp_d hG (1_Hom(G,A)) inferInstance f.",
  "GP-full-04 identity-simplification: simplify ModuleCat.hom_id, LinearMap.id_coe, id_eq, and GabrielPopescuAux.d in the kernel-vanishing result.",
  "GP-full-05 epi-desc-construction: define the candidate lift A -> B by epiDesc along the epimorphism d (1_Hom(G,A)).",
  "GP-full-06 map-check: ext on q : Hom(G,A) and use comp_epiDesc with Sigma.ι to show Hom(G,lift) = f.",
  "GP-full-07 full-instance: package GP-full-01 through GP-full-06 as the map_surjective field of (preadditiveCoyonedaObj G).Full.",
  "GP-full-08 local-wrapper: expose the same map_surjective field as AwesomeTheorems.Stage1.S1_M_133.embedding_full_map_surjective."
]

/--
Primary upstream source dependencies for the `GabrielPopescu.full` proof tree.
-/
def gabrielPopescuFullAuditAnchors : List String := [
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescuAux.d",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescuAux.ι_d",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescuAux.kernel_ι_d_comp_d",
  "CategoryTheory.isSeparator_iff_epi",
  "CategoryTheory.Limits.epiDesc",
  "CategoryTheory.Limits.comp_epiDesc",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.full",
  "AwesomeTheorems.Stage1.S1_M_133.embedding_full",
  "AwesomeTheorems.Stage1.S1_M_133.embedding_full_map_surjective"
]

/--
Machine-audit leaves for the upstream proof of
`CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.preservesInjectiveObjects`.

These leaves follow the pinned mathlib proof body.  They are metadata for a
public audit expansion and do not replace the checked upstream proof.
-/
def gabrielPopescuPreservesInjectiveObjectsAuditLeaves : List String := [
  "GP-inj-01 class-field: build (preadditiveCoyonedaObj G).PreservesInjectiveObjects by proving the injective_obj field.",
  "GP-inj-02 object-context: fix B : C and hB : Injective B, then target injectivity of Hom(G,B) as a ModuleCat object.",
  "GP-inj-03 module-translation: rewrite the category-theoretic injective-object target by Module.injective_iff_injective_object.",
  "GP-inj-04 carrier-normalization: simplify preadditiveCoyonedaObj_obj_carrier so the target is ordinary module injectivity for Hom(G,B).",
  "GP-inj-05 Baer-reduction: apply Module.Baer.injective, reducing injectivity to extending every map g from a left ideal/submodule M.",
  "GP-inj-06 canonical-map: form the Gabriel-Popescu auxiliary map from M to Hom(G,A) by ModuleCat.ofHom and the unop endomorphism action.",
  "GP-inj-07 mono-check: prove the canonical map is a monomorphism by rewriting with ModuleCat.mono_iff_injective and closing the linear injectivity goal by cat_disch.",
  "GP-inj-08 extension-existence: invoke GabrielPopescuAux.exists_d_comp_eq_d hG B on the canonical mono and the map ModuleCat.ofHom g.",
  "GP-inj-09 factor-map: obtain l : A -> B and the identity d canonical_map ≫ l = d (ModuleCat.ofHom g).",
  "GP-inj-10 Baer-extension: define the module extension by Hom(G,l) composed with (Preadditive.homSelfLinearEquivEndMulOpposite G).symm.toLinearMap.",
  "GP-inj-11 restriction-check: for f in M, prove the extension restricts to g f using Sigma.ι _ <f,hf> whiskered into the identity from GP-inj-09.",
  "GP-inj-12 simplification-close: simplify GabrielPopescuAux.d and the preadditive coyoneda action to close the Baer extension equality.",
  "GP-inj-13 package-field: package GP-inj-02 through GP-inj-12 as the injective_obj field of PreservesInjectiveObjects.",
  "GP-inj-14 local-wrapper: expose the branch as AwesomeTheorems.Stage1.S1_M_133.embedding_preservesInjectiveObjects."
]

/--
Primary upstream source dependencies for the
`GabrielPopescu.preservesInjectiveObjects` proof tree.
-/
def gabrielPopescuPreservesInjectiveObjectsAuditAnchors : List String := [
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu",
  "CategoryTheory.Functor.PreservesInjectiveObjects",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescuAux.d",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescuAux.exists_d_comp_eq_d",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.preservesInjectiveObjects",
  "Mathlib.Algebra.Category.ModuleCat.Injective",
  "Module.injective_iff_injective_object",
  "Module.Baer.injective",
  "CategoryTheory.preadditiveCoyonedaObj_obj_carrier",
  "CategoryTheory.ModuleCat.ofHom",
  "CategoryTheory.ModuleCat.mono_iff_injective",
  "CategoryTheory.Preadditive.homSelfLinearEquivEndMulOpposite",
  "AwesomeTheorems.Stage1.S1_M_133.embedding_preservesInjectiveObjects"
]

/--
Machine-audit leaves for the upstream proof of
`CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits`.

These leaves follow the proof body in pinned mathlib.  The local wrapper checks
the terminal theorem and the intermediate homology-preservation step; the leaves
are metadata for public audit backfill.
-/
def gabrielPopescuPreservesFiniteLimitsAuditLeaves : List String := [
  "GP-finlim-01 theorem-context: fix G : C and hG : IsSeparator G; target PreservesFiniteLimits (tensorObj G).",
  "GP-finlim-02 injective-transfer: instantiate (preadditiveCoyonedaObj G).PreservesInjectiveObjects via GabrielPopescu.preservesInjectiveObjects G hG.",
  "GP-finlim-03 adjunction-input: use tensorObjPreadditiveCoyonedaObjAdjunction G as the adjunction tensorObj G ⊣ preadditiveCoyonedaObj G.",
  "GP-finlim-04 mono-preservation: apply Functor.preservesMonomorphisms_of_adjunction_of_preservesInjectiveObjects to prove (tensorObj G).PreservesMonomorphisms.",
  "GP-finlim-05 binary-biproducts: obtain PreservesBinaryBiproducts (tensorObj G) from left-adjoint preservation of binary coproducts via preservesBinaryBiproducts_of_preservesBinaryCoproducts.",
  "GP-finlim-06 additive-structure: derive (tensorObj G).Additive using Functor.additive_of_preservesBinaryBiproducts.",
  "GP-finlim-07 homology-preservation: combine mono preservation, additive structure, and cokernel preservation of the left adjoint through preservesHomology_of_preservesMonos_and_cokernels.",
  "GP-finlim-08 finite-limit-close: apply preservesFiniteLimits_of_preservesHomology to obtain PreservesFiniteLimits (tensorObj G).",
  "GP-finlim-09 local-terminal-wrapper: expose the terminal branch as AwesomeTheorems.Stage1.S1_M_133.leftAdjoint_preservesFiniteLimits.",
  "GP-finlim-10 local-homology-wrapper: expose the intermediate homology branch as AwesomeTheorems.Stage1.S1_M_133.leftAdjoint_preservesHomology."
]

/--
Primary upstream source dependencies for the
`GabrielPopescu.preservesFiniteLimits` proof tree.
-/
def gabrielPopescuPreservesFiniteLimitsAuditAnchors : List String := [
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.preservesInjectiveObjects",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits",
  "CategoryTheory.IsGrothendieckAbelian.tensorObj",
  "CategoryTheory.IsGrothendieckAbelian.tensorObjPreadditiveCoyonedaObjAdjunction",
  "CategoryTheory.Functor.preservesMonomorphisms_of_adjunction_of_preservesInjectiveObjects",
  "CategoryTheory.Limits.preservesBinaryBiproducts_of_preservesBinaryCoproducts",
  "CategoryTheory.Functor.additive_of_preservesBinaryBiproducts",
  "CategoryTheory.Functor.preservesHomology_of_preservesMonos_and_cokernels",
  "CategoryTheory.Functor.preservesFiniteLimits_of_preservesHomology",
  "AwesomeTheorems.Stage1.S1_M_133.leftAdjoint_preservesFiniteLimits",
  "AwesomeTheorems.Stage1.S1_M_133.leftAdjoint_preservesHomology"
]

/-- Public statement variants considered for THM-M-0087. -/
inductive PublicTargetStatement
  | exactLeftAdjointFullFaithfulEmbedding
  | explicitSerreQuotientCharacterization
  deriving DecidableEq, Repr

/--
Stage1 target-statement decision for THM-M-0087.

The checked repo-local theorem surface follows mathlib's stated
Gabriel-Popescu theorem: the `Hom(G, -)` functor is full and faithful and has
an exact left adjoint, represented here by finite-limit preservation of
`tensorObj G`.  The pinned mathlib source records the Serre quotient
characterization as an implication/future-work note rather than as the terminal
checked theorem, so the quotient formulation should remain a separate package
unless a later worker adds a checked quotient wrapper.
-/
def publicTargetStatementDecision : PublicTargetStatement :=
  .exactLeftAdjointFullFaithfulEmbedding

/--
Concrete integration boundary for the Serre quotient variant.

General Serre-class localization APIs exist in mathlib, but this Stage1 slot has
not checked a theorem identifying `C` as a Serre quotient of
`ModuleCat (End G)ᵐᵒᵖ`; that work should be tracked separately if the public
statement is broadened.
-/
def serreQuotientIntegrationBoundary : List String := [
  "Mathlib.CategoryTheory.Abelian.SerreClass.Localization",
  "Mathlib.CategoryTheory.Abelian.SerreClass.Bousfield",
  "CategoryTheory.Abelian.isLocalization_isoModSerre_kernel_of_leftAdjoint",
  "conditional bridge: tensorObj G is a Serre-class localization once finite-colimit preservation is available as an instance",
  "no checked Gabriel-Popescu Serre quotient characterization in this wrapper"
]

/--
Generic checked API package for a localization by a Serre class.

This is not yet the Gabriel-Popescu quotient theorem.  It records that the
mathlib Serre-class localization surface needed by a future quotient child is
available in the local dependency closure.
-/
structure SerreLocalizationApiData
    {A : Type u} [Category.{v} A] [Abelian A]
    {B : Type u'} [Category.{v'} B]
    (L : A ⥤ B) (P : ObjectProperty A) [P.IsSerreClass]
    [L.IsLocalization P.isoModSerre] [Preadditive B] [L.Additive] where
  localizedAbelian : Abelian B
  localizationPreservesFiniteLimits : PreservesFiniteLimits L
  localizationPreservesFiniteColimits : PreservesFiniteColimits L

/-- Checked wrapper around the core Serre-class localization API. -/
def serreLocalizationApiData
    {A : Type u} [Category.{v} A] [Abelian A]
    {B : Type u'} [Category.{v'} B]
    (L : A ⥤ B) (P : ObjectProperty A) [P.IsSerreClass]
    [L.IsLocalization P.isoModSerre] [Preadditive B] [L.Additive] :
    SerreLocalizationApiData L P where
  localizedAbelian := ObjectProperty.SerreClassLocalization.abelian L P
  localizationPreservesFiniteLimits :=
    ObjectProperty.SerreClassLocalization.preservesFiniteLimits L P
  localizationPreservesFiniteColimits :=
    ObjectProperty.SerreClassLocalization.preservesFiniteColimits L P

/--
Checked exact-functor transport API for a localization by a Serre class.
-/
theorem serreLocalization_exactFunctor_comp_iff
    {A : Type u} [Category.{v} A] [Abelian A]
    {B : Type u'} [Category.{v'} B]
    (L : A ⥤ B) (P : ObjectProperty A) [P.IsSerreClass]
    [L.IsLocalization P.isoModSerre] [Preadditive B] [L.Additive]
    {E : Type u''} [Category.{v''} E] [Abelian E] (H : B ⥤ E) :
    exactFunctor A E (L ⋙ H) ↔ exactFunctor B E H := by
  exact ObjectProperty.SerreClassLocalization.exactFunctor_comp_iff L P H

/--
Conditional bridge from the Gabriel-Popescu embedding package to a Serre-class
localization statement.

The bridge is intentionally conditional on finite-colimit preservation being
available as an instance for the left adjoint.  The current local wrapper checks
finite-limit preservation via `GabrielPopescu.preservesFiniteLimits`; it does
not claim a terminal explicit equivalence with a named Serre quotient category.
-/
theorem gabrielPopescuLeftAdjoint_isSerreLocalization_of_exact
    (G : C) (hG : IsSeparator G)
    [PreservesFiniteLimits (gabrielPopescuLeftAdjoint G)]
    [PreservesFiniteColimits (gabrielPopescuLeftAdjoint G)] :
    (gabrielPopescuLeftAdjoint G).IsLocalization
      (gabrielPopescuLeftAdjoint G).kernel.isoModSerre := by
  haveI : (gabrielPopescuEmbedding G).Full := embedding_full G hG
  haveI : (gabrielPopescuEmbedding G).Faithful := embedding_faithful G hG
  exact Abelian.isLocalization_isoModSerre_kernel_of_leftAdjoint
    (leftAdjoint_adjunction G)

/-- Serre-class localization API anchors audited for the quotient child branch. -/
def serreQuotientApiAnchorNames : List String := [
  "CategoryTheory.ObjectProperty.isoModSerre",
  "CategoryTheory.ObjectProperty.SerreClassLocalization.abelian",
  "CategoryTheory.ObjectProperty.SerreClassLocalization.preservesFiniteLimits",
  "CategoryTheory.ObjectProperty.SerreClassLocalization.preservesFiniteColimits",
  "CategoryTheory.ObjectProperty.SerreClassLocalization.exactFunctor_comp_iff",
  "CategoryTheory.Abelian.isoModSerre_kernel_eq_inverseImage_isomorphisms",
  "CategoryTheory.Abelian.isLocalization_isoModSerre_kernel_of_leftAdjoint",
  "AwesomeTheorems.Stage1.S1_M_133.gabrielPopescuLeftAdjoint_isSerreLocalization_of_exact"
]

/--
Search terms audited while checking for alternative or quotient-form terminal
statements around the Gabriel-Popescu theorem.
-/
def anchorSearchTerms : List String := [
  "GabrielPopescu",
  "Gabriel-Popescu",
  "Popesco",
  "IsGrothendieckAbelian",
  "preadditiveCoyonedaObj",
  "Serre quotient",
  "SerreClass.Localization",
  "ModuleEmbedding"
]

end S1_M_133
end Stage1
end AwesomeTheorems
