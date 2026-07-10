import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Predictable
import Mathlib.Probability.Moments.Basic
import Mathlib.Probability.Moments.IntegrableExpMul
import Mathlib.MeasureTheory.Measure.Tilted

/-!
# S1-M-239 / THM-M-1046: Novikov condition

This Stage1 artifact records a conservative Lean boundary for Novikov's
condition: under exponential integrability of one half of the terminal quadratic
variation, the stochastic exponential of a continuous local martingale is a true
martingale.

The pinned mathlib snapshot has filtrations, predictable processes,
martingales, conditional expectation, moment-generating functions, exponential
integrability lemmas, and exponentially tilted measures.  It does not expose a
terminal API for stochastic integration, semimartingales, local martingales,
quadratic variation, Doleans-Dade stochastic exponentials, or Novikov's theorem.

Accordingly this file gives a typed statement shape and low-risk wrappers
around existing mathlib predicates.  It does not prove Novikov's condition.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory Topology

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_239

/-- The nonnegative continuous-time axis used for the Novikov boundary. -/
abbrev Time : Type := ℝ≥0

/-- Real-valued stochastic process on a measurable probability space. -/
abbrev RealProcess (Ω : Type u) :=
  Time → Ω → ℝ

/-- A localizing sequence of stopping times for a continuous-time process. -/
abbrev LocalizingSequence (Ω : Type u) :=
  ℕ → Ω → WithTop Time

/--
Normalized data for Novikov's condition on a finite horizon.

The quadratic-variation candidate, stochastic-integral compatibility boundary,
and stochastic-exponential local-martingale boundary are packaged with the
concrete predictable-process, `MemLp`, stopped-process, and martingale APIs that
are available in the current repo-local mathlib closure.  The closure still
lacks the stochastic-calculus API needed to construct these objects from first
principles or prove that the supplied quadratic-variation candidate is the
bracket of the supplied local martingale.
-/
structure PredictableQuadraticVariationCandidate (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (filtration : Filtration Time ‹MeasurableSpace Ω›)
    (quadraticVariation : RealProcess Ω) : Prop where
  isPredictable : IsPredictable filtration quadraticVariation
  pathContinuous : ∀ᵐ ω ∂μ, Continuous fun t : Time => quadraticVariation t ω
  monotone : ∀ᵐ ω ∂μ, Monotone fun t : Time => quadraticVariation t ω
  nonnegative : ∀ t : Time, 0 ≤ᵐ[μ] quadraticVariation t
  startsAtZero : quadraticVariation 0 =ᵐ[μ] 0

/--
The formal expression expected for the stochastic exponential
`exp(M_t - 1/2 <M>_t)`, parametrized by explicit process and bracket
candidates.

This is an expression-level object only.  A terminal proof must connect it to a
real stochastic-exponential construction once such an API is available locally.
-/
def stochasticExponentialFormula {Ω : Type u} (process quadraticVariation : RealProcess Ω) :
    RealProcess Ω :=
  fun t ω => Real.exp (process t ω - ((1 : ℝ) / 2) * quadraticVariation t ω)

/--
Checked repo-local boundary for the Doleans-Dade stochastic exponential being a
local martingale.

The process is not an arbitrary proposition: the structure carries an explicit
process, identifies it with the formula `exp(M_t - 1/2 <M>_t)`, records that it
starts at one, and requires stopped-martingale evidence along the supplied
localizing sequence.  This is still not a terminal Doleans-Dade construction
from a stochastic-calculus API; it is the strongest currently checkable
replacement for the old bare `stochasticExponentialIsLocalMartingale : Prop`
field.
-/
structure DoleansDadeExponentialLocalMartingaleCandidate (Ω : Type u)
    [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration Time ‹MeasurableSpace Ω›)
    (process quadraticVariation : RealProcess Ω)
    (localizingSeq : LocalizingSequence Ω) where
  exponentialProcess : RealProcess Ω
  exponential_eq_formula :
    exponentialProcess = stochasticExponentialFormula process quadraticVariation
  startsAtOne : exponentialProcess 0 =ᵐ[μ] 1
  localizingSeq_isStoppingTime :
    ∀ n : ℕ, IsStoppingTime filtration (localizingSeq n)
  stopped_stochasticExponential_martingale :
    ∀ n : ℕ,
      Martingale (stoppedProcess exponentialProcess (localizingSeq n)) filtration μ

/--
Repo-local stochastic-integral compatibility boundary for Novikov's condition.

The pinned mathlib closure does not expose a canonical stochastic integral
against a continuous local martingale.  This structure therefore records the
concrete checked interface that Novikov's theorem will need from such an API:
a stochastic-integral operation, a predictable square-integrable domain, zero
initial value, and stopped martingality along the supplied localizing sequence.
It is not a construction of stochastic integration.
-/
structure StochasticIntegralCompatibilityCandidate (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (filtration : Filtration Time ‹MeasurableSpace Ω›)
    (integrator : RealProcess Ω) (localizingSeq : LocalizingSequence Ω) where
  stochasticIntegral : RealProcess Ω → RealProcess Ω
  integrablePredictable : RealProcess Ω → Prop
  domain_predictable :
    ∀ {integrand : RealProcess Ω},
      integrablePredictable integrand → IsPredictable filtration integrand
  domain_memLp :
    ∀ {integrand : RealProcess Ω},
      integrablePredictable integrand → ∀ t : Time, MemLp (integrand t) 2 μ
  integral_startsAtZero :
    ∀ {integrand : RealProcess Ω},
      integrablePredictable integrand → stochasticIntegral integrand 0 =ᵐ[μ] 0
  stopped_integral_martingale :
    ∀ {integrand : RealProcess Ω},
      integrablePredictable integrand → ∀ n : ℕ,
        Martingale (stoppedProcess (stochasticIntegral integrand) (localizingSeq n))
          filtration μ

/--
Normalized data for Novikov's condition on a finite horizon.
-/
structure NovikovData (Ω : Type u) [MeasurableSpace Ω] : Type (u + 1) where
  μ : Measure Ω
  filtration : Filtration Time ‹MeasurableSpace Ω›
  process : RealProcess Ω
  quadraticVariation : RealProcess Ω
  localizingSeq : LocalizingSequence Ω
  terminalTime : Time
  isProbability : IsProbabilityMeasure μ
  sigmaFiniteFiltration : SigmaFiniteFiltration μ filtration
  stronglyAdapted : StronglyAdapted filtration process
  predictableQuadraticVariation :
    PredictableQuadraticVariationCandidate Ω μ filtration quadraticVariation
  stoppedMartingale :
    ∀ n : ℕ,
      IsStoppingTime filtration (localizingSeq n) ∧
        Martingale (stoppedProcess process (localizingSeq n)) filtration μ
  pathContinuous : ∀ᵐ ω ∂μ, Continuous fun t : Time => process t ω
  startsAtZero : process 0 =ᵐ[μ] 0
  terminalQuadraticVariationIntegrable :
    Integrable (fun ω => Real.exp (((1 : ℝ) / 2) * quadraticVariation terminalTime ω)) μ
  stochasticIntegralCompatibility :
    StochasticIntegralCompatibilityCandidate Ω μ filtration process localizingSeq
  stochasticExponentialLocalMartingale :
    DoleansDadeExponentialLocalMartingaleCandidate Ω μ filtration process
      quadraticVariation localizingSeq
  stochasticExponentialIntegrandInDomain :
    stochasticIntegralCompatibility.integrablePredictable
      stochasticExponentialLocalMartingale.exponentialProcess

/--
The formal expression expected for the stochastic exponential
`exp(M_t - 1/2 <M>_t)`.

This is an expression-level object only.  A terminal proof must connect it to a
real stochastic-exponential construction once such an API is available locally.
-/
def stochasticExponential {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) :
    RealProcess Ω :=
  D.stochasticExponentialLocalMartingale.exponentialProcess

/-- The terminal random variable used in Novikov's exponential-integrability assumption. -/
def terminalNovikovWeight {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) :
    Ω → ℝ :=
  fun ω => Real.exp (((1 : ℝ) / 2) * D.quadraticVariation D.terminalTime ω)

/-- Hypotheses outside the current mathlib stochastic-calculus boundary. -/
def NovikovHypotheses {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) : Prop :=
  Integrable (terminalNovikovWeight D) D.μ

/--
Conclusion expected from Novikov's condition: the stochastic exponential is a
true martingale on the supplied finite time horizon.
-/
def NovikovConclusion {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) : Prop :=
  Martingale (stochasticExponential D) D.filtration D.μ

/--
Stage1 normalized statement shape for Novikov's condition.

For every probability space and every real continuous local martingale with a
candidate predictable quadratic variation, exponential integrability of
`exp(1/2 * <M>_T)` should imply that the stochastic exponential
`exp(M_t - 1/2 * <M>_t)` is a true martingale.

This declaration is a precise formalization boundary only.  The repo-local Lean
closure does not contain the proof body or the stochastic-calculus primitives
required for a terminal proof.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : NovikovData Ω,
      NovikovHypotheses D → NovikovConclusion D

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω],
      ∀ D : NovikovData Ω,
        NovikovHypotheses D → NovikovConclusion D) :
    StatementShape.{u} :=
  h

