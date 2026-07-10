import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Convex.Function
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Topology.MetricSpace.Bounded
import Mathlib.Topology.Semicontinuity.Basic

/-!
# S1-M-162 / THM-M-1266: Tonelli theorem for variational existence

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Tonelli direct-method existence theorem in the calculus of variations.

The pinned mathlib snapshot `8a178386ffc0f5fef0b77738bb5449d50efeea95`
has derivatives of curves, Bochner integrals, convexity predicates, lower
semicontinuity, compact minimization, and the measure-theoretic Tonelli theorem.
It does not expose a terminal theorem saying that a coercive convex Lagrangian
on an admissible class has an action-minimizing curve.  The declarations below
therefore normalize the action functional and the minimizer statement while
keeping weak compactness, boundary closure, coercivity, and lower-semicontinuity
proof packages explicit.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_162

universe u v

/-- Curves used by the normalized one-dimensional variational problem. -/
abbrev Curve (E : Type u) : Type u :=
  ℝ → E

/--
Formal velocity of a curve.

This uses mathlib's classical derivative for `ℝ`-parameterized curves.  A
terminal Tonelli formalization may replace this by an a.e. weak derivative or
Sobolev representative, but this definition fixes the classical boundary for
the Stage1 statement shape.
-/
def curveVelocity
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (u : Curve E) : Curve E :=
  fun t => deriv u t

/-- The formal action functional `u ↦ ∫ L(t, u(t), u'(t)) dμ(t)`. -/
def TonelliAction
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (μ : Measure ℝ) (L : ℝ × E × E → ℝ) (u : Curve E) : ℝ :=
  ∫ t, L (t, u t, curveVelocity u t) ∂ μ

/-- The formal action unfolds to the expected integral of the Lagrangian. -/
theorem tonelliAction_eq_integral
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (μ : Measure ℝ) (L : ℝ × E × E → ℝ) (u : Curve E) :
    TonelliAction μ L u = ∫ t, L (t, u t, curveVelocity u t) ∂ μ :=
  rfl

/--
Input data for the Tonelli variational-existence theorem.

The fields `coercive_growth`, `boundary_conditions_closed`, and
`compactness_or_weakCompactness` are deliberately explicit propositions: the
audited repo-local dependency closure does not yet provide a canonical Sobolev
admissible-class compactness theorem for this calculus-of-variations result.
The lower-semicontinuity and convexity predicates are expressed with current
mathlib APIs.
-/
structure TonelliVariationalProblem
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] : Type u where
  admissible : Set (Curve E)
  lagrangian : ℝ × E × E → ℝ
  measure : Measure ℝ
  nonempty_admissible : admissible.Nonempty
  lagrangian_lowerSemicontinuous : LowerSemicontinuous lagrangian
  velocity_convex : ∀ t x, ConvexOn ℝ univ (fun v : E => lagrangian (t, x, v))
  action_lowerSemicontinuous :
    LowerSemicontinuousOn (TonelliAction measure lagrangian) admissible
  coercive_growth : Prop
  boundary_conditions_closed : Prop
  compactness_or_weakCompactness : Prop

/-- The direct-method hypotheses that remain to be supplied by a terminal proof. -/
def DirectMethodHypotheses
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) : Prop :=
  P.coercive_growth ∧
    P.boundary_conditions_closed ∧
      P.compactness_or_weakCompactness

/-- A minimizer package for the formal Tonelli action. -/
structure TonelliMinimizerPackage
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) : Type u where
  minimizer : Curve E
  minimizer_admissible : minimizer ∈ P.admissible
  is_minimizer :
    IsMinOn (TonelliAction P.measure P.lagrangian) P.admissible minimizer

/--
Normalized Stage1 statement shape for Tonelli's existence theorem.

For every normed real state space and every admissible variational problem with
a lower-semicontinuous velocity-convex Lagrangian, the direct-method packages
should produce an action-minimizing admissible curve.
-/
def StatementShape
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] : Prop :=
  ∀ P : TonelliVariationalProblem E,
    DirectMethodHypotheses P → Nonempty (TonelliMinimizerPackage P)

