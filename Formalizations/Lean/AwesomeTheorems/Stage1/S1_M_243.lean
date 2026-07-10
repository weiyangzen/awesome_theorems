import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.MeasureTheory.Integral.Lebesgue.Basic
import Mathlib.MeasureTheory.Function.LpSeminorm.Prod
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Kolmogorov

/-!
# S1-M-243 / THM-M-1050: Krylov estimate

This Stage1 artifact records a conservative Lean 4 statement boundary for a
Krylov estimate for diffusion processes.

Informally, the target theorem bounds the expected occupation integral
`E[∫_0^T f(t, X_t) dt]` of a nonnegative spacetime test function along a
diffusion process by a constant times an appropriate spacetime `L^p` norm of
`f`, under hypotheses such as probability-space assumptions, adaptedness,
integrability, bounded coefficients, and nondegenerate ellipticity.

The pinned mathlib snapshot provides measure theory, Bochner/Lebesgue
integration, probability measures, filtrations/adapted processes, martingales,
and `MemLp`/`eLpNorm`.  It does not expose a terminal
diffusion/SDE/Krylov-estimate API. Accordingly, this file provides only a
checked statement shape, a local martingale-problem boundary API, a concrete
product-measure spacetime `L^p` norm boundary, and low-risk wrappers around
the boundary data. It does not prove the Krylov estimate.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal BigOperators

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_243

universe u v

/-- Continuous time is represented by real time in this Stage1 boundary. -/
abbrev Time : Type := ℝ

/-- A stochastic process with state space `E`. -/
abbrev Process (Ω : Type u) (E : Type v) :=
  Time → Ω → E

/-- Nonnegative spacetime test functions used in the occupation estimate. -/
abbrev NonnegativeSpacetimeFunction (E : Type v) :=
  Time × E → ℝ≥0∞

/--
Concrete Stage1 martingale-problem API for the diffusion model.

This is still a boundary API, not the analytic proof of Krylov's estimate.
It replaces the previous anonymous `Prop` fields by named data: a class of
test functions, a generator, compensated observables that are martingales,
and boundedness/ellipticity/exponent witnesses.  Later work can refine this
API to a full SDE or second-order generator without changing the theorem
boundary back to unstructured placeholders.
-/
structure KrylovMartingaleProblemAPI (Ω : Type u) (E : Type v)
    [MeasurableSpace Ω] [MeasurableSpace E]
    (μ : Measure Ω) (filtration : Filtration Time ‹MeasurableSpace Ω›)
    (process : Process Ω E) (dimension : ℕ)
    (integrabilityExponent : ℝ≥0∞) where
  TestFunction : Type v
  testFunction : TestFunction → E → ℝ
  testFunctionMeasurable : ∀ φ : TestFunction, Measurable (testFunction φ)
  generator : TestFunction → Time × E → ℝ
  generatorMeasurable : ∀ φ : TestFunction, Measurable (generator φ)
  observable : TestFunction → Process Ω ℝ
  observable_eq_process :
    ∀ (φ : TestFunction) (t : Time) (ω : Ω),
      observable φ t ω = testFunction φ (process t ω)
  compensatedObservable : TestFunction → Process Ω ℝ
  compensatedObservable_martingale :
    ∀ φ : TestFunction, Martingale (compensatedObservable φ) filtration μ
  coefficientEnvelope : Time × E → ℝ≥0∞
  coefficientEnvelopeBound : ℝ≥0∞
  coefficientEnvelope_bounded :
    ∀ z : Time × E, coefficientEnvelope z ≤ coefficientEnvelopeBound
  coefficientEnvelopeBound_lt_top : coefficientEnvelopeBound < ⊤
  ellipticityProfile : Time × E → ℝ≥0∞
  ellipticityConstant : ℝ≥0∞
  uniformEllipticity :
    ∀ z : Time × E, ellipticityConstant ≤ ellipticityProfile z
  ellipticityConstant_pos : 0 < ellipticityConstant
  dimension_pos : 0 < dimension
  exponent_pos : 0 < integrabilityExponent
  exponent_lt_top : integrabilityExponent < ⊤

/--
Occupation integral of a nonnegative spacetime function along a process over
the deterministic time interval `[0, T]`.

For `T < 0`, `Set.Icc 0 T` is empty, so the expression is still total.  The
normalized Krylov hypotheses below include `0 ≤ T` for the intended theorem.
-/
def occupationIntegral {Ω : Type u} {E : Type v}
    (X : Process Ω E) (T : Time) (f : NonnegativeSpacetimeFunction E)
    (ω : Ω) : ℝ≥0∞ :=
  ∫⁻ t, f (t, X t ω) ∂(volume.restrict (Set.Icc (0 : Time) T))

