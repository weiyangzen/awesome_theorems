import Mathlib.Analysis.Calculus.ContDiffHolder.Pointwise
import Mathlib.Analysis.Convex.Continuous
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Topology.MetricSpace.HolderNorm

/-!
# S1-M-149 / THM-M-1181: Caffarelli regularity theorem

This Stage1 artifact records a conservative Lean 4 boundary for Caffarelli's
interior regularity theorem for convex solutions of the real Monge-Ampere
equation.  The pinned mathlib snapshot has useful APIs for convex functions,
finite-dimensional calculus, Holder regularity, determinants, Lebesgue measure,
and distribution-adjacent analysis, but this audit did not find a terminal
Monge-Ampere or Caffarelli theorem.

The declarations below therefore define an explicit statement-shape package and
small checked wrappers around available mathlib anchors.  They introduce no
proof placeholders and do not claim the terminal PDE theorem.
-/

noncomputable section

open Set
open scoped NNReal ENNReal Topology unitInterval

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_149

universe u v

/-- Euclidean domain type used for the normalized Caffarelli statement boundary. -/
abbrev EuclideanDomain (ι : Type u) [Fintype ι] : Type u :=
  Set (EuclideanSpace ℝ ι)

/-- Scalar field on a finite-dimensional real Euclidean space. -/
abbrev ScalarField (ι : Type u) [Fintype ι] : Type u :=
  EuclideanSpace ℝ ι → ℝ

/--
Input data for a future formal statement of Caffarelli interior regularity.

The Monge-Ampere equation is intentionally recorded as a `Prop` field because
the audited mathlib snapshot does not expose a canonical Aleksandrov,
viscosity, or classical `det D^2 u = f` API.  The remaining fields use current
mathlib objects where they are available: convex domains/functions, Holder
continuity, and two-sided positivity bounds for the right-hand side.
-/
structure CaffarelliInput (ι : Type u) [Fintype ι] [DecidableEq ι] : Type u where
  Ω : EuclideanDomain ι
  u : ScalarField ι
  rhs : ScalarField ι
  rhsHolderExponent : ℝ≥0
  pointwiseExponent : I
  isOpenDomain : IsOpen Ω
  isConvexDomain : Convex ℝ Ω
  solutionConvex : ConvexOn ℝ Ω u
  rhsHolder : ∃ C : ℝ≥0, HolderOnWith C rhsHolderExponent rhs Ω
  rhsPositiveBounds :
    ∃ lam bigLam : ℝ,
      0 < lam ∧ lam ≤ bigLam ∧ ∀ x ∈ Ω, lam ≤ rhs x ∧ rhs x ≤ bigLam
  mongeAmpereEquation : Prop
  normalizedSections : Prop

/--
Output package expected from the terminal Caffarelli theorem.

`interiorC2` and `interiorC2Holder` are stated with mathlib's differentiability
and pointwise Holder APIs.  The bridge and estimate fields remain explicit
propositions because the current local dependency closure does not yet provide
the Monge-Ampere measure, section geometry, or nonlinear PDE estimate APIs.
-/
structure CaffarelliInteriorRegularityPackage
    {ι : Type u} [Fintype ι] [DecidableEq ι] (X : CaffarelliInput ι) :
    Type u where
  interiorC2 : ContDiffOn ℝ 2 X.u (interior X.Ω)
  interiorC2Holder :
    ∀ x ∈ interior X.Ω, ContDiffPointwiseHolderAt 2 X.pointwiseExponent X.u x
  classicalMongeAmpereBridge : Prop
  localInteriorEstimates : Prop
  bridge_holds : classicalMongeAmpereBridge
  estimates_hold : localInteriorEstimates

/--
Normalized Stage1 statement shape for THM-M-1181.

