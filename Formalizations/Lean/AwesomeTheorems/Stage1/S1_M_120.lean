import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Topology.Category.TopCat.Sphere
import Mathlib.Topology.Compactification.OnePoint.Sphere

/-!
# S1-M-120 / THM-M-0548: Alexander duality

This Stage1 file records a conservative Lean statement-shape boundary for
Alexander duality for a subspace of a sphere.

The pinned mathlib snapshot
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has concrete substrates for
`TopCat` spheres, one-point compactifications of Euclidean spaces, and singular
homology functors.  It does not contain a terminal Alexander-duality theorem,
reduced cohomology theory for the closed subset, or the local exact/naturality
package needed for the full theorem.

The declarations below therefore avoid proof placeholders and false completion
claims: they normalize the sphere/complement/homology side of the statement and
keep the missing reduced-cohomology and duality-isomorphism side explicit.

## Public statement-normalization boundary

For the Stage1 public backfill, the current repo-local Lean boundary is
`AwesomeTheorems.Stage1.S1_M_120.StatementShape`, with
`StatementNormalizationBoundary` as a checked alias for that same proposition.
This boundary is intentionally not a terminal Alexander-duality theorem: it
packages the expected shape of the complement homology, shifted subset
cohomology, and duality isomorphism, while leaving the reduced-cohomology API,
exact-sequence/excision input, construction of the isomorphism, and naturality as
formalization debt.
-/

noncomputable section

open CategoryTheory AlgebraicTopology

universe w v u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_120

/-- The `n`-sphere object currently available in mathlib's `TopCat` API. -/
abbrev Sphere (n : ℕ) : TopCat.{w} :=
  TopCat.sphere n

/--
The complement of a selected subspace of a sphere, as a `TopCat` object.

For Alexander duality this is the homology-side space `S^n \ A`.  The subspace
itself is represented by the carrier set `A : Set (Sphere n)`.
-/
abbrev SphereSubsetComplement (n : ℕ) (A : Set (Sphere.{w} n)) : TopCat.{w} :=
  TopCat.of {x : Sphere.{w} n // x ∉ A}

/-- Singular homology of the complement of a sphere subspace, with coefficients `R`. -/
abbrev ComplementSingularHomology
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C)
    (n degree : ℕ) (A : Set (Sphere.{w} n)) : C :=
  (((singularHomologyFunctor C degree).obj R).obj (SphereSubsetComplement.{w} n A))

/--
Statement-shape data for Alexander duality.

The classical theorem relates reduced homology/cohomology groups of `S^n \ A`
and `A`, with a degree shift.  In the current local mathlib snapshot the
complement singular homology object is concrete, while reduced cohomology of the
subspace and the duality isomorphism are still formalization boundaries.
-/
structure AlexanderDualityData
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C) :
    Type (max (max (max u v) w) 1) where
  ambientDimension : ℕ
  homologyDegree : ℕ
  carrier : Set (Sphere.{w} ambientDimension)
  carrier_isClosed : IsClosed carrier
  subsetReducedCohomology : ℕ → C
  degreeShift : ℕ
  degreeShift_eq : degreeShift = ambientDimension - homologyDegree - 1
  dualityIso :
    ComplementSingularHomology C R ambientDimension homologyDegree carrier ≅
      subsetReducedCohomology degreeShift

/--
Stage1 statement-shape candidate for Alexander duality.

This proposition says that the normalized sphere/complement/singular-homology
input has the expected degree-shifted duality data.  It is intentionally a
statement shape, not a proof of Alexander duality.
-/
def StatementShape
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C) : Prop :=
  Nonempty (AlexanderDualityData.{w, v, u} C R)

/-- The statement-shape definition unfolds to nonemptiness of the normalized data package. -/
theorem statementShape_iff_nonempty
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C) :
    StatementShape.{w, v, u} C R ↔ Nonempty (AlexanderDualityData.{w, v, u} C R) :=
  Iff.rfl