/-- The normalized statement unfolds to the expected data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : NovikovData Ω,
          NovikovHypotheses D → NovikovConclusion D :=
  Iff.rfl

/-! ## Public statement-normalization boundary -/

/--
Public Stage1 boundary for `THM-M-1046`.

This deliberately aliases `AwesomeTheorems.Stage1.S1_M_239.StatementShape`.
Use the `NovikovData` package as the current canonical repo-local statement
shape until stochastic-integral, predictable-quadratic-variation, and
Doleans-Dade stochastic-exponential APIs are available locally.
-/
abbrev PublicStatementNormalization : Prop :=
  StatementShape.{u}

/-- The public-normalization boundary is definitionally the same as `StatementShape`. -/
theorem publicStatementNormalization_iff_statementShape :
    PublicStatementNormalization.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/-- Canonical checked name for the current repo-local statement boundary. -/
def publicStatementBoundaryName : String :=
  "AwesomeTheorems.Stage1.S1_M_239.StatementShape"

/-- The audited `NovikovData` boundary is the recommended public canonical shape. -/
def novikovDataBoundaryShouldBePublicCanonical : Bool := true

/-- Sanity check for the public canonical-boundary decision. -/
theorem novikovDataBoundaryShouldBePublicCanonical_eq_true :
    novikovDataBoundaryShouldBePublicCanonical = true :=
  rfl

/-- Checked metadata for the public Stage1 backfill note. -/
def publicStatementNormalizationNotes : List String := [
  "Use AwesomeTheorems.Stage1.S1_M_239.StatementShape as the current repo-local Lean statement boundary for THM-M-1046.",
  "The checked boundary packages a finite-horizon probability space, filtration, real process, concrete predictable quadratic-variation candidate, localizing sequence, stopped-martingale local-martingale evidence, path regularity, monotone nonnegative quadratic-variation evidence, a concrete stochastic-integral compatibility interface, a concrete stopped-martingale candidate for the formula exp(M_t - 1/2 <M>_t), and the Novikov exponential-integrability hypothesis.",
  "This is not a terminal Novikov theorem: construction of the stochastic-integral interface, bracket identification for the predictable quadratic-variation candidate, Doleans-Dade stochastic-exponential construction, local-to-true martingale upgrade, and terminal assembly remain formalization debt."
]

/-- The public statement-normalization metadata is explicitly non-terminal. -/
def publicStatementNormalizationIsTerminal : Bool := false

/-- Sanity check for the non-terminal public-normalization gate. -/
theorem publicStatementNormalizationIsTerminal_eq_false :
    publicStatementNormalizationIsTerminal = false :=
  rfl

/-! ## External anchor integration gate -/

/--
Audit shape for a possible future external Lean 4 terminal proof of Novikov's
condition.
-/
structure ExternalLeanAnchorAudit where
  exactTerminalProofFound : Prop
  importedIntoLakeClosure : Prop
  concreteIntegrationBlockerRecorded : Prop

/--
Repo-local integration-debt gate: if an exact external Lean 4 terminal proof is
found, it must either enter this Lake closure or be blocked by a concrete
integration reason.  Anchor-only evidence is not a completed state for this
slot.
-/
def RepoLocalIntegrationDebtGate (A : ExternalLeanAnchorAudit) : Prop :=
  A.exactTerminalProofFound →
    A.importedIntoLakeClosure ∨ A.concreteIntegrationBlockerRecorded

/-- If no exact external anchor is found, the integration-debt gate is vacuous. -/
theorem repoLocalIntegrationDebtGate_of_no_external_anchor
    (A : ExternalLeanAnchorAudit) (h : Not A.exactTerminalProofFound) :
    RepoLocalIntegrationDebtGate A := by
  intro hfound
  exact False.elim (h hfound)

/-- The packaged data exposes each stopped martingale in the localizing sequence. -/
theorem stoppedMartingale_of_data {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) (n : ℕ) :
    Martingale (stoppedProcess D.process (D.localizingSeq n)) D.filtration D.μ :=
  (D.stoppedMartingale n).2

/-- The packaged data exposes each localizing stopping time. -/
theorem localizingSeq_isStoppingTime {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) (n : ℕ) :
    IsStoppingTime D.filtration (D.localizingSeq n) :=
  (D.stoppedMartingale n).1

