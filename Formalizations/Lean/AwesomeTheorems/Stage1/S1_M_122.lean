import Mathlib.Geometry.Manifold.IntegralCurve.Basic
import Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.Riemannian.PathELength
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion
import Mathlib.Geometry.Manifold.VectorBundle.Riemannian
import Mathlib.Topology.MetricSpace.ProperSpace

/-!
# S1-M-122 / THM-M-0166: Hopf-Rinow theorem

This Stage1 file records a conservative Lean 4 boundary for the Hopf-Rinow
theorem for complete Riemannian manifolds.

The pinned mathlib snapshot has a substantial Riemannian-manifold substrate:
Riemannian bundles, `IsRiemannianManifold`, Riemannian path length,
`riemannianEDist`, and local integral-curve existence/uniqueness.  This audit
did not find a terminal Hopf-Rinow theorem, a concrete geodesic equation API, or
the global exponential-map/properness package needed to close the classical
result.

The declarations below therefore normalize the statement boundary and provide
checked wrappers around adjacent mathlib facts.  They introduce no proof
placeholders and make no terminal proof claim for Hopf-Rinow.
-/

noncomputable section

set_option linter.unusedSectionVars false

open scoped Manifold Topology
open Manifold

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_122

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {H : Type v} [TopologicalSpace H]
variable (I : ModelWithCorners ℝ E H)
variable {M : Type w} [TopologicalSpace M] [PseudoEMetricSpace M] [ChartedSpace H M]
variable [Bundle.RiemannianBundle (fun x : M => TangentSpace I x)]
variable [∀ x : M, ENorm (TangentSpace I x)]

/--
Stage1 package for the expected minimizing geodesic between two points.

The currently checked part uses mathlib's Riemannian path-length API.  The
`geodesicEquation` field is deliberately abstract because this audit did not
locate a concrete mathlib definition of geodesics, the Levi-Civita connection,
or the exponential map suitable for the Hopf-Rinow terminal theorem.
-/
structure MinimizingGeodesicPackage (x y : M) : Type (max u w) where
  curve : ℝ → M
  source_eq : curve 0 = x
  target_eq : curve 1 = y
  curve_c1 : ContMDiffOn 𝓘(ℝ, ℝ) I 1 curve (Set.Icc 0 1)
  length_eq_edist : pathELength I curve 0 1 = edist x y
  geodesicEquation : Prop
  geodesicEquation_holds : geodesicEquation

/--
Stage1 terminal conclusion package for Hopf-Rinow.

Classically, complete connected Riemannian manifolds have minimizing geodesics
between points, with equivalent compactness/properness and geodesic-completeness
formulations.  The latter two clauses are kept abstract here until mathlib
provides or imports the required global geodesic/exponential-map bridge.
-/
structure HopfRinowConclusion : Type (max u w) where
  minimizingGeodesic :
    ∀ x y : M, Nonempty (MinimizingGeodesicPackage I x y)
  closedBoundedCompact : Prop
  closedBoundedCompact_holds : closedBoundedCompact
  metricCompleteEquivalentGeodesicComplete : Prop
  metricCompleteEquivalentGeodesicComplete_holds :
    metricCompleteEquivalentGeodesicComplete

/--
Normalized Stage1 statement shape for Hopf-Rinow.

This is a statement boundary only: under metric completeness, connectedness,
smooth manifold structure, and mathlib's Riemannian-manifold predicate, a future
formalization should produce the Hopf-Rinow conclusion package.
-/
def StatementShape : Prop :=
  CompleteSpace M →
    PreconnectedSpace M →
      IsManifold I (⊤ : WithTop ℕ∞) M →
        IsRiemannianManifold I M →
          Nonempty (HopfRinowConclusion I (M := M))

/-- The statement-shape definition unfolds to the normalized Hopf-Rinow package. -/
theorem statementShape_iff :
    StatementShape I (M := M) ↔
      (CompleteSpace M →
        PreconnectedSpace M →
          IsManifold I (⊤ : WithTop ℕ∞) M →
            IsRiemannianManifold I M →
              Nonempty (HopfRinowConclusion I (M := M))) :=
  Iff.rfl

