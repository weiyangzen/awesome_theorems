import Mathlib.Algebra.Homology.HomologicalComplex
import Mathlib.Algebra.Homology.HomologySequenceLemmas
import Mathlib.Algebra.Homology.Monoidal
import Mathlib.Algebra.Homology.ShortComplex.ShortExact
import Mathlib.Algebra.Homology.SpectralObject.SpectralSequence
import Mathlib.Algebra.Homology.SpectralSequence.Basic
import Mathlib.AlgebraicTopology.SingularHomology.Basic

/-!
# S1-M-100 / THM-M-0005: Kunneth formula

This Stage1 file records a conservative Lean 4 boundary for the Kunneth formula
for homology of products.  The pinned mathlib snapshot has substantial
category-level homological algebra: homological complexes, tensor products of
complexes, short exact complexes, long exact homology-sequence naturality, and
quasi-isomorphism transfer lemmas.  It does not expose a terminal theorem named
`Kunneth`/`Künneth`, nor a product-space singular-homology Kunneth theorem.

The declarations below therefore provide statement-shape data and low-risk
wrappers around existing mathlib facts.  They contain no proof of the terminal
Kunneth formula.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

universe v u w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_100

/--
The tensor product complex currently available from mathlib's monoidal
homological-complex API.
-/
abbrev TensorComplex
    (C : Type u) [Category.{v} C] [Preadditive C] [MonoidalCategory C]
    [(MonoidalCategory.curriedTensor C).Additive]
    [∀ X : C, ((MonoidalCategory.curriedTensor C).obj X).Additive]
    (I : Type w) [AddMonoid I] [DecidableEq I] (c : ComplexShape I) [c.TensorSigns]
    (K L : HomologicalComplex C c) [K.HasTensor L] :
    HomologicalComplex C c :=
  K.tensorObj L

/--
Stage1 statement-shape data for a categorical Kunneth comparison in a fixed
degree.

The field `kunnethComparison` is the future comparison map from the homology of
the tensor/product complex to whichever direct-sum/Tor/spectral-sequence target
is appropriate in the chosen coefficient and flatness regime.  Requiring
`IsIso` here records what a completed Kunneth theorem must prove or import; this
structure is not inhabited locally.
-/
structure KunnethComparisonData
    (C : Type u) [Category.{v} C] [Preadditive C] [Abelian C] [CategoryWithHomology C]
    [MonoidalCategory C]
    [(MonoidalCategory.curriedTensor C).Additive]
    [∀ X : C, ((MonoidalCategory.curriedTensor C).obj X).Additive]
    (I : Type w) [AddMonoid I] [DecidableEq I] (c : ComplexShape I) [c.TensorSigns]
    (K L : HomologicalComplex C c) [K.HasTensor L] where
  degree : I
  target : C
  kunnethComparison :
    ((HomologicalComplex.homologyFunctor C c degree).obj (TensorComplex C I c K L)) ⟶ target
  comparison_isIso : IsIso kunnethComparison
  naturality_square : Prop
  short_exact_or_spectral_sequence_compatibility : Prop

/--
Normalized Stage1 statement-shape candidate for THM-M-0005.

It says that every admissible pair of complexes in the selected monoidal
homological category has Kunneth comparison data.  This intentionally leaves the
coefficient ring, product-space chain model, flatness/projectivity hypotheses,
Tor correction term, and target decomposition abstract.
-/
def StatementShape
    (C : Type u) [Category.{v} C] [Preadditive C] [Abelian C] [CategoryWithHomology C]
    [MonoidalCategory C]
    [(MonoidalCategory.curriedTensor C).Additive]
    [∀ X : C, ((MonoidalCategory.curriedTensor C).obj X).Additive]
    (I : Type w) [AddMonoid I] [DecidableEq I] (c : ComplexShape I) [c.TensorSigns] :
    Prop :=
  ∀ K L : HomologicalComplex C c,
    [K.HasTensor L] → Nonempty (KunnethComparisonData C I c K L)

/-! ## Public statement-normalization boundary -/

/--
Named public boundary for the Stage1 statement-normalization pass.

