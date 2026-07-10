import Mathlib.CategoryTheory.Yoneda

/-!
# S1-M-137 / THM-M-0088: Yoneda embedding

This Stage1 file records the Lean 4/mathlib closure point for the category-level
statement that a category embeds fully faithfully into its presheaf category.

The proof body is supplied by the pinned mathlib theorem
`CategoryTheory.Yoneda.fullyFaithful`.  The declarations below are repo-local
wrappers and statement-shape checks; they do not introduce any proof
placeholders.
-/

noncomputable section

open CategoryTheory Opposite

universe w v u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_137

/--
Stage1 statement shape for the Yoneda embedding.

For any category `C`, the functor `yoneda : C ⥤ Cᵒᵖ ⥤ Type v` is fully
faithful, so `C` embeds in its presheaf category.
-/
def StatementShape (C : Type u) [Category.{v} C] : Prop :=
  Nonempty ((yoneda (C := C)).FullyFaithful)

/-- Checked repo-local wrapper for the mathlib Yoneda embedding data. -/
def yoneda_embedding_fullyFaithful (C : Type u) [Category.{v} C] :
    (yoneda (C := C)).FullyFaithful :=
  Yoneda.fullyFaithful

/-- The pinned mathlib revision used for the primary Yoneda proof body. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- The pinned mathlib source file containing the primary category-level proof body. -/
def primaryLeanProofBodySource : String :=
  "Mathlib/CategoryTheory/Yoneda.lean"

/-- The mathlib declaration used as the primary proof body for the core theorem. -/
def primaryLeanProofBodyName : String :=
  "CategoryTheory.Yoneda.fullyFaithful"

/-- The repo-local checked wrapper is definitionally the pinned mathlib proof body. -/
theorem primaryLeanProofBody_matches_wrapper (C : Type u) [Category.{v} C] :
    yoneda_embedding_fullyFaithful C = Yoneda.fullyFaithful :=
  rfl

/-- The normalized statement shape is closed by the pinned mathlib theorem. -/
theorem statementShape (C : Type u) [Category.{v} C] :
    StatementShape C :=
  ⟨yoneda_embedding_fullyFaithful C⟩

/-- Fullness of the Yoneda embedding, exposed as a low-risk wrapper. -/
theorem yoneda_embedding_full (C : Type u) [Category.{v} C] :
    (yoneda (C := C)).Full := by
  infer_instance

/-- Faithfulness of the Yoneda embedding, exposed as a low-risk wrapper. -/
theorem yoneda_embedding_faithful (C : Type u) [Category.{v} C] :
    (yoneda (C := C)).Faithful := by
  infer_instance

/--
The hom-set equivalence induced by the fully faithful Yoneda embedding.

This is the concrete categorical sense in which the embedding preserves and
reflects morphisms.
-/
def yonedaHomEquiv {C : Type u} [Category.{v} C] (X Y : C) :
    (X ⟶ Y) ≃ (yoneda.obj X ⟶ yoneda.obj Y) :=
  (Yoneda.fullyFaithful (C := C)).homEquiv

/-- The preimage of a natural transformation under the Yoneda embedding. -/
theorem yoneda_fullyFaithful_preimage {C : Type u} [Category.{v} C]
    {X Y : C} (f : yoneda.obj X ⟶ yoneda.obj Y) :
    (Yoneda.fullyFaithful (C := C)).preimage f = f.app (op X) (𝟙 X) :=
  Yoneda.fullyFaithful_preimage f