/-! ## Public statement normalization -/

/--
Public statement-normalization boundary for `THM-M-0166`.

This deliberately aliases `AwesomeTheorems.Stage1.S1_M_122.StatementShape`.
It is the current repo-local Lean statement boundary for Hopf-Rinow, not a
terminal Hopf-Rinow theorem.
-/
def PublicStatementNormalization : Prop :=
  StatementShape I (M := M)

/-- The public-normalization boundary is definitionally the same as `StatementShape`. -/
theorem publicStatementNormalization_iff_statementShape :
    PublicStatementNormalization I (M := M) ↔ StatementShape I (M := M) :=
  Iff.rfl

/-- Canonical checked name for the current repo-local statement boundary. -/
def publicStatementBoundaryName : String :=
  "AwesomeTheorems.Stage1.S1_M_122.StatementShape"

/-- Checked metadata for the public statement-normalization backfill. -/
def publicStatementNormalizationNotes : List String := [
  "Use AwesomeTheorems.Stage1.S1_M_122.StatementShape as the current repo-local Lean statement boundary for THM-M-0166.",
  "The boundary assumes metric completeness, connectedness, smooth manifold structure, and IsRiemannianManifold, then asks for a HopfRinowConclusion package.",
  "This is not a terminal Hopf-Rinow theorem: geodesic completeness, the geodesic equation, the exponential map, minimizing geodesic existence, and compact/proper equivalence remain formalization debt."
]

/-- The public statement-normalization metadata is explicitly non-terminal. -/
def publicStatementNormalizationIsTerminal : Bool := false

/-- Sanity check for the non-terminal public-normalization gate. -/
theorem publicStatementNormalizationIsTerminal_eq_false :
    publicStatementNormalizationIsTerminal = false :=
  rfl

/-! ## Missing formal API split -/

/--
The six formal API branches currently missing for a terminal Hopf-Rinow
formalization in this repository.

This is a checked taxonomy for `THM-M-0166.missing-api`; it is not a replacement
for the absent mathematical APIs.
-/
inductive MissingFormalAPI : Type where
  | leviCivitaConnection
  | geodesicEquation
  | riemannianExponentialMap
  | geodesicCompleteness
  | minimizingGeodesicExistence
  | compactProperEquivalence
  deriving DecidableEq, Repr

/-- Canonical public-facing names for the missing Hopf-Rinow API branches. -/
def MissingFormalAPI.canonicalName : MissingFormalAPI → String
  | leviCivitaConnection => "Levi-Civita connection"
  | geodesicEquation => "geodesic equation"
  | riemannianExponentialMap => "Riemannian exponential map"
  | geodesicCompleteness => "geodesic completeness"
  | minimizingGeodesicExistence => "minimizing geodesic existence"
  | compactProperEquivalence => "compact/proper equivalence"

/--
Repo-local machine status for every missing branch.

All six branches remain formalization debt: the adjacent mathlib APIs imported in
this file do not yet expose the terminal Hopf-Rinow theorem package needed here.
-/
def MissingFormalAPI.machineDebt : MissingFormalAPI → String
  | _ => "formalization_debt"

/--
Repo-local completion status for every missing branch.

This deliberately avoids `repo_local_integration_debt`: this child did not find
an external Lean 4 closure that is merely waiting to be pinned/imported.
-/
def MissingFormalAPI.repoLocalStatus : MissingFormalAPI → String
  | _ => "not_repo_local_closed"

/-- Adjacent checked anchors currently available for each missing API branch. -/
def MissingFormalAPI.availableRepoLocalAnchors : MissingFormalAPI → List String
  | leviCivitaConnection => [
      "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
      "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
      "Mathlib.Geometry.Manifold.VectorBundle.Riemannian"
    ]
  | geodesicEquation => [
      "Mathlib.Geometry.Manifold.IntegralCurve.Basic",
      "Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique"
    ]
  | riemannianExponentialMap => []
  | geodesicCompleteness => [
      "CompleteSpace"
    ]
  | minimizingGeodesicExistence => [
      "Manifold.pathELength",
      "Manifold.riemannianEDist",
      "Manifold.exists_lt_of_riemannianEDist_lt"
    ]
  | compactProperEquivalence => [
      "ProperSpace",
      "isCompact_closedBall",
      "complete_of_proper"
    ]