/-- The statement shape unfolds to the expected direct-method implication. -/
theorem statementShape_iff_forall_problem
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    StatementShape E ↔
      ∀ P : TonelliVariationalProblem E,
        DirectMethodHypotheses P → Nonempty (TonelliMinimizerPackage P) :=
  Iff.rfl

/-- Status tag: the normalized statement shape is locally checked. -/
theorem statement_shape_local_checked
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    StatementShape E ↔
      ∀ P : TonelliVariationalProblem E,
        DirectMethodHypotheses P → Nonempty (TonelliMinimizerPackage P) :=
  statementShape_iff_forall_problem E

/-- The Lagrangian is convex in the velocity variable. -/
theorem lagrangian_velocity_convex
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) (t : ℝ) (x : E) :
    ConvexOn ℝ univ (fun v : E => P.lagrangian (t, x, v)) :=
  P.velocity_convex t x

/-- The formal action is lower semicontinuous on the admissible class. -/
theorem action_lowerSemicontinuousOn
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) :
    LowerSemicontinuousOn (TonelliAction P.measure P.lagrangian) P.admissible :=
  P.action_lowerSemicontinuous

/-- Checked compact lower-semicontinuous minimization anchor from mathlib. -/
theorem exists_minimizer_on_compact
    {A : Type u} [TopologicalSpace A] {s : Set A} {F : A → ℝ}
    (hne : s.Nonempty) (hcompact : IsCompact s)
    (hlsc : LowerSemicontinuousOn F s) :
    ∃ x ∈ s, IsMinOn F s x :=
  LowerSemicontinuousOn.exists_isMinOn hne hcompact hlsc

/--
If the admissible class is genuinely compact in the topology used for curves,
mathlib's lower-semicontinuous minimum theorem gives a minimizer for the formal
Tonelli action.
-/
theorem exists_action_minimizer_of_compact_admissible
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) (hcompact : IsCompact P.admissible) :
    ∃ u ∈ P.admissible,
      IsMinOn (TonelliAction P.measure P.lagrangian) P.admissible u :=
  exists_minimizer_on_compact P.nonempty_admissible hcompact
    P.action_lowerSemicontinuous

/-- Status tag: the compact lower-semicontinuity wrapper is locally checked. -/
theorem compact_lsc_wrapper_local_checked
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) (hcompact : IsCompact P.admissible) :
    ∃ u ∈ P.admissible,
      IsMinOn (TonelliAction P.measure P.lagrangian) P.admissible u :=
  exists_action_minimizer_of_compact_admissible P hcompact

/-- A terminal minimizer package exposes the expected comparison inequality. -/
theorem minimizer_action_le
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) (Q : TonelliMinimizerPackage P)
    {v : Curve E} (hv : v ∈ P.admissible) :
    TonelliAction P.measure P.lagrangian Q.minimizer ≤
      TonelliAction P.measure P.lagrangian v :=
  Q.is_minimizer hv

/-- Pinned mathlib revision used for the Stage1 anchor audit. -/
def mathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.Deriv.Basic",
  "Mathlib.Analysis.Convex.Function",
  "Mathlib.Analysis.Convex.Continuous",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Measure.Prod",
  "Mathlib.Topology.MetricSpace.Bounded",
  "Mathlib.Topology.Semicontinuity.Basic"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "deriv",
  "Bochner integral notation: ∫ t, f t ∂ μ",
  "MeasureTheory.integral",
  "MeasureTheory.lintegral_prod",
  "ConvexOn",
  "LowerSemicontinuous",
  "LowerSemicontinuousOn",
  "LowerSemicontinuousOn.exists_isMinOn",
  "IsMinOn",
  "IsCompact",
  "Bornology.cobounded",
  "MemLp",
  "HasCompactSupport"
]

