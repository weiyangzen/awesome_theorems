import Mathlib.Algebra.Homology.HomologySequenceLemmas
import Mathlib.Algebra.Module.SnakeLemma

/-!
# S1-M-098 / THM-M-0003: Snake lemma

This Stage1 artifact records checked wrappers around the pinned mathlib snake
lemma APIs. It deliberately avoids adding new proof obligations beyond the
available Lean 4 proof bodies in mathlib.
-/

noncomputable section

open CategoryTheory Category Limits

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_098

/-- Audit identifier for this Stage1 theorem. -/
def theoremUID : String := "THM-M-0003"

/-- Public Lean artifact path for serialized blueprint/todo backfill. -/
def publicLeanArtifactPath : String :=
  "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_098.lean"

/-- Required repo-local validation command for this checked artifact. -/
def localValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_098.lean"

/-- Current repo-local machine state for the checked wrapper package. -/
def machineProofStatus : String :=
  "local_wrapper_upstream_mathlib"

/--
Current machine-proof debt classification for the checked wrapper package.

The proof bodies are supplied by pinned mathlib and this module checks local
wrappers against that dependency.
-/
def machineProofDebt : String :=
  "none_for_checked_mathlib_wrapper"

/-- This checked artifact retains no repo-local integration debt. -/
def repoLocalIntegrationDebtRetained : Bool := false

/-- Repo-local integration-debt gate result for the mathlib-backed wrapper. -/
def repoLocalIntegrationDebtGate : String :=
  "passed_no_residual_repo_local_integration_debt"

/--
Public completion remains pending until serialized blueprint/todo synchronization
records this local wrapper and its validation result.
-/
def publicCompletionPending : Bool := true

/-- Reason the public Stage1 queue item is not marked completed by this artifact alone. -/
def publicCompletionPendingReason : String :=
  "public_surface_synchronization_pending"

/-- This module should be added to the shared Lean aggregator by a serialized patch. -/
def sharedImportAggregatorPatchRecommended : Bool := true

/-- Shared Lean aggregator target for the later serialized integration patch. -/
def sharedImportAggregatorTarget : String :=
  "Formalizations/Lean/AwesomeTheorems.lean"

/-- Exact import line for the later serialized aggregator patch. -/
def sharedImportAggregatorImportLine : String :=
  "import AwesomeTheorems.Stage1.S1_M_098"

/-- Reason the aggregator edit is deferred from this parallel child pass. -/
def sharedImportAggregatorDecisionReason : String :=
  "shared_import_aggregator_requires_serialized_integration_patch"

/-- Category-level statement shape for the snake lemma in an abelian category. -/
def CategorySnakeLemmaStatement (C : Type u) [Category.{v} C] [Abelian C] : Prop :=
  ∀ S : ShortComplex.SnakeInput C, S.composableArrows.Exact

/-- Checked wrapper around `ShortComplex.SnakeInput.snake_lemma`. -/
theorem categorySnakeLemmaStatement
    (C : Type u) [Category.{v} C] [Abelian C] : CategorySnakeLemmaStatement C := by
  intro S
  exact S.snake_lemma

/-- The six-term exact sequence attached to one snake input. -/
theorem snakeInput_exact_sequence
    {C : Type u} [Category.{v} C] [Abelian C] (S : ShortComplex.SnakeInput C) :
    S.composableArrows.Exact :=
  S.snake_lemma

/-- The connecting morphism is natural with respect to morphisms of snake inputs. -/
theorem snakeInput_delta_naturality
    {C : Type u} [Category.{v} C] [Abelian C]
    {S₁ S₂ : ShortComplex.SnakeInput C} (f : S₁ ⟶ S₂) :
    S₁.δ ≫ f.f₃.τ₁ = f.f₀.τ₃ ≫ S₂.δ :=
  ShortComplex.SnakeInput.naturality_δ f

/-- Statement shape for the long exact homology sequence induced by a short exact sequence. -/
def HomologyLongExactStatement
    (C : Type u) [Category.{v} C] [Abelian C] {ι : Type w} (c : ComplexShape ι) : Prop :=
  ∀ (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact)
    (i j : ι) (hij : c.Rel i j),
      (HomologicalComplex.HomologySequence.composableArrows₅ hS i j hij).Exact

