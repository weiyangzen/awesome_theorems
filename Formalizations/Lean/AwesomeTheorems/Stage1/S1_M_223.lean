import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Martingale.OptionalSampling
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# S1-M-223 / THM-M-1030: Dubins-Schwarz theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Dubins-Schwarz theorem, also commonly called the Dambis-Dubins-Schwarz theorem:
a continuous local martingale, after the inverse quadratic-variation time
change, is a Brownian motion.

The pinned mathlib snapshot has substantial adjacent probability infrastructure:
filtrations, stopping times, stopped processes, martingales, Gaussian laws,
Gaussian processes, and independent increments.  It does not expose a terminal
API for continuous local martingales, predictable quadratic variation,
stochastic integration, Brownian motion, or the Dubins-Schwarz theorem itself.

Accordingly, this file gives a typed statement shape and low-risk wrappers
around existing mathlib predicates.  It does not prove the Dubins-Schwarz
theorem.
-/

noncomputable section

open MeasureTheory
open ProbabilityTheory

open scoped NNReal

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_223

/-- Continuous-time real-valued stochastic process indexed by nonnegative time. -/
abbrev ContinuousTimeProcess (Ω : Type u) :=
  ℝ≥0 → Ω → ℝ

/-- Family of candidate stopping times used to localize a continuous-time process. -/
abbrev LocalizingSequence (Ω : Type u) :=
  ℕ → Ω → WithTop ℝ≥0

/-- Family of inverse time changes, one stopping time for each nonnegative target time. -/
abbrev InverseTimeChange (Ω : Type u) :=
  ℝ≥0 → Ω → WithTop ℝ≥0

/--
Stage1 candidate API for continuous predictable quadratic variation and inverse
quadratic-variation stopping times.

The pinned mathlib snapshot exposes a generic `IsPredictable` process
predicate, but it does not expose a canonical predictable quadratic-variation
predicate.  This structure therefore uses the generic predictability API while
keeping the genuinely missing stochastic-analysis obligations as proposition
fields.
-/
structure ContinuousPredictableQuadraticVariationData (Ω : Type u)
    [MeasurableSpace Ω]
    (filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›) : Type (u + 1) where
  quadraticVariation : ℝ≥0 → Ω → ℝ≥0
  predictableQuadraticVariation : IsPredictable filtration quadraticVariation
  quadraticVariationContinuous :
    ∀ ω : Ω, Continuous fun t : ℝ≥0 => quadraticVariation t ω
  quadraticVariationMonotone :
    ∀ ω : Ω, Monotone fun t : ℝ≥0 => quadraticVariation t ω
  inverseTimeChange : InverseTimeChange Ω
  inverseTimeChangeStopping :
    ∀ t : ℝ≥0, IsStoppingTime filtration (inverseTimeChange t)
  inverseQuadraticVariation : Prop
  quadraticVariationUnbounded : Prop
  terminalValueConvention : Prop

/--
Canonical Stage1 candidate API for continuous local martingales over `ℝ≥0`.

Since the pinned mathlib snapshot does not expose a named continuous local
martingale predicate, this structure records the first repo-local bridge:
localization by stopping times whose stopped processes are mathlib
`Martingale`s.  It intentionally does not include quadratic variation or
Dubins-Schwarz time-change data.
-/
structure ContinuousLocalMartingaleOverNNReal (Ω : Type u) [MeasurableSpace Ω]
    (P : Measure Ω) : Type (u + 1) where
  process : ContinuousTimeProcess Ω
  filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›
  localizingSeq : LocalizingSequence Ω
  adapted : StronglyAdapted filtration process
  stoppedMartingale :
    ∀ n : ℕ,
      IsStoppingTime filtration (localizingSeq n) ∧
        Martingale (stoppedProcess process (localizingSeq n)) filtration P
  pathContinuous : ∀ ω : Ω, Continuous fun t : ℝ≥0 => process t ω

/-- The localized stopped process attached to a Stage1 continuous local martingale. -/
def ContinuousLocalMartingaleOverNNReal.localizedProcess {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω}
    (M : ContinuousLocalMartingaleOverNNReal Ω P) (n : ℕ) :
    ContinuousTimeProcess Ω :=
  MeasureTheory.stoppedProcess M.process (M.localizingSeq n)