/-- Exact six-way split required by `THM-M-0166.missing-api`. -/
def missingFormalAPIs : List MissingFormalAPI := [
  MissingFormalAPI.leviCivitaConnection,
  MissingFormalAPI.geodesicEquation,
  MissingFormalAPI.riemannianExponentialMap,
  MissingFormalAPI.geodesicCompleteness,
  MissingFormalAPI.minimizingGeodesicExistence,
  MissingFormalAPI.compactProperEquivalence
]

/-- Public names of the six missing formal API branches. -/
def missingFormalAPINames : List String :=
  missingFormalAPIs.map MissingFormalAPI.canonicalName

/-- The missing-API split has exactly six branches. -/
theorem missingFormalAPIs_length :
    missingFormalAPIs.length = 6 :=
  rfl

/-- The missing-API split names exactly six branches. -/
theorem missingFormalAPINames_length :
    missingFormalAPINames.length = 6 :=
  rfl

/-- The Levi-Civita connection branch is listed in the missing-API split. -/
theorem leviCivitaConnection_mem_missingFormalAPIs :
    MissingFormalAPI.leviCivitaConnection ∈ missingFormalAPIs := by
  simp [missingFormalAPIs]

/-- The geodesic equation branch is listed in the missing-API split. -/
theorem geodesicEquation_mem_missingFormalAPIs :
    MissingFormalAPI.geodesicEquation ∈ missingFormalAPIs := by
  simp [missingFormalAPIs]

/-- The Riemannian exponential-map branch is listed in the missing-API split. -/
theorem riemannianExponentialMap_mem_missingFormalAPIs :
    MissingFormalAPI.riemannianExponentialMap ∈ missingFormalAPIs := by
  simp [missingFormalAPIs]

/-- The geodesic-completeness branch is listed in the missing-API split. -/
theorem geodesicCompleteness_mem_missingFormalAPIs :
    MissingFormalAPI.geodesicCompleteness ∈ missingFormalAPIs := by
  simp [missingFormalAPIs]

/-- The minimizing-geodesic-existence branch is listed in the missing-API split. -/
theorem minimizingGeodesicExistence_mem_missingFormalAPIs :
    MissingFormalAPI.minimizingGeodesicExistence ∈ missingFormalAPIs := by
  simp [missingFormalAPIs]

/-- The compact/proper equivalence branch is listed in the missing-API split. -/
theorem compactProperEquivalence_mem_missingFormalAPIs :
    MissingFormalAPI.compactProperEquivalence ∈ missingFormalAPIs := by
  simp [missingFormalAPIs]

/-- No missing-API branch is marked as repo-local integration debt by this child. -/
theorem missingFormalAPI_repoLocalStatus_not_integration_debt
    (api : MissingFormalAPI) :
    api.repoLocalStatus ≠ "repo_local_integration_debt" := by
  cases api <;> decide

/-- Every missing-API branch remains formalization debt. -/
theorem missingFormalAPI_machineDebt_eq_formalization_debt
    (api : MissingFormalAPI) :
    api.machineDebt = "formalization_debt" := by
  cases api <;> rfl

/-- Checked wrapper: a path has zero Riemannian length on a degenerate interval. -/
theorem pathELength_self_wrapper (γ : ℝ → M) (a : ℝ) :
    pathELength I γ a a = 0 := by
  exact pathELength_self

/-- Checked wrapper: Riemannian extended distance from a point to itself is zero. -/
theorem riemannianEDist_self_wrapper
    [∀ x : M, ENormSMulClass ℝ (TangentSpace I x)] (x : M) :
    riemannianEDist I x x = 0 := by
  exact riemannianEDist_self

/-- Checked wrapper: Riemannian extended distance is symmetric. -/
theorem riemannianEDist_comm_wrapper
    [∀ x : M, ENormSMulClass ℝ (TangentSpace I x)] (x y : M) :
    riemannianEDist I x y = riemannianEDist I y x := by
  exact riemannianEDist_comm

