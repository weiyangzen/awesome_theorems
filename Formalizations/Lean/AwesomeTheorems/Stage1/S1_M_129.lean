import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique
import Mathlib.Analysis.ODE.PicardLindelof

/-!
# S1-M-129 / THM-M-0181: Hamilton's short-time Ricci-flow theorem

This Stage1 file records a conservative Lean 4 statement-shape boundary for
Hamilton's short-time existence and uniqueness theorem for Ricci flow.

The pinned mathlib snapshot has substantial manifold, Riemannian-metric,
integral-curve, and Picard-Lindelof ODE infrastructure. It does not expose a
terminal Ricci tensor, parabolic PDE, or Ricci-flow short-time existence theorem.

The declarations below therefore avoid proof placeholders and false completion
claims. They freeze the formalization boundary and add only checked wrappers
around adjacent mathlib declarations.
-/

noncomputable section

open Function Manifold Set Bundle
open scoped ContDiff Topology Bundle

universe uE uH uM

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_129

/--
Statement-shape data for Hamilton's short-time Ricci-flow theorem.

The fields `initialMetric`, `evolvingMetric`, and `ricciTensorModel` are kept as
propositions because the pinned mathlib snapshot does not yet provide a Ricci
tensor or parabolic Ricci-flow PDE object model. The surrounding parameters
still expose the intended smooth manifold universe, model-with-corners, and
compactness boundary.
-/
structure HamiltonRicciFlowData
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] : Type (max uE uH uM) where
  timeInterval : Set ℝ
  positiveTime : Prop
  positiveTime_realizesInterval : positiveTime → ∃ T : ℝ, 0 < T ∧ Icc (0 : ℝ) T ⊆ timeInterval
  compactInitialManifold : Prop
  initialMetric : Prop
  evolvingMetric : ℝ → Prop
  ricciTensorModel : Prop
  ricciFlowEquationOn : Set ℝ → Prop
  initialCondition : Prop
  uniquenessWithinClass : Prop

namespace HamiltonRicciFlowData

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
  {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]

/-- The normalized conclusion package: existence, equation, initial condition, and uniqueness. -/
def ShortTimeExistenceUniqueness
    (D : HamiltonRicciFlowData E H I M) : Prop :=
  D.compactInitialManifold →
    D.initialMetric →
      D.positiveTime ∧
        D.ricciTensorModel ∧
        D.ricciFlowEquationOn D.timeInterval ∧
        D.initialCondition ∧
        D.uniquenessWithinClass

end HamiltonRicciFlowData

/--
Stage1 statement-shape candidate for Hamilton's short-time Ricci-flow theorem.

This is intentionally a proposition boundary, not a proof of Ricci-flow
existence. A terminal theorem must replace the abstract metric/Ricci/PDE fields
by concrete mathlib or pinned external Lean 4 APIs.
-/
def StatementShape : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
    [CompactSpace M],
      ∀ D : HamiltonRicciFlowData E H I M, D.ShortTimeExistenceUniqueness

/-- Trivial checked wrapper retaining `StatementShape` as a concrete proposition. -/
theorem statementShape_self : StatementShape.{uE, uH, uM} ↔ StatementShape.{uE, uH, uM} :=
  Iff.rfl

/-!
## Public statement-normalization boundary

The public Stage1 backfill should cite `StatementNormalizationBoundary` as the
repo-local Lean boundary for `THM-M-0181.statement`. This boundary is exactly
`StatementShape`: it records the intended compact-manifold, short positive time,
existence, equation, initial-condition, and uniqueness slots, while keeping the
metric, Ricci tensor, parabolic PDE, and uniqueness class abstract.

This is not a terminal Ricci-flow theorem. Completing Hamilton's theorem still
requires replacing the abstract fields of `HamiltonRicciFlowData` with concrete
Ricci-flow APIs and proving the resulting theorem, or importing and checking a
pinned external Lean 4 closure.
-/