/--
Search terms that did not locate a terminal calculus-of-variations Tonelli
existence theorem in pinned mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Tonelli",
  "calculus of variations",
  "direct method",
  "Lagrangian minimizer",
  "coercive Lagrangian",
  "weak derivative",
  "Sobolev minimizer",
  "variational existence",
  "action minimizer",
  "Euler Lagrange existence"
]

/-! ## External Lean project audit boundary -/

/--
Search terms assigned to the external Lean/GitHub audit child.

This list is kept separate from `absentTerminalSearchTerms`: the latter records
the pinned mathlib/local-anchor search boundary, while this one records the
external primary-source audit request that must be run with GitHub
authentication before the child can be closed as fully audited.
-/
def externalLeanAuditTerms : List String := [
  "Tonelli",
  "calculus of variations",
  "direct method",
  "Lagrangian minimizer",
  "coercive Lagrangian",
  "Sobolev minimizer"
]

/--
Machine-readable status for the external Lean project audit.

The authenticated GitHub code search was not available in the local execution
environment, so this status intentionally records an integration blocker rather
than converting anchor-only evidence into a completed theorem or dependency
task.  The local mathlib source tree was searched, and it only exposed the
measure-theoretic Tonelli anchors already disambiguated below.
-/
structure ExternalLeanAuditStatus : Type where
  terms : List String
  localMathlibAuditCompleted : Bool
  authenticatedGitHubSearchCompleted : Bool
  terminalExternalProofFound : Bool
  serializedDependencyIntegrationTaskRequired : Bool
  blocker : String

/-- Status for child `S1-M-162-C009` as of the local Stage1 execution pass. -/
def externalLeanAuditStatus : ExternalLeanAuditStatus where
  terms := externalLeanAuditTerms
  localMathlibAuditCompleted := true
  authenticatedGitHubSearchCompleted := false
  terminalExternalProofFound := false
  serializedDependencyIntegrationTaskRequired := false
  blocker :=
    "gh auth status reported no logged-in GitHub hosts on 2026-05-01; rerun authenticated GitHub code search before closing S1-M-162-C009."

/--
Status tag: the external audit is represented locally without claiming
completion of the authenticated GitHub search or a terminal imported proof.
-/
theorem external_lean_audit_status_local_checked :
    externalLeanAuditStatus.terms = externalLeanAuditTerms ∧
      externalLeanAuditStatus.localMathlibAuditCompleted = true ∧
      externalLeanAuditStatus.authenticatedGitHubSearchCompleted = false ∧
      externalLeanAuditStatus.terminalExternalProofFound = false ∧
      externalLeanAuditStatus.serializedDependencyIntegrationTaskRequired = false :=
  by
    simp [externalLeanAuditStatus]

/--
Machine status tags for this Stage1 slot.

These tags deliberately stop short of `terminal_theorem_completed`: the local
file checks the normalized statement shape and the compact-lsc minimization
wrapper, while the coercive/weak-compact direct-method proof package remains
future formalization work.
-/
def machineStatusTags : List String := [
  "statement_shape_local_checked",
  "compact_lsc_wrapper_local_checked"
]

/--
Name-disambiguation note: mathlib's `MeasureTheory.lintegral_prod` is the
measure-theoretic Tonelli theorem, not the calculus-of-variations existence
theorem targeted by this Stage1 slot.
-/
def tonelliNameDisambiguation : String :=
  "MeasureTheory.lintegral_prod is measure-theoretic Tonelli, not the variational existence theorem."

/--
Status tag: the Tonelli name collision is locally documented.  In particular,
the mathlib anchor `MeasureTheory.lintegral_prod` is not counted as a proof of
the calculus-of-variations existence theorem targeted by this Stage1 slot.
-/
theorem tonelli_name_disambiguation_local_checked :
    tonelliNameDisambiguation =
      "MeasureTheory.lintegral_prod is measure-theoretic Tonelli, not the variational existence theorem." :=
  rfl