/-- A Stage1 continuous local martingale exposes the adaptedness hypothesis. -/
theorem ContinuousLocalMartingaleOverNNReal.stronglyAdapted {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω}
    (M : ContinuousLocalMartingaleOverNNReal Ω P) :
    StronglyAdapted M.filtration M.process :=
  M.adapted

/-- A Stage1 continuous local martingale exposes each localizing stopping time. -/
theorem ContinuousLocalMartingaleOverNNReal.localizingSeq_isStoppingTime {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω}
    (M : ContinuousLocalMartingaleOverNNReal Ω P) (n : ℕ) :
    IsStoppingTime M.filtration (M.localizingSeq n) :=
  (M.stoppedMartingale n).1

/-- A Stage1 continuous local martingale exposes each stopped-process martingale. -/
theorem ContinuousLocalMartingaleOverNNReal.stoppedProcess_martingale {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω}
    (M : ContinuousLocalMartingaleOverNNReal Ω P) (n : ℕ) :
    Martingale (MeasureTheory.stoppedProcess M.process (M.localizingSeq n)) M.filtration P :=
  (M.stoppedMartingale n).2

/-- A Stage1 continuous local martingale exposes sample-path continuity. -/
theorem ContinuousLocalMartingaleOverNNReal.pathContinuous_of {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω}
    (M : ContinuousLocalMartingaleOverNNReal Ω P) :
    ∀ ω : Ω, Continuous fun t : ℝ≥0 => M.process t ω :=
  M.pathContinuous

/--
Brownian-motion statement boundary over `ℝ≥0`.

The predicate combines the mathlib Gaussian-process and independent-increments
interfaces with one-dimensional Gaussian marginals, almost-sure origin, and
continuous sample paths.  This is a Stage1 normalized target, not a claim that
mathlib already has a canonical `BrownianMotion` definition.
-/
def StandardBrownianMotion {Ω : Type u} [MeasurableSpace Ω]
    (B : ContinuousTimeProcess Ω) (P : Measure Ω) : Prop :=
  IsGaussianProcess B P ∧
    HasIndepIncrements B P ∧
      (∀ t : ℝ≥0, HasLaw (B t) (gaussianReal 0 t) P) ∧
        (∀ᵐ ω ∂P, B 0 ω = 0) ∧
          (∀ ω : Ω, Continuous fun t : ℝ≥0 => B t ω)

/--
Dedicated Brownian-motion package for the Dubins-Schwarz conclusion.

This child-task API keeps the process carrier explicit and names each current
mathlib component separately: Gaussian process, independent increments,
one-dimensional Gaussian laws, zero start, and continuous paths.  It is
equivalent to the local `StandardBrownianMotion` predicate below, but easier for
later theorem-tree leaves to target one obligation at a time.
-/
structure BrownianMotionPackage (Ω : Type u) [MeasurableSpace Ω]
    (P : Measure Ω) : Type (u + 1) where
  process : ContinuousTimeProcess Ω
  gaussianProcess : IsGaussianProcess process P
  independentIncrements : HasIndepIncrements process P
  gaussianMarginals : ∀ t : ℝ≥0, HasLaw (process t) (gaussianReal 0 t) P
  originAE : ∀ᵐ ω ∂P, process 0 ω = 0
  pathContinuous : ∀ ω : Ω, Continuous fun t : ℝ≥0 => process t ω

/-- A packaged Brownian motion exposes the local predicate used by the statement. -/
def BrownianMotionPackage.standardBrownianMotion {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω} (B : BrownianMotionPackage Ω P) :
    StandardBrownianMotion B.process P :=
  ⟨B.gaussianProcess, B.independentIncrements, B.gaussianMarginals,
    B.originAE, B.pathContinuous⟩

/-- A local Brownian predicate can be repackaged with named child-task fields. -/
def BrownianMotionPackage.ofStandardBrownianMotion {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : StandardBrownianMotion B P) : BrownianMotionPackage Ω P where
  process := B
  gaussianProcess := hB.1
  independentIncrements := hB.2.1
  gaussianMarginals := hB.2.2.1
  originAE := hB.2.2.2.1
  pathContinuous := hB.2.2.2.2