/--
Checked public-normalization hook for `THM-M-0548.statement`.

Integrators should cite `StatementShape` as the repo-local Lean statement
boundary.  This alias exists only to make the public backfill target explicit
inside the Lean artifact; it adds no proof of Alexander duality beyond the
normalized statement shape.
-/
def StatementNormalizationBoundary
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C) : Prop :=
  StatementShape.{w, v, u} C R

/-- The public-normalization hook is exactly the existing `StatementShape`. -/
theorem statementNormalizationBoundary_iff
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C) :
    StatementNormalizationBoundary.{w, v, u} C R ↔ StatementShape.{w, v, u} C R :=
  Iff.rfl

/-- mathlib provides compactness of the `TopCat` sphere object. -/
theorem sphere_compactSpace (n : ℕ) : CompactSpace (Sphere.{w} n : Type w) := by
  change CompactSpace (TopCat.diskBoundary.{w} (n + 1) : Type w)
  infer_instance

/-- mathlib's boundary inclusion `∂D^n -> D^n` is a monomorphism in `TopCat`. -/
theorem diskBoundaryInclusion_mono (n : ℕ) :
    Mono (TopCat.diskBoundaryInclusion.{w} n) := by
  infer_instance

/--
Checked wrapper around the singular-homology calculation available for totally
disconnected spaces.  This is a low-dimensional/simple-space substrate, not an
Alexander-duality theorem.
-/
theorem singularHomology_isZero_of_totallyDisconnectedSpace
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C) (X : TopCat.{w})
    [TotallyDisconnectedSpace X] {n : ℕ} (hn : n ≠ 0) :
    CategoryTheory.Limits.IsZero (((singularHomologyFunctor C n).obj R).obj X) := by
  exact isZero_singularHomologyFunctor_of_totallyDisconnectedSpace C n R X hn

/-- The mathlib revision pinned by this repository for the `THM-M-0548` audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Module labels requested by the Stage1 public audit, paired with the concrete
mathlib import path present at `pinnedMathlibRevision`.
-/
def mathlibAuditModuleEntries : List (String × String) := [
  ("TopCat.Sphere", "Mathlib.Topology.Category.TopCat.Sphere"),
  ("OnePoint.Sphere", "Mathlib.Topology.Compactification.OnePoint.Sphere"),
  ("Geometry.Manifold.Instances.Sphere", "Mathlib.Geometry.Manifold.Instances.Sphere"),
  ("SingularHomology.Basic", "Mathlib.AlgebraicTopology.SingularHomology.Basic"),
  ("SingularHomology.HomotopyInvariance",
    "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvariance"),
  ("HomologySequence", "Mathlib.Algebra.Homology.HomologySequence"),
  ("SpectralSequence.Basic", "Mathlib.Algebra.Homology.SpectralSequence.Basic"),
  ("Geometry.Manifold.Bordism", "Mathlib.Geometry.Manifold.Bordism")
]

/-- Public module labels checked while locating repo-local anchors for this slot. -/
def mathlibAuditModuleLabels : List String :=
  mathlibAuditModuleEntries.map Prod.fst

/-- Concrete mathlib import paths checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String :=
  mathlibAuditModuleEntries.map Prod.snd

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "TopCat.sphere",
  "TopCat.diskBoundary",
  "TopCat.diskBoundaryInclusion",
  "onePointEquivSphereOfFinrankEq",
  "onePointHyperplaneHomeoUnitSphere",
  "AlgebraicTopology.singularHomologyFunctor",
  "AlgebraicTopology.isZero_singularHomologyFunctor_of_totallyDisconnectedSpace",
  "AlgebraicTopology.singularHomologyFunctorZeroOfTotallyDisconnectedSpace"
]