/--
The public theorem-tree packages that should be serialized into the Stage1
planning surface.  P0-P1 are represented by checked local statement/wrapper
artifacts; P2-P5 remain nonterminal planning packages.
-/
def theoremTreePackagesForPublicBackfill : List String := [
  "P0 statement normalization and notation freeze",
  "P1 mathlib object-model and imported theorem audit",
  "P2 direct-method compactness package",
  "P3 lower-semicontinuity and convex-integral bridge",
  "P4 existence theorem wrapper",
  "P5 public merge-back gate"
]

/--
Unchecked terminal leaves for the public Stage1 backfill.  These are deliberately
listed as planning leaves, not as Lean proof obligations discharged by this
file.
-/
def uncheckedTerminalLeafIdsForPublicBackfill : List String := [
  "M1266-L014",
  "M1266-L015",
  "M1266-L016",
  "M1266-L017",
  "M1266-L018",
  "M1266-L019",
  "M1266-L020",
  "M1266-L021",
  "M1266-L022"
]

/-- Status tag: the public backfill leaf range is recorded locally. -/
theorem unchecked_terminal_leaf_ids_local_checked :
    uncheckedTerminalLeafIdsForPublicBackfill =
      ["M1266-L014", "M1266-L015", "M1266-L016", "M1266-L017",
       "M1266-L018", "M1266-L019", "M1266-L020", "M1266-L021",
       "M1266-L022"] :=
  rfl

/-! ## Admissible-topology selection task -/

/--
Topology choices that must be compared before the terminal Tonelli
formalization can leave the compact-surrogate wrapper.

This is a checked planning datatype, not a proof that any Sobolev or weak
compactness theorem is already available in the local dependency closure.
-/
inductive AdmissibleTopologyChoice where
  | classicalC1
  | sobolevW1p
  | weakSobolev
  | compactSurrogate
  deriving DecidableEq, Repr

/-- Stable public labels for the admissible-topology alternatives. -/
def admissibleTopologyChoiceLabel : AdmissibleTopologyChoice → String
  | .classicalC1 => "classical C^1 topology on curves"
  | .sobolevW1p => "Sobolev W^{1,p} strong topology"
  | .weakSobolev => "weak topology on a Sobolev admissible class"
  | .compactSurrogate => "compact surrogate admissible class for the first repo-local wrapper"

/-- The alternatives to record in the public topology-selection task. -/
def admissibleTopologyAlternatives : List AdmissibleTopologyChoice := [
  .classicalC1,
  .sobolevW1p,
  .weakSobolev,
  .compactSurrogate
]

/--
Repo-local task schema for selecting the admissible topology.

The `compactSurrogate` branch is the current checked wrapper path because
`compact_lsc_wrapper_local_checked` only needs an explicit compactness
hypothesis.  The Sobolev and weak-topology branches remain formalization debt
until the required compactness and lower-semicontinuity API is pinned or proved
locally.
-/
structure AdmissibleTopologySelectionTask : Type where
  alternatives : List AdmissibleTopologyChoice
  firstWrapperChoice : AdmissibleTopologyChoice
  mustCompareClassicalC1 : Prop
  mustCompareSobolevW1p : Prop
  mustCompareWeakTopology : Prop
  mustKeepCompactSurrogateOption : Prop
  noTerminalSobolevClaimYet : Prop

/-- Integration-ready topology-selection task for the public Stage1 backfill. -/
def admissibleTopologySelectionTask : AdmissibleTopologySelectionTask where
  alternatives := admissibleTopologyAlternatives
  firstWrapperChoice := .compactSurrogate
  mustCompareClassicalC1 := True
  mustCompareSobolevW1p := True
  mustCompareWeakTopology := True
  mustKeepCompactSurrogateOption := True
  noTerminalSobolevClaimYet := True

/--
Status tag: the admissible-topology choice task is locally represented while
the first checked wrapper remains the compact-surrogate route.
-/
theorem admissible_topology_selection_task_local_checked :
    admissibleTopologySelectionTask.alternatives = admissibleTopologyAlternatives ∧
      admissibleTopologySelectionTask.firstWrapperChoice =
        AdmissibleTopologyChoice.compactSurrogate ∧
      admissibleTopologySelectionTask.mustCompareClassicalC1 ∧
      admissibleTopologySelectionTask.mustCompareSobolevW1p ∧
      admissibleTopologySelectionTask.mustCompareWeakTopology ∧
      admissibleTopologySelectionTask.mustKeepCompactSurrogateOption ∧
      admissibleTopologySelectionTask.noTerminalSobolevClaimYet := by
  simp [admissibleTopologySelectionTask]