/-- The named package is exactly the local Brownian-motion statement boundary. -/
theorem standardBrownianMotion_iff_exists_package {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω} {B : ContinuousTimeProcess Ω} :
    StandardBrownianMotion B P ↔
      ∃ Bpkg : BrownianMotionPackage Ω P, Bpkg.process = B := by
  constructor
  · intro hB
    exact ⟨BrownianMotionPackage.ofStandardBrownianMotion hB, rfl⟩
  · rintro ⟨Bpkg, hproc⟩
    simpa [hproc] using Bpkg.standardBrownianMotion

/--
Candidate data for the continuous local-martingale side of Dubins-Schwarz.

The local martingale condition is represented using mathlib's stopped-process
and martingale predicates.  The quadratic-variation and inverse-time-change
requirements remain proposition fields because the pinned dependency closure
does not yet provide a canonical continuous quadratic-variation API.
-/
structure ContinuousLocalMartingaleData (Ω : Type u) [MeasurableSpace Ω]
    (P : Measure Ω) : Type (u + 1) where
  process : ContinuousTimeProcess Ω
  filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›
  localizingSeq : LocalizingSequence Ω
  adapted : StronglyAdapted filtration process
  stoppedMartingale :
    ∀ n : ℕ,
      IsStoppingTime filtration (localizingSeq n) ∧
        Martingale (stoppedProcess process (localizingSeq n)) filtration P
  pathContinuous : ∀ ω : Ω, Continuous fun t : ℝ≥0 => process t ω
  quadraticVariation : ℝ≥0 → Ω → ℝ≥0
  predictableQuadraticVariation : IsPredictable filtration quadraticVariation
  quadraticVariationContinuous :
    ∀ ω : Ω, Continuous fun t : ℝ≥0 => quadraticVariation t ω
  quadraticVariationMonotone :
    ∀ ω : Ω, Monotone fun t : ℝ≥0 => quadraticVariation t ω
  inverseTimeChange : InverseTimeChange Ω
  inverseTimeChangeStopping :
    ∀ t : ℝ≥0, IsStoppingTime filtration (inverseTimeChange t)
  inverseQuadraticVariation : Prop
  quadraticVariationUnbounded : Prop
  terminalValueConvention : Prop

/--
The local-martingale part of the full Dubins-Schwarz data, factored through the
dedicated child-task API.
-/
def ContinuousLocalMartingaleData.toLocalMartingale {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω}
    (D : ContinuousLocalMartingaleData Ω P) :
    ContinuousLocalMartingaleOverNNReal Ω P where
  process := D.process
  filtration := D.filtration
  localizingSeq := D.localizingSeq
  adapted := D.adapted
  stoppedMartingale := D.stoppedMartingale
  pathContinuous := D.pathContinuous

/--
The quadratic-variation side of the full Dubins-Schwarz data, factored through
the dedicated child-task API.
-/
def ContinuousLocalMartingaleData.toQuadraticVariationData {Ω : Type u}
    [MeasurableSpace Ω] {P : Measure Ω}
    (D : ContinuousLocalMartingaleData Ω P) :
    ContinuousPredictableQuadraticVariationData Ω D.filtration where
  quadraticVariation := D.quadraticVariation
  predictableQuadraticVariation := D.predictableQuadraticVariation
  quadraticVariationContinuous := D.quadraticVariationContinuous
  quadraticVariationMonotone := D.quadraticVariationMonotone
  inverseTimeChange := D.inverseTimeChange
  inverseTimeChangeStopping := D.inverseTimeChangeStopping
  inverseQuadraticVariation := D.inverseQuadraticVariation
  quadraticVariationUnbounded := D.quadraticVariationUnbounded
  terminalValueConvention := D.terminalValueConvention

/--
The process obtained by applying the inverse quadratic-variation time change.

When the inverse time change takes value `⊤`, `WithTop.untopA` chooses an
arbitrary index.  The mathematical theorem therefore needs the accompanying
terminal-value convention and unboundedness hypotheses recorded in
`ContinuousLocalMartingaleData`.
-/
def timeChangedProcess {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ContinuousLocalMartingaleData Ω P) : ContinuousTimeProcess Ω :=
  fun t ω => D.process (D.inverseTimeChange t ω).untopA ω

