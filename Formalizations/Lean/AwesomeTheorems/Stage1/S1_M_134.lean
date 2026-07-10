import Mathlib.CategoryTheory.Abelian.FreydMitchell
import Mathlib.CategoryTheory.Generator.Abelian

/-!
# S1-M-134 / THM-M-0086: Freyd theorem

This Stage1 artifact records repo-local Lean 4 wrappers for the mathlib
Freyd-Mitchell embedding theorem and the adjacent Freyd generator/cogenerator
existence results available in the pinned mathlib snapshot.

The terminal embedding theorem is already present in mathlib as
`CategoryTheory.Abelian.freyd_mitchell`.  The generator branch is represented by
`CategoryTheory.Abelian.has_injective_coseparator` and
`CategoryTheory.Abelian.has_projective_separator`.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits
open CategoryTheory.Abelian

universe v u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_134

variable (C : Type u) [Category.{v} C] [Abelian C]

/-! ## Machine anchor metadata -/

/-- The pinned mathlib revision audited for this Stage1 Freyd-theorem wrapper. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Repo-local validation command for this wrapper artifact. -/
def localWrapperValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_134.lean"

/--
The Freyd-Mitchell embedding theorem in the form used by this Stage1 slot.

An abelian category embeds fully, faithfully, and exactly into a module
category over a ring.  In mathlib the exactness side is expressed by
preservation of finite limits and finite colimits.
-/
def FreydMitchellEmbeddingStatement : Prop :=
  ∃ (R : Type (max u v)) (_ : Ring R) (F : C ⥤ ModuleCat.{max u v} R),
    F.Full ∧ F.Faithful ∧ PreservesFiniteLimits F ∧ PreservesFiniteColimits F

/--
Generator/cogenerator statement used by the Freyd-theorem audit branch.

If a complete abelian category has enough injectives and a separator, then it
has an injective coseparator.  Dually, if it is cocomplete with enough
projectives and a coseparator, then it has a projective separator.
-/
def GeneratorExistenceStatement : Prop :=
  (∀ [HasLimits C] [EnoughInjectives C] (G : C),
      IsSeparator G → ∃ I : C, Injective I ∧ IsCoseparator I) ∧
    (∀ [HasColimits C] [EnoughProjectives C] (G : C),
      IsCoseparator G → ∃ P : C, Projective P ∧ IsSeparator P)

/-- Combined normalized Stage1 statement shape for S1-M-134. -/
def StatementShape : Prop :=
  FreydMitchellEmbeddingStatement C ∧ GeneratorExistenceStatement C

/-- Checked wrapper around mathlib's Freyd-Mitchell embedding theorem. -/
theorem freydMitchellEmbeddingStatement_mathlib :
    FreydMitchellEmbeddingStatement C := by
  simpa [FreydMitchellEmbeddingStatement] using
    CategoryTheory.Abelian.freyd_mitchell C

/-! ## Exactness-language audit -/

/--
The exactness branch of mathlib's Freyd-Mitchell theorem, stated in the
language actually exposed by `CategoryTheory.Abelian.freyd_mitchell`.

The theorem does not use a separate public predicate named `Exact`; it packages
the exactness of the embedding as preservation of finite limits and finite
colimits.
-/
def FreydMitchellExactnessLanguageStatement : Prop :=
  ∃ (R : Type (max u v)) (_ : Ring R) (F : C ⥤ ModuleCat.{max u v} R),
    PreservesFiniteLimits F ∧ PreservesFiniteColimits F

/--
Checked projection of the exactness-language branch from the local
Freyd-Mitchell embedding wrapper.
-/
theorem freydMitchellExactnessLanguage_mathlib :
    FreydMitchellExactnessLanguageStatement C := by
  rcases freydMitchellEmbeddingStatement_mathlib C with
    ⟨R, ringR, F, _hFull, _hFaithful, hFiniteLimits, hFiniteColimits⟩
  exact ⟨R, ringR, F, hFiniteLimits, hFiniteColimits⟩

