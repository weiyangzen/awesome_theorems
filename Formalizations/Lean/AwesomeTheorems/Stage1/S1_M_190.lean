import Mathlib.Analysis.InnerProductSpace.MeanErgodic
import Mathlib.Dynamics.Ergodic.Ergodic

/-!
# S1-M-190 / THM-M-1522: Ergodic theory

This Stage1 artifact records a conservative Lean 4 boundary for the slogan
"time average equals space average".

The repo-local checked part is the Hilbert-space von Neumann mean ergodic
theorem already present in the pinned mathlib snapshot: Cesaro averages of a
contracting operator converge to the orthogonal projection onto its fixed
subspace.  The stronger Birkhoff/Koopman statement identifying that projection
with integration over an ergodic probability space is kept as an explicit bridge
boundary, not as a completed theorem.
-/

noncomputable section

open Filter
open scoped Topology

namespace AwesomeTheorems.Stage1.S1_M_190

universe u v

variable {𝕜 : Type u} {E : Type v}
variable [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E]

/--
The fixed-vector subspace of a linear time-evolution operator.

In the usual Koopman/L2 reading, later bridge work should identify this
subspace with the constant functions when the measure-preserving system is
ergodic.
-/
abbrev FixedSubspace (U : E →L[𝕜] E) : Submodule 𝕜 E :=
  LinearMap.eqLocus U 1

/--
The Hilbert-space "space average" supplied by mathlib's mean ergodic theorem:
orthogonal projection onto the fixed-vector subspace.
-/
abbrev SpaceAverageProjection (U : E →L[𝕜] E) (x : E) : E :=
  ((FixedSubspace U).orthogonalProjection x : E)

/-- Time averages along iterates of a linear evolution operator. -/
abbrev TimeAverage (U : E →L[𝕜] E) : ℕ → E → E :=
  birkhoffAverage 𝕜 U _root_.id

/--
The checked Hilbert-space conclusion: operator time averages converge to the
orthogonal projection onto fixed vectors.
-/
def MeanErgodicConclusion (U : E →L[𝕜] E) : Prop :=
  ∀ x : E, Tendsto (fun n : ℕ => TimeAverage U n x) atTop
    (𝓝 (SpaceAverageProjection U x))

/--
Stage1 statement shape for the repo-local checked mean-ergodic anchor.

This is not the full pointwise Birkhoff theorem.  It is the Hilbert-space
operator statement that supplies the safest current mathlib anchor for this
slot.
-/
def MeanErgodicStatementShape (𝕜 : Type u) (E : Type v)
    [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E] : Prop :=
  ∀ U : E →L[𝕜] E, ‖U‖ ≤ 1 → MeanErgodicConclusion U

/--
Local wrapper around mathlib's von Neumann mean ergodic theorem.
-/
theorem timeAverage_tendsto_spaceAverageProjection
    (U : E →L[𝕜] E) (hU : ‖U‖ ≤ 1) :
    MeanErgodicConclusion U := by
  intro x
  simpa [MeanErgodicConclusion, TimeAverage, SpaceAverageProjection, FixedSubspace]
  using ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection
      (𝕜 := 𝕜) (E := E) U hU x

/-- Checked closure of the normalized mean-ergodic statement shape. -/
theorem meanErgodicStatementShape_from_mathlib :
    MeanErgodicStatementShape 𝕜 E := by
  intro U hU
  exact timeAverage_tendsto_spaceAverageProjection U hU

/--
Data for a declared time-average/space-average interpretation.

The field `spaceAverage_eq_fixedProjection` is the checked bridge available
inside this file.  The two proposition fields isolate the remaining semantic
work needed to turn an informal ergodic-theory or mathematical-physics model
into this Hilbert-space statement.
-/
structure TimeSpaceAverageData (𝕜 : Type u) (E : Type v)
    [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E] :
    Type (max u v) where
  evolution : E →L[𝕜] E
  spaceAverage : E → E
  contractive : ‖evolution‖ ≤ 1
  spaceAverage_eq_fixedProjection : spaceAverage = SpaceAverageProjection evolution
  modeledByMeasurePreservingDynamics : Prop
  fixedSubspaceIdentifiedWithSpatialConstants : Prop

/-- The declared time average equals the declared space average in the limit. -/
def TimeAverageEqualsSpaceAverage
    (D : TimeSpaceAverageData 𝕜 E) : Prop :=
  ∀ x : E, Tendsto (fun n : ℕ => TimeAverage D.evolution n x) atTop
    (𝓝 (D.spaceAverage x))