/-- Normalized hypotheses for the Dubins-Schwarz statement boundary. -/
def DubinsSchwarzHypotheses {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ContinuousLocalMartingaleData Ω P) : Prop :=
  D.inverseQuadraticVariation ∧
    D.quadraticVariationUnbounded ∧
      D.terminalValueConvention

/-- Normalized conclusion for the Dubins-Schwarz statement boundary. -/
def DubinsSchwarzConclusion {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ContinuousLocalMartingaleData Ω P) : Prop :=
  StandardBrownianMotion (timeChangedProcess D) P

/--
Stage1 normalized statement shape for the Dubins-Schwarz theorem.

For every probability space and every continuous real-valued local martingale
equipped with continuous increasing quadratic variation and inverse
quadratic-variation stopping times, the time-changed process should be a
standard Brownian motion.

This declaration is a precise formalization boundary only.  The repo-local Lean
closure does not contain the proof body or all required stochastic-analysis APIs.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω),
    IsProbabilityMeasure P →
      ∀ D : ContinuousLocalMartingaleData Ω P,
        DubinsSchwarzHypotheses D → DubinsSchwarzConclusion D

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω),
      IsProbabilityMeasure P →
        ∀ D : ContinuousLocalMartingaleData Ω P,
          DubinsSchwarzHypotheses D → DubinsSchwarzConclusion D) :
    StatementShape.{u} :=
  h

/-- The statement shape unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω),
        IsProbabilityMeasure P →
          ∀ D : ContinuousLocalMartingaleData Ω P,
            DubinsSchwarzHypotheses D → DubinsSchwarzConclusion D :=
  Iff.rfl

/-! ## Repo-local completion gate retained by child task S1-M-223-C007. -/

/-- Accepted repo-local closure modes for a future Dubins-Schwarz completion claim. -/
inductive RepoLocalClosureMode : Type where
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
deriving DecidableEq, Repr

/--
Machine-readable witness required before the Stage1 item can move from open to
completed.  This file intentionally constructs no value of this type: a value
would have to carry a proof of the full `StatementShape`.
-/
structure RepoLocalCompletionWitness : Type (u + 1) where
  mode : RepoLocalClosureMode
  statementShape : StatementShape.{u}

/-- Any repo-local completion witness exposes the full Dubins-Schwarz statement. -/
theorem RepoLocalCompletionWitness.toStatementShape
    (W : RepoLocalCompletionWitness.{u}) : StatementShape.{u} :=
  W.statementShape

/-- Textual names of the only closure modes accepted by the Stage1 gate. -/
def acceptedRepoLocalClosureModes : List String := [
  "local_proof_body",
  "local_wrapper_upstream_mathlib",
  "external_upstream_pinned"
]

/-- A packaged local-martingale candidate exposes each stopped martingale. -/
theorem stoppedMartingale_of_data {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ContinuousLocalMartingaleData Ω P) (n : ℕ) :
    Martingale (stoppedProcess D.process (D.localizingSeq n)) D.filtration P :=
  (D.stoppedMartingale n).2

/-- A packaged local-martingale candidate exposes each localizing stopping time. -/
theorem localizingSeq_isStoppingTime {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ContinuousLocalMartingaleData Ω P) (n : ℕ) :
    IsStoppingTime D.filtration (D.localizingSeq n) :=
  (D.stoppedMartingale n).1

/-- A packaged local-martingale candidate exposes its inverse time-change stopping times. -/
theorem inverseTimeChange_isStoppingTime {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} (D : ContinuousLocalMartingaleData Ω P) (t : ℝ≥0) :
    IsStoppingTime D.filtration (D.inverseTimeChange t) :=
  D.inverseTimeChangeStopping t

/-! ## Continuous predictable quadratic-variation child-task wrappers. -/

/-- A packaged quadratic-variation candidate exposes sample-path continuity. -/
theorem ContinuousPredictableQuadraticVariationData.qv_pathContinuous
    {Ω : Type u} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›}
    (Q : ContinuousPredictableQuadraticVariationData Ω filtration) :
    ∀ ω : Ω, Continuous fun t : ℝ≥0 => Q.quadraticVariation t ω :=
  Q.quadraticVariationContinuous