/-! ## Coercive-growth and minimizing-sequence compactness task -/

/--
Formal branches needed to turn coercive growth into compactness of minimizing
sequences.

These branches are planning leaves for the direct-method proof package.  They
do not assert that the Sobolev, weak-compactness, or compact-embedding theorem
has already been proved in this repository.
-/
inductive CoerciveCompactnessLeaf where
  | actionBoundToCoerciveEstimate
  | coerciveEstimateToVelocityBound
  | boundaryDataToCurveBound
  | minimizingSequenceSubsequence
  | limitCurveAdmissible
  | compactSurrogateBridge
  deriving DecidableEq, Repr

/-- Stable public labels for the coercive-growth compactness leaves. -/
def coerciveCompactnessLeafLabel : CoerciveCompactnessLeaf → String
  | .actionBoundToCoerciveEstimate =>
      "derive coercive estimates from a bounded action minimizing sequence"
  | .coerciveEstimateToVelocityBound =>
      "convert coercive Lagrangian growth into uniform velocity or Sobolev bounds"
  | .boundaryDataToCurveBound =>
      "use endpoint/boundary data to bound the curves, not just their velocities"
  | .minimizingSequenceSubsequence =>
      "extract a convergent or weakly convergent subsequence of a minimizing sequence"
  | .limitCurveAdmissible =>
      "prove the subsequential limit remains in the admissible boundary class"
  | .compactSurrogateBridge =>
      "specialize the branch to the compact-admissible surrogate used by the local wrapper"

/-- Coercive-growth compactness leaves to serialize into the public task. -/
def coerciveCompactnessLeaves : List CoerciveCompactnessLeaf := [
  .actionBoundToCoerciveEstimate,
  .coerciveEstimateToVelocityBound,
  .boundaryDataToCurveBound,
  .minimizingSequenceSubsequence,
  .limitCurveAdmissible,
  .compactSurrogateBridge
]

/--
Repo-local task schema for the coercive-growth and minimizing-sequence
compactness package.

The `compactSurrogateBridge` field records the only currently checked local
route: if an integrator supplies `IsCompact P.admissible`, the existing compact
lower-semicontinuity wrapper produces a minimizer.  The genuine Tonelli route
through coercive estimates and weak compactness remains formalization debt.
-/
structure CoerciveCompactnessTask : Type where
  leaves : List CoerciveCompactnessLeaf
  mustStartFromBoundedActionSequence : Prop
  mustProveCoerciveGrowthEstimate : Prop
  mustProveCurveOrVelocityBound : Prop
  mustExtractCompactOrWeaklyCompactSubsequence : Prop
  mustProveLimitAdmissibility : Prop
  compactSurrogateBridge : Prop
  noTerminalWeakCompactnessClaimYet : Prop

/-- Integration-ready coercive-growth compactness task for the public backfill. -/
def coerciveCompactnessTask : CoerciveCompactnessTask where
  leaves := coerciveCompactnessLeaves
  mustStartFromBoundedActionSequence := True
  mustProveCoerciveGrowthEstimate := True
  mustProveCurveOrVelocityBound := True
  mustExtractCompactOrWeaklyCompactSubsequence := True
  mustProveLimitAdmissibility := True
  compactSurrogateBridge := True
  noTerminalWeakCompactnessClaimYet := True

/-- The direct-method hypothesis package exposes the coercive-growth branch. -/
theorem directMethodHypotheses_coercive_growth
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {P : TonelliVariationalProblem E} (h : DirectMethodHypotheses P) :
    P.coercive_growth :=
  h.1