/-- Checked wrapper: Riemannian extended distance satisfies the triangle inequality. -/
theorem riemannianEDist_triangle_wrapper
    [∀ x : M, ENormSMulClass ℝ (TangentSpace I x)] (x y z : M) :
    riemannianEDist I x z ≤ riemannianEDist I x y + riemannianEDist I y z := by
  exact riemannianEDist_triangle

/-- Checked wrapper: Riemannian extended distance is bounded by any `C^1` path length. -/
theorem riemannianEDist_le_pathELength_wrapper
    [∀ x : M, ENormSMulClass ℝ (TangentSpace I x)]
    {x y : M} {a b : ℝ} {γ : ℝ → M}
    (hγ : ContMDiffOn 𝓘(ℝ, ℝ) I 1 γ (Set.Icc a b))
    (ha : γ a = x) (hb : γ b = y) (hab : a ≤ b) :
    riemannianEDist I x y ≤ pathELength I γ a b := by
  exact riemannianEDist_le_pathELength hγ ha hb hab

/--
Checked wrapper: if `r` is larger than the Riemannian extended distance, mathlib
constructs a `C^1` path from `x` to `y` of length `< r`.

This is an approximation/infimum anchor, not a Hopf-Rinow minimizing-geodesic
existence theorem.
-/
theorem exists_short_path_of_riemannianEDist_lt {x y : M} {r : ENNReal}
    (hr : riemannianEDist I x y < r) :
    ∃ γ : ℝ → M, γ 0 = x ∧ γ 1 = y ∧
      ContMDiffOn 𝓘(ℝ, ℝ) I 1 γ (Set.Icc 0 1) ∧ pathELength I γ 0 1 < r := by
  exact exists_lt_of_riemannianEDist_lt hr

/-- Checked wrapper: compact pseudo-metric spaces are proper. -/
theorem compact_space_gives_proper_space
    {X : Type*} [PseudoMetricSpace X] [CompactSpace X] : ProperSpace X := by
  infer_instance

/-- Checked wrapper: proper pseudo-metric spaces are complete. -/
theorem proper_space_gives_complete_space
    {X : Type*} [PseudoMetricSpace X] [ProperSpace X] : CompleteSpace X := by
  infer_instance

/-- Checked wrapper: closed balls are compact in a proper pseudo-metric space. -/
theorem proper_space_closedBall_compact
    {X : Type*} [PseudoMetricSpace X] [ProperSpace X] (x : X) (r : ℝ) :
    IsCompact (Metric.closedBall x r) := by
  exact isCompact_closedBall x r

/-! ## Metric bridge audit -/

/--
Ordered bridge nodes for the intended Hopf-Rinow metric formulation.

The order is intentionally explicit: mathlib's Riemannian metric first builds
an extended metric, while `ProperSpace` currently lives over a real-valued
`PseudoMetricSpace`.
-/
inductive MetricBridgeNode : Type where
  | riemannianExtendedDistance
  | pseudoEMetricOfRiemannianMetric
  | eMetricOfRiemannianMetric
  | finiteDistancePseudoMetric
  | metricCompleteness
  | metricProperness
  deriving DecidableEq, Repr

/-- Canonical Lean/mathlib name or concept for a metric-bridge node. -/
def MetricBridgeNode.canonicalName : MetricBridgeNode → String
  | riemannianExtendedDistance => "Manifold.riemannianEDist"
  | pseudoEMetricOfRiemannianMetric => "PseudoEMetricSpace.ofRiemannianMetric"
  | eMetricOfRiemannianMetric => "EMetricSpace.ofRiemannianMetric"
  | finiteDistancePseudoMetric => "PseudoEMetricSpace.toPseudoMetricSpace"
  | metricCompleteness => "CompleteSpace"
  | metricProperness => "ProperSpace"