/--
Repo-local public statement-normalization boundary for Hamilton's short-time
Ricci-flow theorem.

This is intentionally definitionally equal to `StatementShape`; it is a stable
name for public documentation, not a stronger mathematical theorem.
-/
def StatementNormalizationBoundary : Prop :=
  StatementShape.{uE, uH, uM}

/-- Checked equivalence between the public normalization boundary and `StatementShape`. -/
theorem statementNormalizationBoundary_iff_statementShape :
    StatementNormalizationBoundary.{uE, uH, uM} ↔ StatementShape.{uE, uH, uM} :=
  Iff.rfl

/--
Machine-readable status tag for downstream ledgers and public backfill.

The tag deliberately says `not_terminal`: no declaration in this file proves
Hamilton's Ricci-flow theorem.
-/
def statementNormalizationStatusTag : String :=
  "statement_shape_only_not_terminal_ricci_flow_theorem"

/-- Checked anchor: inner-product vector spaces carry mathlib's Riemannian-manifold structure. -/
theorem vectorSpace_isRiemannianManifold
    (F : Type uE) [NormedAddCommGroup F] [InnerProductSpace ℝ F] :
    IsRiemannianManifold 𝓘(ℝ, F) F := by
  infer_instance

/-- Checked anchor: the Riemannian extended distance from a point to itself is zero. -/
theorem riemannianEDist_self_anchor
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    [RiemannianBundle (fun (x : M) ↦ TangentSpace I x)] (x : M) :
    riemannianEDist I x x = 0 := by
  exact riemannianEDist_self

/--
Checked anchor: mathlib gives local existence of integral curves for `C^1`
vector fields on boundaryless manifolds.

This is ODE/manifold infrastructure only. It is not a Ricci-flow existence
theorem, because Ricci flow is a nonlinear parabolic PDE on metrics.
-/
theorem integralCurve_localExistence_anchor
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] [IsManifold I 1 M]
    [BoundarylessManifold I M]
    {v : (x : M) → TangentSpace I x} {t₀ : ℝ} {x₀ : M}
    (hv : CMDiffAt 1 (fun x ↦ (⟨x, v x⟩ : TangentBundle I M)) x₀) :
    ∃ γ : ℝ → M, γ t₀ = x₀ ∧ IsMIntegralCurveAt γ v t₀ := by
  exact exists_isMIntegralCurveAt_of_contMDiffAt_boundaryless t₀ hv

/--
Checked anchor: mathlib gives uniqueness for global integral curves of `C^1`
vector fields on Hausdorff boundaryless manifolds.