/-- The concrete ring selected by mathlib's Freyd-Mitchell construction. -/
abbrev EmbeddingRing : Type (max u v) :=
  CategoryTheory.Abelian.FreydMitchell.EmbeddingRing C

/-- The concrete functor selected by mathlib's Freyd-Mitchell construction. -/
abbrev embeddingFunctor : C ⥤ ModuleCat.{max u v} (EmbeddingRing C) :=
  CategoryTheory.Abelian.FreydMitchell.functor C

/-- Checked wrapper: the mathlib Freyd-Mitchell functor is full. -/
theorem embeddingFunctor_full : (embeddingFunctor C).Full := by
  infer_instance

/-- Checked wrapper: the mathlib Freyd-Mitchell functor is faithful. -/
theorem embeddingFunctor_faithful : (embeddingFunctor C).Faithful := by
  infer_instance

/-- Checked wrapper: the mathlib Freyd-Mitchell functor preserves finite limits. -/
theorem embeddingFunctor_preservesFiniteLimits :
    PreservesFiniteLimits (embeddingFunctor C) := by
  infer_instance

/-- Checked wrapper: the mathlib Freyd-Mitchell functor preserves finite colimits. -/
theorem embeddingFunctor_preservesFiniteColimits :
    PreservesFiniteColimits (embeddingFunctor C) := by
  infer_instance

/-- Checked wrapper around Freyd's injective-coseparator existence theorem. -/
theorem exists_injective_coseparator
    [HasLimits C] [EnoughInjectives C] (G : C) (hG : IsSeparator G) :
    ∃ I : C, Injective I ∧ IsCoseparator I := by
  exact CategoryTheory.Abelian.has_injective_coseparator G hG

/-- Checked wrapper around the dual projective-separator existence theorem. -/
theorem exists_projective_separator
    [HasColimits C] [EnoughProjectives C] (G : C) (hG : IsCoseparator G) :
    ∃ P : C, Projective P ∧ IsSeparator P := by
  exact CategoryTheory.Abelian.has_projective_separator G hG

/-- Checked wrapper for the generator/cogenerator branch of the statement shape. -/
theorem generatorExistenceStatement_mathlib :
    GeneratorExistenceStatement C := by
  constructor
  · intro _ _ G hG
    exact exists_injective_coseparator C G hG
  · intro _ _ G hG
    exact exists_projective_separator C G hG

/-- The combined Stage1 statement shape is closed by the pinned mathlib theorems. -/
theorem statementShape_mathlib : StatementShape C := by
  exact ⟨freydMitchellEmbeddingStatement_mathlib C, generatorExistenceStatement_mathlib C⟩

/-! ## Audit probes -/

#check CategoryTheory.Abelian.freyd_mitchell
#check CategoryTheory.Abelian.FreydMitchell.EmbeddingRing
#check CategoryTheory.Abelian.FreydMitchell.functor
#check CategoryTheory.Abelian.has_injective_coseparator
#check CategoryTheory.Abelian.has_projective_separator
#check CategoryTheory.ObjectProperty.IsSeparating
#check CategoryTheory.IsSeparator
#check CategoryTheory.IsCoseparator
#check CategoryTheory.Injective
#check CategoryTheory.Projective

/-- mathlib modules checked for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Abelian.FreydMitchell",
  "Mathlib.CategoryTheory.Generator.Abelian",
  "Mathlib.CategoryTheory.Generator.Basic",
  "Mathlib.CategoryTheory.Generator.Preadditive",
  "Mathlib.CategoryTheory.Generator.Indization",
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.Opposite",
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu",
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.EnoughInjectives",
  "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "CategoryTheory.Abelian.freyd_mitchell",
  "CategoryTheory.Abelian.FreydMitchell.EmbeddingRing",
  "CategoryTheory.Abelian.FreydMitchell.functor",
  "CategoryTheory.Abelian.has_injective_coseparator",
  "CategoryTheory.Abelian.has_projective_separator",
  "CategoryTheory.ObjectProperty.IsSeparating",
  "CategoryTheory.IsSeparator",
  "CategoryTheory.IsCoseparator",
  "CategoryTheory.IsGrothendieckAbelian.OppositeModuleEmbedding.embedding",
  "CategoryTheory.IsGrothendieckAbelian.GabrielPopescu.full"
]