/-- The direct-method hypothesis package exposes the compactness branch. -/
theorem directMethodHypotheses_compactness_or_weakCompactness
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {P : TonelliVariationalProblem E} (h : DirectMethodHypotheses P) :
    P.compactness_or_weakCompactness :=
  h.2.2

/--
Status tag: the coercive-growth and minimizing-sequence compactness task is
locally represented without claiming a terminal weak-compactness theorem.
-/
theorem coercive_compactness_task_local_checked :
    coerciveCompactnessTask.leaves = coerciveCompactnessLeaves ∧
      coerciveCompactnessTask.mustStartFromBoundedActionSequence ∧
      coerciveCompactnessTask.mustProveCoerciveGrowthEstimate ∧
      coerciveCompactnessTask.mustProveCurveOrVelocityBound ∧
      coerciveCompactnessTask.mustExtractCompactOrWeaklyCompactSubsequence ∧
      coerciveCompactnessTask.mustProveLimitAdmissibility ∧
      coerciveCompactnessTask.compactSurrogateBridge ∧
      coerciveCompactnessTask.noTerminalWeakCompactnessClaimYet := by
  simp [coerciveCompactnessTask]

/-! ## Convex-integral lower-semicontinuity task -/

/--
Target proposition for the future convex-integral lower-semicontinuity theorem.

At this Stage1 boundary the target is still supplied as the
`action_lowerSemicontinuous` field of `TonelliVariationalProblem`.  A terminal
formalization should replace that abstract field by a proof from convergence
hypotheses, measurability/integrability, and convexity in the velocity variable.
-/
def ConvexIntegralLowerSemicontinuityTarget
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) : Prop :=
  LowerSemicontinuousOn (TonelliAction P.measure P.lagrangian) P.admissible

/-- The current problem field provides the normalized lower-semicontinuity target. -/
theorem convexIntegralLowerSemicontinuityTarget_of_problem_field
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : TonelliVariationalProblem E) :
    ConvexIntegralLowerSemicontinuityTarget P :=
  P.action_lowerSemicontinuous

/--
Formal leaves for replacing the abstract action-lower-semicontinuity field by a
concrete convex-integral theorem for `u ↦ ∫ L(t, u, u')`.

These are checked planning leaves.  They do not assert that the weak
lower-semicontinuity or Ioffe/Tonelli integral theorem has already been proved
in the repo-local Lean dependency closure.
-/
inductive ConvexIntegralLscLeaf where
  | convergenceModeForCurves
  | lagrangianMeasurableIntegrable
  | stateConvergencePassage
  | velocityConvergencePassage
  | convexVelocityLiminf
  | integralLiminfPassage
  | actionLscReplacement
  | weakDerivativeCompatibility
  deriving DecidableEq, Repr

/-- Stable public labels for the convex-integral lower-semicontinuity leaves. -/
def convexIntegralLscLeafLabel : ConvexIntegralLscLeaf → String
  | .convergenceModeForCurves =>
      "fix the curve convergence mode used by the admissible topology"
  | .lagrangianMeasurableIntegrable =>
      "prove measurability and integrability for t ↦ L(t, u(t), u'(t))"
  | .stateConvergencePassage =>
      "pass the state argument u_n(t) to the limit in the Lagrangian"
  | .velocityConvergencePassage =>
      "identify the velocity convergence or weak-derivative convergence hypothesis"
  | .convexVelocityLiminf =>
      "use convexity in the velocity variable for the lower-bound step"
  | .integralLiminfPassage =>
      "turn pointwise or weak lower bounds into an integral liminf inequality"
  | .actionLscReplacement =>
      "replace the abstract action_lowerSemicontinuous field by the concrete theorem"
  | .weakDerivativeCompatibility =>
      "bridge the classical derivative action with Sobolev or weak-derivative representatives"

/-- Convex-integral lower-semicontinuity leaves to serialize into the public task. -/
def convexIntegralLscLeaves : List ConvexIntegralLscLeaf := [
  .convergenceModeForCurves,
  .lagrangianMeasurableIntegrable,
  .stateConvergencePassage,
  .velocityConvergencePassage,
  .convexVelocityLiminf,
  .integralLiminfPassage,
  .actionLscReplacement,
  .weakDerivativeCompatibility
]