This is definitionally the same proposition as `StatementShape`: it records the
current repo-local Lean shape for a future categorical Kunneth comparison and is
safe for public blueprint backfill.  It is deliberately not a terminal Kunneth
formula for singular homology of product spaces, and it does not provide the
missing Eilenberg-Zilber/Alexander-Whitney maps, Tor correction target,
spectral-sequence branch, or final naturality theorem.
-/
def StatementNormalizationBoundary
    (C : Type u) [Category.{v} C] [Preadditive C] [Abelian C] [CategoryWithHomology C]
    [MonoidalCategory C]
    [(MonoidalCategory.curriedTensor C).Additive]
    [∀ X : C, ((MonoidalCategory.curriedTensor C).obj X).Additive]
    (I : Type w) [AddMonoid I] [DecidableEq I] (c : ComplexShape I) [c.TensorSigns] :
    Prop :=
  StatementShape C I c

/-- The public statement-normalization boundary is exactly `StatementShape`. -/
theorem statementNormalizationBoundary_iff
    (C : Type u) [Category.{v} C] [Preadditive C] [Abelian C] [CategoryWithHomology C]
    [MonoidalCategory C]
    [(MonoidalCategory.curriedTensor C).Additive]
    [∀ X : C, ((MonoidalCategory.curriedTensor C).obj X).Additive]
    (I : Type w) [AddMonoid I] [DecidableEq I] (c : ComplexShape I) [c.TensorSigns] :
    StatementNormalizationBoundary C I c ↔ StatementShape C I c :=
  Iff.rfl

/-! ## Mathlib audit boundary -/

/-- Pinned mathlib revision used for the Stage1 Kunneth audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Mathlib modules requested by `THM-M-0005.mathlib-audit`.

`Mathlib.AlgebraicTopology.SingularHomology.Basic` is the concrete importable
module for the available singular-homology API at the pinned revision.
-/
def requiredMathlibAuditModules : List String := [
  "Mathlib.Algebra.Homology.HomologicalComplex",
  "Mathlib.Algebra.Homology.Monoidal",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas",
  "Mathlib.Algebra.Homology.ShortComplex.ShortExact",
  "Mathlib.Algebra.Homology.SpectralObject.SpectralSequence",
  "Mathlib.Algebra.Homology.SpectralSequence.Basic",
  "Mathlib.AlgebraicTopology.SingularHomology.Basic"
]

/-- The pinned revision string in this artifact is the requested mathlib commit. -/
theorem pinnedMathlibRevision_eq :
    pinnedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- The repo-local mathlib-audit module list is exactly the requested Stage1 set. -/
theorem requiredMathlibAuditModules_eq :
    requiredMathlibAuditModules = [
      "Mathlib.Algebra.Homology.HomologicalComplex",
      "Mathlib.Algebra.Homology.Monoidal",
      "Mathlib.Algebra.Homology.HomologySequenceLemmas",
      "Mathlib.Algebra.Homology.ShortComplex.ShortExact",
      "Mathlib.Algebra.Homology.SpectralObject.SpectralSequence",
      "Mathlib.Algebra.Homology.SpectralSequence.Basic",
      "Mathlib.AlgebraicTopology.SingularHomology.Basic"
    ] :=
  rfl

/-! ## Missing API split boundary -/

/--
The six formal API families still missing before a terminal product-space
Kunneth theorem can be stated and proved repo-locally.
-/
inductive MissingAPIBranch where
  | productSpaceChainModel
  | eilenbergZilberAlexanderWhitneyChainMaps
  | kunnethComparisonTarget
  | torSpectralSequenceCorrectionBranch
  | naturality
  | terminalProductSpaceTheorem
  deriving DecidableEq, Repr

/-- Stable public task name for each missing Kunneth API branch. -/
def MissingAPIBranch.canonicalTaskName : MissingAPIBranch → String
  | .productSpaceChainModel => "THM-M-0005.product-space-chain-model"
  | .eilenbergZilberAlexanderWhitneyChainMaps =>
      "THM-M-0005.eilenberg-zilber-alexander-whitney-chain-maps"
  | .kunnethComparisonTarget => "THM-M-0005.kunneth-comparison-target"
  | .torSpectralSequenceCorrectionBranch =>
      "THM-M-0005.tor-spectral-sequence-correction-branch"
  | .naturality => "THM-M-0005.naturality"
  | .terminalProductSpaceTheorem => "THM-M-0005.terminal-product-space-theorem"

