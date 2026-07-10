import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# S1-M-116 / THM-M-0583: four-dimensional topological Poincare conjecture

This Stage1 artifact records the Lean 4 boundary for the four-dimensional
topological Poincare conjecture.  The pinned mathlib snapshot contains the
manifold, sphere, homeomorphism, homotopy-equivalence, compactness, and simply
connected infrastructure needed to state the theorem, plus a source-level
`proof_wanted` marker for the generalized topological Poincare conjecture.

The terminal four-dimensional theorem is not proved here.  The checked content
below is limited to statement normalization and low-risk wrappers around
available mathlib infrastructure.
-/

noncomputable section

open scoped Manifold ContDiff
open Metric ContinuousMap

universe u

namespace AwesomeTheorems.Stage1.S1_M_116

/-- The Euclidean model space for a topological 4-manifold. -/
abbrev Euclidean4 : Type :=
  EuclideanSpace ℝ (Fin 4)

/-- The topological 4-sphere, realized as the unit sphere in `R^5`. -/
abbrev Sphere4 : Type :=
  Metric.sphere (0 : EuclideanSpace ℝ (Fin 5)) 1

/--
Stage1 statement-shape for the four-dimensional topological Poincare
conjecture.

Every compact simply connected Hausdorff topological 4-manifold, expressed as a
space charted over `EuclideanSpace R (Fin 4)`, is homeomorphic to the 4-sphere.
This is a proposition only; no proof of the terminal theorem is claimed.
-/
def StatementShape : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [ChartedSpace Euclidean4 M]
    [SimplyConnectedSpace M] [CompactSpace M],
      Nonempty (M ≃ₜ Sphere4)

/--
A named predicate wrapper for the exact compact simply connected topological
4-manifold hypotheses used by `StatementShape`.

This exists to make later public backfill text precise.  It is not a proof of
the four-dimensional Poincare conjecture.
-/
def ClosedSimplyConnectedTopologicalFourManifold
    (M : Type u) [TopologicalSpace M] : Prop :=
  Nonempty (T2Space M) ∧ Nonempty (ChartedSpace Euclidean4 M) ∧
    Nonempty (SimplyConnectedSpace M) ∧ Nonempty (CompactSpace M)

/-- The same statement shape using the named hypothesis wrapper. -/
def NamedStatementShape : Prop :=
  ∀ (M : Type u) [TopologicalSpace M],
    ClosedSimplyConnectedTopologicalFourManifold M → Nonempty (M ≃ₜ Sphere4)

/--
The named wrapper is propositionally equivalent to the direct mathlib-style
typeclass signature.  This keeps the statement boundary integration-ready
without changing the proof status.
-/
theorem namedStatementShape_iff_statementShape :
    NamedStatementShape.{u} ↔ StatementShape.{u} := by
  constructor
  · intro h M _ _ _ _ _
    exact h M ⟨⟨inferInstance⟩, ⟨inferInstance⟩, ⟨inferInstance⟩, ⟨inferInstance⟩⟩
  · intro h M _ hM
    rcases hM with ⟨hT2, hCharted, hSimplyConnected, hCompact⟩
    letI : T2Space M := hT2.some
    letI : ChartedSpace Euclidean4 M := hCharted.some
    letI : SimplyConnectedSpace M := hSimplyConnected.some
    letI : CompactSpace M := hCompact.some
    exact h M

/--
Homotopy-sphere version matching the shape of mathlib's generalized
topological Poincare `proof_wanted` source declaration at dimension 4.

This is weaker as a manifold-recognition input than the compact simply
connected statement above because it assumes an explicit homotopy equivalence to
`Sphere4`.
-/
def HomotopySphereFourStatementShape : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [ChartedSpace Euclidean4 M],
    M ≃ₕ Sphere4 → Nonempty (M ≃ₜ Sphere4)

/-- Checked mathlib infrastructure: the canonical 4-sphere is an analytic 4-manifold. -/
theorem sphere4_isManifold :
    IsManifold (𝓡 4) ω Sphere4 := by
  infer_instance

/-- Checked mathlib infrastructure: the canonical 4-sphere is compact. -/
theorem sphere4_compact : CompactSpace Sphere4 := by
  infer_instance

/-- Checked mathlib infrastructure: the canonical 4-sphere is Hausdorff. -/
theorem sphere4_t2 : T2Space Sphere4 := by
  infer_instance

/-- Checked mathlib infrastructure: simply connected spaces are path connected. -/
theorem simplyConnected_implies_pathConnected
    (M : Type u) [TopologicalSpace M] [SimplyConnectedSpace M] :
    PathConnectedSpace M := by
  infer_instance