/--
If the declared space-average operator is the fixed-subspace projection, then
mathlib's mean ergodic theorem proves the time-average convergence.
-/
theorem timeAverageEqualsSpaceAverage_of_projection
    (D : TimeSpaceAverageData 𝕜 E) :
    TimeAverageEqualsSpaceAverage D := by
  intro x
  rw [D.spaceAverage_eq_fixedProjection]
  exact timeAverage_tendsto_spaceAverageProjection D.evolution D.contractive x

/--
Stage1 statement boundary for the full slogan.

This shape requires future bridge hypotheses explaining how a concrete
measure-preserving ergodic system produces the Hilbert operator and why fixed
vectors are exactly spatial constants.  The local proof below uses the
projection equality field and does not claim that the bridge propositions have
already been derived.
-/
def StatementShape : Prop :=
  ∀ (𝕜 : Type u) (E : Type v)
    [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E],
      ∀ D : TimeSpaceAverageData 𝕜 E,
        D.modeledByMeasurePreservingDynamics →
          D.fixedSubspaceIdentifiedWithSpatialConstants →
            TimeAverageEqualsSpaceAverage D

/--
The current Stage1 file closes the abstract Hilbert-space projection wrapper.
The proof deliberately does not use the bridge propositions; those fields remain
the formalization boundary for a concrete Birkhoff/Koopman/integral theorem.
-/
theorem statementShape_of_projection_data : StatementShape.{u, v} := by
  intro 𝕜 E _ _ _ _ D _ _
  exact timeAverageEqualsSpaceAverage_of_projection D

/-- Mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.MeanErgodic",
  "Mathlib.Dynamics.BirkhoffSum.NormedSpace",
  "Mathlib.Dynamics.BirkhoffSum.Average",
  "Mathlib.Dynamics.Ergodic.Ergodic",
  "Mathlib.Dynamics.Ergodic.MeasurePreserving",
  "Mathlib.MeasureTheory.Measure.Typeclasses.Probability"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection",
  "LinearMap.tendsto_birkhoffAverage_of_ker_subset_closure",
  "birkhoffAverage",
  "birkhoffSum",
  "LinearMap.eqLocus",
  "Submodule.orthogonalProjection",
  "Ergodic",
  "PreErgodic",
  "MeasureTheory.MeasurePreserving"
]

/-- Primary-source URLs at the pinned mathlib revision audited for this slot. -/
def primarySourceAnchors : List String := [
  "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/InnerProductSpace/MeanErgodic.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Dynamics/Ergodic/Ergodic.lean"
]

/-- Pinned mathlib revision used for the checked Hilbert-space wrapper. -/
def meanErgodicMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Pinned mathlib module containing the upstream mean-ergodic theorem. -/
def meanErgodicMathlibModule : String :=
  "Mathlib.Analysis.InnerProductSpace.MeanErgodic"

/--
Machine-status wording justified for the Hilbert-space mean-ergodic wrapper.

The proof body is imported from pinned mathlib and checked through the local
wrapper theorem `timeAverage_tendsto_spaceAverageProjection`.
-/
def hilbertMeanErgodicWrapperMachineStatus : String :=
  "local_wrapper_upstream_mathlib"

/--
Public-status boundary for the broader ergodic-theory slogan.

The Hilbert-space projection wrapper is locally checked.  The concrete
Birkhoff/Koopman/spatial-integral interpretation still needs a future
measure-theoretic bridge or a pinned/imported/checked external Lean proof.
-/
def fullBirkhoffKoopmanBridgeStatus : String :=
  "formalization_debt"

/--
Machine-status boundary for the full bridge.

This is separate from `hilbertMeanErgodicWrapperMachineStatus`: the local file
contains a checked wrapper for the Hilbert-space mean-ergodic theorem, but it
does not yet contain a repo-local closure of the concrete Koopman/integral
interpretation.
-/
def fullBirkhoffKoopmanBridgeMachineStatus : String :=
  "not_repo_local_closed"

/--
Open bridge leaves that must be supplied before the informal ergodic-theory
slogan can be counted as a completed Birkhoff/Koopman/spatial-integral theorem.
-/
def fullBirkhoffKoopmanBridgeOpenLeaves : List String := [
  "construct a Koopman operator on a concrete L2 or function-space model",
  "prove the Koopman operator is contractive or unitary from measure preservation",
  "identify fixed functions with spatial constants under ergodicity",
  "identify the fixed-subspace projection with spatial integral or conditional expectation",
  "pin/import/check a primary-source Lean 4 proof if one is found externally"
]