This is adjacent ODE infrastructure and does not close Hamilton's Ricci-flow
short-time uniqueness theorem.
-/
theorem integralCurve_globalUniqueness_anchor
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] [IsManifold I 1 M]
    [T2Space M] [BoundarylessManifold I M]
    {γ γ' : ℝ → M} {v : (x : M) → TangentSpace I x} {t₀ : ℝ}
    (hv : CMDiff 1 (fun x ↦ (⟨x, v x⟩ : TangentBundle I M)))
    (hγ : IsMIntegralCurve γ v) (hγ' : IsMIntegralCurve γ' v) (h : γ t₀ = γ' t₀) :
    γ = γ' := by
  exact isMIntegralCurve_Ioo_eq_of_contMDiff_boundaryless hv hγ hγ' h

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.Riemannian.PathELength",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
  "Mathlib.Geometry.Manifold.IntegralCurve.Basic",
  "Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique",
  "Mathlib.Analysis.ODE.PicardLindelof",
  "Mathlib.Analysis.ODE.Gronwall",
  "Mathlib.Dynamics.Flow"
]

/-- Pinned mathlib revision audited for the `THM-M-0181.mathlib-audit` child task. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Public-facing short module labels from the `THM-M-0181.mathlib-audit` child task. -/
def mathlibAuditShortModuleLabels : List String := [
  "Riemannian.Basic",
  "Riemannian.PathELength",
  "VectorBundle.Riemannian",
  "CovariantDerivative.Basic",
  "CovariantDerivative.Torsion",
  "IntegralCurve.Basic",
  "IntegralCurve.ExistUnique",
  "ODE.PicardLindelof",
  "ODE.Gronwall",
  "Dynamics.Flow"
]

/--
Integration-ready public mathlib-audit note for `THM-M-0181.mathlib-audit`.

The named modules are available in the pinned local mathlib source tree and
provide Riemannian-manifold, tangent-bundle, covariant-derivative, integral
curve, Picard-Lindelof, Gronwall, and flow infrastructure. This is substrate
evidence only: it is not a terminal Hamilton Ricci-flow theorem.
-/
def mathlibAuditNote : String :=
  "THM-M-0181.mathlib-audit: at pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95, the local mathlib source tree contains Mathlib.Geometry.Manifold.Riemannian.Basic, Mathlib.Geometry.Manifold.Riemannian.PathELength, Mathlib.Geometry.Manifold.VectorBundle.Riemannian, Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic, Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion, Mathlib.Geometry.Manifold.IntegralCurve.Basic, Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique, Mathlib.Analysis.ODE.PicardLindelof, Mathlib.Analysis.ODE.Gronwall, and Mathlib.Dynamics.Flow. These modules provide Riemannian-manifold, tangent-bundle, covariant-derivative, integral-curve, Picard-Lindelof, Gronwall, and flow infrastructure, but they do not by themselves close a terminal Hamilton short-time Ricci-flow theorem in this repository."

/-- The audit table records exactly the requested pinned mathlib revision. -/
theorem pinnedMathlibRevision_eq_requested :
    pinnedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- The audit records exactly ten mathlib module anchors for this child task. -/
theorem mathlibAnchorModules_length :
    mathlibAnchorModules.length = 10 :=
  rfl

/-- The public short-label audit records exactly the ten requested module labels. -/
theorem mathlibAuditShortModuleLabels_length :
    mathlibAuditShortModuleLabels.length = 10 :=
  rfl

/-!
## Missing formal API split

`THM-M-0181.missing-api` is a formalization-debt child, not a proof child.  The
following checked data splits the missing Ricci-flow API into the nine M0387
leaves requested by the public Stage1 checklist.  Every leaf is explicitly
unchecked, has a `<= 100` local expansion budget, and is not repo-locally closed.
-/

/-- Canonical missing formal-API branches for Hamilton's Ricci-flow theorem. -/
inductive RicciFlowMissingAPIBranch where
  | leviCivitaConnection
  | riemannCurvatureTensor
  | ricciContraction
  | localCoordinateFormulas
  | smoothDependenceOnMetric
  | parabolicPDEExistence
  | deturckVectorField
  | pullbackEquivalence
  | smoothSolutionUniqueness
  deriving DecidableEq, Repr

namespace RicciFlowMissingAPIBranch

/-- Stable public task name for each missing formal-API branch. -/
def canonicalTaskName : RicciFlowMissingAPIBranch → String
  | leviCivitaConnection => "THM-M-0181.missing-api.levi-civita-connection"
  | riemannCurvatureTensor => "THM-M-0181.missing-api.riemann-curvature-tensor"
  | ricciContraction => "THM-M-0181.missing-api.ricci-contraction"
  | localCoordinateFormulas => "THM-M-0181.missing-api.local-coordinate-formulas"
  | smoothDependenceOnMetric => "THM-M-0181.missing-api.smooth-dependence-on-metric"
  | parabolicPDEExistence => "THM-M-0181.missing-api.parabolic-pde-existence"
  | deturckVectorField => "THM-M-0181.missing-api.deturck-vector-field"
  | pullbackEquivalence => "THM-M-0181.missing-api.pullback-equivalence"
  | smoothSolutionUniqueness => "THM-M-0181.missing-api.smooth-solution-uniqueness"

end RicciFlowMissingAPIBranch

/--
M0387-style leaf record for a missing Ricci-flow formal API.

The string fields are audit metadata for public backfill.  They deliberately do
not assert that any missing branch has a concrete repo-local proof body.
-/
structure RicciFlowMissingAPILeaf where
  branch : RicciFlowMissingAPIBranch
  requiredPayload : String
  currentBoundary : String
  currentStatus : String
  debtClass : String
  leafBudgetBound : Nat
  repoLocalClosed : Bool

/-- Integration-ready missing formal-API split for `THM-M-0181.missing-api`. -/
def ricciFlowMissingAPILeaves : List RicciFlowMissingAPILeaf := [
  {
    branch := RicciFlowMissingAPIBranch.leviCivitaConnection
    requiredPayload :=
      "Define or import the Levi-Civita connection of a smooth Riemannian metric, with torsion-free and metric-compatible characterizations usable by curvature."
    currentBoundary :=
      "Pinned mathlib has covariant-derivative and Riemannian-bundle substrate, but this file has no concrete Levi-Civita API tied to an evolving metric."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  },
  {
    branch := RicciFlowMissingAPIBranch.riemannCurvatureTensor
    requiredPayload :=
      "Define or import the Riemann curvature tensor of the Levi-Civita connection with tensor symmetries and smoothness properties."
    currentBoundary :=
      "No repo-local curvature tensor object is available; `HamiltonRicciFlowData.ricciTensorModel` remains propositional."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  },
  {
    branch := RicciFlowMissingAPIBranch.ricciContraction
    requiredPayload :=
      "Define or import Ricci curvature as the contraction of the Riemann tensor and connect it to the metric tensor slot."
    currentBoundary :=
      "No checked contraction from a Riemann curvature tensor to a Ricci tensor exists in this Stage1 artifact."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  },
  {
    branch := RicciFlowMissingAPIBranch.localCoordinateFormulas
    requiredPayload :=
      "Provide local-coordinate formulas for Christoffel symbols, curvature, Ricci tensor, and the Ricci-flow equation."
    currentBoundary :=
      "The current statement-shape boundary has charted-manifold parameters but no coordinate expression API for the geometric PDE."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  },
  {
    branch := RicciFlowMissingAPIBranch.smoothDependenceOnMetric
    requiredPayload :=
      "Prove smooth dependence of the Levi-Civita connection, curvature, and Ricci tensor on a smoothly time-dependent metric."
    currentBoundary :=
      "The evolving metric is still an abstract `ℝ → Prop`, so smooth dependence on metric coefficients is not encoded."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  },
  {
    branch := RicciFlowMissingAPIBranch.parabolicPDEExistence
    requiredPayload :=
      "Define or import short-time existence for the relevant nonlinear strongly parabolic PDE on symmetric 2-tensors."
    currentBoundary :=
      "Pinned mathlib has ODE Picard-Lindelof infrastructure, but no parabolic PDE existence theorem sufficient for Ricci flow."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  },
  {
    branch := RicciFlowMissingAPIBranch.deturckVectorField
    requiredPayload :=
      "Define the DeTurck vector field relative to a background connection and prove the gauge-fixed equation is strictly parabolic."
    currentBoundary :=
      "No DeTurck vector-field, gauge-fixing, or background-connection comparison API is present in the local artifact."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  },
  {
    branch := RicciFlowMissingAPIBranch.pullbackEquivalence
    requiredPayload :=
      "Prove equivalence between the DeTurck flow and Ricci flow via pullback along the generated diffeomorphism family."
    currentBoundary :=
      "Mathlib flow/integral-curve anchors are adjacent ODE infrastructure only; no metric pullback-equivalence theorem is encoded."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  },
  {
    branch := RicciFlowMissingAPIBranch.smoothSolutionUniqueness
    requiredPayload :=
      "Prove uniqueness of smooth Ricci-flow solutions in the selected compact-manifold solution class."
    currentBoundary :=
      "The checked integral-curve uniqueness anchor does not imply uniqueness for nonlinear parabolic metric PDE solutions."
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
  }
]

/-- The missing formal-API split has exactly the nine requested leaves. -/
theorem ricciFlowMissingAPILeaves_length :
    ricciFlowMissingAPILeaves.length = 9 :=
  rfl

/-- The checked split records exactly the requested branch order. -/
theorem ricciFlowMissingAPILeaves_branches_eq :
    List.map (fun leaf => leaf.branch) ricciFlowMissingAPILeaves = [
      RicciFlowMissingAPIBranch.leviCivitaConnection,
      RicciFlowMissingAPIBranch.riemannCurvatureTensor,
      RicciFlowMissingAPIBranch.ricciContraction,
      RicciFlowMissingAPIBranch.localCoordinateFormulas,
      RicciFlowMissingAPIBranch.smoothDependenceOnMetric,
      RicciFlowMissingAPIBranch.parabolicPDEExistence,
      RicciFlowMissingAPIBranch.deturckVectorField,
      RicciFlowMissingAPIBranch.pullbackEquivalence,
      RicciFlowMissingAPIBranch.smoothSolutionUniqueness
    ] :=
  rfl

/-- No missing formal-API leaf is repo-locally closed by this Stage1 artifact. -/
theorem ricciFlowMissingAPILeaves_repoLocalClosed_eq :
    List.map (fun leaf => leaf.repoLocalClosed) ricciFlowMissingAPILeaves =
      [false, false, false, false, false, false, false, false, false] :=
  rfl

/-- Each missing formal-API leaf keeps the M0387 local expansion budget at `100`. -/
theorem ricciFlowMissingAPILeaves_budget_eq :
    List.map (fun leaf => leaf.leafBudgetBound) ricciFlowMissingAPILeaves =
      [100, 100, 100, 100, 100, 100, 100, 100, 100] :=
  rfl

/-- Each missing formal-API leaf remains unchecked formalization debt. -/
theorem ricciFlowMissingAPILeaves_statusDebt_eq :
    List.map (fun leaf => (leaf.currentStatus, leaf.debtClass)) ricciFlowMissingAPILeaves = [
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt")
    ] :=
  rfl

/--
M0387 gate: this child does not mark a completed state while retaining
repo-local integration debt.
-/
def missingAPIRepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- Checked gate fact for the missing-API child ledger. -/
theorem missingAPIRepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    missingAPIRepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "RiemannianBundle",
  "IsContMDiffRiemannianBundle",
  "ContMDiffRiemannianMetric",
  "IsRiemannianManifold",
  "riemannianEDist",
  "riemannianEDist_self",
  "exists_isMIntegralCurveAt_of_contMDiffAt_boundaryless",
  "isMIntegralCurve_Ioo_eq_of_contMDiff_boundaryless",
  "IsPicardLindelof",
  "ODE_solution_unique"
]