/-- Expected occupation integral with respect to the ambient probability law. -/
def expectedOccupation {Ω : Type u} [MeasurableSpace Ω] {E : Type v}
    (μ : Measure Ω) (X : Process Ω E) (T : Time)
    (f : NonnegativeSpacetimeFunction E) : ℝ≥0∞ :=
  ∫⁻ ω, occupationIntegral X T f ω ∂μ

/--
Concrete product spacetime measure for the finite horizon `[0, T]`.

This is the repo-local `L^p` measure selected by child task C005: Lebesgue time
restricted to the deterministic horizon, producted with a reference state
measure.
-/
def spacetimeMeasure {E : Type v} [MeasurableSpace E]
    (ν : Measure E) (T : Time) : Measure (Time × E) :=
  (volume.restrict (Set.Icc (0 : Time) T)).prod ν

/--
Concrete spacetime `L^p` norm using mathlib's `eLpNorm` API over the product
measure `(volume.restrict (Set.Icc 0 T)).prod ν`.
-/
def spacetimeLpNorm {E : Type v} [MeasurableSpace E]
    (ν : Measure E) (p : ℝ≥0∞) (T : Time)
    (f : NonnegativeSpacetimeFunction E) : ℝ≥0∞ :=
  eLpNorm f p (spacetimeMeasure ν T)

/--
Concrete finite spacetime `L^p` membership using mathlib's `MemLp` API over
the product measure `(volume.restrict (Set.Icc 0 T)).prod ν`.
-/
def spacetimeMemLp {E : Type v} [MeasurableSpace E]
    (ν : Measure E) (p : ℝ≥0∞) (T : Time)
    (f : NonnegativeSpacetimeFunction E) : Prop :=
  MemLp f p (spacetimeMeasure ν T)

/--
Normalized data for a diffusion-process Krylov estimate.

The `model` field is a concrete Stage1 martingale-problem boundary replacing
the former raw `Prop` placeholders for the diffusion equation, coefficient
boundedness, uniform ellipticity, and exponent admissibility.  The
`stateReferenceMeasure` field supplies the state-space side of the concrete
product measure used by `spacetimeMemLp` and `spacetimeLpNorm`.
-/
structure KrylovDiffusionData (Ω : Type u) (E : Type v)
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E] where
  μ : Measure Ω
  isProbability : IsProbabilityMeasure μ
  filtration : Filtration Time ‹MeasurableSpace Ω›
  process : Process Ω E
  processStronglyAdapted : StronglyAdapted filtration process
  processAEMeasurable : ∀ t : Time, AEMeasurable (process t) μ
  dimension : ℕ
  integrabilityExponent : ℝ≥0∞
  model :
    KrylovMartingaleProblemAPI Ω E μ filtration process dimension integrabilityExponent
  stateReferenceMeasure : Measure E
  krylovConstant : ℝ≥0∞
  finiteTimeConstant : ∀ T : Time, 0 ≤ T → krylovConstant < ⊤

/-- Hypotheses for one finite-time Krylov estimate instance. -/
def KrylovEstimateHypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    (D : KrylovDiffusionData Ω E) (T : Time)
    (f : NonnegativeSpacetimeFunction E) : Prop :=
  0 ≤ T ∧
    Measurable f ∧
      spacetimeMemLp D.stateReferenceMeasure D.integrabilityExponent T f

/--
Conclusion of the Krylov estimate boundary: expected occupation is bounded by
the supplied Krylov constant times the intended spacetime `L^p` norm.
-/
def KrylovEstimateConclusion {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    (D : KrylovDiffusionData Ω E) (T : Time)
    (f : NonnegativeSpacetimeFunction E) : Prop :=
  expectedOccupation D.μ D.process T f ≤
    D.krylovConstant *
      spacetimeLpNorm D.stateReferenceMeasure D.integrabilityExponent T f

/--
Stage1 normalized statement shape for a diffusion-process Krylov estimate.

This is a formalization boundary only.  It says that every packaged diffusion
datum satisfying the analytic assumptions should satisfy the expected
occupation bound for every nonnegative measurable spacetime function with
finite target `L^p` norm.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) (E : Type v) [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E],
    ∀ D : KrylovDiffusionData Ω E,
      ∀ (T : Time) (f : NonnegativeSpacetimeFunction E),
        KrylovEstimateHypotheses D T f →
          KrylovEstimateConclusion D T f