/-- Search terms that did not locate a terminal Alexander-duality theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Alexander duality",
  "AlexanderDuality",
  "alexander",
  "reduced cohomology",
  "reduced homology",
  "Cech cohomology",
  "Čech cohomology",
  "Poincare duality",
  "Lefschetz duality"
]

/-! ## Missing formal API split -/

/--
The formal API families still missing before this Stage1 slot can state and
prove a terminal Alexander-duality theorem repo-locally.
-/
inductive AlexanderDualityMissingAPIBranch where
  | reducedHomology
  | reducedCohomologyForSubspaces
  | complementPairBridge
  | excisionOrMayerVietorisInput
  | degreeShiftNormalization
  | dualityIsomorphismConstruction
  | naturality
  deriving DecidableEq, Repr

/-- Stable public task name for each missing Alexander-duality API branch. -/
def AlexanderDualityMissingAPIBranch.canonicalTaskName :
    AlexanderDualityMissingAPIBranch → String
  | .reducedHomology => "THM-M-0548.reduced-homology"
  | .reducedCohomologyForSubspaces =>
      "THM-M-0548.reduced-cohomology-for-subspaces"
  | .complementPairBridge => "THM-M-0548.complement-pair-bridge"
  | .excisionOrMayerVietorisInput =>
      "THM-M-0548.excision-or-mayer-vietoris-input"
  | .degreeShiftNormalization => "THM-M-0548.degree-shift-normalization"
  | .dualityIsomorphismConstruction =>
      "THM-M-0548.duality-isomorphism-construction"
  | .naturality => "THM-M-0548.naturality"

/-- One M0387-style repo-local leaf for a missing formal Alexander-duality API family. -/
structure AlexanderDualityMissingAPILeaf where
  branch : AlexanderDualityMissingAPIBranch
  canonicalTaskName : String
  requiredPayload : String
  currentBoundary : String
  currentStatus : String
  debtClass : String
  leafBudgetBound : Nat
  repoLocalClosed : Bool
  derivesFromBranchName : canonicalTaskName = branch.canonicalTaskName

/--
Integration-ready split of `THM-M-0548.missing-api`.

Every leaf is deliberately marked open and `formalization_debt`: this file
records the missing API frontier but does not construct reduced theories,
the complement/pair comparison, exact-sequence input, the shifted duality
isomorphism, or naturality.
-/
def alexanderDualityMissingAPILeaves : List AlexanderDualityMissingAPILeaf := [
  {
    branch := .reducedHomology
    canonicalTaskName :=
      AlexanderDualityMissingAPIBranch.reducedHomology.canonicalTaskName
    requiredPayload :=
      "define or import reduced homology with functoriality and comparison to singular homology"
    currentBoundary :=
      "ComplementSingularHomology uses ordinary singular homology of the complement only"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .reducedCohomologyForSubspaces
    canonicalTaskName :=
      AlexanderDualityMissingAPIBranch.reducedCohomologyForSubspaces.canonicalTaskName
    requiredPayload :=
      "define or import reduced cohomology for closed subspaces of spheres with usable coefficients"
    currentBoundary :=
      "AlexanderDualityData has only an abstract subsetReducedCohomology field"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .complementPairBridge
    canonicalTaskName :=
      AlexanderDualityMissingAPIBranch.complementPairBridge.canonicalTaskName
    requiredPayload :=
      "connect the complement of a sphere subspace to the relative or pair object used by duality"
    currentBoundary :=
      "SphereSubsetComplement is concrete, but no pair/complement comparison theorem is supplied"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .excisionOrMayerVietorisInput
    canonicalTaskName :=
      AlexanderDualityMissingAPIBranch.excisionOrMayerVietorisInput.canonicalTaskName
    requiredPayload :=
      "provide the excision, Mayer-Vietoris, or equivalent exact-sequence input for the proof"
    currentBoundary :=
      "mathlib homology-sequence substrates are audited, but no Alexander-duality exact input is instantiated"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .degreeShiftNormalization
    canonicalTaskName :=
      AlexanderDualityMissingAPIBranch.degreeShiftNormalization.canonicalTaskName
    requiredPayload :=
      "normalize the Alexander-duality degree shift and its admissible index range"
    currentBoundary :=
      "AlexanderDualityData stores only degreeShift_eq as an abstract field"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .dualityIsomorphismConstruction
    canonicalTaskName :=
      AlexanderDualityMissingAPIBranch.dualityIsomorphismConstruction.canonicalTaskName
    requiredPayload :=
      "construct the degree-shifted isomorphism between complement homology and subspace reduced cohomology"
    currentBoundary :=
      "AlexanderDualityData has an abstract dualityIso field and no construction theorem"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .naturality
    canonicalTaskName :=
      AlexanderDualityMissingAPIBranch.naturality.canonicalTaskName
    requiredPayload :=
      "prove naturality of the duality isomorphism under maps or inclusions in the intended category"
    currentBoundary :=
      "no naturality statement is encoded in StatementShape or AlexanderDualityData"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  }
]