/-- A packaged quadratic-variation candidate exposes monotonicity. -/
theorem ContinuousPredictableQuadraticVariationData.qv_monotone
    {Ω : Type u} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›}
    (Q : ContinuousPredictableQuadraticVariationData Ω filtration) :
    ∀ ω : Ω, Monotone fun t : ℝ≥0 => Q.quadraticVariation t ω :=
  Q.quadraticVariationMonotone

/-- A packaged quadratic-variation candidate exposes mathlib predictability. -/
theorem ContinuousPredictableQuadraticVariationData.qv_predictable
    {Ω : Type u} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›}
    (Q : ContinuousPredictableQuadraticVariationData Ω filtration) :
    IsPredictable filtration Q.quadraticVariation :=
  Q.predictableQuadraticVariation

/-- A packaged quadratic-variation candidate exposes inverse-time stopping times. -/
theorem ContinuousPredictableQuadraticVariationData.inverseTimeChange_isStoppingTime
    {Ω : Type u} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›}
    (Q : ContinuousPredictableQuadraticVariationData Ω filtration) (t : ℝ≥0) :
    IsStoppingTime filtration (Q.inverseTimeChange t) :=
  Q.inverseTimeChangeStopping t

/-- Full Dubins-Schwarz data exposes the dedicated quadratic-variation package. -/
theorem ContinuousLocalMartingaleData.qvData_inverseTimeChange_isStoppingTime
    {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ContinuousLocalMartingaleData Ω P) (t : ℝ≥0) :
    IsStoppingTime D.filtration
      ((D.toQuadraticVariationData).inverseTimeChange t) :=
  (D.toQuadraticVariationData).inverseTimeChange_isStoppingTime t

/-- The Brownian-motion boundary exposes the Gaussian-process component. -/
theorem StandardBrownianMotion.isGaussianProcess {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : StandardBrownianMotion B P) :
    IsGaussianProcess B P :=
  hB.1

/-- The Brownian-motion boundary exposes independent increments. -/
theorem StandardBrownianMotion.hasIndepIncrements {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : StandardBrownianMotion B P) :
    HasIndepIncrements B P :=
  hB.2.1

/-- The Brownian-motion boundary exposes the one-dimensional Gaussian marginals. -/
theorem StandardBrownianMotion.hasLaw_gaussianReal {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : StandardBrownianMotion B P) (t : ℝ≥0) :
    HasLaw (B t) (gaussianReal 0 t) P :=
  hB.2.2.1 t

/-- The Brownian-motion boundary exposes the almost-sure origin condition. -/
theorem StandardBrownianMotion.origin_ae {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : StandardBrownianMotion B P) :
    ∀ᵐ ω ∂P, B 0 ω = 0 :=
  hB.2.2.2.1

/-- The Brownian-motion boundary exposes sample-path continuity. -/
theorem StandardBrownianMotion.pathContinuous {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : StandardBrownianMotion B P) :
    ∀ ω : Ω, Continuous fun t : ℝ≥0 => B t ω :=
  hB.2.2.2.2

/-! ## Audit probes retained in the checked file. -/

#check Filtration
#check StronglyAdapted
#check ProgMeasurable
#check IsPredictable
#check IsStoppingTime
#check stoppedProcess
#check stoppedValue
#check Martingale
#check Martingale.integrable
#check Submartingale
#check Supermartingale
#check IsGaussianProcess
#check ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_eval
#check HasIndepIncrements
#check ProbabilityTheory.HasIndepIncrements.indepFun_sub_sub
#check HasLaw
#check gaussianReal
#check gaussianReal_zero_var
#check StandardBrownianMotion
#check BrownianMotionPackage
#check BrownianMotionPackage.standardBrownianMotion
#check BrownianMotionPackage.ofStandardBrownianMotion
#check standardBrownianMotion_iff_exists_package
#check RepoLocalClosureMode
#check RepoLocalCompletionWitness
#check RepoLocalCompletionWitness.toStatementShape
#check acceptedRepoLocalClosureModes
#check ContinuousLocalMartingaleOverNNReal
#check ContinuousLocalMartingaleOverNNReal.localizedProcess
#check ContinuousLocalMartingaleOverNNReal.stoppedProcess_martingale
#check ContinuousPredictableQuadraticVariationData
#check ContinuousPredictableQuadraticVariationData.qv_predictable
#check ContinuousPredictableQuadraticVariationData.inverseTimeChange_isStoppingTime
#check ContinuousLocalMartingaleData
#check ContinuousLocalMartingaleData.toLocalMartingale
#check ContinuousLocalMartingaleData.toQuadraticVariationData
#check StatementShape