/--
Repo-local task schema for the convex-integral lower-semicontinuity package.

The `currentTargetStillAbstract` field records the exact integration boundary:
the local Tonelli statement already requires action lower semicontinuity, but
this child does not prove that hypothesis from convexity and convergence data.
-/
structure ConvexIntegralLowerSemicontinuityTask : Type where
  leaves : List ConvexIntegralLscLeaf
  targetIsTonelliActionLsc : Prop
  mustChooseConvergenceMode : Prop
  mustProveMeasurabilityAndIntegrability : Prop
  mustUseVelocityConvexity : Prop
  mustProveIntegralLiminfInequality : Prop
  mustReplaceAbstractActionLscField : Prop
  mustBridgeClassicalAndWeakDerivatives : Prop
  currentTargetStillAbstract : Prop
  noTerminalConvexIntegralLscClaimYet : Prop

/-- Integration-ready convex-integral lower-semicontinuity task for public backfill. -/
def convexIntegralLowerSemicontinuityTask :
    ConvexIntegralLowerSemicontinuityTask where
  leaves := convexIntegralLscLeaves
  targetIsTonelliActionLsc := True
  mustChooseConvergenceMode := True
  mustProveMeasurabilityAndIntegrability := True
  mustUseVelocityConvexity := True
  mustProveIntegralLiminfInequality := True
  mustReplaceAbstractActionLscField := True
  mustBridgeClassicalAndWeakDerivatives := True
  currentTargetStillAbstract := True
  noTerminalConvexIntegralLscClaimYet := True

/--
Status tag: the convex-integral lower-semicontinuity task is locally
represented without claiming the terminal theorem that derives action lower
semicontinuity from convexity and convergence hypotheses.
-/
theorem convex_integral_lsc_task_local_checked :
    convexIntegralLowerSemicontinuityTask.leaves = convexIntegralLscLeaves ∧
      convexIntegralLowerSemicontinuityTask.targetIsTonelliActionLsc ∧
      convexIntegralLowerSemicontinuityTask.mustChooseConvergenceMode ∧
      convexIntegralLowerSemicontinuityTask.mustProveMeasurabilityAndIntegrability ∧
      convexIntegralLowerSemicontinuityTask.mustUseVelocityConvexity ∧
      convexIntegralLowerSemicontinuityTask.mustProveIntegralLiminfInequality ∧
      convexIntegralLowerSemicontinuityTask.mustReplaceAbstractActionLscField ∧
      convexIntegralLowerSemicontinuityTask.mustBridgeClassicalAndWeakDerivatives ∧
      convexIntegralLowerSemicontinuityTask.currentTargetStillAbstract ∧
      convexIntegralLowerSemicontinuityTask.noTerminalConvexIntegralLscClaimYet := by
  simp [convexIntegralLowerSemicontinuityTask]

/-! ## Shared import aggregator decision task -/

/--
Serialized choices for the later shared-import decision.

The child execution pass is not allowed to edit shared aggregators directly, so
this datatype records the integration-ready decision without changing
`AwesomeTheorems.lean`.
-/
inductive SharedImportAggregatorDecision where
  | addStage1Module
  | deferUntilTerminalTheorem
  | keepStandaloneOnly
  deriving DecidableEq, Repr

/--
Machine-readable status for deciding whether this Stage1 artifact should be
added to a shared Lean import aggregator.

The local recommendation is to add the module in a later serialized patch
because the file is a validated Stage1 artifact with explicit nonterminal
status tags.  That import must not be described as completing Tonelli's
calculus-of-variations theorem.
-/
structure SharedImportAggregatorDecisionStatus : Type where
  modulePath : String
  candidateImportLine : String
  targetAggregator : String
  moduleValidatedLocally : Bool
  sharedAggregatorEditedInChild : Bool
  recommendedDecision : SharedImportAggregatorDecision
  terminalTheoremCompletedByImport : Bool
  reason : String