/-- The missing-api split has exactly the seven branches requested by Stage1. -/
theorem alexanderDualityMissingAPILeaves_branches_eq :
    alexanderDualityMissingAPILeaves.map (fun leaf => leaf.branch) = [
      AlexanderDualityMissingAPIBranch.reducedHomology,
      AlexanderDualityMissingAPIBranch.reducedCohomologyForSubspaces,
      AlexanderDualityMissingAPIBranch.complementPairBridge,
      AlexanderDualityMissingAPIBranch.excisionOrMayerVietorisInput,
      AlexanderDualityMissingAPIBranch.degreeShiftNormalization,
      AlexanderDualityMissingAPIBranch.dualityIsomorphismConstruction,
      AlexanderDualityMissingAPIBranch.naturality
    ] :=
  rfl

/-- No missing-api leaf is locally closed by this Stage1 scaffold. -/
theorem alexanderDualityMissingAPILeaves_repoLocalClosed_eq :
    alexanderDualityMissingAPILeaves.map (fun leaf => leaf.repoLocalClosed) =
      [false, false, false, false, false, false, false] :=
  rfl

/-- Every missing-api leaf is currently an unchecked formalization-debt leaf. -/
theorem alexanderDualityMissingAPILeaves_statusDebt_eq :
    alexanderDualityMissingAPILeaves.map
      (fun leaf => (leaf.currentStatus, leaf.debtClass)) = [
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt")
      ] :=
  rfl

/-- M0387 gate: this child records no completed-state repo-local integration debt. -/
def missingAPIRepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- Checked gate for the current missing-API split. -/
theorem missingAPIRepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    missingAPIRepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-! ## External Lean 4 audit record -/

/-- Search terms requested by `THM-M-0548.external-audit`. -/
def externalAuditRequestedSearchTerms : List String := [
  "AlexanderDuality",
  "Alexander duality",
  "alexander_duality",
  "ReducedHomology",
  "ReducedCohomology",
  "reduced cohomology",
  "Cech",
  "PoincareDuality",
  "LefschetzDuality"
]

/--
GitHub authentication status for this child audit.

The local `gh auth status` check reported that no GitHub host was logged in, and
the GitHub code-search REST endpoint returned a rate-limit response for
unauthenticated requests.  This is recorded as an integration blocker rather
than as completed authenticated external search evidence.
-/
def externalAuditAuthenticatedGitHubSearchAvailable : Bool :=
  false

/-- Concrete blocker preventing this child from claiming authenticated GitHub code search. -/
def externalAuditAuthenticationBlocker : String :=
  "gh auth status reported no logged-in GitHub host; unauthenticated GitHub code search was rate-limited"