/-- Required input or side condition for each metric-bridge node. -/
def MetricBridgeNode.requiredInput : MetricBridgeNode → String
  | riemannianExtendedDistance =>
      "RiemannianBundle, ENorm/ENormSMulClass tangent fibers, C^1 path-length API"
  | pseudoEMetricOfRiemannianMetric =>
      "RegularSpace M; constructs a PseudoEMetricSpace whose edist is riemannianEDist"
  | eMetricOfRiemannianMetric =>
      "T3Space M; upgrades the Riemannian pseudo-emetric to an EMetricSpace"
  | finiteDistancePseudoMetric =>
      "proof that all selected extended distances are finite, edist x y ≠ ⊤"
  | metricCompleteness =>
      "CompleteSpace for the uniform structure induced by the selected metric structure"
  | metricProperness =>
      "PseudoMetricSpace M; ProperSpace means every closed metric ball is compact"

/-- Role of each metric-bridge node in the future Hopf-Rinow package. -/
def MetricBridgeNode.bridgeRole : MetricBridgeNode → String
  | riemannianExtendedDistance =>
      "infimum of Riemannian path lengths; gives the intrinsic extended distance"
  | pseudoEMetricOfRiemannianMetric =>
      "connects the Riemannian distance to the manifold topology and IsRiemannianManifold"
  | eMetricOfRiemannianMetric =>
      "adds T0 separation for an EMetricSpace when the topology is T3"
  | finiteDistancePseudoMetric =>
      "turns the extended metric into the real-valued metric required by Metric.closedBall"
  | metricCompleteness =>
      "hypothesis side of Hopf-Rinow; also follows from ProperSpace after the metric bridge"
  | metricProperness =>
      "compactness side of Hopf-Rinow; supplies compact closed balls and completeness"

/--
Repo-local status for metric-bridge nodes.

Only adjacent constructors/wrappers are available locally.  The bridge from
metric completeness of the Riemannian extended metric to properness/minimizing
geodesics remains formalization debt.
-/
def MetricBridgeNode.repoLocalStatus : MetricBridgeNode → String
  | riemannianExtendedDistance => "local_wrapper_upstream_mathlib_adjacent"
  | pseudoEMetricOfRiemannianMetric => "local_wrapper_upstream_mathlib_adjacent"
  | eMetricOfRiemannianMetric => "local_wrapper_upstream_mathlib_adjacent"
  | finiteDistancePseudoMetric => "formalization_debt"
  | metricCompleteness => "statement_hypothesis_only"
  | metricProperness => "formalization_debt"

/-- The intended dependency order for the Hopf-Rinow metric bridge. -/
def metricBridgePlan : List MetricBridgeNode := [
  MetricBridgeNode.riemannianExtendedDistance,
  MetricBridgeNode.pseudoEMetricOfRiemannianMetric,
  MetricBridgeNode.eMetricOfRiemannianMetric,
  MetricBridgeNode.finiteDistancePseudoMetric,
  MetricBridgeNode.metricCompleteness,
  MetricBridgeNode.metricProperness
]

/-- Public names for the intended metric bridge, in dependency order. -/
def metricBridgePlanNames : List String :=
  metricBridgePlan.map MetricBridgeNode.canonicalName

/-- The metric bridge has the six audited nodes requested by `THM-M-0166.metric-bridge`. -/
theorem metricBridgePlan_length :
    metricBridgePlan.length = 6 :=
  rfl

/-- The metric bridge names have the six audited nodes requested by `THM-M-0166.metric-bridge`. -/
theorem metricBridgePlanNames_length :
    metricBridgePlanNames.length = 6 :=
  rfl

/-- `PseudoEMetricSpace.ofRiemannianMetric` is part of the metric-bridge plan. -/
theorem pseudoEMetricOfRiemannianMetric_mem_metricBridgePlan :
    MetricBridgeNode.pseudoEMetricOfRiemannianMetric ∈ metricBridgePlan := by
  simp [metricBridgePlan]

/-- `EMetricSpace.ofRiemannianMetric` is part of the metric-bridge plan. -/
theorem eMetricOfRiemannianMetric_mem_metricBridgePlan :
    MetricBridgeNode.eMetricOfRiemannianMetric ∈ metricBridgePlan := by
  simp [metricBridgePlan]