/-- Integration-ready shared-import decision for child `S1-M-162-C010`. -/
def sharedImportAggregatorDecisionStatus :
    SharedImportAggregatorDecisionStatus where
  modulePath := "AwesomeTheorems/Stage1/S1_M_162.lean"
  candidateImportLine := "import AwesomeTheorems.Stage1.S1_M_162"
  targetAggregator := "Formalizations/Lean/AwesomeTheorems.lean"
  moduleValidatedLocally := true
  sharedAggregatorEditedInChild := false
  recommendedDecision := .addStage1Module
  terminalTheoremCompletedByImport := false
  reason :=
    "Add the validated Stage1 module in a later serialized aggregator patch; this records statement-shape and compact-lsc-wrapper evidence only, not a terminal Tonelli theorem."

/--
Status tag: the aggregator decision is locally checked while the shared
aggregator remains untouched by this child worker.
-/
theorem shared_import_aggregator_decision_local_checked :
    sharedImportAggregatorDecisionStatus.modulePath =
        "AwesomeTheorems/Stage1/S1_M_162.lean" ∧
      sharedImportAggregatorDecisionStatus.candidateImportLine =
        "import AwesomeTheorems.Stage1.S1_M_162" ∧
      sharedImportAggregatorDecisionStatus.targetAggregator =
        "Formalizations/Lean/AwesomeTheorems.lean" ∧
      sharedImportAggregatorDecisionStatus.moduleValidatedLocally = true ∧
      sharedImportAggregatorDecisionStatus.sharedAggregatorEditedInChild = false ∧
      sharedImportAggregatorDecisionStatus.recommendedDecision =
        SharedImportAggregatorDecision.addStage1Module ∧
      sharedImportAggregatorDecisionStatus.terminalTheoremCompletedByImport = false :=
  by
    simp [sharedImportAggregatorDecisionStatus]

/-! ## Audit probes -/

#check Curve
#check curveVelocity
#check TonelliAction
#check TonelliVariationalProblem
#check DirectMethodHypotheses
#check TonelliMinimizerPackage
#check StatementShape
#check statement_shape_local_checked
#check exists_minimizer_on_compact
#check exists_action_minimizer_of_compact_admissible
#check compact_lsc_wrapper_local_checked
#check tonelli_name_disambiguation_local_checked
#check theoremTreePackagesForPublicBackfill
#check uncheckedTerminalLeafIdsForPublicBackfill
#check unchecked_terminal_leaf_ids_local_checked
#check AdmissibleTopologyChoice
#check admissibleTopologyChoiceLabel
#check admissibleTopologySelectionTask
#check admissible_topology_selection_task_local_checked
#check CoerciveCompactnessLeaf
#check coerciveCompactnessLeafLabel
#check coerciveCompactnessTask
#check directMethodHypotheses_coercive_growth
#check directMethodHypotheses_compactness_or_weakCompactness
#check coercive_compactness_task_local_checked
#check ConvexIntegralLowerSemicontinuityTarget
#check convexIntegralLowerSemicontinuityTarget_of_problem_field
#check ConvexIntegralLscLeaf
#check convexIntegralLscLeafLabel
#check convexIntegralLscLeaves
#check ConvexIntegralLowerSemicontinuityTask
#check convexIntegralLowerSemicontinuityTask
#check convex_integral_lsc_task_local_checked
#check SharedImportAggregatorDecision
#check SharedImportAggregatorDecisionStatus
#check sharedImportAggregatorDecisionStatus
#check shared_import_aggregator_decision_local_checked
#check externalLeanAuditTerms
#check ExternalLeanAuditStatus
#check externalLeanAuditStatus
#check external_lean_audit_status_local_checked
#check deriv
#check ConvexOn
#check LowerSemicontinuousOn.exists_isMinOn
#check IsMinOn
#check IsCompact
#check MemLp
#check HasCompactSupport

end S1_M_162
end Stage1
end AwesomeTheorems