/-- One repo-level external-audit finding for the requested Lean 4 search terms. -/
structure ExternalLeanAuditFinding where
  searchedTerm : String
  repositoryURL : String
  commit : String
  sourcePaths : List String
  theoremOrDefinitionNames : List String
  toolchain : String
  placeholderStatus : String
  lakeDependencyFeasible : Bool
  terminalAlexanderDualityClosure : Bool
  notes : String
  deriving Repr

/--
Primary-source Lean 4 findings located repo-locally in the pinned mathlib
dependency while auditing the requested terms.

The `Cech` entries are real Lean 4 infrastructure at the pinned mathlib commit,
but they are not reduced cohomology of closed subspaces and not Alexander
duality.  The absent exact-name searches are therefore kept in
`externalAuditAbsentTerminalTerms`.
-/
def externalLeanAuditFindings : List ExternalLeanAuditFinding := [
  {
    searchedTerm := "Cech"
    repositoryURL := "https://github.com/leanprover-community/mathlib4"
    commit := pinnedMathlibRevision
    sourcePaths := [
      "Mathlib/AlgebraicTopology/CechNerve.lean",
      "Mathlib/CategoryTheory/Sites/SheafCohomology/Cech.lean",
      "Mathlib/Topology/Compactification/StoneCech.lean"
    ]
    theoremOrDefinitionNames := [
      "CategoryTheory.Arrow.cechNerve",
      "CategoryTheory.Arrow.augmentedCechNerve",
      "CategoryTheory.SimplicialObject.cechNerve",
      "CategoryTheory.SimplicialObject.augmentedCechNerve",
      "CategoryTheory.cechComplexFunctor",
      "StoneCech",
      "stoneCechUnit",
      "stoneCechExtend"
    ]
    toolchain := "leanprover/lean4:v4.29.0"
    placeholderStatus := "compiled dependency substrate; no proof placeholders observed in cited local snippets"
    lakeDependencyFeasible := true
    terminalAlexanderDualityClosure := false
    notes :=
      "Cech infrastructure is available in the already-pinned mathlib dependency, but it is not a terminal Alexander-duality theorem."
  }
]

/--
Requested exact searches that did not locate a terminal Lean 4 Alexander-duality
closure in the repo-local pinned mathlib dependency or this Stage1 artifact.
-/
def externalAuditAbsentTerminalTerms : List String := [
  "AlexanderDuality",
  "Alexander duality",
  "alexander_duality",
  "ReducedHomology",
  "ReducedCohomology",
  "reduced cohomology",
  "PoincareDuality",
  "LefschetzDuality"
]

/-- This child found no external Lean 4 terminal Alexander-duality closure. -/
def externalAuditTerminalClosureFound : Bool :=
  false

/-- M0387 gate: no anchor-only external evidence is counted as completed repo-local closure. -/
def externalAuditRepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- Checked record of the exact requested external-audit terms. -/
theorem externalAuditRequestedSearchTerms_eq :
    externalAuditRequestedSearchTerms = [
      "AlexanderDuality",
      "Alexander duality",
      "alexander_duality",
      "ReducedHomology",
      "ReducedCohomology",
      "reduced cohomology",
      "Cech",
      "PoincareDuality",
      "LefschetzDuality"
    ] :=
  rfl

/-- Checked record that authenticated GitHub code search was unavailable in this child shell. -/
theorem externalAuditAuthenticatedGitHubSearchAvailable_eq_false :
    externalAuditAuthenticatedGitHubSearchAvailable = false :=
  rfl

/-- Checked record that this child found no terminal external Alexander-duality closure. -/
theorem externalAuditTerminalClosureFound_eq_false :
    externalAuditTerminalClosureFound = false :=
  rfl

/-- Checked external-audit integration-debt gate. -/
theorem externalAuditRepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    externalAuditRepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-! ## External closure integration gate -/

/--
One repo-local integration-gate record for `THM-M-0548.integration-gate`.