/-- One M0387-style repo-local leaf for a missing formal Kunneth API family. -/
structure MissingAPILeaf where
  branch : MissingAPIBranch
  canonicalTaskName : String
  requiredPayload : String
  currentStatus : String
  debtClass : String
  leafBudgetBound : Nat
  repoLocalClosed : Bool
  derivesFromBranchName : canonicalTaskName = branch.canonicalTaskName

/--
Integration-ready split of `THM-M-0005.missing-api`.

Every leaf is deliberately marked open and `formalization_debt`: this file
records the missing API frontier but does not create product-space singular
chains, Eilenberg-Zilber/Alexander-Whitney maps, the Tor/spectral-sequence
endpoint, or the terminal Kunneth isomorphism.
-/
def missingAPILeaves : List MissingAPILeaf := [
  {
    branch := .productSpaceChainModel
    canonicalTaskName := MissingAPIBranch.productSpaceChainModel.canonicalTaskName
    requiredPayload :=
      "select and formalize the product-space singular-chain model and its tensor-complex bridge"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .eilenbergZilberAlexanderWhitneyChainMaps
    canonicalTaskName :=
      MissingAPIBranch.eilenbergZilberAlexanderWhitneyChainMaps.canonicalTaskName
    requiredPayload :=
      "construct Eilenberg-Zilber and Alexander-Whitney chain maps and their homotopy-equivalence data"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .kunnethComparisonTarget
    canonicalTaskName := MissingAPIBranch.kunnethComparisonTarget.canonicalTaskName
    requiredPayload :=
      "select the direct-sum tensor-homology comparison target for the chosen coefficient regime"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .torSpectralSequenceCorrectionBranch
    canonicalTaskName :=
      MissingAPIBranch.torSpectralSequenceCorrectionBranch.canonicalTaskName
    requiredPayload :=
      "formalize the Tor correction term or spectral-sequence branch and its convergence/exactness bridge"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .naturality
    canonicalTaskName := MissingAPIBranch.naturality.canonicalTaskName
    requiredPayload :=
      "prove naturality in both product-space variables and in the selected comparison target"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .terminalProductSpaceTheorem
    canonicalTaskName := MissingAPIBranch.terminalProductSpaceTheorem.canonicalTaskName
    requiredPayload :=
      "assemble the terminal singular-homology Kunneth theorem for product spaces"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  }
]

/-- The missing-api split has exactly the six branches requested by Stage1. -/
theorem missingAPILeaves_branches_eq :
    missingAPILeaves.map (fun leaf => leaf.branch) = [
      MissingAPIBranch.productSpaceChainModel,
      MissingAPIBranch.eilenbergZilberAlexanderWhitneyChainMaps,
      MissingAPIBranch.kunnethComparisonTarget,
      MissingAPIBranch.torSpectralSequenceCorrectionBranch,
      MissingAPIBranch.naturality,
      MissingAPIBranch.terminalProductSpaceTheorem
    ] :=
  rfl

/-- No missing-api leaf is locally closed by this Stage1 scaffold. -/
theorem missingAPILeaves_repoLocalClosed_eq :
    missingAPILeaves.map (fun leaf => leaf.repoLocalClosed) =
      [false, false, false, false, false, false] :=
  rfl

/-- Every missing-api leaf is currently an unchecked formalization-debt leaf. -/
theorem missingAPILeaves_statusDebt_eq :
    missingAPILeaves.map (fun leaf => (leaf.currentStatus, leaf.debtClass)) = [
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt")
    ] :=
  rfl

/--
Naturality square expected of a Kunneth comparison under maps of both input
complexes.

This is a checkable proposition using mathlib's `tensorHom` and `homologyFunctor`
APIs.  It is a boundary predicate, not a proof that such a square is available
for a terminal Kunneth theorem.
-/
def KunnethNaturalitySquare
    (C : Type u) [Category.{v} C] [Preadditive C] [Abelian C] [CategoryWithHomology C]
    [MonoidalCategory C]
    [(MonoidalCategory.curriedTensor C).Additive]
    [∀ X : C, ((MonoidalCategory.curriedTensor C).obj X).Additive]
    (I : Type w) [AddMonoid I] [DecidableEq I] (c : ComplexShape I) [c.TensorSigns]
    {K₁ K₂ L₁ L₂ : HomologicalComplex C c}
    [K₁.HasTensor L₁] [K₂.HasTensor L₂]
    (n : I) (T₁ T₂ : C)
    (κ₁ : ((HomologicalComplex.homologyFunctor C c n).obj (TensorComplex C I c K₁ L₁)) ⟶ T₁)
    (κ₂ : ((HomologicalComplex.homologyFunctor C c n).obj (TensorComplex C I c K₂ L₂)) ⟶ T₂)
    (f : K₁ ⟶ K₂) (g : L₁ ⟶ L₂) (targetMap : T₁ ⟶ T₂) : Prop :=
  κ₁ ≫ targetMap =
    ((HomologicalComplex.homologyFunctor C c n).map (HomologicalComplex.tensorHom f g)) ≫ κ₂