/-- The `PseudoMetricSpace` finiteness bridge is part of the metric-bridge plan. -/
theorem finiteDistancePseudoMetric_mem_metricBridgePlan :
    MetricBridgeNode.finiteDistancePseudoMetric ∈ metricBridgePlan := by
  simp [metricBridgePlan]

/-- `CompleteSpace` is part of the metric-bridge plan. -/
theorem metricCompleteness_mem_metricBridgePlan :
    MetricBridgeNode.metricCompleteness ∈ metricBridgePlan := by
  simp [metricBridgePlan]

/-- `ProperSpace` is part of the metric-bridge plan. -/
theorem metricProperness_mem_metricBridgePlan :
    MetricBridgeNode.metricProperness ∈ metricBridgePlan := by
  simp [metricBridgePlan]

/-- No metric-bridge node is marked as repo-local integration debt by this child. -/
theorem metricBridgeNode_repoLocalStatus_not_integration_debt
    (node : MetricBridgeNode) :
    node.repoLocalStatus ≠ "repo_local_integration_debt" := by
  cases node <;> decide

/--
Audit conclusion for the metric bridge.

The present mathlib bridge reaches `PseudoEMetricSpace`/`EMetricSpace` from the
Riemannian metric and reaches `CompleteSpace` from `ProperSpace` for any
real-valued pseudo-metric.  The missing Hopf-Rinow bridge is the converse
direction from Riemannian metric completeness to finite real-valued distance,
properness, and minimizing geodesic existence.
-/
def metricBridgeAuditConclusion : String :=
  "Use PseudoEMetricSpace.ofRiemannianMetric or EMetricSpace.ofRiemannianMetric to align edist with riemannianEDist; introduce a finite-distance PseudoMetricSpace before using ProperSpace; keep CompleteSpace as the metric-completeness hypothesis and do not claim Hopf-Rinow properness/minimizing geodesics until the geodesic and compactness bridge is formalized."

/-! ## Audit metadata -/

/-- Pinned mathlib revision audited for the `THM-M-0166.mathlib-audit` child. -/
def mathlibAuditPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Sanity check for the pinned mathlib revision recorded by this child audit. -/
theorem mathlibAuditPinnedRevision_eq :
    mathlibAuditPinnedRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Requested mathlib modules available at the pinned revision for Hopf-Rinow audit work. -/
def mathlibAuditAvailableModules : List String := [
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.Riemannian.PathELength",
  "Mathlib.Geometry.Manifold.IntegralCurve.Basic",
  "Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
  "Mathlib.Topology.MetricSpace.ProperSpace"
]

/-- The mathlib audit records exactly the eight requested available module anchors. -/
theorem mathlibAuditAvailableModules_length :
    mathlibAuditAvailableModules.length = 8 :=
  rfl

/-- mathlib modules checked while locating repo-local Hopf-Rinow anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.Riemannian.PathELength",
  "Mathlib.Geometry.Manifold.IntegralCurve.Basic",
  "Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
  "Mathlib.Topology.MetricSpace.ProperSpace"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "IsRiemannianManifold",
  "Manifold.riemannianEDist",
  "Manifold.pathELength",
  "Manifold.riemannianEDist_le_pathELength",
  "Manifold.exists_lt_of_riemannianEDist_lt",
  "Manifold.exists_lt_locally_constant_of_riemannianEDist_lt",
  "IsMIntegralCurve",
  "exists_isMIntegralCurveAt_of_contMDiffAt_boundaryless",
  "isMIntegralCurveAt_eventuallyEq_of_contMDiffAt_boundaryless",
  "ProperSpace",
  "isCompact_closedBall",
  "complete_of_proper"
]

/-- Search terms that did not locate a terminal Hopf-Rinow theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "HopfRinow",
  "Hopf Rinow",
  "Hopf-Rinow",
  "geodesic",
  "Geodesic",
  "geodesically complete",
  "minimizing geodesic",
  "expMap",
  "LeviCivita"
]

/-! ## External Lean audit gate -/