/-! ## Theorem-tree backfill metadata -/

/-- Public proof-tree package metadata prepared for Stage1 backfill. -/
structure ProofTreePackage where
  id : String
  status : String
  summary : String

/-- Public leaf-budget metadata prepared for Stage1 backfill. -/
structure LeafBudgetEntry where
  id : String
  package : String
  target : String
  budget : String
  status : String

/-- Status-gate metadata prepared for serial public backfill. -/
structure StatusGateRecord where
  childId : String
  theoremId : String
  publicCompletionClaimed : String
  repoLocalIntegrationDebt : String
  gateResult : String
  integratorRequirement : String

/--
Integration-ready status-gate record for child `S1-M-134-C006`.

This worker-owned artifact does not edit the shared public status surfaces.  If
an integrator later claims public completion, the blueprint/todo/README or other
authoritative public status surfaces must be updated in the same serial patch.
-/
def statusGateRecord : StatusGateRecord := {
  childId := "S1-M-134-C006",
  theoremId := "THM-M-0086",
  publicCompletionClaimed := "no",
  repoLocalIntegrationDebt := "no for the checked local wrapper",
  gateResult := "local Lean wrapper checked; public completion gate remains open",
  integratorRequirement :=
    "Any public completion claim must update authoritative public status surfaces " ++
    "and state that no repo_local_integration_debt remains."
}

/--
Integration-ready public package split for the Stage1 Freyd theorem slot.

Packages `P0` through `P3` and the local validation gate in `P5` are represented
by checked declarations in this file.  Package `P4` is an upstream proof-path
audit over pinned mathlib internals and remains an unchecked public/process
backfill item here.
-/
def proofTreePackages : List ProofTreePackage := [
  {
    id := "M0086.P0.statement_normalization",
    status := "checked locally",
    summary :=
      "Freeze universes, category assumptions, module target universe, and exactness as " ++
      "PreservesFiniteLimits plus PreservesFiniteColimits."
  },
  {
    id := "M0086.P1.freyd_mitchell_embedding",
    status := "checked locally",
    summary :=
      "Wrap CategoryTheory.Abelian.freyd_mitchell, FreydMitchell.EmbeddingRing, and " ++
      "FreydMitchell.functor."
  },
  {
    id := "M0086.P2.embedding_properties",
    status := "checked locally",
    summary :=
      "Expose fullness, faithfulness, finite-limit preservation, and finite-colimit " ++
      "preservation for the canonical embedding functor."
  },
  {
    id := "M0086.P3.generator_cogenerator_branch",
    status := "checked locally",
    summary :=
      "Wrap has_injective_coseparator and has_projective_separator for the generator " ++
      "and cogenerator branch."
  },
  {
    id := "M0086.P4.upstream_proof_path_audit",
    status := "unchecked public/process backfill",
    summary :=
      "Record the upstream mathlib proof path through Indization, Grothendieck abelian " ++
      "categories, opposite module embedding, and preadditive generator APIs."
  },
  {
    id := "M0086.P5.repo_local_gate",
    status := "checked locally for the Lean wrapper; public status gate open",
    summary :=
      "Record local validation, placeholder scan, pinned mathlib closure, and the " ++
      "requirement that public blueprint/todo surfaces be updated serially by an integrator."
  }
]

/--
Integration-ready leaf ledger for the Stage1 Freyd theorem slot.