/-- The naturality-square predicate unfolds to its defining commutative-square equation. -/
theorem kunnethNaturalitySquare_iff
    (C : Type u) [Category.{v} C] [Preadditive C] [Abelian C] [CategoryWithHomology C]
    [MonoidalCategory C]
    [(MonoidalCategory.curriedTensor C).Additive]
    [∀ X : C, ((MonoidalCategory.curriedTensor C).obj X).Additive]
    (I : Type w) [AddMonoid I] [DecidableEq I] (c : ComplexShape I) [c.TensorSigns]
    {K₁ K₂ L₁ L₂ : HomologicalComplex C c}
    [K₁.HasTensor L₁] [K₂.HasTensor L₂]
    (n : I) (T₁ T₂ : C)
    (κ₁ : ((HomologicalComplex.homologyFunctor C c n).obj (TensorComplex C I c K₁ L₁)) ⟶ T₁)
    (κ₂ : ((HomologicalComplex.homologyFunctor C c n).obj (TensorComplex C I c K₂ L₂)) ⟶ T₂)
    (f : K₁ ⟶ K₂) (g : L₁ ⟶ L₂) (targetMap : T₁ ⟶ T₂) :
    KunnethNaturalitySquare C I c n T₁ T₂ κ₁ κ₂ f g targetMap ↔
      κ₁ ≫ targetMap =
        ((HomologicalComplex.homologyFunctor C c n).map (HomologicalComplex.tensorHom f g)) ≫ κ₂ :=
  Iff.rfl