/-- Search terms that did not locate a terminal Ricci-flow theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "RicciFlow",
  "Ricci flow",
  "ricci_flow",
  "Ricci tensor",
  "RicciTensor",
  "Ricci curvature",
  "Riemann curvature",
  "Hamilton Ricci",
  "short-time existence",
  "parabolic PDE"
]

/-!
## External Lean 4 audit

`THM-M-0181.external-audit` is an external-anchor audit child.  In the
2026-05-01 child execution environment, `gh auth status` reported no logged-in
GitHub host and the unauthenticated GitHub Search API was rate-limited.  The
requested authenticated GitHub Code Search pass is therefore recorded as an
integration blocker, not as a completed authenticated audit.

The fallback checks were:

* local pinned dependency search in mathlib/flt-regular with `rg`;
* public Sourcegraph code-search API queries for Lean files, with archived and
  forked repositories included, for every requested search term.

Those fallback checks found no Lean file hit and no external terminal theorem
candidate for Hamilton's short-time Ricci-flow theorem.  Since no external Lean
4 closure was located, there is no Lake dependency to pin/import/check in this
child.
-/

/-- Exact public search terms requested by `THM-M-0181.external-audit`. -/
def ricciFlowExternalAuditSearchTerms : List String := [
  "RicciFlow",
  "Ricci flow",
  "ricci_flow",
  "RicciTensor",
  "Ricci tensor",
  "Ricci curvature",
  "Hamilton Ricci",
  "DeTurck",
  "parabolic PDE",
  "short-time existence"
]