Leaves `M0086-L001` through `M0086-L015` are covered by checked local Lean
declarations.  Leaves `M0086-L016` through `M0086-L020` intentionally remain
unchecked because they concern public proof-path exposition or serial public-doc
integration rather than additional repo-local proof terms in this file.
-/
def leafBudgetLedger : List LeafBudgetEntry := [
  {
    id := "M0086-L001",
    package := "P0",
    target := "Declare universes v u, category variable C, and Abelian C assumptions.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L002",
    package := "P0",
    target :=
      "Define FreydMitchellEmbeddingStatement with ring, module-category functor, full, " ++
      "faithful, finite-limit, and finite-colimit clauses.",
    budget := "<=20",
    status := "checked locally"
  },
  {
    id := "M0086-L003",
    package := "P0",
    target :=
      "Define GeneratorExistenceStatement with injective-coseparator and " ++
      "projective-separator branches.",
    budget := "<=25",
    status := "checked locally"
  },
  {
    id := "M0086-L004",
    package := "P0",
    target := "Define combined StatementShape.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L005",
    package := "P1",
    target := "Prove freydMitchellEmbeddingStatement_mathlib from freyd_mitchell.",
    budget := "<=15",
    status := "checked locally"
  },
  {
    id := "M0086-L006",
    package := "P1",
    target := "Alias EmbeddingRing to CategoryTheory.Abelian.FreydMitchell.EmbeddingRing C.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L007",
    package := "P1",
    target := "Alias embeddingFunctor to CategoryTheory.Abelian.FreydMitchell.functor C.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L008",
    package := "P2",
    target := "Prove embeddingFunctor_full by typeclass inference.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L009",
    package := "P2",
    target := "Prove embeddingFunctor_faithful by typeclass inference.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L010",
    package := "P2",
    target := "Prove embeddingFunctor_preservesFiniteLimits by typeclass inference.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L011",
    package := "P2",
    target := "Prove embeddingFunctor_preservesFiniteColimits by typeclass inference.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L012",
    package := "P3",
    target := "Prove exists_injective_coseparator from has_injective_coseparator.",
    budget := "<=15",
    status := "checked locally"
  },
  {
    id := "M0086-L013",
    package := "P3",
    target := "Prove exists_projective_separator from has_projective_separator.",
    budget := "<=15",
    status := "checked locally"
  },
  {
    id := "M0086-L014",
    package := "P3",
    target := "Prove generatorExistenceStatement_mathlib by combining the generator wrappers.",
    budget := "<=20",
    status := "checked locally"
  },
  {
    id := "M0086-L015",
    package := "P5",
    target := "Prove statementShape_mathlib by combining embedding and generator branches.",
    budget := "<=10",
    status := "checked locally"
  },
  {
    id := "M0086-L016",
    package := "P4",
    target :=
      "Expand the Freyd-Mitchell upstream proof path through Ind.yoneda, " ++
      "Grothendieck abelian categories, and opposite module embedding.",
    budget := "<=100",
    status := "unchecked public/process backfill"
  },
  {
    id := "M0086-L017",
    package := "P4",
    target :=
      "Expand the generator/cogenerator upstream proof path through WellPowered, " ++
      "products over subobjects, enough injectives, and preadditive separator characterizations.",
    budget := "<=100",
    status := "unchecked public/process backfill"
  },
  {
    id := "M0086-L018",
    package := "P4",
    target :=
      "Audit the public wording that exactness is expressed by PreservesFiniteLimits plus " ++
      "PreservesFiniteColimits.",
    budget := "<=60",
    status := "unchecked public/process backfill"
  },
  {
    id := "M0086-L019",
    package := "P5",
    target :=
      "Backfill the public Stage1 blueprint/todo entry with pinned mathlib theorem names " ++
      "and the local validation command.",
    budget := "<=40",
    status := "unchecked serial public-doc integration"
  },
  {
    id := "M0086-L020",
    package := "P5",
    target :=
      "Add public human-readable proof-tree notes only after an integrator serially edits " ++
      "the shared public surface.",
    budget := "<=80",
    status := "unchecked serial public-doc integration"
  }
]

end S1_M_134
end Stage1
end AwesomeTheorems