/-- The target sphere is homeomorphic to itself; this is only a sanity wrapper. -/
theorem sphere4_self_homeomorph : Nonempty (Sphere4 ≃ₜ Sphere4) :=
  ⟨Homeomorph.refl Sphere4⟩

/-- Local Lake/mathlib revision used for this Stage1 audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Source module for the mathlib Poincare markers audited for this slot. -/
def mathlibPoincareSourceModule : String :=
  "Mathlib.Geometry.Manifold.PoincareConjecture"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  mathlibPoincareSourceModule,
  "Mathlib.Geometry.Manifold.Instances.Sphere",
  "Mathlib.AlgebraicTopology.FundamentalGroupoid.SimplyConnected",
  "Mathlib.Topology.Homotopy.Equiv",
  "Mathlib.Topology.Category.TopCat.Sphere",
  "Mathlib.Topology.Homotopy.HomotopyGroup",
  "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvariance"
]

/-- Integration-ready record for Stage1 public item `S1-M-116-PUB-02`. -/
structure MathlibSourcePin where
  revision : String
  moduleName : String

/-- The exact pinned mathlib source anchor requested by `S1-M-116-PUB-02`. -/
def mathlibPoincareSourcePin : MathlibSourcePin where
  revision := mathlibPinnedRevision
  moduleName := mathlibPoincareSourceModule

/-- Sanity check: the requested Poincare source module is included in the anchor list. -/
theorem mathlibPoincareSourceModule_mem_anchorModules :
    mathlibPoincareSourceModule ∈ mathlibAnchorModules := by
  native_decide

/-- Sanity check: the PUB-02 source pin records the requested revision. -/
theorem mathlibPoincareSourcePin_revision :
    mathlibPoincareSourcePin.revision =
      "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Sanity check: the PUB-02 source pin records the requested source module. -/
theorem mathlibPoincareSourcePin_moduleName :
    mathlibPoincareSourcePin.moduleName =
      "Mathlib.Geometry.Manifold.PoincareConjecture" :=
  rfl

/--
Source-level mathlib markers audited in `Mathlib.Geometry.Manifold.PoincareConjecture`.

These names appear as `proof_wanted` declarations in the pinned mathlib source,
not as importable theorem constants in this local environment.
-/
def mathlibProofWantedMarkers : List String := [
  "ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere",
  "SimplyConnectedSpace.nonempty_homeomorph_sphere_three",
  "SimplyConnectedSpace.nonempty_diffeomorph_sphere_three",
  "exists_homeomorph_isEmpty_diffeomorph_sphere_seven",
  "exists_open_nonempty_homeomorph_isEmpty_diffeomorph_euclideanSpace_four"
]

/--
Public-item `S1-M-116-PUB-03` boundary.

The Poincare entries above are source markers emitted by mathlib's
`proof_wanted` command in the pinned source file.  They are not importable proof
constants available to close `StatementShape` in this repository.
-/
def mathlibPoincareProofWantedSourceStatus : String :=
  "proof_wanted_source_markers_not_importable_proof_constants"

/-- Boolean form of the PUB-03 source-marker classification. -/
def mathlibPoincareMarkersAreImportableProofConstants : Bool :=
  false

/-- Checked sanity theorem for the PUB-03 source-marker classification. -/
theorem mathlibPoincareMarkersAreImportableProofConstants_eq_false :
    mathlibPoincareMarkersAreImportableProofConstants = false :=
  rfl

/-- Search terms that did not locate a terminal importable 4D Poincare theorem in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "PoincareConjecture",
  "Poincare",
  "nonempty_homeomorph_sphere",
  "SimplyConnectedSpace.nonempty_homeomorph_sphere_four",
  "Sphere4",
  "topological Poincare conjecture",
  "four-dimensional Poincare conjecture",
  "Freedman"
]

/--
Public audit note for integrators.

This declaration is checked bookkeeping: it states the repo-local boundary and
prevents the statement-shape artifact from being mistaken for a proof.
-/
def statementShapePublicBoundaryNote : String :=
  "AwesomeTheorems.Stage1.S1_M_116.StatementShape is the public Lean statement boundary for THM-M-0583; it is not a proof of the four-dimensional Poincare conjecture."

/-- Machine-proof debt classification for the terminal theorem in this artifact. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
PUB-05 gate input: no terminal local Lean proof body for `StatementShape` has
validated in this repository.
-/
def terminalLeanProofBodyValidatedLocally : Bool :=
  false