/-- Naturality square for a natural transformation between representable presheaves. -/
theorem yoneda_naturality_square {C : Type u} [Category.{v} C]
    {X Y Z Z' : C} (α : yoneda.obj X ⟶ yoneda.obj Y) (f : Z ⟶ Z')
    (h : Z' ⟶ X) :
    f ≫ α.app (op Z') h = α.app (op Z) (f ≫ h) :=
  Yoneda.naturality α f h

/-- The Yoneda lemma as the natural isomorphism exposed by mathlib. -/
def yonedaLemmaIso (C : Type u) [Category.{v} C] :
    yonedaPairing C ≅ yonedaEvaluation C :=
  yonedaLemma C

/-- The element-level Yoneda equivalence used by the natural-isomorphism form. -/
def yonedaElementEquiv {C : Type u} [Category.{v} C]
    {X : C} {F : Cᵒᵖ ⥤ Type v} :
    (yoneda.obj X ⟶ F) ≃ F.obj (op X) :=
  yonedaEquiv

/-- Universe-raised Yoneda embedding wrapper, useful for later presheaf-size integration. -/
def uliftYoneda_embedding_fullyFaithful (C : Type u) [Category.{v} C] :
    (uliftYoneda.{w} (C := C)).FullyFaithful :=
  ULiftYoneda.fullyFaithful C

/-- The co-Yoneda embedding has the corresponding fully faithful wrapper. -/
def coyoneda_embedding_fullyFaithful (C : Type u) [Category.{v} C] :
    (coyoneda (C := C)).FullyFaithful :=
  Coyoneda.fullyFaithful

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Yoneda",
  "Mathlib.CategoryTheory.Functor.FullyFaithful",
  "Mathlib.CategoryTheory.Functor.Hom",
  "Mathlib.CategoryTheory.Products.Basic",
  "Mathlib.CategoryTheory.Elements",
  "Mathlib.CategoryTheory.ShrinkYoneda",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Basic",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Limits",
  "Mathlib.CategoryTheory.Triangulated.Pretriangulated"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "CategoryTheory.yoneda",
  "CategoryTheory.uliftYoneda",
  "CategoryTheory.coyoneda",
  "CategoryTheory.Yoneda.fullyFaithful",
  "CategoryTheory.Yoneda.yoneda_full",
  "CategoryTheory.Yoneda.yoneda_faithful",
  "CategoryTheory.Yoneda.naturality",
  "CategoryTheory.yonedaEquiv",
  "CategoryTheory.yonedaLemma",
  "CategoryTheory.ULiftYoneda.fullyFaithful",
  "CategoryTheory.Coyoneda.fullyFaithful"
]

/-- Search terms used while checking for exactness and derived-category collateral APIs. -/
def collateralSearchTerms : List String := [
  "preadditiveYoneda",
  "yoneda_exact",
  "coyoneda_exact",
  "preservesHomology_preadditiveYoneda",
  "short exact",
  "long exact",
  "derived",
  "spectral sequence"
]

/--
Decision recorded for child task `S1-M-137-C004`.

The core Stage1 theorem is the category-level fully faithful Yoneda embedding.
Homological exactness, triangulated homological-functor facts, and
long-exact-sequence consequences should be split into separate child theorem
tasks unless a later public integrator freezes an exact non-core target
statement.
-/
def homologicalCollateralDecision : String :=
  "split_into_separate_child_theorem_tasks"

/--
Decision recorded for child task `S1-M-137-C005`.

Triangulated and pretriangulated Yoneda-exactness wrappers are not part of the
core Yoneda embedding package.  They should only be added in separate child
theorem tasks after exact target statements have been frozen.
-/
def triangulatedCollateralWrapperPolicy : String :=
  "do_not_add_wrappers_until_split_task_targets_are_frozen"

/--
The current core `S1-M-137` package does not retain homological collateral
under the category-level Yoneda embedding theorem.
-/
def homologicalCollateralStaysUnderCore : Bool :=
  false

/--
No `Mathlib.CategoryTheory.Triangulated.*` wrapper target is frozen for this
core file as of the `S1-M-137-C005` child pass.
-/
def triangulatedWrapperTargetsFrozen : Bool :=
  false

/--
Local wrapper reconciliation state for child task `S1-M-137-C006`.

The core category-level wrapper is checked in this file, but the shared public
blueprint/todo surfaces are not edited by child workers.  Public completion is
therefore gated on a later serial merge-back.
-/
def publicBlueprintTodoSurfacesReconciled : Bool :=
  false

/--
The local Lean artifact scopes the homological and long-exact-sequence
collateral as non-core split-task material.
-/
def localUncheckedCollateralScopedNonCore : Bool :=
  true

/-- Public completion is allowed only after public reconciliation and scoping. -/
def publicCompletionGateSatisfied : Bool :=
  publicBlueprintTodoSurfacesReconciled && localUncheckedCollateralScopedNonCore

/--
As of child task `S1-M-137-C006`, the public status must remain below completed.
-/
theorem publicCompletionGateSatisfied_eq_false :
    publicCompletionGateSatisfied = false :=
  rfl

/-- Checked machine packages that belong to the core Yoneda embedding wrapper. -/
def coreYonedaEmbeddingPackages : List String := [
  "P1.statement_normalization_and_universe_freeze",
  "P2.core_mathlib_anchor_CategoryTheory.Yoneda.fullyFaithful",
  "P3.full_and_faithful_projections",
  "P4.hom_set_equivalence_and_preimage_formula",
  "P5.naturality_and_Yoneda_lemma_collateral",
  "P6.universe_raised_and_dual_variants"
]

/-- Non-core collateral packages that should become separate theorem tasks. -/
def separateHomologicalCollateralPackages : List String := [
  "P7.preadditive_Yoneda_exactness",
  "P8.triangulated_Yoneda_exactness",
  "P9.derived_and_long_exact_sequence_bridge"
]

/--
Pinned mathlib modules that provide plausible anchors for the separated
homological collateral; these are not imported by the core wrapper.
-/
def separatedHomologicalAnchorModules : List String := [
  "Mathlib.CategoryTheory.Triangulated.Yoneda",
  "Mathlib.CategoryTheory.Triangulated.Pretriangulated",
  "Mathlib.CategoryTheory.Triangulated.HomologicalFunctor",
  "Mathlib.Algebra.Homology.HomologySequence",
  "Mathlib.Algebra.Homology.DerivedCategory.HomologySequence"
]

/-- Pinned mathlib declaration names audited as candidates for the split tasks. -/
def separatedHomologicalAnchorNames : List String := [
  "CategoryTheory.Pretriangulated.Triangle.yoneda_exact₂",
  "CategoryTheory.Pretriangulated.Triangle.yoneda_exact₃",
  "CategoryTheory.Pretriangulated.Triangle.coyoneda_exact₁",
  "CategoryTheory.Pretriangulated.Triangle.coyoneda_exact₂",
  "CategoryTheory.Pretriangulated.Triangle.coyoneda_exact₃",
  "CategoryTheory.Pretriangulated.preadditiveYoneda_map_distinguished",
  "CategoryTheory.Functor.homologySequenceδ",
  "CategoryTheory.Functor.homologySequence_exact₁",
  "CategoryTheory.Functor.homologySequence_exact₂",
  "CategoryTheory.Functor.homologySequence_exact₃"
]

end S1_M_137
end Stage1
end AwesomeTheorems