For each finite-dimensional Euclidean domain, a convex solution of the audited
Monge-Ampere boundary object with positive Holder right-hand side and normalized
sections should have a C² plus pointwise Holder regularity package on the
interior of the domain.
-/
def StatementShape : Prop :=
  ∀ (ι : Type u) [Fintype ι] [DecidableEq ι] (X : CaffarelliInput ι),
    X.mongeAmpereEquation →
      X.normalizedSections →
        Nonempty (CaffarelliInteriorRegularityPackage X)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (ι : Type u) [Fintype ι] [DecidableEq ι] (X : CaffarelliInput ι),
      X.mongeAmpereEquation →
        X.normalizedSections →
          Nonempty (CaffarelliInteriorRegularityPackage X)) :
    StatementShape.{u} :=
  h

/-- Checked mathlib anchor: convex functions are continuous on the interior of their domain. -/
theorem convexSolution_continuousOn_interior
    {ι : Type u} [Fintype ι] [DecidableEq ι] (X : CaffarelliInput ι) :
    ContinuousOn X.u (interior X.Ω) :=
  X.solutionConvex.continuousOn_interior

/-- Checked mathlib anchor: convex functions are locally Lipschitz on the domain interior. -/
theorem convexSolution_locallyLipschitzOn_interior
    {ι : Type u} [Fintype ι] [DecidableEq ι] (X : CaffarelliInput ι) :
    LocallyLipschitzOn (interior X.Ω) X.u :=
  X.solutionConvex.locallyLipschitzOn_interior

/-- Checked wrapper exposing the stored Holder condition on the right-hand side. -/
theorem rhs_holderOnWith
    {ι : Type u} [Fintype ι] [DecidableEq ι] (X : CaffarelliInput ι) :
    ∃ C : ℝ≥0, HolderOnWith C X.rhsHolderExponent X.rhs X.Ω :=
  X.rhsHolder

/-- Checked wrapper exposing the stored uniform positive bounds on the right-hand side. -/
theorem rhs_positiveBounds
    {ι : Type u} [Fintype ι] [DecidableEq ι] (X : CaffarelliInput ι) :
    ∃ lam bigLam : ℝ,
      0 < lam ∧ lam ≤ bigLam ∧ ∀ x ∈ X.Ω, lam ≤ X.rhs x ∧ X.rhs x ≤ bigLam :=
  X.rhsPositiveBounds

/-- Checked mathlib anchor: a higher `ContDiffAt` hypothesis gives pointwise Holder regularity. -/
theorem contDiffAt_to_pointwiseHolderAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {F : Type v} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {k : ℕ} {α : I} {f : E → F} {a : E} {n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f a) (hk : k < n) :
    ContDiffPointwiseHolderAt k α f a :=
  hf.contDiffPointwiseHolderAt hk α

/-- Checked mathlib anchor: Holder exponent `1` is exactly Lipschitz continuity on a set. -/
theorem holderOnWith_one_iff_lipschitzOnWith
    {X Y : Type u} [PseudoEMetricSpace X] [PseudoEMetricSpace Y]
    {C : ℝ≥0} {f : X → Y} {s : Set X} :
    HolderOnWith C 1 f s ↔ LipschitzOnWith C f s :=
  holderOnWith_one

/-- mathlib modules checked while locating repo-local anchors for this PDE slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Convex.Function",
  "Mathlib.Analysis.Convex.Continuous",
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Calculus.ContDiffHolder.Pointwise",
  "Mathlib.Analysis.Calculus.MeanValue",
  "Mathlib.Analysis.InnerProductSpace.Laplacian",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Topology.MetricSpace.Holder",
  "Mathlib.Topology.MetricSpace.HolderNorm",
  "Mathlib.MeasureTheory.Function.Holder",
  "Mathlib.MeasureTheory.Measure.Lebesgue.Basic",
  "Mathlib.LinearAlgebra.Matrix.Determinant.Basic"
]