/-- The process is strongly adapted to the supplied filtration. -/
theorem process_stronglyAdapted {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    StronglyAdapted D.filtration D.process :=
  D.stronglyAdapted

/-- The quadratic-variation candidate is strongly adapted to the supplied filtration. -/
theorem quadraticVariation_stronglyAdapted {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    StronglyAdapted D.filtration D.quadraticVariation :=
  D.predictableQuadraticVariation.isPredictable.adapted

/-- The quadratic-variation candidate is predictable in mathlib's checked sense. -/
theorem quadraticVariation_isPredictable {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    IsPredictable D.filtration D.quadraticVariation :=
  D.predictableQuadraticVariation.isPredictable

/-- The concrete predictable-quadratic-variation candidate stores path continuity. -/
theorem quadraticVariation_pathContinuous {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    ∀ᵐ ω ∂D.μ, Continuous fun t : Time => D.quadraticVariation t ω :=
  D.predictableQuadraticVariation.pathContinuous

/-- The concrete predictable-quadratic-variation candidate stores monotonicity. -/
theorem quadraticVariation_monotone {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    ∀ᵐ ω ∂D.μ, Monotone fun t : Time => D.quadraticVariation t ω :=
  D.predictableQuadraticVariation.monotone

/-- The concrete predictable-quadratic-variation candidate stores nonnegativity. -/
theorem quadraticVariation_nonnegative {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) (t : Time) :
    0 ≤ᵐ[D.μ] D.quadraticVariation t :=
  D.predictableQuadraticVariation.nonnegative t

/-- The concrete predictable-quadratic-variation candidate starts at zero. -/
theorem quadraticVariation_startsAtZero {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    D.quadraticVariation 0 =ᵐ[D.μ] 0 :=
  D.predictableQuadraticVariation.startsAtZero

/-- The Novikov terminal weight is exactly the stored exponential-integrability expression. -/
theorem terminalNovikovWeight_integrable {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    Integrable (terminalNovikovWeight D) D.μ :=
  D.terminalQuadraticVariationIntegrable

/-- The terminal Novikov weight is a.e. strongly measurable. -/
theorem terminalNovikovWeight_aestronglyMeasurable {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    AEStronglyMeasurable (terminalNovikovWeight D) D.μ :=
  D.terminalQuadraticVariationIntegrable.aestronglyMeasurable

/-- A probability measure with integrable exponential tilt gives a probability tilted measure. -/
theorem tilted_terminalNovikovWeight_isProbability {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    IsProbabilityMeasure
      (D.μ.tilted fun ω => ((1 : ℝ) / 2) * D.quadraticVariation D.terminalTime ω) := by
  have hne : NeZero D.μ := ⟨D.isProbability.ne_zero⟩
  letI : NeZero D.μ := hne
  simpa [terminalNovikovWeight] using
    (isProbabilityMeasure_tilted
      (μ := D.μ)
      (f := fun ω => ((1 : ℝ) / 2) * D.quadraticVariation D.terminalTime ω)
      D.terminalQuadraticVariationIntegrable)

/-- mathlib's stopped martingale API supplies integrability of every stopped slice. -/
theorem stopped_process_integrable {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) (n : ℕ) (t : Time) :
    Integrable (stoppedProcess D.process (D.localizingSeq n) t) D.μ :=
  (stoppedMartingale_of_data D n).integrable t

/-- The stochastic exponential unfolds to the explicit formula stored in the boundary. -/
theorem stochasticExponential_eq_formula {Ω : Type u} [MeasurableSpace Ω]
    (D : NovikovData Ω) :
    stochasticExponential D = stochasticExponentialFormula D.process D.quadraticVariation :=
  D.stochasticExponentialLocalMartingale.exponential_eq_formula

/-- The stochastic-integral compatibility boundary exposes predictable integrands. -/
theorem stochasticIntegralCompatibility_domain_predictable
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω)
    {integrand : RealProcess Ω}
    (hintegrand : D.stochasticIntegralCompatibility.integrablePredictable integrand) :
    IsPredictable D.filtration integrand :=
  D.stochasticIntegralCompatibility.domain_predictable hintegrand

/-- The stochastic-integral compatibility boundary exposes time-slice `L2` integrability. -/
theorem stochasticIntegralCompatibility_domain_memLp
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω)
    {integrand : RealProcess Ω}
    (hintegrand : D.stochasticIntegralCompatibility.integrablePredictable integrand) :
    ∀ t : Time, MemLp (integrand t) 2 D.μ :=
  D.stochasticIntegralCompatibility.domain_memLp hintegrand

/-- The stochastic integral of a domain integrand starts at zero. -/
theorem stochasticIntegralCompatibility_integral_startsAtZero
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω)
    {integrand : RealProcess Ω}
    (hintegrand : D.stochasticIntegralCompatibility.integrablePredictable integrand) :
    D.stochasticIntegralCompatibility.stochasticIntegral integrand 0 =ᵐ[D.μ] 0 :=
  D.stochasticIntegralCompatibility.integral_startsAtZero hintegrand

/--
The stochastic-integral compatibility boundary exposes stopped martingality
along the localizing sequence.
-/
theorem stochasticIntegralCompatibility_stopped_integral_martingale
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω)
    {integrand : RealProcess Ω}
    (hintegrand : D.stochasticIntegralCompatibility.integrablePredictable integrand)
    (n : ℕ) :
    Martingale
      (stoppedProcess (D.stochasticIntegralCompatibility.stochasticIntegral integrand)
        (D.localizingSeq n)) D.filtration D.μ :=
  D.stochasticIntegralCompatibility.stopped_integral_martingale hintegrand n

/-- The Novikov stochastic-exponential integrand lies in the compatibility domain. -/
theorem stochasticExponential_integrablePredictable
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) :
    D.stochasticIntegralCompatibility.integrablePredictable (stochasticExponential D) :=
  D.stochasticExponentialIntegrandInDomain

/-- The Novikov stochastic-exponential integrand is predictable in the checked API sense. -/
theorem stochasticExponential_isPredictable
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) :
    IsPredictable D.filtration (stochasticExponential D) :=
  D.stochasticIntegralCompatibility.domain_predictable
    (stochasticExponential_integrablePredictable D)

/-- The Novikov stochastic-exponential integrand is square-integrable at every time slice. -/
theorem stochasticExponential_memLp_two
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) :
    ∀ t : Time, MemLp (stochasticExponential D t) 2 D.μ :=
  D.stochasticIntegralCompatibility.domain_memLp
    (stochasticExponential_integrablePredictable D)

/-- The stochastic integral of the Novikov exponential integrand starts at zero. -/
theorem stochasticIntegral_stochasticExponential_startsAtZero
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) :
    D.stochasticIntegralCompatibility.stochasticIntegral (stochasticExponential D) 0 =ᵐ[D.μ] 0 :=
  D.stochasticIntegralCompatibility.integral_startsAtZero
    (stochasticExponential_integrablePredictable D)

/--
The stochastic integral of the Novikov exponential integrand is a stopped
martingale along every supplied localizing time.
-/
theorem stochasticIntegral_stochasticExponential_stopped_martingale
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) (n : ℕ) :
    Martingale
      (stoppedProcess
        (D.stochasticIntegralCompatibility.stochasticIntegral (stochasticExponential D))
        (D.localizingSeq n)) D.filtration D.μ :=
  D.stochasticIntegralCompatibility.stopped_integral_martingale
    (stochasticExponential_integrablePredictable D) n