/-- Checked wrapper around the mathlib long exact homology-sequence exactness theorem. -/
theorem homologyLongExactStatement
    (C : Type u) [Category.{v} C] [Abelian C] {ι : Type w} (c : ComplexShape ι) :
    HomologyLongExactStatement C c := by
  intro S hS i j hij
  exact HomologicalComplex.HomologySequence.composableArrows₅_exact hS i j hij

/-- The naturality square for the connecting morphism in the long exact homology sequence. -/
theorem homologyConnecting_naturality
    {C : Type u} [Category.{v} C] [Abelian C] {ι : Type w} {c : ComplexShape ι}
    {S₁ S₂ : ShortComplex (HomologicalComplex C c)}
    (φ : S₁ ⟶ S₂) (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (i j : ι) (hij : c.Rel i j) :
    hS₁.δ i j hij ≫ HomologicalComplex.homologyMap φ.τ₁ _ =
      HomologicalComplex.homologyMap φ.τ₃ _ ≫ hS₂.δ i j hij :=
  HomologicalComplex.HomologySequence.δ_naturality φ hS₁ hS₂ i j hij

/-- A compact Stage1 statement shape combining the checked category and homology-sequence APIs. -/
def StatementShape : Prop :=
  (∀ (C : Type u) [Category.{v} C] [Abelian C], CategorySnakeLemmaStatement C) ∧
  (∀ (C : Type u) [Category.{v} C] [Abelian C]
    {ι : Type w} (c : ComplexShape ι), HomologyLongExactStatement C c)

/-- The combined statement shape is satisfied by the pinned mathlib wrappers above. -/
theorem statementShape_checked : StatementShape.{u, v, w} := by
  constructor
  · intro C _ _
    exact categorySnakeLemmaStatement C
  · intro C _ _ ι c
    exact homologyLongExactStatement C c

/-- mathlib modules checked for the repo-local snake-lemma anchor. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Source files in the pinned mathlib revision that contain the audited anchors. -/
def mathlibAnchorSourceFiles : List String := [
  "Mathlib/Algebra/Homology/ShortComplex/SnakeLemma.lean",
  "Mathlib/Algebra/Homology/HomologySequence.lean",
  "Mathlib/Algebra/Homology/HomologySequenceLemmas.lean",
  "Mathlib/Algebra/Module/SnakeLemma.lean"
]

/-- mathlib modules checked for the repo-local snake-lemma anchor. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Homology.ShortComplex.SnakeLemma",
  "Mathlib.Algebra.Homology.HomologySequence",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas",
  "Mathlib.Algebra.Module.SnakeLemma",
  "Mathlib.CategoryTheory.Abelian.DiagramLemmas.KernelCokernelComp",
  "Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four",
  "Mathlib.CategoryTheory.Abelian.Pseudoelements"
]

/-- Principal theorem and definition names used by this Stage1 wrapper. -/
def mathlibAnchorNames : List String := [
  "ShortComplex.SnakeInput",
  "ShortComplex.SnakeInput.δ",
  "ShortComplex.SnakeInput.snake_lemma",
  "ShortComplex.SnakeInput.naturality_δ",
  "ShortComplex.SnakeInput.mono_δ",
  "ShortComplex.SnakeInput.epi_δ",
  "ShortComplex.SnakeInput.δIso",
  "HomologicalComplex.HomologySequence.snakeInput",
  "HomologicalComplex.HomologySequence.composableArrows₅_exact",
  "HomologicalComplex.HomologySequence.δ_naturality",
  "SnakeLemma.δ",
  "SnakeLemma.δ'",
  "SnakeLemma.exact_δ_left",
  "SnakeLemma.exact_δ_right",
  "SnakeLemma.exact_δ'_left",
  "SnakeLemma.exact_δ'_right"
]

/-- Search terms used to distinguish the checked anchors from absent or broader APIs. -/
def anchorAuditSearchTerms : List String := [
  "SnakeInput",
  "snake_lemma",
  "naturality_δ",
  "HomologySequence.composableArrows₅_exact",
  "SnakeLemma.exact_δ'_left",
  "long exact sequence",
  "short exact sequence"
]