/-- Nearby mathlib names audited for the Caffarelli statement boundary. -/
def mathlibAnchorNames : List String := [
  "ConvexOn",
  "ConvexOn.continuousOn_interior",
  "ConvexOn.locallyLipschitzOn_interior",
  "HolderOnWith",
  "MemHolder",
  "ContDiffOn",
  "ContDiffAt",
  "ContDiffPointwiseHolderAt",
  "ContDiffAt.contDiffPointwiseHolderAt",
  "iteratedFDeriv",
  "Matrix.det",
  "MeasureTheory.volume",
  "Laplacian.laplacian",
  "MeasureTheory.Lp",
  "MeasureTheory.ContinuousLinearMap.holder"
]

/-- Search terms that did not locate a terminal importable Caffarelli theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Caffarelli",
  "Monge Ampere",
  "Monge-Ampere",
  "MongeAmpere",
  "Aleksandrov solution",
  "viscosity solution",
  "det D^2",
  "interior regularity",
  "convex solution regularity"
]

/-!
Machine-status metadata for the Stage1 public backfill.

These constants are intentionally non-mathematical metadata.  They keep the
local Lean artifact aligned with the audit status: the statement shape and
nearby anchors are checked, but the terminal Caffarelli theorem is not claimed.
-/

/-- Current machine status for this Stage1 artifact. -/
def machineStatus : String :=
  "statement_shape_local_checked"

/-- Pinned mathlib revision used by the parent audit. -/
def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact mathlib anchors requested by child audit `S1-M-149-C003`. -/
def childC003AnchorNames : List String := [
  "ConvexOn.continuousOn_interior",
  "ConvexOn.locallyLipschitzOn_interior",
  "HolderOnWith",
  "ContDiffPointwiseHolderAt",
  "Matrix.det",
  "MeasureTheory.volume",
  "Laplacian.laplacian"
]

/-- Whether this artifact proves the terminal Caffarelli interior regularity theorem. -/
def terminalTheoremCompleted : Bool :=
  false

/-- Public blocker requested by child audit `S1-M-149-C004`. -/
def childC004PublicBlocker : String :=
  "no pinned mathlib or external Lean 4 theorem for Caffarelli interior regularity / Monge-Ampere equation was found in this pass"

/-- Whether child audit `S1-M-149-C004` found an importable terminal Lean theorem. -/
def childC004ImportableTerminalTheoremFound : Bool :=
  false

/-- The theorem-tree leaves requested by child audit `S1-M-149-C005`. -/
def childC005TheoremTreeLeaves : List String := [
  "A1 finite-dimensional Euclidean domain model",
  "A2 convex solution represented by ConvexOn",
  "A3 Holder right-hand side represented by HolderOnWith",
  "A4 C2 alpha-style interior conclusion boundary",
  "B1 convex-function continuity anchor",
  "B2 convex-function local Lipschitz anchor",
  "B3 calculus and pointwise Holder anchor",
  "B4 determinant Lebesgue measure Laplacian adjacent anchors",
  "B5 absence check for Monge-Ampere Caffarelli terminal API",
  "C1 Aleksandrov or viscosity Monge-Ampere solution API",
  "C2 bridge classical determinant Hessian equation to weak formulation",
  "C3 normalized sections and section geometry",
  "C4 compactness and engulfing estimate package",
  "D1 strict convexity and section normalization branch",
  "D2 interior C1 alpha or W2p estimate branch",
  "D3 Schauder or linearized Monge-Ampere bridge branch",
  "D4 terminal C2 alpha Caffarelli regularity wrapper",
  "E1 validate repo-local statement-shape artifact",
  "E2 pin import check future external proof or record blocker",
  "E3 serial public blueprint todo synchronization"
]

/-- Terminal or integration leaves that remain unchecked after child audit `S1-M-149-C005`. -/
def childC005UncheckedTerminalLeaves : List String := [
  "B5",
  "C1",
  "C2",
  "C3",
  "C4",
  "D1",
  "D2",
  "D3",
  "D4",
  "E2",
  "E3"
]