/-- The checked Doleans-Dade exponential candidate starts at one. -/
theorem stochasticExponential_startsAtOne
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) :
    stochasticExponential D 0 =ᵐ[D.μ] 1 :=
  D.stochasticExponentialLocalMartingale.startsAtOne

/--
The checked Doleans-Dade exponential candidate uses stopping times from the
supplied localizing sequence.
-/
theorem stochasticExponential_localizingSeq_isStoppingTime
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) (n : ℕ) :
    IsStoppingTime D.filtration (D.localizingSeq n) :=
  D.stochasticExponentialLocalMartingale.localizingSeq_isStoppingTime n

/--
The checked Doleans-Dade exponential candidate is a stopped martingale along
the supplied localizing sequence.
-/
theorem stochasticExponential_stopped_martingale
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) (n : ℕ) :
    Martingale (stoppedProcess (stochasticExponential D) (D.localizingSeq n))
      D.filtration D.μ :=
  D.stochasticExponentialLocalMartingale.stopped_stochasticExponential_martingale n

/-- The checked Doleans-Dade exponential candidate gives integrability of stopped slices. -/
theorem stochasticExponential_stopped_integrable
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) (n : ℕ) (t : Time) :
    Integrable (stoppedProcess (stochasticExponential D) (D.localizingSeq n) t) D.μ :=
  (stochasticExponential_stopped_martingale D n).integrable t

/-- The Novikov hypotheses expose the explicit exponential-integrability condition. -/
theorem integrable_terminalNovikovWeight_of_hypotheses
    {Ω : Type u} [MeasurableSpace Ω] {D : NovikovData Ω}
    (hD : NovikovHypotheses D) :
    Integrable (terminalNovikovWeight D) D.μ :=
  hD

/-- The data exposes the checked local stochastic-exponential boundary. -/
def stochasticExponential_localMartingale_boundary
    {Ω : Type u} [MeasurableSpace Ω] (D : NovikovData Ω) :
    DoleansDadeExponentialLocalMartingaleCandidate Ω D.μ D.filtration
      D.process D.quadraticVariation D.localizingSeq :=
  D.stochasticExponentialLocalMartingale

/-! ## Discrete-time exponential-martingale surrogate -/

/-- Real-valued discrete-time process used for the finite-time surrogate. -/
abbrev DiscreteRealProcess (Ω : Type u) :=
  ℕ → Ω → ℝ

/--
Discrete-time analogue of the exponential expression
`exp(M_n - 1/2 A_n)`.

Here `bracketProxy` is only a discrete compensator/bracket proxy.  This is not a
quadratic-variation construction.
-/
def discreteExponentialFormula {Ω : Type u}
    (process bracketProxy : DiscreteRealProcess Ω) : DiscreteRealProcess Ω :=
  fun n ω => Real.exp (process n ω - ((1 : ℝ) / 2) * bracketProxy n ω)

/--
Checked finite/discrete-time surrogate for exponential martingales.

If the discrete exponential formula is adapted, integrable, and satisfies the
one-step conditional-expectation identity, mathlib's `martingale_nat` upgrades
the one-step identities to the full martingale property over all `i ≤ j`.
This is a genuine repo-local Lean lemma, but it assumes the exponential
compensation identity rather than deriving it from stochastic calculus or
Novikov's condition.
-/
theorem discreteExponential_martingale_of_oneStep_condExp
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℕ ‹MeasurableSpace Ω›)
    [IsFiniteMeasure μ]
    (process bracketProxy : DiscreteRealProcess Ω)
    (hadapted :
      StronglyAdapted filtration (discreteExponentialFormula process bracketProxy))
    (hintegrable :
      ∀ n : ℕ, Integrable (discreteExponentialFormula process bracketProxy n) μ)
    (honeStep :
      ∀ n : ℕ,
        μ[discreteExponentialFormula process bracketProxy (n + 1) | filtration n]
          =ᵐ[μ] discreteExponentialFormula process bracketProxy n) :
    Martingale (discreteExponentialFormula process bracketProxy) filtration μ :=
  martingale_nat hadapted hintegrable fun n => (honeStep n).symm

/-- The discrete surrogate exposes the all-times conditional-expectation identity. -/
theorem discreteExponential_condExp_ae_eq_of_oneStep
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℕ ‹MeasurableSpace Ω›)
    [IsFiniteMeasure μ]
    (process bracketProxy : DiscreteRealProcess Ω)
    (hadapted :
      StronglyAdapted filtration (discreteExponentialFormula process bracketProxy))
    (hintegrable :
      ∀ n : ℕ, Integrable (discreteExponentialFormula process bracketProxy n) μ)
    (honeStep :
      ∀ n : ℕ,
        μ[discreteExponentialFormula process bracketProxy (n + 1) | filtration n]
          =ᵐ[μ] discreteExponentialFormula process bracketProxy n)
    {i j : ℕ} (hij : i ≤ j) :
    μ[discreteExponentialFormula process bracketProxy j | filtration i]
      =ᵐ[μ] discreteExponentialFormula process bracketProxy i :=
  (discreteExponential_martingale_of_oneStep_condExp μ filtration process bracketProxy
    hadapted hintegrable honeStep).condExp_ae_eq hij

/-- The discrete surrogate is a checked lemma, not a terminal Novikov proof. -/
def discreteExponentialSurrogateIsTerminalNovikovProof : Bool := false

/-- Sanity check for the non-terminal discrete-surrogate gate. -/
theorem discreteExponentialSurrogateIsTerminalNovikovProof_eq_false :
    discreteExponentialSurrogateIsTerminalNovikovProof = false :=
  rfl

/-- Metadata for the checked finite/discrete-time surrogate. -/
def discreteExponentialSurrogateNotes : List String := [
  "The repo-local lemma AwesomeTheorems.Stage1.S1_M_239.discreteExponential_martingale_of_oneStep_condExp is checked against mathlib's discrete-time martingale API.",
  "It states that exp(M_n - 1/2 A_n) is a martingale when adaptation, integrability, and the one-step conditional-expectation identity are supplied.",
  "It does not derive the one-step identity from independent increments, conditional Gaussianity, quadratic variation, stochastic integration, or Novikov's continuous-time condition."
]

/-! ## Expanded L025-L035 proof-leaf budget -/

/--
Machine-readable Stage1 proof-leaf budget record.

This is process metadata, not a theorem proof.  It keeps the broad L025-L035
frontier split into independent leaves whose intended local proof scripts are
small enough to stay below the M0387 `<= 100` step budget once the missing
stochastic-calculus APIs exist in the repo-local Lean closure.
-/
structure ProofLeafBudgetRecord where
  id : String
  parent : String
  status : String
  maxSteps : Nat
  anchor : String
  task : String

/--
Expansion of the previously broad `N239.L025` through `N239.L035` frontier into
independent proof leaves.