/-- Public unchecked bridge leaves requested for the full Koopman/integral theorem. -/
structure UncheckedPublicBridgeLeaf where
  leafId : String
  packageName : String
  localStatus : String
  target : String
  completionGate : String

/--
Unchecked public leaves for the missing Koopman and projection-as-integral
bridge.

These are deliberately metadata leaves, not theorem declarations.  They mark
the exact formalization work that must remain open until supplied locally or
replaced by a pinned/imported/checked primary-source Lean 4 proof.
-/
def uncheckedPublicBridgeLeaves : List UncheckedPublicBridgeLeaf := [
  {
    leafId := "koopman_operator_construction"
    packageName := "measure_ergodic_bridge"
    localStatus := "unchecked_formalization_debt"
    target := "construct a Koopman operator on a concrete L2 or function-space model"
    completionGate := "open_until_concrete_koopman_operator_is_checked"
  },
  {
    leafId := "contractive_or_unitary_proof"
    packageName := "measure_ergodic_bridge"
    localStatus := "unchecked_formalization_debt"
    target := "prove the Koopman operator is contractive or unitary from measure preservation"
    completionGate := "open_until_measure_preservation_yields_checked_norm_bound"
  },
  {
    leafId := "fixed_functions_as_constants_under_ergodicity"
    packageName := "measure_ergodic_bridge"
    localStatus := "unchecked_formalization_debt"
    target := "identify fixed functions with spatial constants under ergodicity"
    completionGate := "open_until_ergodicity_constants_identification_is_checked"
  },
  {
    leafId := "projection_as_integral"
    packageName := "spatial_integral_identification"
    localStatus := "unchecked_formalization_debt"
    target := "identify the fixed-subspace projection with spatial integral or conditional expectation"
    completionGate := "open_until_projection_integral_identification_is_checked"
  }
]

/-- Identifiers for the unchecked public bridge leaves. -/
def uncheckedPublicBridgeLeafIds : List String :=
  uncheckedPublicBridgeLeaves.map UncheckedPublicBridgeLeaf.leafId

/-- Checkable guard for the exact unchecked public bridge leaves requested. -/
theorem uncheckedPublicBridgeLeafIds_eq :
    uncheckedPublicBridgeLeafIds = [
      "koopman_operator_construction",
      "contractive_or_unitary_proof",
      "fixed_functions_as_constants_under_ergodicity",
      "projection_as_integral"
    ] := by
  rfl

/-- Status guard: every public bridge leaf remains unchecked formalization debt. -/
theorem uncheckedPublicBridgeLeafStatuses_eq :
    uncheckedPublicBridgeLeaves.map UncheckedPublicBridgeLeaf.localStatus = [
      "unchecked_formalization_debt",
      "unchecked_formalization_debt",
      "unchecked_formalization_debt",
      "unchecked_formalization_debt"
    ] := by
  rfl

/-- Metadata for the Stage1 theorem-tree split requested for THM-M-1522. -/
structure TheoremTreePackage where
  packageName : String
  localStatus : String
  proofSurface : String
  childLeaves : List String
  completionGate : String

/--
M0387-level theorem-tree split for the current Stage1 boundary.