/-- mathlib revision used for this Stage1 anchor audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Child-task anchor audit for the exact public checklist request.

Each name in this table is also exercised by a `#check` probe above and by the
typed statement boundary in this file, except for `Filtration`/`IsStoppingTime`
and `stoppedProcess`/`Martingale`, which are additionally used in
`ContinuousLocalMartingaleData`.
-/
def requestedMathlibAnchorAudit : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.stoppedProcess",
  "MeasureTheory.Martingale",
  "ProbabilityTheory.IsGaussianProcess",
  "ProbabilityTheory.HasIndepIncrements",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.gaussianReal"
]

/-- mathlib modules checked while locating repo-local Dubins-Schwarz anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.HittingTime",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Independence.Process.HasIndepIncrements",
  "Mathlib.Probability.Distributions.Gaussian.Real",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.IdentDistrib"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.ProgMeasurable",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.stoppedProcess",
  "MeasureTheory.stoppedValue",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.Submartingale",
  "MeasureTheory.Supermartingale",
  "MeasureTheory.Martingale.stoppedValue_ae_eq_condExp_of_le",
  "MeasureTheory.Submartingale.stoppedProcess",
  "ProbabilityTheory.IsGaussianProcess",
  "ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_eval",
  "ProbabilityTheory.HasIndepIncrements",
  "ProbabilityTheory.HasIndepIncrements.indepFun_sub_sub",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.gaussianReal"
]

/-- Search terms that did not locate a terminal Dubins-Schwarz proof in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Dubins",
  "Dambis",
  "Schwarz",
  "Brownian",
  "Wiener",
  "LocalMartingale",
  "local martingale",
  "quadratic variation",
  "QuadraticVariation",
  "predictable quadratic variation",
  "stochastic integral",
  "StochasticIntegral",
  "semimartingale"
]

/-! ## Public theorem-tree split proposed by child task S1-M-223-C003. -/

/-- Canonical root name for the Dubins-Schwarz theorem-tree boundary. -/
def theoremTreeRoot : String :=
  "DS.root"

/--
The public package split requested for the Stage1 theorem-tree backfill.

These are process/planning nodes for the statement-boundary artifact.  They are
not completed proof leaves for the Dubins-Schwarz theorem.
-/
def theoremTreePackages : List String := [
  "statement_normalization",
  "mathlib_object_model",
  "local_martingale_bridge",
  "quadratic_variation_api",
  "time_change_stopping",
  "gaussian_marginals",
  "independent_increments",
  "brownian_conclusion"
]

/-- Human-readable responsibilities for the public theorem-tree package split. -/
def theoremTreePackageResponsibilities : List (String × String) := [
  ("statement_normalization",
    "Freeze the process carrier, probability measure, filtration, local martingale data, quadratic variation, inverse time change, and Brownian-motion target."),
  ("mathlib_object_model",
    "Map the normalized statement to mathlib anchors for filtrations, stopping times, stopped processes, martingales, Gaussian processes, independent increments, laws, and Gaussian real distributions."),
  ("local_martingale_bridge",
    "Bridge continuous local martingales to localized stopped-process martingales over nonnegative real time."),
  ("quadratic_variation_api",
    "Provide or import continuous predictable quadratic variation, monotonicity, continuity, inverse relation, and unboundedness hypotheses."),
  ("time_change_stopping",
    "Construct inverse quadratic-variation times and prove the required stopping-time and terminal-value properties."),
  ("gaussian_marginals",
    "Prove the time-changed process has the target one-dimensional laws `gaussianReal 0 t`."),
  ("independent_increments",
    "Prove independent increments for the time-changed process after optional-sampling and time-change reductions."),
  ("brownian_conclusion",
    "Assemble Gaussian-process, marginal-law, independent-increment, origin, and path-continuity components into `StandardBrownianMotion`.")
]