Leaves marked `checked-local` already correspond to declarations in this file.
Leaves marked `formalization-debt` need stochastic-calculus APIs or terminal
Novikov proof bodies that are not present in the current repo-local closure.
Leaves marked `integration-gate` or `serial-public-backfill` are process gates
and must not be counted as terminal theorem completion.
-/
def expandedLeaves_L025_L035 : List ProofLeafBudgetRecord := [
  { id := "N239.L025.PQV.predictable",
    parent := "N239.L025",
    status := "checked-local",
    maxSteps := 6,
    anchor := "quadraticVariation_isPredictable",
    task := "Project mathlib IsPredictable evidence for the quadratic-variation candidate." },
  { id := "N239.L025.PQV.adapted",
    parent := "N239.L025",
    status := "checked-local",
    maxSteps := 6,
    anchor := "quadraticVariation_stronglyAdapted",
    task := "Project strong adaptedness from the predictable quadratic-variation candidate." },
  { id := "N239.L025.PQV.regularity",
    parent := "N239.L025",
    status := "checked-local",
    maxSteps := 12,
    anchor := "quadraticVariation_pathContinuous/quadraticVariation_monotone/quadraticVariation_nonnegative/quadraticVariation_startsAtZero",
    task := "Project path continuity, monotonicity, nonnegativity, and zero-start evidence." },
  { id := "N239.L025.PQV.bracket-identity",
    parent := "N239.L025",
    status := "formalization-debt",
    maxSteps := 80,
    anchor := "missing canonical bracket/quadratic-variation API",
    task := "Replace the candidate boundary by a theorem identifying it with the bracket of the local martingale." },
  { id := "N239.L026.SI.domain-predictable",
    parent := "N239.L026",
    status := "checked-local",
    maxSteps := 6,
    anchor := "stochasticIntegralCompatibility_domain_predictable",
    task := "Project predictability for integrands in the local stochastic-integral compatibility domain." },
  { id := "N239.L026.SI.domain-memLp",
    parent := "N239.L026",
    status := "checked-local",
    maxSteps := 6,
    anchor := "stochasticIntegralCompatibility_domain_memLp",
    task := "Project time-slice L2 integrability for compatibility-domain integrands." },
  { id := "N239.L026.SI.zero-start",
    parent := "N239.L026",
    status := "checked-local",
    maxSteps := 6,
    anchor := "stochasticIntegralCompatibility_integral_startsAtZero",
    task := "Project the zero initial value of the supplied stochastic-integral operation." },
  { id := "N239.L026.SI.stopped-martingale",
    parent := "N239.L026",
    status := "checked-local",
    maxSteps := 8,
    anchor := "stochasticIntegralCompatibility_stopped_integral_martingale",
    task := "Project stopped martingality of stochastic integrals along the localizing sequence." },
  { id := "N239.L026.SI.canonical-integral",
    parent := "N239.L026",
    status := "formalization-debt",
    maxSteps := 90,
    anchor := "missing canonical continuous-time stochastic-integral API",
    task := "Replace the abstract compatibility operation by a repo-local canonical stochastic integral." },
  { id := "N239.L027.DE.formula",
    parent := "N239.L027",
    status := "checked-local",
    maxSteps := 6,
    anchor := "stochasticExponential_eq_formula",
    task := "Identify the packaged exponential process with exp(M_t - 1/2 <M>_t)." },
  { id := "N239.L027.DE.starts-at-one",
    parent := "N239.L027",
    status := "checked-local",
    maxSteps := 6,
    anchor := "stochasticExponential_startsAtOne",
    task := "Project that the packaged stochastic exponential starts at one." },
  { id := "N239.L027.DE.stopping-times",
    parent := "N239.L027",
    status := "checked-local",
    maxSteps := 6,
    anchor := "stochasticExponential_localizingSeq_isStoppingTime",
    task := "Project stopping-time evidence for the exponential localizing sequence." },
  { id := "N239.L027.DE.stopped-martingale",
    parent := "N239.L027",
    status := "checked-local",
    maxSteps := 8,
    anchor := "stochasticExponential_stopped_martingale",
    task := "Project stopped martingality of the packaged stochastic exponential." },
  { id := "N239.L027.DE.canonical-construction",
    parent := "N239.L027",
    status := "formalization-debt",
    maxSteps := 95,
    anchor := "missing Doleans-Dade stochastic-exponential API",
    task := "Construct the exponential as a Doleans-Dade object rather than supplying it as boundary data." },
  { id := "N239.L028.LOC.stopping-times",
    parent := "N239.L028",
    status := "checked-local",
    maxSteps := 8,
    anchor := "localizingSeq_isStoppingTime/stochasticExponential_localizingSeq_isStoppingTime",
    task := "Expose stopping-time evidence for both the original process and its exponential." },
  { id := "N239.L028.LOC.stopped-integrability",
    parent := "N239.L028",
    status := "checked-local",
    maxSteps := 8,
    anchor := "stopped_process_integrable/stochasticExponential_stopped_integrable",
    task := "Expose integrability of stopped process and stopped exponential slices." },
  { id := "N239.L028.LOC.horizon-boundedness",
    parent := "N239.L028",
    status := "formalization-debt",
    maxSteps := 70,
    anchor := "missing finite-horizon stopping-time comparison lemmas",
    task := "Prove the horizon and localization comparison assumptions needed by a true-martingale upgrade." },
  { id := "N239.L029.UI.novikov-integrability",
    parent := "N239.L029",
    status := "checked-local",
    maxSteps := 6,
    anchor := "integrable_terminalNovikovWeight_of_hypotheses",
    task := "Expose the Novikov exponential-integrability hypothesis." },
  { id := "N239.L029.UI.tilted-probability",
    parent := "N239.L029",
    status := "checked-local",
    maxSteps := 20,
    anchor := "tilted_terminalNovikovWeight_isProbability",
    task := "Build the exponential tilted probability measure from the terminal Novikov weight." },
  { id := "N239.L029.UI.expectation-one",
    parent := "N239.L029",
    status := "formalization-debt",
    maxSteps := 95,
    anchor := "missing Novikov expectation-one/uniform-integrability theorem",
    task := "Derive expectation one or uniform integrability of the stochastic exponential from Novikov integrability." },
  { id := "N239.L030.TRUE.statement",
    parent := "N239.L030",
    status := "checked-local",
    maxSteps := 4,
    anchor := "NovikovConclusion",
    task := "Keep the true-martingale target as the explicit formal conclusion." },
  { id := "N239.L030.TRUE.local-to-true",
    parent := "N239.L030",
    status := "formalization-debt",
    maxSteps := 95,
    anchor := "missing local-to-true martingale upgrade under Novikov condition",
    task := "Prove Martingale (stochasticExponential D) from the local boundary and Novikov integrability." },
  { id := "N239.L031.CAN.expression",
    parent := "N239.L031",
    status := "checked-local",
    maxSteps := 4,
    anchor := "stochasticExponentialFormula",
    task := "Define the expression-level exponential exp(M_t - 1/2 <M>_t)." },
  { id := "N239.L031.CAN.boundary-equality",
    parent := "N239.L031",
    status := "checked-local",
    maxSteps := 6,
    anchor := "stochasticExponential_eq_formula",
    task := "Connect the packaged process to the expression-level formula." },
  { id := "N239.L031.CAN.canonical-object",
    parent := "N239.L031",
    status := "formalization-debt",
    maxSteps := 80,
    anchor := "missing canonical stochastic-exponential object",
    task := "Connect the expression-level exponential to a canonical Doleans-Dade object once one exists locally." },
  { id := "N239.L032.DISC.one-step",
    parent := "N239.L032",
    status := "checked-local",
    maxSteps := 20,
    anchor := "discreteExponential_martingale_of_oneStep_condExp",
    task := "Use mathlib martingale_nat to turn the one-step conditional-expectation identity into a discrete martingale." },
  { id := "N239.L032.DISC.all-times",
    parent := "N239.L032",
    status := "checked-local",
    maxSteps := 20,
    anchor := "discreteExponential_condExp_ae_eq_of_oneStep",
    task := "Project the all-times conditional-expectation identity from the discrete martingale." },
  { id := "N239.L032.DISC.non-terminal-gate",
    parent := "N239.L032",
    status := "checked-local",
    maxSteps := 2,
    anchor := "discreteExponentialSurrogateIsTerminalNovikovProof_eq_false",
    task := "Record that the discrete surrogate is not a terminal continuous-time Novikov proof." },
  { id := "N239.L033.EXT.local-mathlib-negative",
    parent := "N239.L033",
    status := "checked-local",
    maxSteps := 4,
    anchor := "requestedMathlibStochasticApiSearchResults",
    task := "Record the negative terminal Novikov/stochastic-calculus search in pinned local mathlib." },
  { id := "N239.L033.EXT.brownian-negative",
    parent := "N239.L033",
    status := "checked-local",
    maxSteps := 4,
    anchor := "brownianMotionTerminalNovikovSearchResults",
    task := "Record the negative terminal Novikov/stochastic-exponential search in the audited external project." },
  { id := "N239.L033.EXT.future-primary-source-refresh",
    parent := "N239.L033",
    status := "formalization-debt",
    maxSteps := 50,
    anchor := "future primary-source audit",
    task := "Refresh the primary-source audit if mathlib or external stochastic-calculus projects add terminal Novikov anchors." },
  { id := "N239.L034.GATE.no-anchor",
    parent := "N239.L034",
    status := "checked-local",
    maxSteps := 8,
    anchor := "brownianMotion_repoLocalIntegrationDebtGate",
    task := "Discharge the integration-debt gate for the audited external project by negative terminal-proof evidence." },
  { id := "N239.L034.GATE.pin-if-found",
    parent := "N239.L034",
    status := "integration-gate",
    maxSteps := 80,
    anchor := "RepoLocalIntegrationDebtGate",
    task := "If an exact external terminal proof is found, pin/import/check it or record a concrete integration blocker before completion." },
  { id := "N239.L035.PUB.private-ledger",
    parent := "N239.L035",
    status := "checked-local",
    maxSteps := 4,
    anchor := "expandedLeaves_L025_L035",
    task := "Keep the L025-L035 expansion in the private checked artifact and child ledger." },
  { id := "N239.L035.PUB.serial-merge",
    parent := "N239.L035",
    status := "serial-public-backfill",
    maxSteps := 30,
    anchor := "Docs/Stage1_Blueprint.md:3163",
    task := "Serially merge the theorem-tree expansion into the public Stage1 surface after validation and debt gates are checked." }
]