/-- The normalized statement unfolds to the expected data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) (E : Type v) [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E],
        ∀ D : KrylovDiffusionData Ω E,
          ∀ (T : Time) (f : NonnegativeSpacetimeFunction E),
            KrylovEstimateHypotheses D T f →
              KrylovEstimateConclusion D T f :=
  Iff.rfl

/-- The packaged law is a probability measure. -/
theorem isProbability_of_data {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    (D : KrylovDiffusionData Ω E) :
    IsProbabilityMeasure D.μ :=
  D.isProbability

/-- The packaged process is strongly adapted to the supplied filtration. -/
theorem stronglyAdapted_of_data {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    (D : KrylovDiffusionData Ω E) :
    StronglyAdapted D.filtration D.process :=
  D.processStronglyAdapted

/-- The packaged process has an a.e.-measurable time slice at every time. -/
theorem aeMeasurable_process_of_data {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    (D : KrylovDiffusionData Ω E) (t : Time) :
    AEMeasurable (D.process t) D.μ :=
  D.processAEMeasurable t

/-- Project the nonnegative time horizon from the normalized hypotheses. -/
theorem nonneg_time_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (h : KrylovEstimateHypotheses D T f) :
    0 ≤ T :=
  h.1

/-- Project measurability of the test function from the normalized hypotheses. -/
theorem measurable_testFunction_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (h : KrylovEstimateHypotheses D T f) :
    Measurable f :=
  h.2.1

/-- Project finite target spacetime `L^p` membership from the normalized hypotheses. -/
theorem spacetimeMemLp_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (h : KrylovEstimateHypotheses D T f) :
    spacetimeMemLp D.stateReferenceMeasure D.integrabilityExponent T f :=
  h.2.2

/-- The concrete finite spacetime `L^p` hypothesis implies finite `eLpNorm`. -/
theorem spacetimeLpNorm_lt_top_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (h : KrylovEstimateHypotheses D T f) :
    spacetimeLpNorm D.stateReferenceMeasure D.integrabilityExponent T f < ⊤ :=
  (spacetimeMemLp_of_hypotheses h).2

/-- Project the concrete martingale-problem model from the packaged data. -/
def martingaleProblemAPI_of_data {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    (D : KrylovDiffusionData Ω E) :
    KrylovMartingaleProblemAPI Ω E D.μ D.filtration D.process D.dimension
      D.integrabilityExponent :=
  D.model

/-- Project the checked martingale property for compensated test observables. -/
theorem martingaleProblem_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (_h : KrylovEstimateHypotheses D T f)
    (φ : D.model.TestFunction) :
    Martingale (D.model.compensatedObservable φ) D.filtration D.μ :=
  D.model.compensatedObservable_martingale φ

/-- Project the observable/process compatibility from the model API. -/
theorem observable_eq_process_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (_h : KrylovEstimateHypotheses D T f)
    (φ : D.model.TestFunction) (t : Time) (ω : Ω) :
    D.model.observable φ t ω = D.model.testFunction φ (D.process t ω) :=
  D.model.observable_eq_process φ t ω

/-- Project boundedness of the concrete coefficient envelope. -/
theorem boundedCoefficients_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (_h : KrylovEstimateHypotheses D T f) :
    ∀ z : Time × E, D.model.coefficientEnvelope z ≤ D.model.coefficientEnvelopeBound :=
  D.model.coefficientEnvelope_bounded

/-- Project finiteness of the coefficient envelope bound. -/
theorem coefficientEnvelopeBound_lt_top_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (_h : KrylovEstimateHypotheses D T f) :
    D.model.coefficientEnvelopeBound < ⊤ :=
  D.model.coefficientEnvelopeBound_lt_top

/-- Project the concrete uniform ellipticity lower bound. -/
theorem uniformEllipticity_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (_h : KrylovEstimateHypotheses D T f) :
    ∀ z : Time × E, D.model.ellipticityConstant ≤ D.model.ellipticityProfile z :=
  D.model.uniformEllipticity

/-- Project admissibility of the dimension/exponent regime. -/
theorem exponentAdmissible_of_hypotheses {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    {D : KrylovDiffusionData Ω E} {T : Time}
    {f : NonnegativeSpacetimeFunction E}
    (_h : KrylovEstimateHypotheses D T f) :
    0 < D.dimension ∧ 0 < D.integrabilityExponent ∧ D.integrabilityExponent < ⊤ :=
  ⟨D.model.dimension_pos, D.model.exponent_pos, D.model.exponent_lt_top⟩

/-- The packaged constant is finite on every nonnegative finite horizon. -/
theorem krylovConstant_lt_top {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] [TopologicalSpace E]
    (D : KrylovDiffusionData Ω E) {T : Time} (hT : 0 ≤ T) :
    D.krylovConstant < ⊤ :=
  D.finiteTimeConstant T hT

/-! ## S1-M-243-C006 discrete-time toy occupation estimate -/

/-- A discrete-time stochastic process indexed by the finite horizon `Fin n`. -/
abbrev DiscreteProcess (Ω : Type u) (E : Type v) (n : ℕ) :=
  Fin n → Ω → E

/-- Nonnegative discrete spacetime functions on `Fin n × E`. -/
abbrev DiscreteNonnegativeSpacetimeFunction (E : Type v) (n : ℕ) :=
  Fin n × E → ℝ≥0∞

/--
Discrete occupation sum along one sample path.

This is the finite-time toy analogue of `occupationIntegral`: the time
integral over `[0, T]` is replaced by a finite sum over `Fin n`.
-/
def discreteOccupationSum {Ω : Type u} {E : Type v} {n : ℕ}
    (X : DiscreteProcess Ω E n)
    (f : DiscreteNonnegativeSpacetimeFunction E n) (ω : Ω) : ℝ≥0∞ :=
  ∑ k : Fin n, f (k, X k ω)

/--
Pointwise time-envelope hypothesis for the discrete toy estimate.

For every time index and sample point, the observed value of `f` along the
path is bounded by a deterministic nonnegative envelope depending only on
time.
-/
def DiscreteTimeEnvelopeHypotheses {Ω : Type u} {E : Type v} {n : ℕ}
    (X : DiscreteProcess Ω E n)
    (f : DiscreteNonnegativeSpacetimeFunction E n)
    (timeEnvelope : Fin n → ℝ≥0∞) : Prop :=
  ∀ (k : Fin n) (ω : Ω), f (k, X k ω) ≤ timeEnvelope k

/--
Conclusion of the discrete toy occupation estimate: the occupation sum along
any sample path is bounded by the sum of the deterministic time envelope.
-/
def DiscreteTimeEnvelopeConclusion {Ω : Type u} {E : Type v} {n : ℕ}
    (X : DiscreteProcess Ω E n)
    (f : DiscreteNonnegativeSpacetimeFunction E n)
    (timeEnvelope : Fin n → ℝ≥0∞) (ω : Ω) : Prop :=
  discreteOccupationSum X f ω ≤ ∑ k : Fin n, timeEnvelope k

/--
Local proof of the discrete-time toy occupation estimate.

This is a genuine checked proof body, but it is intentionally only a
finite-horizon envelope estimate.  It does not prove the continuous diffusion
Krylov estimate represented by `StatementShape`.
-/
theorem discreteOccupationSum_le_timeEnvelope {Ω : Type u} {E : Type v}
    {n : ℕ} (X : DiscreteProcess Ω E n)
    (f : DiscreteNonnegativeSpacetimeFunction E n)
    (timeEnvelope : Fin n → ℝ≥0∞)
    (h : DiscreteTimeEnvelopeHypotheses X f timeEnvelope) (ω : Ω) :
    DiscreteTimeEnvelopeConclusion X f timeEnvelope ω := by
  unfold DiscreteTimeEnvelopeConclusion discreteOccupationSum
  exact Finset.sum_le_sum (fun k _hk => h k ω)

/-- Statement form for the C006 discrete toy Krylov/occupation estimate. -/
def DiscreteToyKrylovEstimateStatement : Prop :=
  ∀ (Ω : Type u) (E : Type v) (n : ℕ),
    ∀ (X : DiscreteProcess Ω E n)
      (f : DiscreteNonnegativeSpacetimeFunction E n)
      (timeEnvelope : Fin n → ℝ≥0∞),
      DiscreteTimeEnvelopeHypotheses X f timeEnvelope →
        ∀ ω : Ω, DiscreteTimeEnvelopeConclusion X f timeEnvelope ω

/-- Checked C006 discrete-time toy Krylov/occupation estimate. -/
theorem discreteToyKrylovEstimate :
    DiscreteToyKrylovEstimateStatement.{u, v} := by
  intro Ω E n X f timeEnvelope h ω
  exact discreteOccupationSum_le_timeEnvelope X f timeEnvelope h ω

/-! ## Audit probes retained in the checked file. -/

#check MeasureTheory.Measure
#check MeasureTheory.IsProbabilityMeasure
#check MeasureTheory.Filtration
#check MeasureTheory.StronglyAdapted
#check AEMeasurable
#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
#check MeasureTheory.lintegral
#check MeasureTheory.Measure.restrict
#check MeasureTheory.Measure.prod
#check MeasureTheory.volume
#check MeasureTheory.Martingale
#check ProbabilityTheory.IsKolmogorovProcess

/-- mathlib revision used for the Stage1 anchor audit. -/
def mathlibAnchorRevision : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Integral.Lebesgue.Basic",
  "Mathlib.MeasureTheory.Measure.Lebesgue.Basic",
  "Mathlib.MeasureTheory.Measure.Prod",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Prod",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Composition",
  "Mathlib.Probability.Independence.Process.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Measure",
  "MeasureTheory.IsProbabilityMeasure",
  "MeasureTheory.Filtration",
  "MeasureTheory.StronglyAdapted",
  "AEMeasurable",
  "MeasureTheory.MemLp",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.lintegral",
  "MeasureTheory.Measure.restrict",
  "MeasureTheory.Measure.prod",
  "MeasureTheory.volume",
  "MeasureTheory.Martingale",
  "ProbabilityTheory.IsKolmogorovProcess"
]

/--
Search terms audited while checking for a terminal Krylov-estimate anchor.
-/
def terminalAnchorSearchTerms : List String := [
  "Krylov",
  "krylov",
  "diffusion",
  "Diffusion",
  "SDE",
  "Ito",
  "Itô",
  "stochastic integral",
  "StochasticIntegral",
  "Brownian",
  "semimartingale",
  "QuadraticVariation"
]

/-! ## S1-M-243-C003 public theorem-tree split -/

/--
The eight package names requested by the public Stage1 theorem-tree backfill.

The constructors are a stable split for later workers.  They deliberately do
not assert that the terminal Krylov estimate is proved in this repository.
-/
inductive KrylovTheoremTreePackage where
  | statementNormalization
  | mathlibObjectModel
  | diffusionModelApi
  | analyticAssumptions
  | occupationIntegralMeasurability
  | fubiniKernelBridge
  | coreKrylovBound
  | repoLocalClosure
  deriving DecidableEq, Repr

/-- C003-local status vocabulary for the public package split. -/
inductive KrylovPackageStatus where
  | checkedStatementBoundary
  | formalizationDebt
  | repoLocalClosureOpen
  deriving DecidableEq, Repr

/-- One M0387-budgeted package row for the C003 Krylov theorem-tree split. -/
structure KrylovPackageLeafBudget where
  package : KrylovTheoremTreePackage
  leafId : String
  obligation : String
  upstreamInputs : String
  downstreamInterface : String
  budgetStepLimit : Nat
  status : KrylovPackageStatus
  completionBoundary : String

/-- M0387 local proof-leaf budget limit used by the C003 split. -/
def c003LeafBudgetLimit : Nat :=
  100

/--
Integration-ready package ledger for the Krylov estimate theorem tree.

The rows separate checked local statement-boundary work from the analytic and
modeling debt still required for a real Krylov-estimate proof.  In particular,
the diffusion/SDE API, product-measure `L^p` norm, occupation measurability,
Fubini/kernel bridge, and core estimate remain open formalization work.
-/
def c003KrylovPackageLeafBudgets : List KrylovPackageLeafBudget := [
  {
    package := .statementNormalization,
    leafId := "S1-M-243-C003-L001-statement-normalization",
    obligation := "Keep the canonical theorem target as the data-parametrized implication from KrylovEstimateHypotheses to KrylovEstimateConclusion.",
    upstreamInputs := "StatementShape, KrylovEstimateHypotheses, KrylovEstimateConclusion, occupationIntegral, expectedOccupation",
    downstreamInterface := "AwesomeTheorems.Stage1.S1_M_243.StatementShape",
    budgetStepLimit := c003LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "checked statement boundary only: statementShape_iff_forall_data is definitional, but no analytic Krylov proof body is present"
  },
  {
    package := .mathlibObjectModel,
    leafId := "S1-M-243-C003-L002-mathlib-object-model",
    obligation := "Use pinned mathlib objects for measures, probability measures, filtrations, adaptedness, a.e. measurability, lintegrals, restrictions, volume, MemLp, martingales, and Kolmogorov-process anchors.",
    upstreamInputs := "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 plus mathlibAnchorNames",
    downstreamInterface := "KrylovDiffusionData fields isProbability, filtration, processStronglyAdapted, processAEMeasurable",
    budgetStepLimit := c003LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "checked anchor boundary only: the imported objects typecheck, but they are not a terminal Krylov theorem"
  },
  {
    package := .diffusionModelApi,
    leafId := "S1-M-243-C003-L003-diffusion-model-api",
    obligation := "Refine the local KrylovMartingaleProblemAPI toward a full Lean diffusion, SDE, generator, or martingale-problem API.",
    upstreamInputs := "KrylovMartingaleProblemAPI plus future repo-local SDE/generator model and compatibility with StronglyAdapted process",
    downstreamInterface := "D.model",
    budgetStepLimit := c003LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "checked model-boundary progress: the old diffusionEquation Prop field is replaced by KrylovMartingaleProblemAPI, but no analytic Krylov proof body is present"
  },
  {
    package := .analyticAssumptions,
    leafId := "S1-M-243-C003-L004-analytic-assumptions",
    obligation := "Refine coefficient-envelope boundedness, ellipticity-profile lower bounds, exponent witnesses, and concrete spacetime Lp assumptions using Lean norm APIs.",
    upstreamInputs := "KrylovMartingaleProblemAPI, stateReferenceMeasure, spacetimeMeasure, MemLp, and eLpNorm APIs",
    downstreamInterface := "D.model.coefficientEnvelope_bounded, D.model.uniformEllipticity, D.model.exponent_pos, D.model.exponent_lt_top, spacetimeMemLp D.stateReferenceMeasure D.integrabilityExponent T f, spacetimeLpNorm D.stateReferenceMeasure D.integrabilityExponent T f",
    budgetStepLimit := c003LeafBudgetLimit,
    status := .formalizationDebt,
    completionBoundary := "partial model-boundary progress: raw analytic Prop fields and arbitrary Lp norm fields are replaced, but terminal analytic assumptions remain formalization debt"
  },
  {
    package := .occupationIntegralMeasurability,
    leafId := "S1-M-243-C003-L005-occupation-integral-measurability",
    obligation := "Prove the measurability/a.e.-measurability side conditions for t ↦ f (t, X_t ω), ω ↦ occupationIntegral X T f ω, and related restricted-lintegral expressions.",
    upstreamInputs := "AEMeasurable process slices, Measurable f, volume.restrict (Set.Icc 0 T), lintegral measurability lemmas",
    downstreamInterface := "occupationIntegral and expectedOccupation are usable in later Fubini and expectation arguments",
    budgetStepLimit := c003LeafBudgetLimit,
    status := .formalizationDebt,
    completionBoundary := "unchecked formalization debt: the current file defines the expressions but does not prove the required measurability lemmas"
  },
  {
    package := .fubiniKernelBridge,
    leafId := "S1-M-243-C003-L006-fubini-kernel-bridge",
    obligation := "Bridge the expected occupation lintegral to spacetime/kernel estimates using Tonelli/Fubini and the chosen transition-law or occupation-measure API.",
    upstreamInputs := "occupation measurability, probability law μ, restricted time measure, future transition kernel or occupation measure construction",
    downstreamInterface := "a reusable equality or inequality reducing expectedOccupation to a spacetime integral estimate",
    budgetStepLimit := c003LeafBudgetLimit,
    status := .formalizationDebt,
    completionBoundary := "unchecked formalization debt: no Fubini/Tonelli kernel bridge is currently proved"
  },
  {
    package := .coreKrylovBound,
    leafId := "S1-M-243-C003-L007-core-krylov-bound",
    obligation := "Prove the analytic Krylov bound from the concrete diffusion model and Lp hypotheses.",
    upstreamInputs := "diffusion model API, analytic assumptions, occupation measurability, Fubini/kernel bridge, and PDE/probabilistic estimate machinery",
    downstreamInterface := "KrylovEstimateConclusion D T f",
    budgetStepLimit := c003LeafBudgetLimit,
    status := .formalizationDebt,
    completionBoundary := "unchecked formalization debt: this is the missing terminal analytic proof package"
  },
  {
    package := .repoLocalClosure,
    leafId := "S1-M-243-C003-L008-repo-local-closure",
    obligation := "Close the theorem in this repository through a local proof body, pinned mathlib wrapper, or pinned/imported external Lean 4 dependency; do not count anchor-only evidence.",
    upstreamInputs := "all preceding packages plus repo-local lake validation",
    downstreamInterface := "repo-local checked theorem aligned with StatementShape",
    budgetStepLimit := c003LeafBudgetLimit,
    status := .repoLocalClosureOpen,
    completionBoundary := "open completion gate: no completed state may retain repo_local_integration_debt"
  }
]

/-- The C003 package split contains exactly the eight requested public packages. -/
theorem c003KrylovPackageLeafBudgets_length :
    c003KrylovPackageLeafBudgets.length = 8 := by
  native_decide

/-- Every C003 package row is explicitly budgeted at the M0387 `<= 100` threshold. -/
theorem c003KrylovPackageLeafBudgets_all_le_100 :
    c003KrylovPackageLeafBudgets.all
      (fun row => row.budgetStepLimit ≤ c003LeafBudgetLimit) = true := by
  native_decide

/-- C003 is ready for public backfill as an open package ledger. -/
def c003PackageSplitReadyForPublicBackfill : Bool :=
  true

/-- The C003 theorem-tree split does not close the Krylov estimate. -/
def c003ClosesKrylovEstimate : Bool :=
  false

/--
No completed state in the C003 package ledger retains repo-local integration
debt: there is no completed terminal theorem state in this child.
-/
def c003NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c003PackageSplitReadyForPublicBackfill_eq_true :
    c003PackageSplitReadyForPublicBackfill = true :=
  rfl

theorem c003ClosesKrylovEstimate_eq_false :
    c003ClosesKrylovEstimate = false :=
  rfl

theorem c003NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c003NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check KrylovTheoremTreePackage
#check KrylovPackageLeafBudget
#check c003KrylovPackageLeafBudgets
#check c003KrylovPackageLeafBudgets_length
#check c003KrylovPackageLeafBudgets_all_le_100

/-! ## S1-M-243-C004 martingale-problem API replacement -/

/--
C004 records that the former raw `Prop` fields for the diffusion equation,
bounded coefficients, uniform ellipticity, and exponent admissibility have
been replaced in `KrylovDiffusionData` by `KrylovMartingaleProblemAPI`.
-/
def c004RawPropFieldsReplacedByModelAPI : Bool :=
  true

/-- C004 adds model API structure but still does not prove the Krylov estimate. -/
def c004ClosesKrylovEstimate : Bool :=
  false

/--
No completed theorem state is introduced by C004, so no completed state can
retain repo-local integration debt.
-/
def c004NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c004RawPropFieldsReplacedByModelAPI_eq_true :
    c004RawPropFieldsReplacedByModelAPI = true :=
  rfl

theorem c004ClosesKrylovEstimate_eq_false :
    c004ClosesKrylovEstimate = false :=
  rfl

theorem c004NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c004NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check KrylovMartingaleProblemAPI
#check martingaleProblemAPI_of_data
#check martingaleProblem_of_hypotheses
#check observable_eq_process_of_hypotheses
#check boundedCoefficients_of_hypotheses
#check uniformEllipticity_of_hypotheses
#check exponentAdmissible_of_hypotheses
#check c004RawPropFieldsReplacedByModelAPI_eq_true
#check c004ClosesKrylovEstimate_eq_false
#check c004NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true

/-! ## S1-M-243-C005 product-measure spacetime `L^p` norm -/

/--
C005 records that the former arbitrary `spacetimeLpNorm` and
`spacetimeLpFinite` fields have been replaced by concrete repo-local
definitions using `Measure.prod`, `MemLp`, and `eLpNorm`.
-/
def c005ConcreteSpacetimeLpNormUsesProductMeasure : Bool :=
  true

/-- C005 adds a concrete `L^p` norm boundary but still does not prove Krylov's estimate. -/
def c005ClosesKrylovEstimate : Bool :=
  false

/--
No completed theorem state is introduced by C005, so no completed state can
retain repo-local integration debt.
-/
def c005NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c005ConcreteSpacetimeLpNormUsesProductMeasure_eq_true :
    c005ConcreteSpacetimeLpNormUsesProductMeasure = true :=
  rfl

theorem c005ClosesKrylovEstimate_eq_false :
    c005ClosesKrylovEstimate = false :=
  rfl

theorem c005NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c005NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check spacetimeMeasure
#check spacetimeLpNorm
#check spacetimeMemLp
#check spacetimeMemLp_of_hypotheses
#check spacetimeLpNorm_lt_top_of_hypotheses
#check c005ConcreteSpacetimeLpNormUsesProductMeasure_eq_true
#check c005ClosesKrylovEstimate_eq_false
#check c005NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true

/-! ## S1-M-243-C006 discrete-time toy Krylov/occupation estimate -/

/--
C006 records that the file contains a checked finite-horizon discrete-time
occupation estimate with a local proof body.
-/
def c006DiscreteToyOccupationEstimateProved : Bool :=
  true

/--
C006 is a lower-risk local proof target only; it does not close the continuous
diffusion Krylov estimate.
-/
def c006ClosesKrylovEstimate : Bool :=
  false

/--
The completed C006 toy theorem is repo-local and does not rely on an
anchor-only external proof, so no completed C006 state retains
repo-local integration debt.
-/
def c006NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c006DiscreteToyOccupationEstimateProved_eq_true :
    c006DiscreteToyOccupationEstimateProved = true :=
  rfl

theorem c006ClosesKrylovEstimate_eq_false :
    c006ClosesKrylovEstimate = false :=
  rfl

theorem c006NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c006NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check DiscreteProcess
#check DiscreteNonnegativeSpacetimeFunction
#check discreteOccupationSum
#check DiscreteTimeEnvelopeHypotheses
#check DiscreteTimeEnvelopeConclusion
#check discreteOccupationSum_le_timeEnvelope
#check DiscreteToyKrylovEstimateStatement
#check discreteToyKrylovEstimate
#check c006DiscreteToyOccupationEstimateProved_eq_true
#check c006ClosesKrylovEstimate_eq_false
#check c006NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true

/-! ## S1-M-243-C007 repo-local closure gate -/

/--
The only completion routes allowed by the C007 gate for the continuous
diffusion Krylov estimate.
-/
inductive KrylovRepoLocalClosureRoute where
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  deriving DecidableEq, Repr

/--
Machine-checkable status vocabulary for the C007 completion gate.

The current artifact is `uncheckedOpen`: it has checked statement-boundary and
toy-estimate content, but no checked proof of the continuous Krylov estimate.
-/
inductive KrylovStage1ClosureStatus where
  | uncheckedOpen
  | completedBy : KrylovRepoLocalClosureRoute → KrylovStage1ClosureStatus
  deriving DecidableEq, Repr

/--
C007 closure evidence for the continuous diffusion Krylov estimate.

Each Boolean represents evidence that has passed `lake env lean` in this
repository.  The C006 discrete toy estimate is intentionally not one of these
routes, because it does not prove `StatementShape`.
-/
structure KrylovC007ClosureGate where
  localProofBodyValidated : Bool
  mathlibWrapperValidated : Bool
  pinnedExternalDependencyValidated : Bool

/-- C007's current repo-local closure evidence for the continuous theorem. -/
def c007CurrentClosureGate : KrylovC007ClosureGate where
  localProofBodyValidated := false
  mathlibWrapperValidated := false
  pinnedExternalDependencyValidated := false

/-- C007 completion is allowed only after one of the three repo-local routes validates. -/
def c007MayComplete (gate : KrylovC007ClosureGate) : Bool :=
  gate.localProofBodyValidated ||
    gate.mathlibWrapperValidated ||
      gate.pinnedExternalDependencyValidated

/--
C007 status rule: keep Stage1 unchecked/open unless repo-local completion
evidence has been validated for the continuous Krylov estimate.
-/
def c007StatusFromGate (gate : KrylovC007ClosureGate) :
    KrylovStage1ClosureStatus :=
  if gate.localProofBodyValidated then
    .completedBy .localProofBody
  else if gate.mathlibWrapperValidated then
    .completedBy .localWrapperUpstreamMathlib
  else if gate.pinnedExternalDependencyValidated then
    .completedBy .externalUpstreamPinned
  else
    .uncheckedOpen

/-- Current C007 status for the continuous Krylov estimate. -/
def c007CurrentStage1ClosureStatus : KrylovStage1ClosureStatus :=
  c007StatusFromGate c007CurrentClosureGate

/--
C007 records that no completed continuous-theorem state is present, so no
completed state retains repo-local integration debt.
-/
def c007NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c007MayComplete_current_eq_false :
    c007MayComplete c007CurrentClosureGate = false :=
  rfl

theorem c007CurrentStage1ClosureStatus_eq_uncheckedOpen :
    c007CurrentStage1ClosureStatus = .uncheckedOpen :=
  rfl

theorem c007NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c007NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check KrylovRepoLocalClosureRoute
#check KrylovStage1ClosureStatus
#check KrylovC007ClosureGate
#check c007MayComplete_current_eq_false
#check c007CurrentStage1ClosureStatus_eq_uncheckedOpen
#check c007NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true

end S1_M_243
end Stage1
end AwesomeTheorems