The first four packages describe repo-local checked statement/object/wrapper
surfaces.  The final two packages are intentionally open: the file has not yet
formalized the concrete measure-preserving-system bridge or the identification
of the fixed-subspace projection with a spatial integral.
-/
def theoremTreeSplit : List TheoremTreePackage := [
  {
    packageName := "statement_normalization"
    localStatus := "checked_statement_boundary"
    proofSurface := "MeanErgodicStatementShape, StatementShape"
    childLeaves := [
      "normalize the safe Hilbert-space mean-ergodic target",
      "separate the full Birkhoff/Koopman/integral slogan from the checked target",
      "record bridge hypotheses as explicit fields of TimeSpaceAverageData"
    ]
    completionGate := "closed_for_current_statement_boundary"
  },
  {
    packageName := "mathlib_object_model"
    localStatus := "checked_anchor_table"
    proofSurface := "mathlibAnchorModules, mathlibAnchorNames, primarySourceAnchors"
    childLeaves := [
      "anchor ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection",
      "anchor birkhoffAverage and fixed-subspace projection objects",
      "record audited ergodic and measure-preserving modules without claiming the bridge"
    ]
    completionGate := "closed_for_mean_ergodic_object_model"
  },
  {
    packageName := "mean_ergodic_anchor"
    localStatus := "local_wrapper_upstream_mathlib"
    proofSurface := "timeAverage_tendsto_spaceAverageProjection, meanErgodicStatementShape_from_mathlib"
    childLeaves := [
      "import Mathlib.Analysis.InnerProductSpace.MeanErgodic",
      "wrap ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection",
      "validate the wrapper through the repo-local lake env lean command"
    ]
    completionGate := "closed_by_pinned_mathlib_wrapper"
  },
  {
    packageName := "declared_space_average_wrapper"
    localStatus := "checked_projection_wrapper"
    proofSurface := "TimeSpaceAverageData, TimeAverageEqualsSpaceAverage, timeAverageEqualsSpaceAverage_of_projection"
    childLeaves := [
      "require the declared spaceAverage to equal the fixed-subspace projection",
      "derive declared time-average convergence from the checked mean-ergodic wrapper",
      "keep modeledByMeasurePreservingDynamics and fixedSubspaceIdentifiedWithSpatialConstants as boundary propositions"
    ]
    completionGate := "closed_for_projection_declared_data_only"
  },
  {
    packageName := "measure_ergodic_bridge"
    localStatus := "unchecked_formalization_debt"
    proofSurface := "future Koopman and ergodicity bridge"
    childLeaves := [
      "construct a Koopman operator on a concrete L2 or function-space model",
      "prove the Koopman operator is contractive or unitary from measure preservation",
      "identify fixed functions with spatial constants under ergodicity"
    ]
    completionGate := "open_until_local_bridge_or_pinned_imported_checked_external_proof"
  },
  {
    packageName := "spatial_integral_identification"
    localStatus := "unchecked_formalization_debt"
    proofSurface := "future projection-as-integral or conditional-expectation theorem"
    childLeaves := [
      "define the concrete spatial integral or conditional expectation target",
      "identify the fixed-subspace projection with that spatial operator",
      "connect the identified operator back to the declared spaceAverage field"
    ]
    completionGate := "open_until_projection_integral_identification_is_checked"
  }
]

/-- Package names in the requested theorem-tree split. -/
def theoremTreePackageNames : List String :=
  theoremTreeSplit.map TheoremTreePackage.packageName

/-- Checkable guard that the public theorem-tree split contains the requested packages. -/
theorem theoremTreePackageNames_eq :
    theoremTreePackageNames = [
      "statement_normalization",
      "mathlib_object_model",
      "mean_ergodic_anchor",
      "declared_space_average_wrapper",
      "measure_ergodic_bridge",
      "spatial_integral_identification"
    ] := by
  rfl

/--
Completion gate for future work: anchor-only evidence is not enough for this
bridge.  A discovered external Lean 4 proof must be brought into the repo-local
validation closure, or else recorded as a concrete integration blocker while the
slot remains open.
-/
def fullBirkhoffKoopmanBridgeCompletionGate : String :=
  "remain_open_until_local_bridge_or_pinned_imported_checked_external_proof"

/--
Integration-gate metadata for future external Lean 4 proofs of the stronger
bridge.

The current repo-local file has a checked mathlib wrapper for the Hilbert-space
mean-ergodic theorem.  A separate pointwise Birkhoff Lean 4 candidate has been
located, but it has not been pinned, imported, or checked in this repo-local
Lake closure.  Any external candidate must therefore enter the local validation
closure, or the exact dependency/toolchain/license/API blocker must be recorded
while this slot stays open.
-/
structure ExternalBridgeIntegrationGate where
  candidateKind : String
  sourceUrl : String
  sourceCommit : String
  sourceModule : String
  sourceTheoremNames : List String
  sourceToolchain : String
  sourceMathlibRevision : String
  currentEvidenceStatus : String
  requiredRepoLocalAction : String
  blockerIfNotIntegrated : String
  completionStatus : String

/--
Repo-local guardrail for external Birkhoff/Koopman candidates.