/-- Step-budget numbers extracted from `expandedLeaves_L025_L035`. -/
def expandedLeaves_L025_L035_stepBounds : List Nat :=
  expandedLeaves_L025_L035.map (fun leaf => leaf.maxSteps)

/-- Computed M0387 step-budget check for the expanded L025-L035 leaves. -/
def expandedLeaves_L025_L035_allStepBounded : Bool :=
  expandedLeaves_L025_L035_stepBounds.all (fun n => decide (n ≤ 100))

/-- Every expanded L025-L035 leaf is budgeted at `<= 100` proof steps. -/
theorem expandedLeaves_L025_L035_allStepBounded_eq_true :
    expandedLeaves_L025_L035_allStepBounded = true :=
  rfl

/-- The L025-L035 expansion is a proof-tree split, not a terminal Novikov proof. -/
def expandedLeaves_L025_L035_closeTerminalNovikov : Bool := false

/-- Sanity check that the expanded L025-L035 frontier does not claim completion. -/
theorem expandedLeaves_L025_L035_closeTerminalNovikov_eq_false :
    expandedLeaves_L025_L035_closeTerminalNovikov = false :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check MeasureTheory.Filtration
#check MeasureTheory.SigmaFiniteFiltration
#check MeasureTheory.StronglyAdapted
#check MeasureTheory.IsPredictable
#check MeasureTheory.IsStoppingTime
#check MeasureTheory.stoppedProcess
#check MeasureTheory.Martingale
#check MeasureTheory.Martingale.integrable
#check MeasureTheory.IsPredictable.adapted
#check MeasureTheory.condExp
#check MeasureTheory.condExpL1
#check MeasureTheory.MemLp
#check ProbabilityTheory.mgf
#check ProbabilityTheory.integrable_exp_mul_of_nonneg_of_le
#check MeasureTheory.Measure.tilted
#check MeasureTheory.isProbabilityMeasure_tilted
#check terminalNovikovWeight
#check stochasticExponentialFormula
#check stochasticExponential
#check stochasticExponential_eq_formula
#check StatementShape
#check PredictableQuadraticVariationCandidate
#check DoleansDadeExponentialLocalMartingaleCandidate
#check StochasticIntegralCompatibilityCandidate
#check stochasticIntegralCompatibility_domain_predictable
#check stochasticIntegralCompatibility_domain_memLp
#check stochasticIntegralCompatibility_integral_startsAtZero
#check stochasticIntegralCompatibility_stopped_integral_martingale
#check stochasticExponential_integrablePredictable
#check stochasticExponential_isPredictable
#check stochasticExponential_memLp_two
#check stochasticIntegral_stochasticExponential_startsAtZero
#check stochasticIntegral_stochasticExponential_stopped_martingale
#check stochasticExponential_startsAtOne
#check stochasticExponential_localizingSeq_isStoppingTime
#check stochasticExponential_stopped_martingale
#check stochasticExponential_stopped_integrable
#check stochasticExponential_localMartingale_boundary
#check discreteExponentialFormula
#check discreteExponential_martingale_of_oneStep_condExp
#check discreteExponential_condExp_ae_eq_of_oneStep
#check ProofLeafBudgetRecord
#check expandedLeaves_L025_L035
#check expandedLeaves_L025_L035_allStepBounded_eq_true
#check expandedLeaves_L025_L035_closeTerminalNovikov_eq_false