/-- Exact external Lean 4 search terms requested for `THM-M-0166.external-audit`. -/
inductive ExternalAuditSearchTerm : Type where
  | hopfRinowIdentifier
  | hopfRinowHyphenated
  | hopfRinowSpaced
  | geodesicComplete
  | geodesicallyComplete
  | minimizingGeodesic
  | leviCivita
  | riemannianExp
  | expMap
  | isGeodesic
  deriving DecidableEq, Repr

/-- Canonical query string for each external Lean 4 audit search term. -/
def ExternalAuditSearchTerm.query : ExternalAuditSearchTerm → String
  | hopfRinowIdentifier => "HopfRinow"
  | hopfRinowHyphenated => "\"Hopf-Rinow\""
  | hopfRinowSpaced => "\"Hopf Rinow\""
  | geodesicComplete => "GeodesicComplete"
  | geodesicallyComplete => "\"geodesically complete\""
  | minimizingGeodesic => "\"minimizing geodesic\""
  | leviCivita => "LeviCivita"
  | riemannianExp => "Riemannian.exp"
  | expMap => "expMap"
  | isGeodesic => "IsGeodesic"

/-- Ordered external Lean 4 audit terms required by the public blueprint leaf. -/
def externalAuditSearchTerms : List ExternalAuditSearchTerm := [
  ExternalAuditSearchTerm.hopfRinowIdentifier,
  ExternalAuditSearchTerm.hopfRinowHyphenated,
  ExternalAuditSearchTerm.hopfRinowSpaced,
  ExternalAuditSearchTerm.geodesicComplete,
  ExternalAuditSearchTerm.geodesicallyComplete,
  ExternalAuditSearchTerm.minimizingGeodesic,
  ExternalAuditSearchTerm.leviCivita,
  ExternalAuditSearchTerm.riemannianExp,
  ExternalAuditSearchTerm.expMap,
  ExternalAuditSearchTerm.isGeodesic
]

/-- Exact query strings for the external Lean 4 audit, in blueprint order. -/
def externalAuditSearchQueries : List String :=
  externalAuditSearchTerms.map ExternalAuditSearchTerm.query

/-- The external audit records exactly the ten requested search terms. -/
theorem externalAuditSearchTerms_length :
    externalAuditSearchTerms.length = 10 :=
  rfl

/-- The external audit records exactly the ten requested query strings. -/
theorem externalAuditSearchQueries_length :
    externalAuditSearchQueries.length = 10 :=
  rfl

/-- Primary-source record shape for external Lean 4 Hopf-Rinow audit candidates. -/
structure ExternalLeanAuditRecord : Type where
  repoURL : String
  commit : String
  theoremNames : List String
  toolchain : String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  relevance : String

/--
Pinned mathlib is the only repo-local primary-source Lean 4 dependency checked
for this audit.  It supplies adjacent Riemannian and metric APIs, but no
terminal Hopf-Rinow theorem.
-/
def pinnedMathlibExternalAuditRecord : ExternalLeanAuditRecord where
  repoURL := "https://github.com/leanprover-community/mathlib4"
  commit := mathlibAuditPinnedRevision
  theoremNames := mathlibAnchorNames
  toolchain := "leanprover/lean4:v4.29.0"
  placeholderStatus :=
    "adjacent imported APIs compile locally; no terminal Hopf-Rinow theorem found in pinned mathlib"
  lakeDependencyFeasibility := "already pinned in this repository's Lake manifest"
  relevance :=
    "Riemannian path-length and metric/properness substrate only; not a Hopf-Rinow closure"

/--
Authenticated GitHub code search status for this child pass.

This is intentionally a blocker note, not completion evidence: the local
environment had no authenticated GitHub host, and unauthenticated GitHub code
search was rate-limited during this execution.
-/
def externalAuditAuthenticatedSearchStatus : String :=
  "blocked: gh auth status reported no logged-in GitHub hosts on 2026-05-01; GitHub REST code search required authentication for all requested queries"

/-- This child did not find an external Lean 4 terminal Hopf-Rinow closure. -/
def externalHopfRinowClosureFound : Bool := false