/--
Machine-checkable metadata row for the theorem-tree leaf budget that should be
backfilled into the serialized public Stage1 queue.
-/
structure TheoremTreeLeaf where
  leafId : String
  packageId : String
  description : String
  localStepBudget : Nat
  machineStatus : String
  publicBackfillStatus : String

/--
The A1-E2 theorem-tree leaves for the snake-lemma Stage1 wrapper.

Leaves A1-D2 are closed by the local mathlib-backed wrapper and source audit.
Leaves E1-E2 are intentionally public-integration leaves and must be resolved by
the serialized integrator patch that edits the public blueprint/todo surfaces.
-/
def theoremTreeLeaves : List TheoremTreeLeaf := [
  {
    leafId := "A1",
    packageId := "A",
    description := "Identify category-level formal object `ShortComplex.SnakeInput C`.",
    localStepBudget := 6,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "A2",
    packageId := "A",
    description :=
      "Identify long exact homology object `HomologicalComplex.HomologySequence.composableArrows₅`.",
    localStepBudget := 8,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "A3",
    packageId := "A",
    description := "Normalize universes, category assumptions, complex shape, indices, and exactness.",
    localStepBudget := 10,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "B1",
    packageId := "B",
    description := "Audit `Mathlib.Algebra.Homology.ShortComplex.SnakeLemma`.",
    localStepBudget := 12,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "B2",
    packageId := "B",
    description := "Audit connecting morphism `ShortComplex.SnakeInput.δ`.",
    localStepBudget := 7,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "B3",
    packageId := "B",
    description := "Audit exactness theorem `ShortComplex.SnakeInput.snake_lemma`.",
    localStepBudget := 8,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "B4",
    packageId := "B",
    description :=
      "Audit homology-sequence exactness theorem `HomologicalComplex.HomologySequence.composableArrows₅_exact`.",
    localStepBudget := 10,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "B5",
    packageId := "B",
    description :=
      "Audit naturality theorem `HomologicalComplex.HomologySequence.δ_naturality`.",
    localStepBudget := 8,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "C1",
    packageId := "C",
    description := "Prove repo wrapper `categorySnakeLemmaStatement`.",
    localStepBudget := 4,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "C2",
    packageId := "C",
    description := "Prove repo wrapper `snakeInput_exact_sequence`.",
    localStepBudget := 3,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "C3",
    packageId := "C",
    description := "Prove repo wrapper `snakeInput_delta_naturality`.",
    localStepBudget := 3,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "C4",
    packageId := "C",
    description := "Prove repo wrapper `homologyLongExactStatement`.",
    localStepBudget := 5,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "C5",
    packageId := "C",
    description := "Prove repo wrapper `homologyConnecting_naturality`.",
    localStepBudget := 5,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "C6",
    packageId := "C",
    description := "Prove combined `statementShape_checked`.",
    localStepBudget := 6,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "D1",
    packageId := "D",
    description := "Audit module-level `SnakeLemma.δ` and `SnakeLemma.δ'`.",
    localStepBudget := 9,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "D2",
    packageId := "D",
    description := "Audit module-level exactness lemmas around the connecting homomorphism.",
    localStepBudget := 9,
    machineStatus := "checked",
    publicBackfillStatus := "ready_for_public_backfill"
  },
  {
    leafId := "E1",
    packageId := "E",
    description := "Merge this audit into public Stage1 blueprint/todo surfaces.",
    localStepBudget := 20,
    machineStatus := "integration_leaf_unchecked",
    publicBackfillStatus := "resolve_in_serialized_integrator_patch"
  },
  {
    leafId := "E2",
    packageId := "E",
    description := "Update public queue status only after surface and validation records synchronize.",
    localStepBudget := 15,
    machineStatus := "integration_leaf_unchecked",
    publicBackfillStatus := "resolve_in_serialized_integrator_patch"
  }
]

/-- Leaves that remain unchecked until the later serialized public-doc integrator patch. -/
def publicIntegratorLeafIds : List String := ["E1", "E2"]

end S1_M_098
end Stage1
end AwesomeTheorems