/-- Record for one external-audit search term. -/
structure RicciFlowExternalAuditResult where
  searchTerm : String
  authenticatedGitHubStatus : String
  fallbackSearchStatus : String
  repoURL : String
  commit : String
  theoremNames : List String
  toolchain : String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  repoLocalIntegrationAction : String

/--
Fallback external-audit table for `THM-M-0181.external-audit`.

Every row records the same hard boundary: authenticated GitHub Code Search was
blocked by absent local GitHub credentials, and fallback Lean-source searches
found no repository/theorem candidate to integrate.
-/
def ricciFlowExternalAuditResults : List RicciFlowExternalAuditResult := [
  {
    searchTerm := "RicciFlow"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "Ricci flow"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "ricci_flow"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "RicciTensor"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "Ricci tensor"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "Ricci curvature"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "Hamilton Ricci"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "DeTurck"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "parabolic PDE"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  },
  {
    searchTerm := "short-time existence"
    authenticatedGitHubStatus := "blocked: gh auth status reports no logged-in GitHub host; unauthenticated GitHub Search API is rate-limited"
    fallbackSearchStatus := "local pinned dependency rg plus public Sourcegraph Lean search returned zero file hits"
    repoURL := "none located"
    commit := "not applicable"
    theoremNames := []
    toolchain := "not applicable"
    placeholderStatus := "not applicable: no candidate file located"
    lakeDependencyFeasibility := "not applicable: no candidate dependency to pin"
    repoLocalIntegrationAction := "no pin/import/check action available from this audit row"
  }
]