/--
Checked wrapper around mathlib's naturality of the connecting morphism in the
homology sequence attached to a morphism of short exact complexes.
-/
theorem homologySequence_delta_naturality
    {C I : Type*} [Category C] [Abelian C] {c : ComplexShape I}
    {S₁ S₂ : ShortComplex (HomologicalComplex C c)} (φ : S₁ ⟶ S₂)
    (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (i j : I) (hij : c.Rel i j) :
    hS₁.δ i j hij ≫ HomologicalComplex.homologyMap φ.τ₁ j =
      HomologicalComplex.homologyMap φ.τ₃ i ≫ hS₂.δ i j hij := by
  exact HomologicalComplex.HomologySequence.δ_naturality φ hS₁ hS₂ i j hij

/--
Checked wrapper: exact functors preserve short exact short complexes in the
mathlib API.
-/
theorem shortExact_map_of_exact
    {C D : Type*} [Category C] [Category D] [Preadditive C] [Preadditive D]
    {S : ShortComplex C} (hS : S.ShortExact) (F : C ⥤ D)
    [F.PreservesZeroMorphisms] [PreservesFiniteLimits F] [PreservesFiniteColimits F] :
    (S.map F).ShortExact := by
  exact hS.map_of_exact F

/--
Checked wrapper: if two terms of a morphism between short exact sequences are
isomorphisms, the middle term is an isomorphism in a balanced preadditive
category.
-/
theorem shortExact_isIso_middle_of_isIso_outer
    {C : Type*} [Category C] [Preadditive C] [Balanced C]
    {S₁ S₂ : ShortComplex C} (φ : S₁ ⟶ S₂)
    (h₁ : S₁.ShortExact) (h₂ : S₂.ShortExact)
    [IsIso φ.τ₁] [IsIso φ.τ₃] :
    IsIso φ.τ₂ := by
  exact ShortComplex.isIso₂_of_shortExact_of_isIso₁₃ φ h₁ h₂

/--
Checked wrapper: in a morphism of short exact complexes of homological
complexes, quasi-isomorphisms on the first two components imply a
quasi-isomorphism on the third.
-/
theorem quasiIso_third_of_quasiIso_first_second
    {C I : Type*} [Category C] [Abelian C] {c : ComplexShape I}
    {S₁ S₂ : ShortComplex (HomologicalComplex C c)} (φ : S₁ ⟶ S₂)
    (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (h₁ : QuasiIso φ.τ₁)
    (h₂ : QuasiIso φ.τ₂) :
    QuasiIso φ.τ₃ := by
  exact HomologicalComplex.HomologySequence.quasiIso_τ₃ φ hS₁ hS₂ h₁ h₂

/-- mathlib modules checked while locating repo-local Kunneth anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Homology.HomologicalComplex",
  "Mathlib.Algebra.Homology.Monoidal",
  "Mathlib.Algebra.Homology.TotalComplex",
  "Mathlib.Algebra.Homology.HomologySequence",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas",
  "Mathlib.Algebra.Homology.ShortComplex.ShortExact",
  "Mathlib.Algebra.Homology.SpectralObject.SpectralSequence",
  "Mathlib.Algebra.Homology.SpectralSequence.Basic",
  "Mathlib.AlgebraicTopology.SingularHomology.Basic",
  "Mathlib.RepresentationTheory.Homological.GroupHomology.LongExactSequence"
]

/-- Exact external-audit search terms requested by `THM-M-0005.external-audit`. -/
def externalAuditSearchTerms : List String := [
  "Kunneth",
  "Künneth",
  "Kuenneth",
  "EilenbergZilber",
  "Eilenberg-Zilber",
  "AlexanderWhitney",
  "SingularHomology",
  "homology product",
  "Tor",
  "KunnethSpectralSequence"
]

/--
Search terms that did not locate a terminal Kunneth theorem in pinned mathlib
or the already-pinned Lean dependencies.

`SingularHomology` and `Tor` do have mathlib API anchors, but not a terminal
product-space Kunneth theorem.  They are kept in this list because the audit
result is negative for the terminal theorem, not for every supporting API.
-/
def absentTerminalSearchTerms : List String := [
  "Kunneth",
  "Künneth",
  "Kuenneth",
  "EilenbergZilber",
  "Eilenberg-Zilber",
  "AlexanderWhitney",
  "SingularHomology",
  "homology product",
  "Tor",
  "KunnethSpectralSequence"
]

/-- The repo-local external-audit search term list is exactly the Stage1 request. -/
theorem externalAuditSearchTerms_eq :
    externalAuditSearchTerms = [
      "Kunneth",
      "Künneth",
      "Kuenneth",
      "EilenbergZilber",
      "Eilenberg-Zilber",
      "AlexanderWhitney",
      "SingularHomology",
      "homology product",
      "Tor",
      "KunnethSpectralSequence"
    ] :=
  rfl

/-- The terminal Kunneth theorem remains absent for every requested search term. -/
theorem absentTerminalSearchTerms_eq_externalAuditSearchTerms :
    absentTerminalSearchTerms = externalAuditSearchTerms :=
  rfl

/-! ## Integration gate boundary -/

/--
Concrete blockers that prevent any public completion claim for the Stage1
Kunneth slot.

These blockers are gate metadata.  They do not assert that no Lean 4 proof can
exist elsewhere; they record why this repository cannot currently claim a
repo-local Kunneth closure.
-/
inductive IntegrationGateBlocker where
  | authenticatedPrimarySourceSearchBlocked
  | noPinnedExternalClosureInLake
  | terminalProductSpaceAPIsMissing
  deriving DecidableEq, Repr

/-- Stable task name for each current integration-gate blocker. -/
def IntegrationGateBlocker.canonicalTaskName : IntegrationGateBlocker → String
  | .authenticatedPrimarySourceSearchBlocked =>
      "THM-M-0005.authenticated-primary-source-search"
  | .noPinnedExternalClosureInLake =>
      "THM-M-0005.pin-import-check-external-closure"
  | .terminalProductSpaceAPIsMissing =>
      "THM-M-0005.terminal-product-space-api-closure"

/--
Repo-local integration-gate audit for `THM-M-0005.integration-gate`.

The current gate state is deliberately non-completing: no external terminal Lean
4 Kunneth closure has been found in the pinned Lake closure, no external proof
has been pin/import/checked, and no completed debt class is recorded.  If a
future authenticated audit finds an external closure, this record must be
replaced by a pinned/imported/checked dependency or by a more specific blocker.
-/
structure IntegrationGateAudit where
  machineStatus : String
  debtClass : String
  externalClosureFound : Bool
  pinImportCheckPerformed : Bool
  completionClaimAllowed : Bool
  completedDebtClasses : List String
  blockers : List IntegrationGateBlocker

/-- Checked repo-local integration-gate state for the current Stage1 pass. -/
def integrationGateAudit : IntegrationGateAudit := {
  machineStatus := "not_repo_local_closed"
  debtClass := "formalization_debt"
  externalClosureFound := false
  pinImportCheckPerformed := false
  completionClaimAllowed := false
  completedDebtClasses := []
  blockers := [
    IntegrationGateBlocker.authenticatedPrimarySourceSearchBlocked,
    IntegrationGateBlocker.noPinnedExternalClosureInLake,
    IntegrationGateBlocker.terminalProductSpaceAPIsMissing
  ]
}

/-- The current integration gate does not permit a completion claim. -/
theorem integrationGateAudit_completionClaimAllowed_eq :
    integrationGateAudit.completionClaimAllowed = false :=
  rfl

/-- No external Lean 4 terminal Kunneth closure is found in the current local closure. -/
theorem integrationGateAudit_externalClosureFound_eq :
    integrationGateAudit.externalClosureFound = false :=
  rfl

/-- No external Kunneth proof has been pin/import/checked in this repo-local pass. -/
theorem integrationGateAudit_pinImportCheckPerformed_eq :
    integrationGateAudit.pinImportCheckPerformed = false :=
  rfl

/-- No completed state in this gate retains a debt class. -/
theorem integrationGateAudit_completedDebtClasses_eq :
    integrationGateAudit.completedDebtClasses = [] :=
  rfl

/-- In particular, the current gate has no completed `repo_local_integration_debt`. -/
theorem integrationGateAudit_noCompletedRepoLocalIntegrationDebt :
    "repo_local_integration_debt" ∉ integrationGateAudit.completedDebtClasses := by
  simp [integrationGateAudit]

/-- The current concrete integration blockers are exactly the three gate leaves. -/
theorem integrationGateAudit_blockers_eq :
    integrationGateAudit.blockers = [
      IntegrationGateBlocker.authenticatedPrimarySourceSearchBlocked,
      IntegrationGateBlocker.noPinnedExternalClosureInLake,
      IntegrationGateBlocker.terminalProductSpaceAPIsMissing
    ] :=
  rfl

/-! ## Audit probes -/

#check TensorComplex
#check KunnethComparisonData
#check StatementShape
#check StatementNormalizationBoundary
#check statementNormalizationBoundary_iff
#check pinnedMathlibRevision
#check requiredMathlibAuditModules
#check pinnedMathlibRevision_eq
#check requiredMathlibAuditModules_eq
#check MissingAPIBranch
#check MissingAPIBranch.canonicalTaskName
#check MissingAPILeaf
#check missingAPILeaves
#check missingAPILeaves_branches_eq
#check missingAPILeaves_repoLocalClosed_eq
#check missingAPILeaves_statusDebt_eq
#check KunnethNaturalitySquare
#check homologySequence_delta_naturality
#check shortExact_map_of_exact
#check quasiIso_third_of_quasiIso_first_second
#check mathlibAnchorModules
#check externalAuditSearchTerms
#check externalAuditSearchTerms_eq
#check absentTerminalSearchTerms
#check absentTerminalSearchTerms_eq_externalAuditSearchTerms
#check IntegrationGateBlocker
#check IntegrationGateBlocker.canonicalTaskName
#check IntegrationGateAudit
#check integrationGateAudit
#check integrationGateAudit_completionClaimAllowed_eq
#check integrationGateAudit_externalClosureFound_eq
#check integrationGateAudit_pinImportCheckPerformed_eq
#check integrationGateAudit_completedDebtClasses_eq
#check integrationGateAudit_noCompletedRepoLocalIntegrationDebt
#check integrationGateAudit_blockers_eq
#check HomologicalComplex
#check HomologicalComplex.tensorObj
#check HomologicalComplex.HomologySequence.δ_naturality
#check CategoryTheory.ShortComplex.ShortExact
#check CategoryTheory.Abelian.SpectralObject
#check CategoryTheory.SpectralSequence
#check AlgebraicTopology.singularHomologyFunctor

end S1_M_100
end Stage1
end AwesomeTheorems