/--
PUB-05 gate input: no pinned/imported dependency wrapper proving
`StatementShape` has validated in this repository.
-/
def pinnedDependencyWrapperValidatedLocally : Bool :=
  false

/--
PUB-05 completion gate.

THM-M-0583 may leave `formalization_debt` only after one of the two terminal
machine-check routes validates locally.
-/
def thmM0583CompletionPermitted : Bool :=
  terminalLeanProofBodyValidatedLocally || pinnedDependencyWrapperValidatedLocally

/-- Checked sanity theorem for the PUB-05 completion gate. -/
theorem thmM0583CompletionPermitted_eq_false :
    thmM0583CompletionPermitted = false := by
  native_decide

/-- Human-readable PUB-05 status for public backfill. -/
def formalizationDebtUntilTerminalClosure : String :=
  "formalization_debt_until_terminal_proof_body_or_pinned_dependency_wrapper_validates_locally"

/--
Repo-local integration gate for completion.

No terminal Lean 4 proof body or external pinned proof dependency is checked by
this module.  Anchor-only evidence must not be used as a completed state.
-/
def repoLocalIntegrationDebtGate : String :=
  "open_not_repo_local_closed; no_completed_state_claimed; no_repo_local_integration_debt_retained"

/-- Boolean form of the completed-state integration-debt gate. -/
def repoLocalIntegrationDebtRetained : Bool :=
  false

/-- Checked sanity theorem for the Boolean integration-debt gate. -/
theorem repoLocalIntegrationDebtRetained_eq_false :
    repoLocalIntegrationDebtRetained = false :=
  rfl

/-- One M0387-style proof-tree leaf for the future 4D Poincare proof route. -/
structure LeafBudgetItem where
  leafId : String
  package : String
  obligation : String
  status : String
  debtClass : String
  budgetStepLimit : Nat
  repoLocalClosed : Bool

/-- M0387 local proof-step budget used for each future proof leaf. -/
def theoremTreeLeafBudgetLimit : Nat :=
  100

/--
Current M0387-level leaf ledger.