/-- External Lean/GitHub audit terms requested by child audit `S1-M-149-C006`. -/
def childC006AuditTerms : List String := [
  "Caffarelli",
  "MongeAmpere",
  "Monge-Ampere",
  "Aleksandrov",
  "viscosity solution"
]

/--
Authentication status for child audit `S1-M-149-C006`.

The requested authenticated GitHub code search could not be completed in this
worker environment because `gh auth status` reported no logged-in GitHub hosts
and neither `GH_TOKEN` nor `GITHUB_TOKEN` was present.  Public repo-search and
local pinned-mathlib probes found no terminal Lean theorem, so this artifact
does not create an anchor-only completion claim.
-/
def childC006GitHubAuthenticationStatus : String :=
  "blocked: gh auth status reports no logged-in hosts and GH_TOKEN/GITHUB_TOKEN are absent"

/-- Whether child audit `S1-M-149-C006` found a terminal external Lean theorem. -/
def childC006TerminalExternalTheoremFound : Bool :=
  false

/-- Whether child audit `S1-M-149-C006` leaves a known external proof as anchor-only debt. -/
def childC006KnownRepoLocalIntegrationDebt : Bool :=
  false

/--
Shared-import decision status for child audit `S1-M-149-C007`.

This child is a serial integration gate, not a terminal PDE proof.  The Stage1
artifact is validated directly by its per-file command, while shared import
aggregators remain outside this worker's write scope.
-/
def childC007AggregatorDecisionStatus : String :=
  "serial_integration_pending: no shared Lean import aggregator edited in this child"

/-- Whether child audit `S1-M-149-C007` edited a shared Lean import aggregator. -/
def childC007SharedAggregatorEdited : Bool :=
  false

/-- Per-file validation command for the `S1-M-149-C007` aggregator decision gate. -/
def childC007ValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_149.lean"

/-- Public backfill task text for the later serialized import-aggregator decision. -/
def childC007PublicBackfillTask : String :=
  "Decide in a later serialized patch whether to add `AwesomeTheorems/Stage1/S1_M_149.lean` to a shared Lean import aggregator; if added, rerun the relevant aggregate build."

/-- Repo-local integration-debt gate result for child audit `S1-M-149-C007`. -/
def childC007RepoLocalIntegrationDebtGate : String :=
  "passed: no terminal theorem completion claimed and no external anchor-only proof treated as completed"

/-- Checked metadata equation for the audited mathlib revision. -/
theorem auditedMathlibRevision_eq :
    auditedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Checked metadata equation for the exact child `S1-M-149-C003` anchor list. -/
theorem childC003AnchorNames_eq :
    childC003AnchorNames = [
      "ConvexOn.continuousOn_interior",
      "ConvexOn.locallyLipschitzOn_interior",
      "HolderOnWith",
      "ContDiffPointwiseHolderAt",
      "Matrix.det",
      "MeasureTheory.volume",
      "Laplacian.laplacian"
    ] :=
  rfl

/-- Checked metadata equation for the nonterminal machine status. -/
theorem machineStatus_eq_statementShapeLocalChecked :
    machineStatus = "statement_shape_local_checked" :=
  rfl

/-- Checked metadata equation preventing this artifact from being read as terminal completion. -/
theorem terminalTheoremCompleted_eq_false :
    terminalTheoremCompleted = false :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C004` public blocker. -/
theorem childC004PublicBlocker_eq :
    childC004PublicBlocker =
      "no pinned mathlib or external Lean 4 theorem for Caffarelli interior regularity / Monge-Ampere equation was found in this pass" :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C004` terminal import status. -/