/-- mathlib commit used for the Stage1 stochastic-calculus API audit. -/
def mathlibAuditCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Commit timestamp for `mathlibAuditCommit`. -/
def mathlibAuditCommitDate : String :=
  "2026-03-30T18:47:58Z"

/-- Commit subject for `mathlibAuditCommit`. -/
def mathlibAuditCommitSubject : String :=
  "chore: bump toolchain to v4.29.0 (#37377)"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Predictable",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Moments.Basic",
  "Mathlib.Probability.Moments.IntegrableExpMul",
  "Mathlib.MeasureTheory.Measure.Tilted",
  "Mathlib.MeasureTheory.Function.ConditionalExpectation.Real",
  "Mathlib.MeasureTheory.Function.ConditionalExpectation.CondexpL1",
  "Mathlib.Probability.Martingale.Basic:martingale_nat"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.SigmaFiniteFiltration",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.IsPredictable",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.stoppedProcess",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.IsPredictable.adapted",
  "MeasureTheory.condExp",
  "MeasureTheory.condExpL1",
  "MeasureTheory.MemLp",
  "ProbabilityTheory.mgf",
  "ProbabilityTheory.integrable_exp_mul_of_nonneg_of_le",
  "MeasureTheory.Measure.tilted",
  "MeasureTheory.isProbabilityMeasure_tilted",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_eq_formula",
  "AwesomeTheorems.Stage1.S1_M_239.DoleansDadeExponentialLocalMartingaleCandidate",
  "AwesomeTheorems.Stage1.S1_M_239.StochasticIntegralCompatibilityCandidate",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticIntegralCompatibility_domain_predictable",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticIntegralCompatibility_domain_memLp",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticIntegralCompatibility_integral_startsAtZero",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticIntegralCompatibility_stopped_integral_martingale",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_integrablePredictable",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_isPredictable",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_memLp_two",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticIntegral_stochasticExponential_startsAtZero",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticIntegral_stochasticExponential_stopped_martingale",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_startsAtOne",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_localizingSeq_isStoppingTime",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_stopped_martingale",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_stopped_integrable",
  "AwesomeTheorems.Stage1.S1_M_239.stochasticExponential_localMartingale_boundary",
  "MeasureTheory.martingale_nat",
  "AwesomeTheorems.Stage1.S1_M_239.discreteExponentialFormula",
  "AwesomeTheorems.Stage1.S1_M_239.discreteExponential_martingale_of_oneStep_condExp",
  "AwesomeTheorems.Stage1.S1_M_239.discreteExponential_condExp_ae_eq_of_oneStep",
  "AwesomeTheorems.Stage1.S1_M_239.expandedLeaves_L025_L035",
  "AwesomeTheorems.Stage1.S1_M_239.expandedLeaves_L025_L035_allStepBounded_eq_true",
  "AwesomeTheorems.Stage1.S1_M_239.expandedLeaves_L025_L035_closeTerminalNovikov_eq_false"
]

/-- Source locations for adjacent mathlib anchors available at `mathlibAuditCommit`. -/
def mathlibAdjacentAnchorSourceLocations : List String := [
  "Mathlib/Probability/Process/Filtration.lean:50 structure Filtration",
  "Mathlib/Probability/Process/Filtration.lean:200 class SigmaFiniteFiltration",
  "Mathlib/Probability/Process/Adapted.lean:103 def StronglyAdapted",
  "Mathlib/Probability/Process/Predictable.lean:63 def IsPredictable",
  "Mathlib/Probability/Process/Stopping.lean:75 def IsStoppingTime",
  "Mathlib/Probability/Process/Stopping.lean:801 def stoppedProcess",
  "Mathlib/Probability/Martingale/Basic.lean:53 def Martingale",
  "Mathlib/Probability/Martingale/Basic.lean:95 theorem Martingale.integrable",
  "Mathlib/Probability/Process/Predictable.lean:130 lemma IsPredictable.adapted",
  "Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean:98 def condExp",
  "Mathlib/MeasureTheory/Function/ConditionalExpectation/CondexpL1.lean:442 def condExpL1",
  "Mathlib/MeasureTheory/Function/LpSeminorm/Defs.lean:119 def MemLp",
  "Mathlib/Probability/Moments/Basic.lean:121 def mgf",
  "Mathlib/Probability/Moments/IntegrableExpMul.lean:97 lemma integrable_exp_mul_of_nonneg_of_le",
  "Mathlib/MeasureTheory/Measure/Tilted.lean:42 def Measure.tilted",
  "Mathlib/MeasureTheory/Measure/Tilted.lean:126 lemma isProbabilityMeasure_tilted",
  "Mathlib/Probability/Martingale/Basic.lean:421 theorem martingale_nat"
]

/--
Search terms that did not locate a terminal Novikov theorem in the pinned local
mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Novikov",
  "Doleans",
  "Doléans",
  "Dade",
  "stochastic exponential",
  "StochasticExponential",
  "stochastic integral",
  "StochasticIntegral",
  "quadratic variation",
  "QuadraticVariation",
  "local martingale",
  "LocalMartingale",
  "semimartingale",
  "Semimartingale"
]

/--
Requested stochastic-calculus API audit results against `mathlibAuditCommit`.

Each requested exact name returned no source match in the local
`Mathlib/` tree, so this Stage1 artifact remains a statement-boundary and
formalization-debt record rather than a wrapper around a terminal mathlib proof.
-/
def requestedMathlibStochasticApiSearchResults : List String := [
  "Novikov: no `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "StochasticExponential: no `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "QuadraticVariation: no `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "LocalMartingale: no `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "Semimartingale: no `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "stochasticIntegral/StochasticIntegral: no `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "stochastic integral/stochastic exponential/quadratic variation/local martingale/semimartingale phrase search: no `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95"
]

/-! ## External Brownian-motion audit metadata -/

/-- External Lean repository audited for the Stage1 Novikov stochastic-calculus anchor search. -/
def brownianMotionAuditRepository : String :=
  "https://github.com/RemyDegenne/brownian-motion"

/-- Concrete external commit audited for `brownian-motion`. -/
def brownianMotionAuditCommit : String :=
  "91885e6172648ea7f9c6a16b3a7069f92c88e023"

/-- Commit timestamp for `brownianMotionAuditCommit`. -/
def brownianMotionAuditCommitDate : String :=
  "2026-05-01T08:05:08+02:00"

/-- Commit subject for `brownianMotionAuditCommit`. -/
def brownianMotionAuditCommitSubject : String :=
  "Bump leanprover/lean-action from 65f454bc22ec83143241456eee965c2ab702ba6e to 6fe4ae6a449c9758f51250ee249ebbc7ec37ee48 (#429)"

/-- Toolchain advertised by the audited external repository. -/
def brownianMotionAuditLeanToolchain : String :=
  "leanprover/lean4:v4.30.0-rc1"

/-- mathlib revision pinned by the audited external repository. -/
def brownianMotionAuditMathlibCommit : String :=
  "f23306121184717ace04f3ac514be974e3224c8b"