These rows are metadata, not theorem completions.  They make the no-anchor-only
rule explicit for the two external proof families relevant to this slot.
-/
def externalBridgeIntegrationGates : List ExternalBridgeIntegrationGate := [
  {
    candidateKind := "pointwise_birkhoff_ergodic_theorem"
    sourceUrl := "https://github.com/lua-vr/pointwise-birkhoff"
    sourceCommit := "fc06094ca0506d8d74eba8b45b34882ce5930bf4"
    sourceModule := "BirkhoffErgodicThm"
    sourceTheoremNames := [
      "birkhoffErgodicTheorem",
      "birkhoffErgodicTheorem'"
    ]
    sourceToolchain := "leanprover/lean4:v4.20.0-rc5"
    sourceMathlibRevision := "83f3832c6cfeecbc8d16b0248c98346956a7f0e5"
    currentEvidenceStatus := "external_candidate_found_not_repo_local_pinned_imported_checked"
    requiredRepoLocalAction := "pin_import_check_primary_source_lean4_proof_if_found"
    blockerIfNotIntegrated :=
      "owned_child_scope_forbids_lake_edits_and_candidate_toolchain_mathlib_do_not_match_repo"
    completionStatus := "not_completed_anchor_only_evidence_is_insufficient"
  },
  {
    candidateKind := "full_koopman_spatial_integral_bridge"
    sourceUrl := "no_full_koopman_bridge_candidate_found_in_this_child"
    sourceCommit := "none"
    sourceModule := "none"
    sourceTheoremNames := []
    sourceToolchain := "none"
    sourceMathlibRevision := "none"
    currentEvidenceStatus := "no_repo_local_pinned_imported_checked_external_candidate"
    requiredRepoLocalAction := "pin_import_check_primary_source_lean4_proof_if_found"
    blockerIfNotIntegrated := "record_exact_dependency_toolchain_license_or_api_blocker"
    completionStatus := "not_completed_anchor_only_evidence_is_insufficient"
  }
]

/-- Candidate families covered by the external bridge integration gate. -/
def externalBridgeIntegrationGateKinds : List String :=
  externalBridgeIntegrationGates.map ExternalBridgeIntegrationGate.candidateKind

/-- Checkable guard for the two external proof families relevant to this slot. -/
theorem externalBridgeIntegrationGateKinds_eq :
    externalBridgeIntegrationGateKinds = [
      "pointwise_birkhoff_ergodic_theorem",
      "full_koopman_spatial_integral_bridge"
    ] := by
  rfl

/-- Checkable guard that external anchor-only evidence is not a completed state. -/
theorem externalBridgeCompletionStatuses_eq :
    externalBridgeIntegrationGates.map ExternalBridgeIntegrationGate.completionStatus = [
      "not_completed_anchor_only_evidence_is_insufficient",
      "not_completed_anchor_only_evidence_is_insufficient"
    ] := by
  rfl

/-- Checkable guard for the external pointwise Birkhoff source commit recorded here. -/
theorem externalPointwiseBirkhoffSourceCommit_eq :
    (externalBridgeIntegrationGates.map ExternalBridgeIntegrationGate.sourceCommit).head? =
      some "fc06094ca0506d8d74eba8b45b34882ce5930bf4" := by
  rfl

/--
Search terms used to distinguish the checked mean-ergodic wrapper from the
stronger Birkhoff pointwise ergodic theorem and Koopman/integral bridge.
-/
def boundarySearchTerms : List String := [
  "MeanErgodic",
  "tendsto_birkhoffAverage_orthogonalProjection",
  "birkhoffAverage",
  "Birkhoff pointwise ergodic theorem",
  "Koopman",
  "Ergodic",
  "MeasurePreserving",
  "fixed subspace constants",
  "space average integral"
]

/-! ## Audit probes -/

#check MeanErgodicStatementShape
#check meanErgodicStatementShape_from_mathlib
#check StatementShape
#check statementShape_of_projection_data
#check timeAverage_tendsto_spaceAverageProjection
#check ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection
#check Ergodic
#check hilbertMeanErgodicWrapperMachineStatus
#check fullBirkhoffKoopmanBridgeStatus
#check fullBirkhoffKoopmanBridgeMachineStatus
#check fullBirkhoffKoopmanBridgeOpenLeaves
#check UncheckedPublicBridgeLeaf
#check uncheckedPublicBridgeLeaves
#check uncheckedPublicBridgeLeafIds
#check uncheckedPublicBridgeLeafIds_eq
#check uncheckedPublicBridgeLeafStatuses_eq
#check TheoremTreePackage
#check theoremTreeSplit
#check theoremTreePackageNames
#check theoremTreePackageNames_eq
#check fullBirkhoffKoopmanBridgeCompletionGate
#check ExternalBridgeIntegrationGate
#check externalBridgeIntegrationGates
#check externalBridgeIntegrationGateKinds
#check externalBridgeIntegrationGateKinds_eq
#check externalBridgeCompletionStatuses_eq
#check externalPointwiseBirkhoffSourceCommit_eq

end AwesomeTheorems.Stage1.S1_M_190