This is deliberately a gate, not an Alexander-duality proof.  It records that
the current checked audit found no terminal external Lean 4 closure to
pin/import/check, and that the remaining public status must stay open until an
authenticated external audit either stays negative or supplies a concrete proof
body that this repository can validate.
-/
structure AlexanderDualityIntegrationGate where
  childID : String
  externalAuditAnchor : String
  externalClosureFound : Bool
  integrationAction : String
  authenticatedAuditBlocked : Bool
  publicCompletionClaimAllowed : Bool
  noAnchorOnlyCompletion : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  currentStatus : String
  currentDebtClass : String
  deriving Repr

/-- Checked C005 integration gate for Alexander duality. -/
def alexanderDualityIntegrationGate : AlexanderDualityIntegrationGate := {
  childID := "S1-M-120-C005"
  externalAuditAnchor :=
    "AwesomeTheorems.Stage1.S1_M_120.externalAuditTerminalClosureFound"
  externalClosureFound := externalAuditTerminalClosureFound
  integrationAction :=
    "no terminal external Lean 4 Alexander-duality closure is available to pin/import/check in the current checked audit; if one is later found, pin/import/check it or record a concrete blocker before any public completion claim"
  authenticatedAuditBlocked := !externalAuditAuthenticatedGitHubSearchAvailable
  publicCompletionClaimAllowed := false
  noAnchorOnlyCompletion := true
  completedStateRetainsRepoLocalIntegrationDebt :=
    externalAuditRepoLocalIntegrationDebtRetainedInCompletedState
  currentStatus := "not_repo_local_closed"
  currentDebtClass := "formalization_debt"
}

/-- The current C005 gate has no terminal external Lean 4 closure to integrate. -/
theorem alexanderDualityIntegrationGate_externalClosureFound_eq_false :
    alexanderDualityIntegrationGate.externalClosureFound = false :=
  rfl

/-- The current C005 gate blocks public completion claims. -/
theorem alexanderDualityIntegrationGate_publicCompletionClaimAllowed_eq_false :
    alexanderDualityIntegrationGate.publicCompletionClaimAllowed = false :=
  rfl

/-- The current C005 gate forbids anchor-only completion evidence. -/
theorem alexanderDualityIntegrationGate_noAnchorOnlyCompletion_eq_true :
    alexanderDualityIntegrationGate.noAnchorOnlyCompletion = true :=
  rfl

/-- The current C005 gate retains no completed-state repo-local integration debt. -/
theorem alexanderDualityIntegrationGate_completedStateRetainsRepoLocalIntegrationDebt_eq_false :
    alexanderDualityIntegrationGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

#check StatementShape
#check StatementNormalizationBoundary
#check statementNormalizationBoundary_iff
#check AlexanderDualityMissingAPIBranch
#check alexanderDualityMissingAPILeaves
#check alexanderDualityMissingAPILeaves_branches_eq
#check alexanderDualityMissingAPILeaves_repoLocalClosed_eq
#check alexanderDualityMissingAPILeaves_statusDebt_eq
#check missingAPIRepoLocalIntegrationDebtRetainedInCompletedState_eq_false
#check externalAuditRequestedSearchTerms
#check externalLeanAuditFindings
#check externalAuditRequestedSearchTerms_eq
#check externalAuditAuthenticatedGitHubSearchAvailable_eq_false
#check externalAuditTerminalClosureFound_eq_false
#check externalAuditRepoLocalIntegrationDebtRetainedInCompletedState_eq_false
#check alexanderDualityIntegrationGate
#check alexanderDualityIntegrationGate_externalClosureFound_eq_false
#check alexanderDualityIntegrationGate_publicCompletionClaimAllowed_eq_false
#check alexanderDualityIntegrationGate_noAnchorOnlyCompletion_eq_true
#check alexanderDualityIntegrationGate_completedStateRetainsRepoLocalIntegrationDebt_eq_false

end S1_M_120
end Stage1
end AwesomeTheorems