theorem childC004ImportableTerminalTheoremFound_eq_false :
    childC004ImportableTerminalTheoremFound = false :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C005` theorem-tree leaves. -/
theorem childC005TheoremTreeLeaves_eq :
    childC005TheoremTreeLeaves = [
      "A1 finite-dimensional Euclidean domain model",
      "A2 convex solution represented by ConvexOn",
      "A3 Holder right-hand side represented by HolderOnWith",
      "A4 C2 alpha-style interior conclusion boundary",
      "B1 convex-function continuity anchor",
      "B2 convex-function local Lipschitz anchor",
      "B3 calculus and pointwise Holder anchor",
      "B4 determinant Lebesgue measure Laplacian adjacent anchors",
      "B5 absence check for Monge-Ampere Caffarelli terminal API",
      "C1 Aleksandrov or viscosity Monge-Ampere solution API",
      "C2 bridge classical determinant Hessian equation to weak formulation",
      "C3 normalized sections and section geometry",
      "C4 compactness and engulfing estimate package",
      "D1 strict convexity and section normalization branch",
      "D2 interior C1 alpha or W2p estimate branch",
      "D3 Schauder or linearized Monge-Ampere bridge branch",
      "D4 terminal C2 alpha Caffarelli regularity wrapper",
      "E1 validate repo-local statement-shape artifact",
      "E2 pin import check future external proof or record blocker",
      "E3 serial public blueprint todo synchronization"
    ] :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C005` unchecked terminal leaves. -/
theorem childC005UncheckedTerminalLeaves_eq :
    childC005UncheckedTerminalLeaves = [
      "B5",
      "C1",
      "C2",
      "C3",
      "C4",
      "D1",
      "D2",
      "D3",
      "D4",
      "E2",
      "E3"
    ] :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C006` external audit terms. -/
theorem childC006AuditTerms_eq :
    childC006AuditTerms = [
      "Caffarelli",
      "MongeAmpere",
      "Monge-Ampere",
      "Aleksandrov",
      "viscosity solution"
    ] :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C006` authentication blocker. -/
theorem childC006GitHubAuthenticationStatus_eq :
    childC006GitHubAuthenticationStatus =
      "blocked: gh auth status reports no logged-in hosts and GH_TOKEN/GITHUB_TOKEN are absent" :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C006` external theorem finding. -/
theorem childC006TerminalExternalTheoremFound_eq_false :
    childC006TerminalExternalTheoremFound = false :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C006` integration-debt gate. -/
theorem childC006KnownRepoLocalIntegrationDebt_eq_false :
    childC006KnownRepoLocalIntegrationDebt = false :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C007` aggregator decision status. -/
theorem childC007AggregatorDecisionStatus_eq :
    childC007AggregatorDecisionStatus =
      "serial_integration_pending: no shared Lean import aggregator edited in this child" :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C007` shared aggregator edit gate. -/
theorem childC007SharedAggregatorEdited_eq_false :
    childC007SharedAggregatorEdited = false :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C007` validation command. -/
theorem childC007ValidationCommand_eq :
    childC007ValidationCommand =
      "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_149.lean" :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C007` public backfill task. -/
theorem childC007PublicBackfillTask_eq :
    childC007PublicBackfillTask =
      "Decide in a later serialized patch whether to add `AwesomeTheorems/Stage1/S1_M_149.lean` to a shared Lean import aggregator; if added, rerun the relevant aggregate build." :=
  rfl

/-- Checked metadata equation for the child `S1-M-149-C007` integration-debt gate. -/
theorem childC007RepoLocalIntegrationDebtGate_eq :
    childC007RepoLocalIntegrationDebtGate =
      "passed: no terminal theorem completion claimed and no external anchor-only proof treated as completed" :=
  rfl

/-! ## Audit probes -/

#check ConvexOn
#check ConvexOn.continuousOn_interior
#check ConvexOn.locallyLipschitzOn_interior
#check HolderOnWith
#check holderOnWith_one
#check ContDiffOn
#check ContDiffPointwiseHolderAt
#check ContDiffAt.contDiffPointwiseHolderAt
#check iteratedFDeriv
#check Matrix.det
#check MeasureTheory.volume
#check Laplacian.laplacian

end S1_M_149
end Stage1
end AwesomeTheorems