/-- Primary Lean source files searched in the audited external repository. -/
def brownianMotionPrimaryLeanSourcesSearched : List String := [
  "BrownianMotion.lean",
  "BrownianMotion/StochasticIntegral/DoobMeyer.lean",
  "BrownianMotion/StochasticIntegral/L2M.lean",
  "BrownianMotion/StochasticIntegral/LocalMartingale.lean",
  "BrownianMotion/StochasticIntegral/QuadraticVariation.lean",
  "BrownianMotion/StochasticIntegral/SimpleProcess.lean"
]

/-- Adjacent external stochastic-calculus anchors found in `brownian-motion`. -/
def brownianMotionAdjacentAnchorSourceLocations : List String := [
  "BrownianMotion.lean:54 imports BrownianMotion.StochasticIntegral.LocalMartingale",
  "BrownianMotion.lean:62 imports BrownianMotion.StochasticIntegral.QuadraticVariation",
  "BrownianMotion/StochasticIntegral/LocalMartingale.lean:29 def ProbabilityTheory.IsLocalMartingale",
  "BrownianMotion/StochasticIntegral/LocalMartingale.lean:35 def ProbabilityTheory.IsLocalSubmartingale",
  "BrownianMotion/StochasticIntegral/LocalMartingale.lean:39 lemma ProbabilityTheory.Martingale.IsLocalMartingale",
  "BrownianMotion/StochasticIntegral/DoobMeyer.lean:26 theorem ProbabilityTheory.IsLocalSubmartingale.doob_meyer",
  "BrownianMotion/StochasticIntegral/DoobMeyer.lean:41 def ProbabilityTheory.IsLocalSubmartingale.predictablePart",
  "BrownianMotion/StochasticIntegral/QuadraticVariation.lean:25 lemma ProbabilityTheory.IsLocalMartingale.isLocalSubmartingale_sq_norm",
  "BrownianMotion/StochasticIntegral/QuadraticVariation.lean:33 def ProbabilityTheory.quadraticVariation",
  "BrownianMotion/StochasticIntegral/SimpleProcess.lean:351 def ProbabilityTheory.SimpleProcess.integral",
  "BrownianMotion/StochasticIntegral/SimpleProcess.lean:358 abbrev ProbabilityTheory.SimpleProcess.integralEval",
  "BrownianMotion/StochasticIntegral/L2M.lean:39 def ProbabilityTheory.L2Predictable"
]

/--
Negative terminal Novikov search results in the audited external repository.

The repository contains adjacent stochastic-integral, local-martingale, and
quadratic-variation scaffolding, but no source match for a Novikov theorem or a
stochastic-exponential/Doleans-Dade terminal proof.
-/
def brownianMotionTerminalNovikovSearchResults : List String := [
  "Novikov: no primary Lean source match at brownian-motion commit 91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "StochasticExponential: no primary Lean source match at brownian-motion commit 91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "stochastic exponential: no primary Lean source match at brownian-motion commit 91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "Doleans/Dade: no primary Lean source match at brownian-motion commit 91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "Semimartingale: no primary Lean source match at brownian-motion commit 91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "exponential martingale: no primary Lean source match at brownian-motion commit 91885e6172648ea7f9c6a16b3a7069f92c88e023"
]

/--
Concrete reasons the audited `brownian-motion` anchors are not a repo-local
terminal proof dependency for Novikov's condition.
-/
def brownianMotionIntegrationBlockers : List String := [
  "No exact Lean theorem for Novikov's condition was found in primary Lean sources.",
  "No stochastic-exponential or Doleans-Dade exponential construction was found in primary Lean sources.",
  "The adjacent quadratic-variation definition depends on unfinished proof placeholders at BrownianMotion/StochasticIntegral/QuadraticVariation.lean:28 and :35.",
  "The adjacent Doob-Meyer theorem contains an unfinished proof placeholder at BrownianMotion/StochasticIntegral/DoobMeyer.lean:30.",
  "The adjacent local-martingale development contains an unfinished proof placeholder at BrownianMotion/StochasticIntegral/LocalMartingale.lean:95.",
  "The external project advertises Lean v4.30.0-rc1 and mathlib f23306121184717ace04f3ac514be974e3224c8b, while this repo-local Stage1 closure currently validates against Lean v4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "The external project is not pinned/imported into this Lake closure."
]

/-- The audited external project does not currently provide an exact terminal Novikov proof. -/
def brownianMotionExactTerminalNovikovProofFound : Prop :=
  False

/--
Checked repo-local integration audit for the external `brownian-motion` search.

This records a negative terminal-proof result, not a completed theorem state.
-/
def brownianMotionExternalLeanAnchorAudit : ExternalLeanAnchorAudit where
  exactTerminalProofFound := brownianMotionExactTerminalNovikovProofFound
  importedIntoLakeClosure := False
  concreteIntegrationBlockerRecorded := True

/--
The `brownian-motion` audit leaves no completed-state repo-local integration
debt: no exact terminal external Novikov proof was found.
-/
theorem brownianMotion_repoLocalIntegrationDebtGate :
    RepoLocalIntegrationDebtGate brownianMotionExternalLeanAnchorAudit :=
  repoLocalIntegrationDebtGate_of_no_external_anchor
    brownianMotionExternalLeanAnchorAudit
    (by
      intro h
      exact h)

/-! ## Serial public backfill gate -/

/--
Machine-readable payload for the serial public Stage1 backfill.

This is intentionally kept in the owned Lean artifact rather than editing the
shared public planning document from a parallel child worker.  An integrator can
copy the corresponding text from the child ledger after the local validation
command and integration-debt gate have been checked.
-/
def publicStage1SerialBackfillPayload : List String := [
  "Public target: Docs/Stage1_Blueprint.md:3164.",
  "Merge AwesomeTheorems.Stage1.S1_M_239.StatementShape as the canonical non-terminal Stage1 statement boundary for THM-M-1046.",
  "Merge expandedLeaves_L025_L035 as the current theorem-tree and <=100-step leaf-budget table.",
  "Merge mathlibAnchorNames, mathlibAdjacentAnchorSourceLocations, requestedMathlibStochasticApiSearchResults, brownianMotionAdjacentAnchorSourceLocations, and brownianMotionTerminalNovikovSearchResults as the machine-anchor audit table.",
  "Keep status not_repo_local_closed/formalization_debt; do not mark THM-M-1046 completed.",
  "The repo-local integration-debt gate is satisfied only as a non-completion gate: no exact external terminal Novikov Lean proof was found in the audited sources."
]

/--
The serial public backfill payload is integration-ready, but it is not a
completion certificate for Novikov's theorem.
-/
def publicStage1SerialBackfillMayMarkCompleted : Bool := false

/-- Sanity check that the serial public backfill payload cannot mark completion. -/
theorem publicStage1SerialBackfillMayMarkCompleted_eq_false :
    publicStage1SerialBackfillMayMarkCompleted = false :=
  rfl

end S1_M_239
end Stage1
end AwesomeTheorems
