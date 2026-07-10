import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Martingale.OptionalStopping
import Mathlib.Probability.Martingale.Upcrossing
import Mathlib.Probability.Process.Predictable
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic

/-!
# S1-M-286 / THM-M-1006: Burkholder-Davis-Gundy inequality

This Stage1 artifact records a conservative Lean 4 boundary for the
Burkholder-Davis-Gundy inequality.  The target theorem says that, for a
martingale, the `L^p` norm of the maximal martingale size is equivalent to the
`L^p` norm of the square root of its quadratic variation.

The pinned mathlib snapshot has probability measures, filtrations, adapted
processes, martingales, conditional expectations, stopping times, stopped
processes, and `L^p` seminorms.  It does not expose a terminal theorem named
Burkholder-Davis-Gundy/BDG, nor a full stochastic-calculus API for predictable
quadratic variation of continuous martingales.  Accordingly, this file gives a
typed discrete-time statement shape, a finite-horizon running-maximum API, and
low-risk wrappers around existing mathlib predicates.  It does not prove the
BDG inequality.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal NNReal ProbabilityTheory

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_286

/-- The discrete time axis used for the conservative BDG boundary. -/
abbrev Time : Type := ℕ

/-- Real-valued discrete-time stochastic process on a measurable space. -/
abbrev RealProcess (Ω : Type u) :=
  Time → Ω → ℝ

/-- One-step martingale increment for the discrete square-function boundary. -/
def martingaleIncrement {Ω : Type u} (process : RealProcess Ω) (n : Time) : Ω → ℝ :=
  fun ω => process (n + 1) ω - process n ω

/--
Pathwise discrete quadratic variation `sum_{k < n} (M_{k+1} - M_k)^2`.

This is the canonical square-function side available repo-locally without a
conditional-expectation/bracket construction.  The predictable quadratic
variation candidate below records separately that the chosen bracket process is
predictable and terminally agrees with the supplied BDG datum.
-/
def pathwiseQuadraticVariation {Ω : Type u} (process : RealProcess Ω) : RealProcess Ω :=
  fun n ω => (Finset.range n).sum fun k => (martingaleIncrement process k ω) ^ 2

/-- Square function associated to the pathwise discrete quadratic variation. -/
def pathwiseSquareFunction {Ω : Type u} (process : RealProcess Ω) : RealProcess Ω :=
  fun n ω => Real.sqrt (pathwiseQuadraticVariation process n ω)

/--
Canonical finite-horizon terminal running maximum for the discrete BDG boundary.

For terminal time `n`, this is the pathwise maximum of `|M_k|` over
`0 ≤ k ≤ n`, implemented as a nonempty `Finset.sup'` over `Finset.range
(n + 1)`.  This gives a concrete repo-local API for the maximal-process side of
BDG without depending on a separate stochastic-process maximal theorem.
-/
def runningMaxProcess {Ω : Type u} (process : RealProcess Ω) : RealProcess Ω :=
  fun n ω =>
    (Finset.range (n + 1)).sup' Finset.nonempty_range_add_one fun k =>
      |process k ω|