/-- The external audit records exactly the ten requested search terms. -/
theorem ricciFlowExternalAuditSearchTerms_length :
    ricciFlowExternalAuditSearchTerms.length = 10 :=
  rfl

/-- The external audit table has one row for each requested search term. -/
theorem ricciFlowExternalAuditResults_length :
    ricciFlowExternalAuditResults.length = 10 :=
  rfl

/-- The external audit table records the requested search terms in order. -/
theorem ricciFlowExternalAuditResults_terms_eq :
    List.map (fun row => row.searchTerm) ricciFlowExternalAuditResults =
      ricciFlowExternalAuditSearchTerms :=
  rfl

/-- No external theorem candidate was located by the available fallback searches. -/
theorem ricciFlowExternalAuditResults_theoremNames_eq_empty :
    List.map (fun row => row.theoremNames) ricciFlowExternalAuditResults =
      [[], [], [], [], [], [], [], [], [], []] :=
  rfl

/-- Authenticated GitHub Code Search could not be completed in this child process. -/
def ricciFlowExternalAuditAuthenticatedGitHubBlocked : Bool :=
  true

/-- Checked blocker flag for the authenticated GitHub external-audit channel. -/
theorem ricciFlowExternalAuditAuthenticatedGitHubBlocked_eq_true :
    ricciFlowExternalAuditAuthenticatedGitHubBlocked = true :=
  rfl

/-- No external upstream closure was available to pin/import/check after this audit. -/
def ricciFlowExternalAuditLocatedExternalClosure : Bool :=
  false

/-- Checked no-candidate gate for this external audit. -/
theorem ricciFlowExternalAuditLocatedExternalClosure_eq_false :
    ricciFlowExternalAuditLocatedExternalClosure = false :=
  rfl

/--
M0387 gate: this external-audit child does not mark a completed state while
retaining repo-local integration debt.
-/
def externalAuditRepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- Checked gate fact for the external-audit child ledger. -/
theorem externalAuditRepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    externalAuditRepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-!
## Integration gate