The first seven rows are checked statement/infrastructure rows.  The remaining
rows are open formalization-debt leaves; none is a completed proof of the
terminal four-dimensional Poincare conjecture.
-/
def leafBudgetLedger : List LeafBudgetItem := [
  {
    leafId := "S1-M-116-L001",
    package := "statement_normalization",
    obligation := "Define Euclidean4 and Sphere4 as the local model and target sphere.",
    status := "checked_statement_shape",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-L002",
    package := "statement_normalization",
    obligation := "State compact simply connected topological 4-manifold conclusion as StatementShape.",
    status := "checked_statement_shape",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-L003",
    package := "homotopy_sphere_bridge",
    obligation := "State the homotopy-sphere variant matching mathlib's proof_wanted source marker at n = 4.",
    status := "checked_statement_shape",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-L004",
    package := "sphere_infrastructure",
    obligation := "Verify Sphere4 has the checked IsManifold instance.",
    status := "checked_infrastructure",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-L005",
    package := "sphere_infrastructure",
    obligation := "Verify Sphere4 has the checked CompactSpace instance.",
    status := "checked_infrastructure",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-L006",
    package := "sphere_infrastructure",
    obligation := "Verify Sphere4 has the checked T2Space instance.",
    status := "checked_infrastructure",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-L007",
    package := "fundamental_groupoid_infrastructure",
    obligation := "Verify SimplyConnectedSpace supplies PathConnectedSpace.",
    status := "checked_infrastructure",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-L008",
    package := "invariant_branch",
    obligation := "Prove or import the invariant package connecting compact simply connected topological 4-manifolds to homotopy-sphere data.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-L009",
    package := "homotopy_sphere_bridge",
    obligation := "Formalize the Hurewicz/Whitehead bridge or selected replacement route from invariants to homotopy equivalence.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-L010",
    package := "freedman_topological_surgery",
    obligation := "Formalize or pin the topological 4-manifold handle, cobordism, disk-embedding, or surgery package needed for Freedman's branch.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-L011",
    package := "external_anchor_audit",
    obligation := "Inspect the retained external Lean 4 repositories named in PUB-06 and PUB-07 before using them as evidence, and classify statement-only files separately from proofs.",
    status := "checked_external_anchor_audit",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-L012",
    package := "terminal_closure_gate",
    obligation := "Replace StatementShape by a local proof body or a pinned/imported/checked upstream wrapper that is kernel-closed and placeholder-free.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  }
]

/-- The current local leaf ledger has twelve rows. -/
theorem leafBudgetLedger_length : leafBudgetLedger.length = 12 := by
  native_decide

/-- The current local leaf ledger stays within the M0387 `<=100` row budget. -/
theorem leafBudgetLedger_length_le_100 :
    leafBudgetLedger.length ≤ theoremTreeLeafBudgetLimit := by
  native_decide

/-! ## PUB-09 theorem-tree package split -/

/--
Invariant-package leaves for the future theorem tree.

These rows are formalization-debt planning leaves only.  They do not prove the
terminal theorem and cannot be used as completion evidence.
-/
def invariantPackageLeafLedger : List LeafBudgetItem := [
  {
    leafId := "S1-M-116-P09-I001",
    package := "invariant",
    obligation := "Normalize the closed topological 4-manifold hypotheses into reusable local invariant predicates.",
    status := "checked_statement_shape",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-P09-I002",
    package := "invariant",
    obligation := "Audit or build singular-homology and fundamental-group invariant APIs for compact simply connected 4-manifolds.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-I003",
    package := "invariant",
    obligation := "Bridge SimplyConnectedSpace to the vanishing fundamental-group statements required by the selected route.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-I004",
    package := "invariant",
    obligation := "Record the homology-sphere invariant target, including H_0, H_4, and middle-dimensional constraints.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-I005",
    package := "invariant",
    obligation := "Connect compactness, Hausdorffness, and manifold chart hypotheses to the invariant package hypotheses.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  }
]

/--
Homotopy-sphere bridge leaves for the future theorem tree.

The checked row is the local statement-shape bridge.  The open rows identify
formalization-debt leaves needed before this package can act as proof evidence.
-/
def homotopySphereBridgePackageLeafLedger : List LeafBudgetItem := [
  {
    leafId := "S1-M-116-P09-H001",
    package := "homotopy_sphere_bridge",
    obligation := "Keep the dimension-4 homotopy-sphere statement shape aligned with mathlib's generalized Poincare source marker.",
    status := "checked_statement_shape",
    debtClass := "none_for_this_leaf",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := true
  },
  {
    leafId := "S1-M-116-P09-H002",
    package := "homotopy_sphere_bridge",
    obligation := "Formalize or import the homology-sphere to homotopy-sphere bridge chosen for the topological route.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-H003",
    package := "homotopy_sphere_bridge",
    obligation := "Audit Hurewicz, Whitehead, and homotopy-equivalence APIs needed by the bridge.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-H004",
    package := "homotopy_sphere_bridge",
    obligation := "State the terminal bridge lemma from the selected invariant package output to `M ≃ₕ Sphere4`.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-H005",
    package := "homotopy_sphere_bridge",
    obligation := "Connect the bridge output to `HomotopySphereFourStatementShape` without changing the theorem's proof status.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  }
]

/--
Freedman/topological-surgery leaves for the future theorem tree.

This package is entirely open formalization debt in the current repository.
-/
def freedmanTopologicalSurgeryPackageLeafLedger : List LeafBudgetItem := [
  {
    leafId := "S1-M-116-P09-F001",
    package := "freedman_topological_surgery",
    obligation := "Select the exact topological 4-manifold classification theorem or pinned upstream theorem to serve as the Freedman branch target.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-F002",
    package := "freedman_topological_surgery",
    obligation := "Formalize or pin the topological handle and cobordism infrastructure required by the selected route.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-F003",
    package := "freedman_topological_surgery",
    obligation := "Formalize or pin the disk-embedding theorem dependency boundary, including any tameness or local-flatness hypotheses.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-F004",
    package := "freedman_topological_surgery",
    obligation := "Record the intersection-form and Kirby-Siebenmann invariant branch conditions needed by the classification theorem.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-F005",
    package := "freedman_topological_surgery",
    obligation := "State the simply connected closed topological 4-manifold to homotopy-sphere classification bridge.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  },
  {
    leafId := "S1-M-116-P09-F006",
    package := "freedman_topological_surgery",
    obligation := "Integrate any external formal proof only through a pinned/imported/checked dependency wrapper or record a concrete blocker.",
    status := "unchecked",
    debtClass := "formalization_debt",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalClosed := false
  }
]

/-- One package in the PUB-09 theorem-tree split. -/
structure TheoremTreePackage where
  packageId : String
  packageName : String
  role : String
  leafLedger : List LeafBudgetItem
  status : String

/-- PUB-09 theorem-tree split required before any completion upgrade. -/
def theoremTreePackageSplit : List TheoremTreePackage := [
  {
    packageId := "S1-M-116-P09-invariant",
    packageName := "invariant",
    role := "Normalize manifold hypotheses and derive the invariant data needed by the later bridge.",
    leafLedger := invariantPackageLeafLedger,
    status := "partially_checked_statement_shape_with_open_formalization_debt"
  },
  {
    packageId := "S1-M-116-P09-homotopy-sphere-bridge",
    packageName := "homotopy_sphere_bridge",
    role := "Bridge invariant data to an explicit homotopy equivalence with Sphere4.",
    leafLedger := homotopySphereBridgePackageLeafLedger,
    status := "partially_checked_statement_shape_with_open_formalization_debt"
  },
  {
    packageId := "S1-M-116-P09-freedman-topological-surgery",
    packageName := "freedman_topological_surgery",
    role := "Supply or pin the Freedman/topological-surgery classification package.",
    leafLedger := freedmanTopologicalSurgeryPackageLeafLedger,
    status := "unchecked_formalization_debt"
  }
]

/-- The PUB-09 theorem tree is split into exactly three packages. -/
theorem theoremTreePackageSplit_length :
    theoremTreePackageSplit.length = 3 := by
  native_decide

/-- The invariant package has a local leaf ledger under the M0387 cap. -/
theorem invariantPackageLeafLedger_length_le_100 :
    invariantPackageLeafLedger.length ≤ theoremTreeLeafBudgetLimit := by
  native_decide

/-- The homotopy-sphere bridge package has a local leaf ledger under the M0387 cap. -/
theorem homotopySphereBridgePackageLeafLedger_length_le_100 :
    homotopySphereBridgePackageLeafLedger.length ≤ theoremTreeLeafBudgetLimit := by
  native_decide

/-- The Freedman/topological-surgery package has a local leaf ledger under the M0387 cap. -/
theorem freedmanTopologicalSurgeryPackageLeafLedger_length_le_100 :
    freedmanTopologicalSurgeryPackageLeafLedger.length ≤ theoremTreeLeafBudgetLimit := by
  native_decide

/-- Checked PUB-09 sanity theorem: every package ledger is below the leaf cap. -/
theorem theoremTreePackageSplit_all_leaf_ledgers_le_100 :
    theoremTreePackageSplit.all
      (fun package => package.leafLedger.length ≤ theoremTreeLeafBudgetLimit) = true := by
  native_decide

/--
PUB-09 completion gate.

The theorem tree is now split into the required three packages with checked
leaf-ledger caps, but the terminal theorem remains open because the proof
leaves are not repo-local closed.
-/
def pub09PackageSplitGateStatus : String :=
  "three_package_split_checked; each_package_leaf_ledger_le_100; terminal_theorem_still_formalization_debt"

/-! ## External anchor audit: `lean-dojo/LeanMillenniumPrizeProblems` -/

/--
Checked bookkeeping record for a pinned external Lean anchor audit.

The fields record source identity and classification only.  They do not import
or prove the four-dimensional Poincare theorem.
-/
structure ExternalLeanAnchorAudit where
  repoSlug : String
  commit : String
  inspected : Bool
  leanToolchain : String
  mathlibInputRevision : String
  poincareModule : String
  theoremOrDefinitionNames : List String
  classification : String
  fourDimensionalTerminalProofImported : Bool
  repoLocalClosureStatus : String

/--
PUB-06 audit record for `lean-dojo/LeanMillenniumPrizeProblems`.

At commit `540da94826f70f3edf4d4fc66ce6cda20e903f61`, the Poincare module
contains statement-shape declarations for the three-dimensional Clay problem
and the generalized Poincare conjecture, plus a checked `n = 0` generalized
case.  It does not provide or import a terminal four-dimensional Poincare proof
for `StatementShape`.
-/
def leanMillenniumPrizeProblemsAudit : ExternalLeanAnchorAudit where
  repoSlug := "lean-dojo/LeanMillenniumPrizeProblems"
  commit := "540da94826f70f3edf4d4fc66ce6cda20e903f61"
  inspected := true
  leanToolchain := "leanprover/lean4:v4.26.0"
  mathlibInputRevision := "v4.26.0"
  poincareModule := "Problems/Poincare/Millennium.lean"
  theoremOrDefinitionNames := [
    "MillenniumPoincare.PoincareConjecture3",
    "MillenniumPoincare.GeneralizedPoincareConjecture",
    "MillenniumPoincare.generalizedPoincareConjecture_zero"
  ]
  classification :=
    "external_upstream_anchor_only_statement_artifact; no_four_dimensional_terminal_poincare_proof"
  fourDimensionalTerminalProofImported := false
  repoLocalClosureStatus :=
    "not_repo_local_closed_for_THM-M-0583; no_completed_state_claimed"

/-- PUB-06 sanity check: the audited external commit is the requested pin. -/
theorem leanMillenniumPrizeProblemsAudit_commit :
    leanMillenniumPrizeProblemsAudit.commit =
      "540da94826f70f3edf4d4fc66ce6cda20e903f61" :=
  rfl

/-- PUB-06 sanity check: the external repository was inspected for this child. -/
theorem leanMillenniumPrizeProblemsAudit_inspected :
    leanMillenniumPrizeProblemsAudit.inspected = true :=
  rfl

/--
PUB-06 terminal-proof gate: the audited external repository is not a
repo-local four-dimensional Poincare proof dependency.
-/
theorem leanMillenniumPrizeProblemsAudit_no_fourDimensionalProofImported :
    leanMillenniumPrizeProblemsAudit.fourDimensionalTerminalProofImported = false :=
  rfl

/--
PUB-07 audit record for `google-deepmind/formal-conjectures`.

At commit `686d32e672974920ca8525aef4a87281bd0cf146`, the Poincare material is
in `FormalConjectures/Millenium/Poincare.lean`.  That file states generalized
topological and smooth Poincare predicates and includes named Poincare entries,
including the four-dimensional topological variant and the still-open smooth
four-dimensional variant, with placeholder proof bodies.  It is statement-level
evidence, not a terminal Lean 4 proof dependency for this repository.
-/
def googleDeepMindFormalConjecturesAudit : ExternalLeanAnchorAudit where
  repoSlug := "google-deepmind/formal-conjectures"
  commit := "686d32e672974920ca8525aef4a87281bd0cf146"
  inspected := true
  leanToolchain := "leanprover/lean4:v4.27.0"
  mathlibInputRevision := "v4.27.0"
  poincareModule := "FormalConjectures/Millenium/Poincare.lean"
  theoremOrDefinitionNames := [
    "PoincareConjecture.ConjectureFor",
    "PoincareConjecture.poincare_conjecture",
    "PoincareConjecture.poincare_conjecture.variants.dimension_two",
    "PoincareConjecture.poincare_conjecture.variants.dimension_ge_five",
    "PoincareConjecture.poincare_conjecture.variants.dimension_four",
    "PoincareConjecture.SmoothConjectureFor",
    "PoincareConjecture.poincare_conjecture.variants.smooth_for_three",
    "PoincareConjecture.poincare_conjecture.variants.smooth_implication",
    "PoincareConjecture.SmoothTrueValues",
    "PoincareConjecture.poincare_conjecture.variants.smooth_known_cases",
    "PoincareConjecture.poincare_conjecture.variants.smooth_dimension_four",
    "PoincareConjecture.poincare_conjecture.variants.smooth_other_cases"
  ]
  classification :=
    "external_upstream_anchor_only_statement_file_with_placeholder_bodies; no_four_dimensional_terminal_poincare_proof"
  fourDimensionalTerminalProofImported := false
  repoLocalClosureStatus :=
    "not_repo_local_closed_for_THM-M-0583; no_completed_state_claimed"

/-- PUB-07 sanity check: the audited external commit is the requested pin. -/
theorem googleDeepMindFormalConjecturesAudit_commit :
    googleDeepMindFormalConjecturesAudit.commit =
      "686d32e672974920ca8525aef4a87281bd0cf146" :=
  rfl

/-- PUB-07 sanity check: the external repository was inspected for this child. -/
theorem googleDeepMindFormalConjecturesAudit_inspected :
    googleDeepMindFormalConjecturesAudit.inspected = true :=
  rfl

/--
PUB-07 terminal-proof gate: the audited external repository is not a
repo-local four-dimensional Poincare proof dependency.
-/
theorem googleDeepMindFormalConjecturesAudit_no_fourDimensionalProofImported :
    googleDeepMindFormalConjecturesAudit.fourDimensionalTerminalProofImported = false :=
  rfl

/-- External repositories audited so far for this Stage1 slot. -/
def auditedExternalLeanAnchors : List String := [
  leanMillenniumPrizeProblemsAudit.repoSlug,
  googleDeepMindFormalConjecturesAudit.repoSlug
]

/--
PUB-08 integration gate.

The external audits retained for this Stage1 slot found statement artifacts and
placeholder files, but no terminal Lean 4 proof candidate for the
four-dimensional topological Poincare theorem.  Therefore there is currently no
external proof dependency to pin/import/check and no Lake/toolchain/license
blocker to record for such a dependency.
-/
def externalTerminalProofCandidateFound : Bool :=
  false

/-- Checked PUB-08 sanity theorem: no external terminal proof candidate was found. -/
theorem externalTerminalProofCandidateFound_eq_false :
    externalTerminalProofCandidateFound = false := by
  native_decide

/--
Checked PUB-08 sanity theorem: neither audited external anchor is imported as a
terminal four-dimensional proof dependency.
-/
theorem auditedExternalAnchors_no_fourDimensionalProofImported :
    leanMillenniumPrizeProblemsAudit.fourDimensionalTerminalProofImported = false ∧
      googleDeepMindFormalConjecturesAudit.fourDimensionalTerminalProofImported = false :=
  ⟨rfl, rfl⟩

/--
PUB-08 public status.

Anchor-only evidence remains non-completing evidence.  If a later audit finds a
terminal Lean 4 proof, this status must be replaced by a pinned/imported/checked
dependency wrapper or by a concrete Lake/toolchain/license blocker.
-/
def pub08ExternalProofGateStatus : String :=
  "no_external_lean4_terminal_proof_found; no_pin_import_check_candidate; anchor_only_evidence_not_completed"

/- The current PUB-08 blocker status: not applicable because no external proof
candidate was found after the retained external audits. -/
def pub08ExternalProofIntegrationBlocker : String :=
  "not_applicable_no_external_terminal_proof_candidate_found_after_pub06_pub07_audits"

/-- Sanity check: the PUB-06 repository appears in the audited-anchor list. -/
theorem leanMillenniumPrizeProblems_mem_auditedExternalLeanAnchors :
    "lean-dojo/LeanMillenniumPrizeProblems" ∈ auditedExternalLeanAnchors := by
  native_decide

/-- Sanity check: the PUB-07 repository appears in the audited-anchor list. -/
theorem googleDeepMindFormalConjectures_mem_auditedExternalLeanAnchors :
    "google-deepmind/formal-conjectures" ∈ auditedExternalLeanAnchors := by
  native_decide

/-! ## PUB-10 public-surface synchronization gate -/

/--
Integration-ready public-surface synchronization gate.

This record is checked bookkeeping only.  It tells the later serial integrator
which public surfaces may be synchronized after the local validation and audit
gates are coherent.  It does not edit shared public docs and does not upgrade
the terminal theorem out of formalization debt.
-/
structure PublicSurfaceSynchronizationGate where
  publicTaskId : String
  stablePublicMergeTargets : List String
  privateChildLedger : String
  localValidationCommand : String
  machineAnchorClassification : String
  leafLedgerStatus : String
  repoLocalIntegrationDebtRetained : Bool
  publicDocsEditedByThisWorker : Bool
  readyForSerialPublicBackfill : Bool
  completionUpgradePermitted : Bool

/--
PUB-10 synchronization gate for THM-M-0583.

The local Lean artifact now has coherent statement-shape anchors, mathlib
source-marker classification, external-anchor classification, and theorem-tree
leaf ledgers.  Public blueprint/todo/README/meta synchronization still belongs
to a serial integrator because those surfaces are outside this worker's write
scope.
-/
def pub10PublicSurfaceSynchronizationGate : PublicSurfaceSynchronizationGate where
  publicTaskId := "S1-M-116-PUB-10"
  stablePublicMergeTargets := [
    "Docs/Stage1_Blueprint.md",
    "Docs/todos_20260430.md",
    "README.md",
    "THM-M-0583/meta.json"
  ]
  privateChildLedger :=
    ".cron/results/stage1_20260430_child/codex_workers/S1-M-116-C010.md"
  localValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_116.lean"
  machineAnchorClassification :=
    "mathlib_proof_wanted_source_markers_not_importable; audited_external_sources_anchor_only_or_statement_placeholder; no_external_terminal_proof_candidate_found"
  leafLedgerStatus :=
    "leafBudgetLedger_length_le_100_and_three_package_split_all_leaf_ledgers_le_100_checked"
  repoLocalIntegrationDebtRetained := repoLocalIntegrationDebtRetained
  publicDocsEditedByThisWorker := false
  readyForSerialPublicBackfill := true
  completionUpgradePermitted := thmM0583CompletionPermitted

/-- Checked PUB-10 gate: this child did not edit shared public docs. -/
theorem pub10PublicSurfaceSynchronizationGate_publicDocsEditedByThisWorker :
    pub10PublicSurfaceSynchronizationGate.publicDocsEditedByThisWorker = false :=
  rfl

/-- Checked PUB-10 gate: the record is ready for a later serial public backfill. -/
theorem pub10PublicSurfaceSynchronizationGate_readyForSerialPublicBackfill :
    pub10PublicSurfaceSynchronizationGate.readyForSerialPublicBackfill = true :=
  rfl

/-- Checked PUB-10 gate: no completed-state repo-local integration debt is retained. -/
theorem pub10PublicSurfaceSynchronizationGate_no_repoLocalIntegrationDebtRetained :
    pub10PublicSurfaceSynchronizationGate.repoLocalIntegrationDebtRetained = false :=
  rfl

/-- Checked PUB-10 gate: public backfill must not be a terminal completion upgrade. -/
theorem pub10PublicSurfaceSynchronizationGate_no_completionUpgrade :
    pub10PublicSurfaceSynchronizationGate.completionUpgradePermitted = false := by
  native_decide

/-- Checked PUB-10 gate: the blueprint is one of the stable merge targets. -/
theorem pub10Stage1Blueprint_mem_stablePublicMergeTargets :
    "Docs/Stage1_Blueprint.md" ∈
      pub10PublicSurfaceSynchronizationGate.stablePublicMergeTargets := by
  native_decide

/-! ## Audit probes -/

#check StatementShape
#check ClosedSimplyConnectedTopologicalFourManifold
#check NamedStatementShape
#check namedStatementShape_iff_statementShape
#check HomotopySphereFourStatementShape
#check sphere4_isManifold
#check sphere4_compact
#check sphere4_t2
#check simplyConnected_implies_pathConnected
#check sphere4_self_homeomorph
#check mathlibPinnedRevision
#check mathlibPoincareSourceModule
#check mathlibAnchorModules
#check MathlibSourcePin
#check mathlibPoincareSourcePin
#check mathlibPoincareSourceModule_mem_anchorModules
#check mathlibPoincareSourcePin_revision
#check mathlibPoincareSourcePin_moduleName
#check mathlibProofWantedMarkers
#check mathlibPoincareProofWantedSourceStatus
#check mathlibPoincareMarkersAreImportableProofConstants_eq_false
#check absentTerminalSearchTerms
#check statementShapePublicBoundaryNote
#check machineProofDebtClassification
#check terminalLeanProofBodyValidatedLocally
#check pinnedDependencyWrapperValidatedLocally
#check thmM0583CompletionPermitted
#check thmM0583CompletionPermitted_eq_false
#check formalizationDebtUntilTerminalClosure
#check repoLocalIntegrationDebtGate
#check repoLocalIntegrationDebtRetained_eq_false
#check leafBudgetLedger
#check leafBudgetLedger_length
#check leafBudgetLedger_length_le_100
#check invariantPackageLeafLedger
#check homotopySphereBridgePackageLeafLedger
#check freedmanTopologicalSurgeryPackageLeafLedger
#check TheoremTreePackage
#check theoremTreePackageSplit
#check theoremTreePackageSplit_length
#check invariantPackageLeafLedger_length_le_100
#check homotopySphereBridgePackageLeafLedger_length_le_100
#check freedmanTopologicalSurgeryPackageLeafLedger_length_le_100
#check theoremTreePackageSplit_all_leaf_ledgers_le_100
#check pub09PackageSplitGateStatus
#check ExternalLeanAnchorAudit
#check leanMillenniumPrizeProblemsAudit
#check leanMillenniumPrizeProblemsAudit_commit
#check leanMillenniumPrizeProblemsAudit_inspected
#check leanMillenniumPrizeProblemsAudit_no_fourDimensionalProofImported
#check googleDeepMindFormalConjecturesAudit
#check googleDeepMindFormalConjecturesAudit_commit
#check googleDeepMindFormalConjecturesAudit_inspected
#check googleDeepMindFormalConjecturesAudit_no_fourDimensionalProofImported
#check auditedExternalLeanAnchors
#check externalTerminalProofCandidateFound
#check externalTerminalProofCandidateFound_eq_false
#check auditedExternalAnchors_no_fourDimensionalProofImported
#check pub08ExternalProofGateStatus
#check pub08ExternalProofIntegrationBlocker
#check leanMillenniumPrizeProblems_mem_auditedExternalLeanAnchors
#check googleDeepMindFormalConjectures_mem_auditedExternalLeanAnchors
#check PublicSurfaceSynchronizationGate
#check pub10PublicSurfaceSynchronizationGate
#check pub10PublicSurfaceSynchronizationGate_publicDocsEditedByThisWorker
#check pub10PublicSurfaceSynchronizationGate_readyForSerialPublicBackfill
#check pub10PublicSurfaceSynchronizationGate_no_repoLocalIntegrationDebtRetained
#check pub10PublicSurfaceSynchronizationGate_no_completionUpgrade
#check pub10Stage1Blueprint_mem_stablePublicMergeTargets

end AwesomeTheorems.Stage1.S1_M_116