/-- Sanity check: no external terminal Hopf-Rinow closure is recorded here. -/
theorem externalHopfRinowClosureFound_eq_false :
    externalHopfRinowClosureFound = false :=
  rfl

/--
Repo-local integration gate for the external audit.

Because no external terminal closure was found, this child leaves no
`repo_local_integration_debt`; because authenticated code search was blocked,
the external-audit public leaf should remain open until an authenticated rerun
confirms the negative result or records a concrete integration blocker.
-/
def externalAuditRepoLocalIntegrationGate : String :=
  "no_repo_local_integration_debt_found; authenticated_external_search_blocked"

/-- The external-audit gate is not the forbidden completed debt state. -/
theorem externalAuditRepoLocalIntegrationGate_ne_integration_debt :
    externalAuditRepoLocalIntegrationGate ≠ "repo_local_integration_debt" := by
  decide

/-! ## C006 integration gate -/

/--
Stable record for the `THM-M-0166.integration-gate` child.

This row is deliberately separate from the broader external-audit metadata:
its only job is to block any public completion claim unless an external Lean 4
terminal Hopf-Rinow closure has actually been pinned, imported, and checked, or
a concrete dependency/toolchain/license blocker has been recorded.
-/
structure ExternalHopfRinowIntegrationGate where
  childTask : String
  externalClosureFound : Bool
  externalClosurePinnedImportedChecked : Bool
  concreteIntegrationBlocker : String
  completionClaimAllowed : Bool
  repoLocalDebtClass : String
  nextAction : String

/--
C006 integration-gate decision for Hopf-Rinow.

No terminal external Lean 4 Hopf-Rinow closure is available in the current
repo-local validation closure.  Pinned mathlib supplies adjacent Riemannian and
metric APIs, not the terminal theorem, and authenticated GitHub code search is
blocked in this environment.  Therefore this child adds no dependency wrapper
and forbids public completion.
-/
def externalHopfRinowIntegrationGateC006 : ExternalHopfRinowIntegrationGate where
  childTask := "S1-M-122-C006"
  externalClosureFound := externalHopfRinowClosureFound
  externalClosurePinnedImportedChecked := false
  concreteIntegrationBlocker :=
    "No terminal external Lean 4 Hopf-Rinow closure is currently available to pin/import/check; authenticated GitHub code search is blocked because gh has no logged-in host, so completion is blocked until authenticated primary-source search either confirms no closure or produces a concrete pin/import/check target or dependency/toolchain/license blocker."
  completionClaimAllowed := false
  repoLocalDebtClass := "formalization_debt"
  nextAction :=
    "Rerun authenticated primary-source Lean 4 code search for the ten recorded terms; if a terminal closure is found, pin/import/check it or record a concrete integration blocker before any public completion claim."

/-- C006 records that no terminal external Hopf-Rinow closure was found. -/
theorem externalHopfRinowIntegrationGateC006_no_externalClosure :
    externalHopfRinowIntegrationGateC006.externalClosureFound = false :=
  rfl

/-- C006 records that no external Hopf-Rinow dependency was pinned/imported/checked. -/
theorem externalHopfRinowIntegrationGateC006_not_pinned :
    externalHopfRinowIntegrationGateC006.externalClosurePinnedImportedChecked = false :=
  rfl

/-- C006 forbids a public completion claim for this parent theorem. -/
theorem externalHopfRinowIntegrationGateC006_no_completionClaim :
    externalHopfRinowIntegrationGateC006.completionClaimAllowed = false :=
  rfl

/-- C006 keeps the remaining debt as formalization debt, not completed integration debt. -/
theorem externalHopfRinowIntegrationGateC006_formalizationDebt :
    externalHopfRinowIntegrationGateC006.repoLocalDebtClass = "formalization_debt" :=
  rfl

/-- C006 does not leave the forbidden completed integration-debt state. -/
theorem externalHopfRinowIntegrationGateC006_not_integrationDebt :
    externalHopfRinowIntegrationGateC006.repoLocalDebtClass ≠ "repo_local_integration_debt" := by
  decide

end S1_M_122
end Stage1
end AwesomeTheorems