`THM-M-0181.integration-gate` is a repo-local integration gate, not a proof of
Hamilton's Ricci-flow theorem.  It records the M0387 rule that an external Lean
4 closure, if later found, must be pinned/imported/checked in this repository or
kept open with a concrete blocker.  The current external audit located no
external Lean 4 closure and the authenticated GitHub channel remains blocked, so
there is no dependency candidate to pin in this child.
-/

/-- Checked integration-gate metadata for `THM-M-0181.integration-gate`. -/
structure RicciFlowIntegrationGate where
  childID : String
  upstreamClosureLocated : Bool
  externalUpstreamAnchorOnlyCompleted : Bool
  pinImportCheckRequiredIfClosureLocated : Bool
  concreteIntegrationBlocker : String
  completionClaimAllowed : Bool
  currentMachineStatus : String
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  nextAction : String

/-- Integration gate for child `S1-M-129-C005`. -/
def ricciFlowIntegrationGate : RicciFlowIntegrationGate := {
  childID := "S1-M-129-C005"
  upstreamClosureLocated := ricciFlowExternalAuditLocatedExternalClosure
  externalUpstreamAnchorOnlyCompleted := false
  pinImportCheckRequiredIfClosureLocated := true
  concreteIntegrationBlocker :=
    "No external Lean 4 closure was located by available fallback searches; the requested authenticated GitHub Code Search pass remains blocked by missing local credentials. If a future authenticated audit locates a closure, pin/import/check it in this Lake closure or record a concrete blocker such as toolchain mismatch, missing theorem API, license incompatibility, or dependency conflict before any completion claim."
  completionClaimAllowed := false
  currentMachineStatus := "formalization_debt_not_repo_local_closed"
  repoLocalIntegrationDebtRetainedInCompletedState := false
  nextAction :=
    "Run authenticated GitHub Code Search for the recorded Ricci-flow terms, then either pin/import/check any located Lean 4 closure or keep the parent open with a concrete integration blocker."
}

/-- The integration gate is attached to the C005 child task. -/
theorem ricciFlowIntegrationGate_childID_eq :
    ricciFlowIntegrationGate.childID = "S1-M-129-C005" :=
  rfl

/-- No external upstream Ricci-flow closure was located by the available audit. -/
theorem ricciFlowIntegrationGate_upstreamClosureLocated_eq_false :
    ricciFlowIntegrationGate.upstreamClosureLocated = false :=
  rfl

/-- The integration gate does not treat anchor-only evidence as completed. -/
theorem ricciFlowIntegrationGate_externalUpstreamAnchorOnlyCompleted_eq_false :
    ricciFlowIntegrationGate.externalUpstreamAnchorOnlyCompleted = false :=
  rfl

/-- Any future external closure must be pinned/imported/checked before completion. -/
theorem ricciFlowIntegrationGate_pinImportCheckRequiredIfClosureLocated_eq_true :
    ricciFlowIntegrationGate.pinImportCheckRequiredIfClosureLocated = true :=
  rfl

/-- This child permits no public completion claim for Hamilton's theorem. -/
theorem ricciFlowIntegrationGate_completionClaimAllowed_eq_false :
    ricciFlowIntegrationGate.completionClaimAllowed = false :=
  rfl

/-- The parent remains formalization debt and is not repo-locally closed. -/
theorem ricciFlowIntegrationGate_currentMachineStatus_eq :
    ricciFlowIntegrationGate.currentMachineStatus =
      "formalization_debt_not_repo_local_closed" :=
  rfl

/--
M0387 gate: this child leaves no completed state retaining repo-local
integration debt.
-/
theorem ricciFlowIntegrationGate_repoLocalIntegrationDebtRetained_eq_false :
    ricciFlowIntegrationGate.repoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

end S1_M_129
end Stage1
end AwesomeTheorems