/-- Dedicated child-task leaves for the continuous-local-martingale bridge. -/
def continuousLocalMartingaleBridgeLeaves : List (String × String) := [
  ("CLM223.L001.checked.process_carrier",
    "Use `ContinuousTimeProcess Ω = ℝ≥0 → Ω → ℝ` as the process carrier."),
  ("CLM223.L002.checked.localization_sequence",
    "Use `LocalizingSequence Ω = ℕ → Ω → WithTop ℝ≥0` for stopping-time localization."),
  ("CLM223.L003.checked.stopped_martingales",
    "Package `IsStoppingTime` and `Martingale (stoppedProcess process τ)` for each localizing index."),
  ("CLM223.L004.checked.path_continuity",
    "Package continuous sample paths separately from the stopped-process martingale bridge."),
  ("CLM223.L005.unchecked.canonical_mathlib_equivalence",
    "If mathlib later adds a canonical continuous local martingale predicate, prove equivalence with this stopped-process package.")
]

/-- Dedicated child-task leaves for continuous predictable quadratic variation. -/
def continuousPredictableQuadraticVariationLeaves : List (String × String) := [
  ("QV223.L001.checked.qv_carrier",
    "Use `ℝ≥0 → Ω → ℝ≥0` as the continuous quadratic-variation carrier."),
  ("QV223.L002.checked.predictable_qv",
    "Use mathlib's generic `IsPredictable filtration quadraticVariation` predicate for predictability."),
  ("QV223.L003.checked.qv_path_continuity",
    "Package sample-path continuity of the quadratic-variation process."),
  ("QV223.L004.checked.qv_monotonicity",
    "Package monotonicity of the quadratic-variation process in nonnegative time."),
  ("QV223.L005.checked.inverse_time_carrier",
    "Use `InverseTimeChange Ω = ℝ≥0 → Ω → WithTop ℝ≥0` for inverse quadratic-variation times."),
  ("QV223.L006.checked.inverse_times_stopping",
    "Package `IsStoppingTime filtration (inverseTimeChange t)` for each target time."),
  ("QV223.L007.unchecked.inverse_qv_relation",
    "Replace the proposition field `inverseQuadraticVariation` with concrete hitting-time/equality lemmas."),
  ("QV223.L008.unchecked.unbounded_and_terminal_convention",
    "Replace proposition fields for unboundedness and `⊤` terminal-value handling with concrete hypotheses and lemmas.")
]

/-- Dedicated child-task leaves for Brownian-motion packaging. -/
def brownianMotionPackagingLeaves : List (String × String) := [
  ("BM223.L001.checked.process_carrier",
    "Use `ContinuousTimeProcess Ω = ℝ≥0 → Ω → ℝ` as the Brownian process carrier."),
  ("BM223.L002.checked.gaussian_process",
    "Package mathlib's `IsGaussianProcess process P` as a named field."),
  ("BM223.L003.checked.independent_increments",
    "Package mathlib's `HasIndepIncrements process P` as a named field."),
  ("BM223.L004.checked.gaussian_marginals",
    "Package one-dimensional laws `HasLaw (process t) (gaussianReal 0 t) P` for each `t : ℝ≥0`."),
  ("BM223.L005.checked.origin_and_path_continuity",
    "Package the a.e. zero-start condition and continuous sample paths."),
  ("BM223.L006.checked.standard_predicate_equivalence",
    "Convert between the named `BrownianMotionPackage` structure and the local `StandardBrownianMotion` predicate."),
  ("BM223.L007.unchecked.canonical_mathlib_brownian_equivalence",
    "If mathlib or a pinned dependency later exposes a canonical Brownian-motion predicate, prove equivalence with this package."),
  ("BM223.L008.unchecked.dubins_schwarz_brownian_proof",
    "Prove that the inverse-quadratic-variation time-changed local martingale satisfies the package fields.")
]

#check theoremTreeRoot
#check theoremTreePackages
#check theoremTreePackageResponsibilities
#check continuousLocalMartingaleBridgeLeaves
#check continuousPredictableQuadraticVariationLeaves
#check brownianMotionPackagingLeaves

end S1_M_223
end Stage1
end AwesomeTheorems