/-- The terminal running maximum is bounded by `a` exactly when every sampled time is. -/
theorem runningMaxProcess_le_iff {Ω : Type u} (process : RealProcess Ω)
    (n : Time) (ω : Ω) (a : ℝ) :
    runningMaxProcess process n ω ≤ a ↔
      ∀ k : Time, k ≤ n → |process k ω| ≤ a := by
  simp [runningMaxProcess, Finset.sup'_le_iff, Finset.mem_range]

/-- The finite-horizon running maximum is nonnegative. -/
theorem runningMaxProcess_nonnegative {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (process : RealProcess Ω) (n : Time) :
    0 ≤ᵐ[μ] runningMaxProcess process n := by
  exact Filter.Eventually.of_forall fun ω =>
    le_trans (abs_nonneg (process 0 ω)) <|
      Finset.le_sup' (fun k => |process k ω|) (by simp [Finset.mem_range])

/-- The finite-horizon running maximum dominates each sampled absolute value. -/
theorem abs_process_le_runningMaxProcess {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (process : RealProcess Ω) {k n : Time} (hkn : k ≤ n) :
    (fun ω => |process k ω|) ≤ᵐ[μ] runningMaxProcess process n := by
  exact Filter.Eventually.of_forall fun ω =>
    Finset.le_sup' (fun j => |process j ω|) <|
      Finset.mem_range.mpr (Nat.lt_succ_of_le hkn)

/--
Canonical Stage1 API for the terminal running-maximum side of BDG.

The supplied terminal random variable must agree almost everywhere with the
finite-horizon maximum `max_{k ≤ terminalTime} |M_k|`.  General pathwise
properties of the chosen maximum are proved above as separate lemmas, so this
package replaces the former unstructured proposition-valued field with a
concrete equality against a checked repo-local definition.
-/
structure DiscreteTerminalRunningMaximum (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (process : RealProcess Ω) (terminalTime : Time)
    (terminalMax : Ω → ℝ) : Type u where
  terminal_eq : terminalMax =ᵐ[μ] runningMaxProcess process terminalTime

/--
Canonical Stage1 API for the discrete predictable quadratic-variation /
square-function side of BDG.

The pinned mathlib closure exposes `MeasureTheory.IsPredictable`, so the
predictability part is no longer a bare placeholder.  The true stochastic
analysis still missing from the repo-local closure is the bracket theorem
connecting this predictable process to the martingale increments; that
obligation is represented here by concrete terminal equality and square-function
alignment fields, not by an unstructured `Prop` field in `BDGData`.
-/
structure DiscretePredictableQuadraticVariation (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (filtration : Filtration Time ‹MeasurableSpace Ω›)
    (process : RealProcess Ω) (terminalTime : Time) (terminalQV : Ω → ℝ) :
    Type (u + 1) where
  qvProcess : RealProcess Ω
  terminal_eq : terminalQV =ᵐ[μ] qvProcess terminalTime
  isPredictable : IsPredictable filtration qvProcess
  startsAtZero : qvProcess 0 =ᵐ[μ] 0
  nonnegative : ∀ n : Time, 0 ≤ᵐ[μ] qvProcess n
  monotone : ∀ᵐ ω ∂μ, Monotone fun n : Time => qvProcess n ω
  squareFunction : RealProcess Ω
  squareFunction_eq_pathwise :
    squareFunction = pathwiseSquareFunction process
  terminal_squareFunction_eq_qvSqrt :
  squareFunction terminalTime =ᵐ[μ] fun ω => Real.sqrt (terminalQV ω)

/--
Data for a discrete-time terminal BDG statement.

The terminal maximum is packaged by `DiscreteTerminalRunningMaximum`, a concrete
finite-horizon `Finset.sup'` API over the absolute value of the process.  The
quadratic-variation side is packaged by `DiscretePredictableQuadraticVariation`,
which uses mathlib `IsPredictable` and an explicit square-function interface.
A future terminal proof still needs to replace the Stage1 quadratic-variation
candidate API with a full bracket construction or prove the bridge obligations
locally.
-/
structure BDGData (Ω : Type u) [MeasurableSpace Ω] : Type (u + 1) where
  μ : Measure Ω
  filtration : Filtration Time ‹MeasurableSpace Ω›
  process : RealProcess Ω
  terminalTime : Time
  p : ℝ≥0∞
  terminalMax : Ω → ℝ
  quadraticVariation : Ω → ℝ
  isProbability : IsProbabilityMeasure μ
  martingale : Martingale process filtration μ
  exponent_pos : p ≠ 0
  exponent_ne_top : p ≠ ∞
  terminalMax_nonneg : 0 ≤ᵐ[μ] terminalMax
  quadraticVariation_nonneg : 0 ≤ᵐ[μ] quadraticVariation
  terminalMax_memLp : MemLp terminalMax p μ
  qvSqrt_memLp : MemLp (fun ω => Real.sqrt (quadraticVariation ω)) p μ
  terminalRunningMaximum :
    DiscreteTerminalRunningMaximum Ω μ process terminalTime terminalMax
  predictableQuadraticVariation :
    DiscretePredictableQuadraticVariation Ω μ filtration process terminalTime quadraticVariation

/-- The square-root quadratic-variation random variable used in the BDG norm comparison. -/
def qvSqrt {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) : Ω → ℝ :=
  fun ω => Real.sqrt (D.quadraticVariation ω)

/--
Hypotheses that remain outside the current repo-local stochastic-calculus
boundary after the data fields have identified the supplied terminal maximum
and quadratic-variation candidate with their intended Stage1 objects.
-/
def BDGHypotheses {Ω : Type u} [MeasurableSpace Ω] (_D : BDGData Ω) : Prop :=
  True

/--
BDG conclusion for the normalized discrete-time statement: there are finite
constants, depending on the exponent in a future strengthened version, which
bound the `L^p` seminorm of the terminal running maximum above and below by
the `L^p` seminorm of the square-root quadratic variation.
-/
def BDGConclusion {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) : Prop :=
  ∃ c C : ℝ≥0∞,
    c ≠ 0 ∧
      C ≠ ∞ ∧
        c * eLpNorm (qvSqrt D) D.p D.μ ≤ eLpNorm D.terminalMax D.p D.μ ∧
          eLpNorm D.terminalMax D.p D.μ ≤ C * eLpNorm (qvSqrt D) D.p D.μ

/--
Stage1 normalized statement shape for the Burkholder-Davis-Gundy inequality.

This is a formalization boundary, not a proof.  It says that every packaged
discrete-time real martingale with identified terminal running maximum and
predictable quadratic variation should satisfy the two-sided `L^p` comparison.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : BDGData Ω,
      BDGHypotheses D → BDGConclusion D

/--
Statement-normalization note for the public Stage1 backfill.

`AwesomeTheorems.Stage1.S1_M_286.StatementShape` is the checked repo-local Lean
boundary for a discrete-time Burkholder-Davis-Gundy statement shape.  It is not
a proof of the BDG inequality: the terminal running-maximum side is a concrete
finite-horizon `Finset.sup'` API, and the predictable quadratic-variation side
is a concrete Stage1 candidate API using mathlib `IsPredictable`, not a
terminal bracket construction or two-sided `L^p` comparison proof.
-/
def statementNormalizationNote : String :=
  "AwesomeTheorems.Stage1.S1_M_286.StatementShape is a checked repo-local " ++
    "Lean statement-shape boundary for BDG, not a proof of the " ++
    "Burkholder-Davis-Gundy inequality."

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω],
      ∀ D : BDGData Ω,
        BDGHypotheses D → BDGConclusion D) :
    StatementShape.{u} :=
  h

/-- The normalized statement unfolds to the expected data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : BDGData Ω,
          BDGHypotheses D → BDGConclusion D :=
  Iff.rfl

/-- The packaged process is a mathlib martingale. -/
theorem martingale_of_data {Ω : Type u} [MeasurableSpace Ω]
    (D : BDGData Ω) :
    Martingale D.process D.filtration D.μ :=
  D.martingale

/-- mathlib's martingale API gives strong adaptedness of the process. -/
theorem process_stronglyAdapted {Ω : Type u} [MeasurableSpace Ω]
    (D : BDGData Ω) :
    StronglyAdapted D.filtration D.process :=
  D.martingale.stronglyAdapted

/-- mathlib's martingale API gives integrability at each discrete time. -/
theorem process_integrable {Ω : Type u} [MeasurableSpace Ω]
    (D : BDGData Ω) (n : Time) :
    Integrable (D.process n) D.μ :=
  D.martingale.integrable n

/-- The packaged terminal running maximum is in the requested `L^p` space. -/
theorem terminalMax_memLp_of_data {Ω : Type u} [MeasurableSpace Ω]
    (D : BDGData Ω) :
    MemLp D.terminalMax D.p D.μ :=
  D.terminalMax_memLp

/-- The packaged square-root quadratic variation is in the requested `L^p` space. -/
theorem qvSqrt_memLp_of_data {Ω : Type u} [MeasurableSpace Ω]
    (D : BDGData Ω) :
    MemLp (qvSqrt D) D.p D.μ :=
  D.qvSqrt_memLp

/-- The boundary hypotheses expose the terminal running-maximum identification. -/
theorem terminalMax_eq_runningMaxProcess
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    D.terminalMax =ᵐ[D.μ] runningMaxProcess D.process D.terminalTime :=
  D.terminalRunningMaximum.terminal_eq

/-- The packaged terminal maximum is nonnegative because it is assumed in `BDGData`. -/
theorem terminalMax_nonnegative_of_data
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    0 ≤ᵐ[D.μ] D.terminalMax :=
  D.terminalMax_nonneg

/-- The canonical running maximum dominates each sampled absolute value up to terminal time. -/
theorem abs_process_le_terminal_runningMax
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω)
    {k : Time} (hk : k ≤ D.terminalTime) :
    (fun ω => |D.process k ω|) ≤ᵐ[D.μ]
      runningMaxProcess D.process D.terminalTime :=
  abs_process_le_runningMaxProcess D.μ D.process hk

/-- Project the concrete predictable quadratic-variation process from the data. -/
def predictableQVProcess {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    RealProcess Ω :=
  D.predictableQuadraticVariation.qvProcess

/-- The quadratic-variation candidate terminally agrees with the predictable process. -/
theorem quadraticVariation_terminal_eq_predictableQV
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    D.quadraticVariation =ᵐ[D.μ] predictableQVProcess D D.terminalTime :=
  D.predictableQuadraticVariation.terminal_eq

/-- The predictable quadratic-variation process is predictable in mathlib's checked sense. -/
theorem predictableQV_isPredictable
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    IsPredictable D.filtration (predictableQVProcess D) :=
  D.predictableQuadraticVariation.isPredictable

/-- A predictable quadratic-variation process is strongly adapted. -/
theorem predictableQV_stronglyAdapted
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    StronglyAdapted D.filtration (predictableQVProcess D) :=
  (predictableQV_isPredictable D).adapted

/-- The predictable quadratic-variation process starts at zero almost everywhere. -/
theorem predictableQV_startsAtZero
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    predictableQVProcess D 0 =ᵐ[D.μ] 0 :=
  D.predictableQuadraticVariation.startsAtZero

/-- The predictable quadratic-variation process is nonnegative at every time. -/
theorem predictableQV_nonnegative
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) (n : Time) :
    0 ≤ᵐ[D.μ] predictableQVProcess D n :=
  D.predictableQuadraticVariation.nonnegative n

/-- The predictable quadratic-variation process is monotone almost surely. -/
theorem predictableQV_monotone
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    ∀ᵐ ω ∂D.μ, Monotone fun n : Time => predictableQVProcess D n ω :=
  D.predictableQuadraticVariation.monotone

/-- The packaged square function is the pathwise discrete square function. -/
theorem squareFunction_eq_pathwise
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    D.predictableQuadraticVariation.squareFunction = pathwiseSquareFunction D.process :=
  D.predictableQuadraticVariation.squareFunction_eq_pathwise

/-- At terminal time, the packaged square function agrees with `qvSqrt`. -/
theorem terminal_squareFunction_eq_qvSqrt
    {Ω : Type u} [MeasurableSpace Ω] (D : BDGData Ω) :
    D.predictableQuadraticVariation.squareFunction D.terminalTime =ᵐ[D.μ] qvSqrt D :=
  D.predictableQuadraticVariation.terminal_squareFunction_eq_qvSqrt

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check BDGData
#check martingaleIncrement
#check pathwiseQuadraticVariation
#check pathwiseSquareFunction
#check runningMaxProcess
#check runningMaxProcess_le_iff
#check runningMaxProcess_nonnegative
#check abs_process_le_runningMaxProcess
#check DiscreteTerminalRunningMaximum
#check DiscretePredictableQuadraticVariation
#check BDGHypotheses
#check BDGConclusion
#check qvSqrt
#check statementNormalizationNote
#check MeasureTheory.Filtration
#check MeasureTheory.StronglyAdapted
#check MeasureTheory.Martingale
#check MeasureTheory.Martingale.integrable
#check MeasureTheory.Martingale.stronglyAdapted
#check MeasureTheory.IsPredictable
#check MeasureTheory.IsPredictable.adapted
#check MeasureTheory.eLpNorm
#check MeasureTheory.MemLp

/-- Pinned mathlib revision used for the `THM-M-1006.mathlib-anchor` child audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Exact module list requested by `THM-M-1006.mathlib-anchor`.

These modules provide martingale, optional-stopping/upcrossing, and `L^p`
seminorm substrate for the Stage1 BDG statement shape.  Recording this list is
not a proof of the Burkholder-Davis-Gundy inequality.
-/
def requestedMathlibAnchorModules : List String := [
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Upcrossing",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic"
]

#check mathlibPinnedRevision
#check requestedMathlibAnchorModules

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Upcrossing",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.Predictable",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.stoppedProcess",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.Martingale.stronglyAdapted",
  "MeasureTheory.IsPredictable",
  "MeasureTheory.IsPredictable.adapted",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.MemLp"
]

/--
Adjacent martingale-inequality anchors requested by `THM-M-1006.doob-audit`.

These names are recorded only as nearby Doob maximal/upcrossing inequalities in
the pinned mathlib tree.  They do not close the Burkholder-Davis-Gundy theorem,
which still needs terminal running-maximum and predictable quadratic-variation
APIs plus a two-sided `L^p` comparison proof.
-/
def adjacentMartingaleInequalityAnchors : List String := [
  "MeasureTheory.maximal_ineq",
  "MeasureTheory.Submartingale.mul_integral_upcrossingsBefore_le_integral_pos_part",
  "MeasureTheory.Submartingale.mul_lintegral_upcrossings_le_lintegral_pos_part"
]

#check adjacentMartingaleInequalityAnchors
#check MeasureTheory.maximal_ineq
#check MeasureTheory.Submartingale.mul_integral_upcrossingsBefore_le_integral_pos_part
#check MeasureTheory.Submartingale.mul_lintegral_upcrossings_le_lintegral_pos_part

/-- Search terms used in the pinned local mathlib tree and external primary-source audit. -/
def anchorSearchTerms : List String := [
  "Burkholder",
  "Davis",
  "Gundy",
  "BDG",
  "martingale Lp norm",
  "quadratic variation",
  "QuadraticVariation",
  "predictable quadratic variation",
  "Doob maximal inequality",
  "martingale maximal inequality"
]

/-- Primary-source pin for the local mathlib audit used by this statement-shape file. -/
def mathlibPrimarySource : String :=
  "https://github.com/leanprover-community/mathlib4, revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Primary-source external audit record for `THM-M-1006.external-audit`.

Accessible Lean 4 sources checked in this worker pass did not expose a theorem
named for Burkholder-Davis-Gundy/BDG.  In particular, the repo-local pinned
mathlib source tree has no `Burkholder`, `BDG`, or `Gundy` match under
`Mathlib/`, and no quadratic-variation API match under mathlib's
`Probability/` or `MeasureTheory/` subtrees.  GitHub code search was not a
usable primary-source oracle in this unauthenticated environment: the REST API
returned a rate-limit response and the web code-search page requires sign-in.
Thus no external theorem candidate is available to pin, import, or check here.
-/
def externalBDGAuditStatus : String :=
  "No accessible primary Lean 4 source checked in this pass exposed a BDG theorem; no external dependency candidate is available to pin/import/check."

/--
Concrete integration blockers if a later authenticated search locates a BDG
formalization.

These are blockers for a future external theorem hit, not evidence that such a
hit currently exists.
-/
def externalBDGIntegrationBlockers : List String := [
  "obtain a primary Lean 4 source location with repository URL, commit SHA, module path, theorem name, toolchain, and license",
  "add the source as a pinned or vendored dependency without editing shared aggregators in this child task",
  "import and #check the theorem or a repo-local wrapper with `lake env lean` before any theorem-completion claim"
]

#check externalBDGAuditStatus
#check externalBDGIntegrationBlockers

/-! ## Theorem-tree audit surface for the Stage1 public backfill. -/

/-- Package row for the `THM-M-1006.theorem-tree` public merge task. -/
structure TheoremTreePackage where
  id : String
  title : String
  status : String
  detail : String

/-- Leaf row for the `THM-M-1006.theorem-tree` public merge task. -/
structure TheoremTreeLeaf where
  id : String
  packageId : String
  budget : String
  status : String
  detail : String

/--
M1006 package split for the BDG Stage1 theorem tree.

These rows are checked repository-local metadata for the public audit surface.
They do not assert that the terminal Burkholder-Davis-Gundy inequality has been
proved.
-/
def theoremTreePackages : List TheoremTreePackage := [
  {
    id := "M1006.P0",
    title := "statement_normalization",
    status := "checked_statement_shape",
    detail := "StatementShape, BDGData, BDGHypotheses, BDGConclusion, qvSqrt, and the discrete-time data boundary are present."
  },
  {
    id := "M1006.P1",
    title := "mathlib_object_model",
    status := "checked_repo_local_wrappers",
    detail := "Martingale, StronglyAdapted, Integrable, MemLp, and eLpNorm anchors are imported and projected by local wrappers."
  },
  {
    id := "M1006.P2",
    title := "maximal_martingale_layer",
    status := "checked_adjacent_anchors",
    detail := "Doob maximal and upcrossing inequalities are recorded as adjacent anchors only, not as BDG closure."
  },
  {
    id := "M1006.P3",
    title := "running_maximum_and_qv_apis",
    status := "checked_stage1_api_boundary",
    detail := "Finite running maximum and predictable quadratic-variation/square-function APIs replace the earlier unstructured Prop placeholders."
  },
  {
    id := "M1006.P4",
    title := "discrete_terminal_BDG_core",
    status := "unchecked_terminal_proof",
    detail := "The two-sided Lp BDG comparison is still absent from the repo-local Lean closure."
  },
  {
    id := "M1006.P5",
    title := "continuous_or_local_extension",
    status := "unchecked_scope_decision",
    detail := "Continuous or local martingale extensions remain separate future branches if the public scope requires them."
  },
  {
    id := "M1006.P6",
    title := "repo_local_wrapper_or_dependency_gate",
    status := "audit_checked_no_external_candidate",
    detail := "Accessible primary Lean 4 audit found no BDG theorem candidate to pin/import/check; future hits must be integrated or blocked explicitly."
  },
  {
    id := "M1006.P7",
    title := "public_merge_surface",
    status := "unchecked_integrator_owned",
    detail := "Public blueprint/todo/README synchronization remains serial integrator work."
  }
]

/--
M1006 leaf ledger for the Stage1 theorem-tree merge.

Terminal BDG proof leaves intentionally remain `unchecked_terminal_proof`; this
file only checks the statement/API/audit boundary.
-/
def theoremTreeLeaves : List TheoremTreeLeaf := [
  {
    id := "M1006-L001",
    packageId := "M1006.P0",
    budget := "<=45",
    status := "checked_statement_shape",
    detail := "Define Time, RealProcess, qvSqrt, BDGData, BDGHypotheses, BDGConclusion, and StatementShape."
  },
  {
    id := "M1006-L002",
    packageId := "M1006.P0",
    budget := "<=25",
    status := "checked_statement_shape",
    detail := "Statement exposes universe, measurable space, measure, filtration, exponent, terminal maximum, quadratic variation, and conclusion type."
  },
  {
    id := "M1006-L003",
    packageId := "M1006.P1",
    budget := "<=20",
    status := "checked_mathlib_anchor",
    detail := "Check Filtration, Martingale, Martingale.integrable, and Martingale.stronglyAdapted."
  },
  {
    id := "M1006-L004",
    packageId := "M1006.P1",
    budget := "<=20",
    status := "checked_mathlib_anchor",
    detail := "Check eLpNorm and MemLp as the Lp interface used by the statement shape."
  },
  {
    id := "M1006-L005",
    packageId := "M1006.P1",
    budget := "<=20",
    status := "checked_repo_local_wrapper",
    detail := "Projection wrappers martingale_of_data, process_stronglyAdapted, and process_integrable are present."
  },
  {
    id := "M1006-L006",
    packageId := "M1006.P1",
    budget := "<=15",
    status := "checked_repo_local_wrapper",
    detail := "Projection wrappers terminalMax_memLp_of_data and qvSqrt_memLp_of_data are present."
  },
  {
    id := "M1006-L007",
    packageId := "M1006.P2",
    budget := "<=35",
    status := "checked_adjacent_anchor",
    detail := "MeasureTheory.maximal_ineq is recorded as a Doob maximal inequality anchor, not BDG closure."
  },
  {
    id := "M1006-L008",
    packageId := "M1006.P2",
    budget := "<=35",
    status := "checked_adjacent_anchor",
    detail := "Upcrossing inequality anchors are recorded as adjacent martingale infrastructure only."
  },
  {
    id := "M1006-L009",
    packageId := "M1006.P3",
    budget := "<=90",
    status := "checked_stage1_api_boundary",
    detail := "runningMaxProcess and DiscreteTerminalRunningMaximum replace terminalMax_is_runningSup."
  },
  {
    id := "M1006-L010",
    packageId := "M1006.P3",
    budget := "<=100",
    status := "checked_stage1_api_boundary",
    detail := "DiscretePredictableQuadraticVariation replaces quadraticVariation_is_predictableQV with an IsPredictable-backed API."
  },
  {
    id := "M1006-L011",
    packageId := "M1006.P4",
    budget := "<=100",
    status := "unchecked_terminal_proof",
    detail := "Prove the lower BDG inequality c * ||[M]^(1/2)||_p <= ||M*||_p for the selected discrete model."
  },
  {
    id := "M1006-L012",
    packageId := "M1006.P4",
    budget := "<=100",
    status := "unchecked_terminal_proof",
    detail := "Prove the upper BDG inequality ||M*||_p <= C * ||[M]^(1/2)||_p for the selected discrete model."
  },
  {
    id := "M1006-L013",
    packageId := "M1006.P5",
    budget := "<=80",
    status := "unchecked_scope_decision",
    detail := "Split continuous/local martingale extensions into explicit branches only if public scope requires them."
  },
  {
    id := "M1006-L014",
    packageId := "M1006.P6",
    budget := "<=70",
    status := "audit_checked_no_external_candidate",
    detail := "No accessible external Lean 4 BDG theorem candidate was found; future candidates must be pinned/imported/checked or blocked."
  },
  {
    id := "M1006-L015",
    packageId := "M1006.P7",
    budget := "<=60",
    status := "unchecked_integrator_owned",
    detail := "Merge checked statement shape, anchors, API boundary, external audit, and theorem tree into the public Stage1 surface."
  },
  {
    id := "M1006-L016",
    packageId := "M1006.P7",
    budget := "<=30",
    status := "unchecked_integrator_owned",
    detail := "Rerun local validation from a clean integrator context and synchronize public status surfaces."
  }
]

/-- Terminal proof leaves that must remain unchecked until a real Lean proof or dependency closes them. -/
def uncheckedTerminalBDGProofLeaves : List String := [
  "M1006-L011",
  "M1006-L012"
]

/-- Current theorem-tree status note for the public backfill. -/
def theoremTreeStatusNote : String :=
  "M1006.P0 through M1006.P7 and M1006-L001 through M1006-L016 are recorded; terminal BDG proof leaves M1006-L011 and M1006-L012 remain unchecked."

#check TheoremTreePackage
#check TheoremTreeLeaf
#check theoremTreePackages
#check theoremTreeLeaves
#check uncheckedTerminalBDGProofLeaves
#check theoremTreeStatusNote

end S1_M_286
end Stage1
end AwesomeTheorems
