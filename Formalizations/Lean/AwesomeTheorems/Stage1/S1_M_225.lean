import Mathlib.Analysis.BoundedVariation
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Process.Predictable
import Mathlib.Probability.Process.Stopping

/-!
# S1-M-225 / THM-M-1032: Ito formula

This Stage1 artifact records a conservative Lean 4 boundary for the
multidimensional Ito formula, viewed as the chain rule for stochastic
processes.

The pinned mathlib snapshot has probability spaces, laws, Gaussian processes,
independent increments, filtrations, adapted/predictable processes, stopping
times, and martingales.  It does not expose a terminal stochastic-calculus API
for semimartingales, stochastic integrals, quadratic covariation, or Ito's
formula.  The main theorem is therefore represented as a precise proposition
shape, while the checked content below consists only of projection wrappers and
small wrappers around available mathlib process APIs.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_225

universe u v

/-- A finite-dimensional real-valued stochastic process indexed by continuous time. -/
abbrev VectorProcess (Ω : Type u) (ι : Type v) :=
  ℝ → Ω → ι → ℝ

/-- A real-valued stochastic process indexed by continuous time. -/
abbrev RealProcess (Ω : Type u) :=
  ℝ → Ω → ℝ

/-- The deterministic clock process `t ↦ t`, used as Brownian quadratic variation. -/
def deterministicTimeProcess (Ω : Type u) : RealProcess Ω :=
  fun t _ => t

/-- The `i`-th coordinate process of a finite-dimensional real process. -/
def componentProcess {Ω : Type u} {ι : Type v}
    (X : VectorProcess Ω ι) (i : ι) : RealProcess Ω :=
  fun t ω => X t ω i

/-- Composition of a deterministic function with a finite-dimensional process. -/
def composedProcess {Ω : Type u} {ι : Type v}
    (f : (ι → ℝ) → ℝ) (X : VectorProcess Ω ι) : RealProcess Ω :=
  fun t ω => f (X t ω)

/--
Repo-local local-martingale API boundary.

This packages the usual localization data against the current mathlib
`Martingale`, `IsStoppingTime`, and `stoppedProcess` APIs.  It is a statement
interface, not a theorem that any particular stochastic process is a local
martingale.
-/
structure LocalMartingaleData
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (M : RealProcess Ω) : Type u where
  stronglyAdapted : StronglyAdapted filtration M
  localizationStoppingTime : ℕ → Ω → WithTop ℝ
  localization_isStoppingTime :
    ∀ n : ℕ, IsStoppingTime filtration (localizationStoppingTime n)
  stopped_martingale :
    ∀ n : ℕ, Martingale (stoppedProcess M (localizationStoppingTime n)) filtration μ
  localization_exhausts :
    ∀ᵐ ω ∂μ, ∀ t : ℝ, 0 ≤ t → ∃ n : ℕ, (t : WithTop ℝ) ≤ localizationStoppingTime n ω

/-- A process is locally martingale when it admits repo-local localization data. -/
def LocalMartingaleProcess
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (M : RealProcess Ω) : Prop :=
  Nonempty (LocalMartingaleData μ filtration M)

/--
Repo-local finite-variation API boundary for scalar continuous-time processes.

The finite-variation condition is pathwise on every compact time interval.
-/
structure FiniteVariationData
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (A : RealProcess Ω) : Type u where
  stronglyAdapted : StronglyAdapted filtration A
  finiteVariationOnCompacts :
    ∀ ω : Ω, ∀ a b : ℝ, BoundedVariationOn (fun t : ℝ => A t ω) (Set.uIcc a b)

/-- A process is finite variation when it admits repo-local finite-variation data. -/
def FiniteVariationProcess
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (A : RealProcess Ω) : Prop :=
  Nonempty (FiniteVariationData μ filtration A)

/--
Repo-local semimartingale decomposition boundary.

A scalar semimartingale is represented by a local-martingale part plus a
finite-variation part, with equality at each time almost everywhere.
-/
structure SemimartingaleDecomposition
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (X : RealProcess Ω) : Type u where
  localMartingalePart : RealProcess Ω
  finiteVariationPart : RealProcess Ω
  localMartingale :
    LocalMartingaleData μ filtration localMartingalePart
  finiteVariation :
    FiniteVariationData μ filtration finiteVariationPart
  decomposes :
    ∀ t : ℝ, X t =ᵐ[μ] fun ω => localMartingalePart t ω + finiteVariationPart t ω

/-- Repo-local semimartingale predicate: existence of a decomposition witness. -/
def SemimartingaleProcess
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (X : RealProcess Ω) : Prop :=
  Nonempty (SemimartingaleDecomposition μ filtration X)

/-- Projection wrapper: a local-martingale data package is adapted. -/
theorem LocalMartingaleData.stronglyAdapted_process
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {M : RealProcess Ω}
    (hM : LocalMartingaleData μ filtration M) :
    StronglyAdapted filtration M :=
  hM.stronglyAdapted

/-- Projection wrapper: a localizing time in the package is a stopping time. -/
theorem LocalMartingaleData.isStoppingTime
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {M : RealProcess Ω}
    (hM : LocalMartingaleData μ filtration M) (n : ℕ) :
    IsStoppingTime filtration (hM.localizationStoppingTime n) :=
  hM.localization_isStoppingTime n

/-- Projection wrapper: every stopped localized process is a martingale. -/
theorem LocalMartingaleData.stoppedMartingale
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {M : RealProcess Ω}
    (hM : LocalMartingaleData μ filtration M) (n : ℕ) :
    Martingale (stoppedProcess M (hM.localizationStoppingTime n)) filtration μ :=
  hM.stopped_martingale n

/-- Projection wrapper: a finite-variation data package is adapted. -/
theorem FiniteVariationData.stronglyAdapted_process
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {A : RealProcess Ω}
    (hA : FiniteVariationData μ filtration A) :
    StronglyAdapted filtration A :=
  hA.stronglyAdapted

/-- Projection wrapper: finite variation holds pathwise on each compact interval. -/
theorem FiniteVariationData.boundedVariationOn_uIcc
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {A : RealProcess Ω}
    (hA : FiniteVariationData μ filtration A) (ω : Ω) (a b : ℝ) :
    BoundedVariationOn (fun t : ℝ => A t ω) (Set.uIcc a b) :=
  hA.finiteVariationOnCompacts ω a b

/-- Projection wrapper: a semimartingale predicate is exactly decomposition existence. -/
theorem semimartingaleProcess_iff_nonempty_decomposition
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {X : RealProcess Ω} :
    SemimartingaleProcess μ filtration X ↔
      Nonempty (SemimartingaleDecomposition μ filtration X) :=
  Iff.rfl

/-- Projection wrapper: a concrete decomposition gives the semimartingale predicate. -/
theorem SemimartingaleDecomposition.semimartingaleProcess
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {X : RealProcess Ω}
    (D : SemimartingaleDecomposition μ filtration X) :
    SemimartingaleProcess μ filtration X :=
  ⟨D⟩

/--
Repo-local predictable simple-process boundary.

The process is represented by finitely many predictable step pieces
`ξ_k 1_(s_k, t_k]`.  This is the intended starting class for a future
construction of stochastic integrals against semimartingales.  The
`predictableBoundary` field is explicit because the pinned mathlib
`IsPredictable` class currently requires an `OrderBot` time index, while the
parent semimartingale boundary is indexed by `ℝ`.
-/
structure PredictableSimpleProcessData
    {Ω : Type u} [MeasurableSpace Ω]
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (H : RealProcess Ω) : Type u where
  stepCount : ℕ
  leftEndpoint : Fin stepCount → ℝ
  rightEndpoint : Fin stepCount → ℝ
  coefficient : Fin stepCount → Ω → ℝ
  endpoints_ordered : ∀ k : Fin stepCount, leftEndpoint k ≤ rightEndpoint k
  coefficientStronglyMeasurable : ∀ k : Fin stepCount, StronglyMeasurable (coefficient k)
  predictableBoundary : Prop
  predictableBoundary_holds : predictableBoundary
  stepRepresentation :
    ∀ t : ℝ, ∀ ω : Ω,
      H t ω =
        ∑ k : Fin stepCount,
          if leftEndpoint k < t ∧ t ≤ rightEndpoint k then coefficient k ω else 0

/-- A process is predictable simple when it has finite-step predictable data. -/
def PredictableSimpleProcess
    {Ω : Type u} [MeasurableSpace Ω]
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (H : RealProcess Ω) : Prop :=
  Nonempty (PredictableSimpleProcessData filtration H)

/--
Repo-local simple stochastic-integral boundary against a semimartingale.

For a simple integrand `H = Σ ξ_k 1_(s_k,t_k]`, the integral candidate is required
to satisfy the usual stopped-increment formula
`Σ ξ_k (X_{min t_k t} - X_{min s_k t})` on nonnegative times.
-/
structure SimpleStochasticIntegralData
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›)
    (X H : RealProcess Ω) : Type u where
  integrandSimple : PredictableSimpleProcessData filtration H
  integratorSemimartingale : SemimartingaleDecomposition μ filtration X
  integral : RealProcess Ω
  stronglyAdapted : StronglyAdapted filtration integral
  startsAtZero : integral 0 =ᵐ[μ] fun _ => 0
  simpleIntegralFormula :
    ∀ t : ℝ, 0 ≤ t →
      ∀ᵐ ω ∂μ,
        integral t ω =
          ∑ k : Fin integrandSimple.stepCount,
            integrandSimple.coefficient k ω *
              (X (min t (integrandSimple.rightEndpoint k)) ω -
                X (min t (integrandSimple.leftEndpoint k)) ω)

/--
Checked boundary for a stochastic-integral API against semimartingales.

This records what a future construction or imported API must provide: a domain
for predictable integrands, a semimartingale domain for integrators, and
agreement with the finite-step construction on predictable simple processes.
-/
structure SemimartingaleStochasticIntegralAPI
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›)
    (stochasticIntegral : RealProcess Ω → RealProcess Ω → RealProcess Ω) : Type u where
  predictableIntegrandDomain : RealProcess Ω → Prop
  integratorDomain : RealProcess Ω → Prop
  predictableSimple_in_domain :
    ∀ {H : RealProcess Ω}, PredictableSimpleProcess filtration H →
      predictableIntegrandDomain H
  semimartingale_in_domain :
    ∀ {X : RealProcess Ω}, SemimartingaleProcess μ filtration X →
      integratorDomain X
  integralStronglyAdapted :
    ∀ {H X : RealProcess Ω}, predictableIntegrandDomain H → integratorDomain X →
      StronglyAdapted filtration (stochasticIntegral H X)
  simpleIntegralData :
    ∀ {X H : RealProcess Ω},
      PredictableSimpleProcessData filtration H →
        SemimartingaleDecomposition μ filtration X →
          SimpleStochasticIntegralData μ filtration X H
  simpleIntegral_agrees :
    ∀ {X H : RealProcess Ω}
      (hH : PredictableSimpleProcessData filtration H)
      (hX : SemimartingaleDecomposition μ filtration X),
        (simpleIntegralData hH hX).integral = stochasticIntegral H X

/-- Projection wrapper: predictable simple data carries the predictable-process boundary. -/
theorem PredictableSimpleProcessData.predictable_boundary
    {Ω : Type u} [MeasurableSpace Ω]
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {H : RealProcess Ω}
    (hH : PredictableSimpleProcessData filtration H) :
    hH.predictableBoundary :=
  hH.predictableBoundary_holds

/-- Projection wrapper: predictable simple data has a finite step representation. -/
theorem PredictableSimpleProcessData.step_representation
    {Ω : Type u} [MeasurableSpace Ω]
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {H : RealProcess Ω}
    (hH : PredictableSimpleProcessData filtration H) (t : ℝ) (ω : Ω) :
    H t ω =
      ∑ k : Fin hH.stepCount,
        if hH.leftEndpoint k < t ∧ t ≤ hH.rightEndpoint k then
          hH.coefficient k ω
        else
          0 :=
  hH.stepRepresentation t ω

/-- Projection wrapper: a simple stochastic-integral package is adapted. -/
theorem SimpleStochasticIntegralData.stronglyAdapted_integral
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {X H : RealProcess Ω}
    (S : SimpleStochasticIntegralData μ filtration X H) :
    StronglyAdapted filtration S.integral :=
  S.stronglyAdapted

/-- Projection wrapper: the simple stochastic integral satisfies the stopped-increment formula. -/
theorem SimpleStochasticIntegralData.formula
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {X H : RealProcess Ω}
    (S : SimpleStochasticIntegralData μ filtration X H) (t : ℝ) (ht : 0 ≤ t) :
    ∀ᵐ ω ∂μ,
      S.integral t ω =
        ∑ k : Fin S.integrandSimple.stepCount,
          S.integrandSimple.coefficient k ω *
            (X (min t (S.integrandSimple.rightEndpoint k)) ω -
              X (min t (S.integrandSimple.leftEndpoint k)) ω) :=
  S.simpleIntegralFormula t ht

/-- Projection wrapper: the API accepts every predictable simple integrand. -/
theorem SemimartingaleStochasticIntegralAPI.predictableSimple_mem
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›}
    {I : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    (A : SemimartingaleStochasticIntegralAPI μ filtration I)
    {H : RealProcess Ω} (hH : PredictableSimpleProcess filtration H) :
    A.predictableIntegrandDomain H :=
  A.predictableSimple_in_domain hH

/-- Projection wrapper: the API accepts every repo-local semimartingale integrator. -/
theorem SemimartingaleStochasticIntegralAPI.semimartingale_mem
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›}
    {I : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    (A : SemimartingaleStochasticIntegralAPI μ filtration I)
    {X : RealProcess Ω} (hX : SemimartingaleProcess μ filtration X) :
    A.integratorDomain X :=
  A.semimartingale_in_domain hX

/-- Projection wrapper: the API agrees with its simple-integral construction. -/
theorem SemimartingaleStochasticIntegralAPI.simpleIntegral_eq
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›}
    {I : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    (A : SemimartingaleStochasticIntegralAPI μ filtration I)
    {X H : RealProcess Ω}
    (hH : PredictableSimpleProcessData filtration H)
    (hX : SemimartingaleDecomposition μ filtration X) :
    (A.simpleIntegralData hH hX).integral = I H X :=
  A.simpleIntegral_agrees hH hX

/--
Repo-local quadratic-variation boundary for scalar semimartingales.

The pathwise partition-limit construction is recorded as an explicit
obligation because the pinned mathlib snapshot has no canonical continuous-time
quadratic-variation API.
-/
structure QuadraticVariationData
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›)
    (X qv : RealProcess Ω) : Type u where
  integratorSemimartingale : SemimartingaleProcess μ filtration X
  finiteVariation : FiniteVariationData μ filtration qv
  startsAtZero : qv 0 =ᵐ[μ] fun _ => 0
  nonnegativeIncrements :
    ∀ ω : Ω, ∀ a b : ℝ, 0 ≤ a → a ≤ b → qv a ω ≤ qv b ω
  partitionLimitBoundary : Prop
  partitionLimitBoundary_holds : partitionLimitBoundary

/-- A process is a quadratic variation candidate when it has checked boundary data. -/
def QuadraticVariationProcess
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›)
    (X qv : RealProcess Ω) : Prop :=
  Nonempty (QuadraticVariationData μ filtration X qv)

/--
Repo-local quadratic-covariation boundary for scalar semimartingales.

The polarization/bilinearity obligations are kept as explicit boundary fields.
They are not proved here and must be replaced by a construction or imported
theorems before Ito's formula can be closed.
-/
structure QuadraticCovariationData
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›)
    (X Y cov : RealProcess Ω) : Type u where
  leftSemimartingale : SemimartingaleProcess μ filtration X
  rightSemimartingale : SemimartingaleProcess μ filtration Y
  finiteVariation : FiniteVariationData μ filtration cov
  startsAtZero : cov 0 =ᵐ[μ] fun _ => 0
  polarizationBoundary : Prop
  polarizationBoundary_holds : polarizationBoundary
  bilinearBoundary : Prop
  bilinearBoundary_holds : bilinearBoundary

/-- A process is a quadratic covariation candidate when it has checked boundary data. -/
def QuadraticCovariationProcess
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›)
    (X Y cov : RealProcess Ω) : Prop :=
  Nonempty (QuadraticCovariationData μ filtration X Y cov)

/--
Repo-local finite-variation integration boundary.

This is the Stieltjes/Lebesgue--Stieltjes style integral used for the
second-order Ito correction against quadratic covariation.  The construction
itself is deliberately left as a boundary obligation.
-/
structure FiniteVariationIntegralData
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›)
    (H A : RealProcess Ω) : Type u where
  integratorFiniteVariation : FiniteVariationData μ filtration A
  integral : RealProcess Ω
  stronglyAdapted : StronglyAdapted filtration integral
  startsAtZero : integral 0 =ᵐ[μ] fun _ => 0
  stieltjesIntegralBoundary : Prop
  stieltjesIntegralBoundary_holds : stieltjesIntegralBoundary

/--
Checked boundary for quadratic covariation and finite-variation integration
against the resulting covariation processes.
-/
structure QuadraticCovariationFiniteVariationAPI
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›)
    (quadraticCovariation : RealProcess Ω → RealProcess Ω → RealProcess Ω)
    (finiteVariationIntegral : RealProcess Ω → RealProcess Ω → RealProcess Ω) :
    Type u where
  quadraticVariationData :
    ∀ {X : RealProcess Ω}, SemimartingaleProcess μ filtration X →
      QuadraticVariationData μ filtration X (quadraticCovariation X X)
  quadraticCovariationData :
    ∀ {X Y : RealProcess Ω}, SemimartingaleProcess μ filtration X →
      SemimartingaleProcess μ filtration Y →
        QuadraticCovariationData μ filtration X Y (quadraticCovariation X Y)
  covariation_symmetric :
    ∀ {X Y : RealProcess Ω},
      SemimartingaleProcess μ filtration X →
        SemimartingaleProcess μ filtration Y →
          ∀ t : ℝ,
            quadraticCovariation X Y t =ᵐ[μ]
              fun ω => quadraticCovariation Y X t ω
  integrandDomain : RealProcess Ω → Prop
  finiteVariationIntegratorDomain : RealProcess Ω → Prop
  covariation_in_integratorDomain :
    ∀ {X Y : RealProcess Ω}, SemimartingaleProcess μ filtration X →
      SemimartingaleProcess μ filtration Y →
        finiteVariationIntegratorDomain (quadraticCovariation X Y)
  finiteVariationIntegratorData :
    ∀ {A : RealProcess Ω}, finiteVariationIntegratorDomain A →
      FiniteVariationData μ filtration A
  finiteVariationIntegralData :
    ∀ {H A : RealProcess Ω}, integrandDomain H →
      finiteVariationIntegratorDomain A →
        FiniteVariationIntegralData μ filtration H A
  finiteVariationIntegral_agrees :
    ∀ {H A : RealProcess Ω}
      (hH : integrandDomain H) (hA : finiteVariationIntegratorDomain A),
        (finiteVariationIntegralData hH hA).integral =
          finiteVariationIntegral H A

/-- Projection wrapper: quadratic-variation data is finite variation. -/
def QuadraticVariationData.finiteVariation_process
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {X qv : RealProcess Ω}
    (Q : QuadraticVariationData μ filtration X qv) :
    FiniteVariationData μ filtration qv :=
  Q.finiteVariation

/-- Projection wrapper: the partition-limit boundary obligation is present. -/
theorem QuadraticVariationData.partition_limit_boundary
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {X qv : RealProcess Ω}
    (Q : QuadraticVariationData μ filtration X qv) :
    Q.partitionLimitBoundary :=
  Q.partitionLimitBoundary_holds

/-- Projection wrapper: quadratic-covariation data is finite variation. -/
def QuadraticCovariationData.finiteVariation_process
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {X Y cov : RealProcess Ω}
    (Q : QuadraticCovariationData μ filtration X Y cov) :
    FiniteVariationData μ filtration cov :=
  Q.finiteVariation

/-- Projection wrapper: the polarization boundary obligation is present. -/
theorem QuadraticCovariationData.polarization_boundary
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {X Y cov : RealProcess Ω}
    (Q : QuadraticCovariationData μ filtration X Y cov) :
    Q.polarizationBoundary :=
  Q.polarizationBoundary_holds

/-- Projection wrapper: a finite-variation integral package is adapted. -/
theorem FiniteVariationIntegralData.stronglyAdapted_integral
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {H A : RealProcess Ω}
    (F : FiniteVariationIntegralData μ filtration H A) :
    StronglyAdapted filtration F.integral :=
  F.stronglyAdapted

/-- Projection wrapper: the Stieltjes integral construction obligation is present. -/
theorem FiniteVariationIntegralData.stieltjes_boundary
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {H A : RealProcess Ω}
    (F : FiniteVariationIntegralData μ filtration H A) :
    F.stieltjesIntegralBoundary :=
  F.stieltjesIntegralBoundary_holds

/-- Projection wrapper: the API provides quadratic covariation for semimartingales. -/
theorem QuadraticCovariationFiniteVariationAPI.covariation_process
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›}
    {Q : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    {J : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    (A : QuadraticCovariationFiniteVariationAPI μ filtration Q J)
    {X Y : RealProcess Ω}
    (hX : SemimartingaleProcess μ filtration X)
    (hY : SemimartingaleProcess μ filtration Y) :
    QuadraticCovariationProcess μ filtration X Y (Q X Y) :=
  ⟨A.quadraticCovariationData hX hY⟩

/-- Projection wrapper: covariation processes are accepted as finite-variation integrators. -/
theorem QuadraticCovariationFiniteVariationAPI.covariation_integrator_mem
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›}
    {Q : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    {J : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    (A : QuadraticCovariationFiniteVariationAPI μ filtration Q J)
    {X Y : RealProcess Ω}
    (hX : SemimartingaleProcess μ filtration X)
    (hY : SemimartingaleProcess μ filtration Y) :
    A.finiteVariationIntegratorDomain (Q X Y) :=
  A.covariation_in_integratorDomain hX hY

/-- Projection wrapper: the finite-variation integral API agrees with its data package. -/
theorem QuadraticCovariationFiniteVariationAPI.finiteVariationIntegral_eq
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›}
    {Q : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    {J : RealProcess Ω → RealProcess Ω → RealProcess Ω}
    (A : QuadraticCovariationFiniteVariationAPI μ filtration Q J)
    {H B : RealProcess Ω}
    (hH : A.integrandDomain H) (hB : A.finiteVariationIntegratorDomain B) :
    (A.finiteVariationIntegralData hH hB).integral = J H B :=
  A.finiteVariationIntegral_agrees hH hB

/--
Boundary data for a future finite-dimensional Ito-formula theorem.

The stochastic integral, finite-variation integral, quadratic covariation, and
semimartingale predicates are kept abstract.  This freezes the formula-level
interface without pretending that the local mathlib snapshot already has a
canonical stochastic-calculus object model.
-/
structure ItoFormulaData
    (Ω : Type u) (ι : Type v) [MeasurableSpace Ω] [Fintype ι] : Type (max u v) where
  probabilityMeasure : Measure Ω
  filtration : Filtration ℝ ‹MeasurableSpace Ω›
  process : VectorProcess Ω ι
  testFunction : (ι → ℝ) → ℝ
  firstPartial : ι → (ι → ℝ) → ℝ
  secondPartial : ι → ι → (ι → ℝ) → ℝ
  stochasticIntegral : RealProcess Ω → RealProcess Ω → RealProcess Ω
  stochasticIntegralAPI :
    SemimartingaleStochasticIntegralAPI probabilityMeasure filtration stochasticIntegral
  finiteVariationIntegral : RealProcess Ω → RealProcess Ω → RealProcess Ω
  quadraticCovariation : RealProcess Ω → RealProcess Ω → RealProcess Ω
  quadraticCovariationAPI :
    QuadraticCovariationFiniteVariationAPI probabilityMeasure filtration
      quadraticCovariation finiteVariationIntegral
  processSemimartingale : Prop
  coordinateSemimartingales :
    ∀ i : ι, SemimartingaleProcess probabilityMeasure filtration (componentProcess process i)
  adaptedToFiltration : StronglyAdapted filtration process
  localIntegrabilityHypotheses : Prop
  testFunctionC2 : ContDiff ℝ 2 testFunction
  firstPartialsAgree : Prop
  secondPartialsAgree : Prop
  stochasticIntegralWellDefined : Prop
  quadraticCovariationWellDefined : Prop
  finiteVariationIntegralWellDefined : Prop
  scalarProcessSemimartingaleTarget : Prop

/-- The scalar process obtained by applying the test function to `D.process`. -/
def ItoFormulaData.scalarProcess
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) : RealProcess Ω :=
  composedProcess D.testFunction D.process

/-- The coordinate process indexed by `i`. -/
def ItoFormulaData.coordinate
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) (i : ι) : RealProcess Ω :=
  componentProcess D.process i

/-- The semimartingale API boundary applies to every coordinate process. -/
theorem ItoFormulaData.coordinate_semimartingale
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) (i : ι) :
    SemimartingaleProcess D.probabilityMeasure D.filtration (D.coordinate i) := by
  simpa [ItoFormulaData.coordinate] using D.coordinateSemimartingales i

/-- The Ito-formula data carries the selected stochastic-integral API boundary. -/
def ItoFormulaData.stochasticIntegral_api
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) :
    SemimartingaleStochasticIntegralAPI
      D.probabilityMeasure D.filtration D.stochasticIntegral :=
  D.stochasticIntegralAPI

/--
The Ito-formula data carries the selected quadratic-covariation and
finite-variation integration API boundary.
-/
def ItoFormulaData.quadraticCovariation_api
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) :
    QuadraticCovariationFiniteVariationAPI D.probabilityMeasure D.filtration
      D.quadraticCovariation D.finiteVariationIntegral :=
  D.quadraticCovariationAPI

/-- The first-derivative integrand appearing in the Ito formula. -/
def ItoFormulaData.firstIntegrand
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) (i : ι) : RealProcess Ω :=
  fun t ω => D.firstPartial i (D.process t ω)

/-- The second-derivative integrand appearing in the Ito formula. -/
def ItoFormulaData.secondIntegrand
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) (i j : ι) : RealProcess Ω :=
  fun t ω => D.secondPartial i j (D.process t ω)

/-- The stochastic-integral summand in the Ito formula. -/
def ItoFormulaData.firstOrderTerm
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) [DecidableEq ι] (t : ℝ) (ω : Ω) : ℝ :=
  ∑ i : ι, D.stochasticIntegral (D.firstIntegrand i) (D.coordinate i) t ω

/-- The quadratic-covariation correction term in the Ito formula. -/
def ItoFormulaData.secondOrderTerm
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) [DecidableEq ι] (t : ℝ) (ω : Ω) : ℝ :=
  (1 / 2 : ℝ) *
    ∑ i : ι, ∑ j : ι,
      D.finiteVariationIntegral (D.secondIntegrand i j)
        (D.quadraticCovariation (D.coordinate i) (D.coordinate j)) t ω

/--
Pointwise almost-everywhere identity expected from the finite-dimensional Ito
formula on nonnegative time intervals starting at `0`.
-/
def ItoFormulaIdentity
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : ItoFormulaData Ω ι) : Prop :=
  ∀ t : ℝ, 0 ≤ t →
    ∀ᵐ ω ∂D.probabilityMeasure,
      D.testFunction (D.process t ω) =
        D.testFunction (D.process 0 ω) +
          D.firstOrderTerm t ω + D.secondOrderTerm t ω

/-- Well-formedness assumptions for the normalized Stage1 statement boundary. -/
def ItoFormulaHypotheses
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : ItoFormulaData Ω ι) : Prop :=
  D.processSemimartingale ∧
    D.localIntegrabilityHypotheses ∧
      D.firstPartialsAgree ∧
        D.secondPartialsAgree ∧
          D.stochasticIntegralWellDefined ∧
            D.quadraticCovariationWellDefined ∧
              D.finiteVariationIntegralWellDefined

/--
Terminal conclusion package for the future Ito-formula theorem.

The conclusion exposes both the scalar semimartingale closure and the
finite-dimensional chain-rule identity.  The proof of these facts is outside
the local mathlib substrate available to this Stage1 artifact.
-/
structure ItoFormulaConclusion
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : ItoFormulaData Ω ι) : Prop where
  scalarProcessSemimartingale_holds : D.scalarProcessSemimartingaleTarget
  formula_identity : ItoFormulaIdentity D

/--
Stage1 normalized statement shape for Ito's formula.

For a finite-dimensional semimartingale `X` and a `C²` scalar test function
`f`, a future formalization should prove that `f(X)` is a semimartingale and
that it satisfies the usual first-order stochastic-integral term plus the
one-half quadratic-covariation correction term.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (ι : Type v) [Fintype ι] [DecidableEq ι],
    ∀ D : ItoFormulaData Ω ι,
      ItoFormulaHypotheses D → ItoFormulaConclusion D

/-- The normalized statement unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω] (ι : Type v) [Fintype ι] [DecidableEq ι],
        ∀ D : ItoFormulaData Ω ι,
          ItoFormulaHypotheses D → ItoFormulaConclusion D :=
  Iff.rfl

/-- Projection wrapper: a conclusion package exposes the Ito identity. -/
theorem conclusion_formula_identity
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : ItoFormulaData Ω ι} (h : ItoFormulaConclusion D) :
    ItoFormulaIdentity D :=
  h.formula_identity

/-- Projection wrapper: a conclusion package exposes scalar semimartingale closure. -/
theorem conclusion_scalarProcessSemimartingale
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : ItoFormulaData Ω ι} (h : ItoFormulaConclusion D) :
    D.scalarProcessSemimartingaleTarget :=
  h.scalarProcessSemimartingale_holds

/-- Projection wrapper: the hypotheses include stochastic-integral well-formedness. -/
theorem hypotheses_stochasticIntegralWellDefined
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : ItoFormulaData Ω ι} (h : ItoFormulaHypotheses D) :
    D.stochasticIntegralWellDefined :=
  h.2.2.2.2.1

/-- Projection wrapper: data accompanying the hypotheses includes coordinate decompositions. -/
theorem hypotheses_coordinate_semimartingale
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : ItoFormulaData Ω ι} (_h : ItoFormulaHypotheses D) (i : ι) :
    SemimartingaleProcess D.probabilityMeasure D.filtration (D.coordinate i) := by
  simpa [ItoFormulaData.coordinate] using D.coordinateSemimartingales i

/-- Projection wrapper: the hypotheses include quadratic-covariation well-formedness. -/
theorem hypotheses_quadraticCovariationWellDefined
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : ItoFormulaData Ω ι} (h : ItoFormulaHypotheses D) :
    D.quadraticCovariationWellDefined :=
  h.2.2.2.2.2.1

/-- Projection wrapper: the hypotheses include finite-variation integration well-formedness. -/
theorem hypotheses_finiteVariationIntegralWellDefined
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : ItoFormulaData Ω ι} (h : ItoFormulaHypotheses D) :
    D.finiteVariationIntegralWellDefined :=
  h.2.2.2.2.2.2

/-- Projection wrapper: the data package carries the `C²` hypothesis on the test function. -/
theorem testFunction_contDiff
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    (D : ItoFormulaData Ω ι) :
    ContDiff ℝ 2 D.testFunction :=
  D.testFunctionC2

/--
Repo-local boundary for a one-dimensional Brownian-process audit.

The pinned local mathlib snapshot has Gaussian-process and independent-increment
predicates, but it does not provide a canonical Brownian-motion structure with
continuous paths, stationary normalized increments, semimartingale closure, and
quadratic variation.  Those facts are therefore packaged as explicit boundary
data for the later finite-dimensional special-case audit.
-/
structure OneDimensionalBrownianData
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (B : RealProcess Ω) : Type u where
  stronglyAdapted : StronglyAdapted filtration B
  startsAtZero : B 0 =ᵐ[μ] fun _ => 0
  gaussianProcess : IsGaussianProcess B μ
  independentIncrements : HasIndepIncrements B μ
  semimartingale : SemimartingaleProcess μ filtration B
  quadraticVariationIsTime :
    QuadraticVariationData μ filtration B (deterministicTimeProcess Ω)
  continuousPathBoundary : Prop
  continuousPathBoundary_holds : continuousPathBoundary
  standardBrownianNormalizationBoundary : Prop
  standardBrownianNormalizationBoundary_holds : standardBrownianNormalizationBoundary

/-- The first-derivative integrand in the one-dimensional Brownian Ito formula. -/
def oneDimensionalItoFirstIntegrand
    {Ω : Type u} (f' : ℝ → ℝ) (B : RealProcess Ω) : RealProcess Ω :=
  fun t ω => f' (B t ω)

/-- The second-derivative integrand in the one-dimensional Brownian Ito formula. -/
def oneDimensionalItoSecondIntegrand
    {Ω : Type u} (f'' : ℝ → ℝ) (B : RealProcess Ω) : RealProcess Ω :=
  fun t ω => f'' (B t ω)

/--
The normalized one-dimensional Brownian Ito identity target.

This is only a proposition shape.  No theorem below proves it.
-/
def OneDimensionalBrownianItoIdentity
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (B : RealProcess Ω) (f f' f'' : ℝ → ℝ)
    (stochasticIntegral finiteVariationIntegral :
      RealProcess Ω → RealProcess Ω → RealProcess Ω) : Prop :=
  ∀ t : ℝ, 0 ≤ t →
    ∀ᵐ ω ∂μ,
      f (B t ω) =
        f (B 0 ω) +
          stochasticIntegral (oneDimensionalItoFirstIntegrand f' B) B t ω +
            (1 / 2 : ℝ) *
              finiteVariationIntegral
                (oneDimensionalItoSecondIntegrand f'' B)
                (deterministicTimeProcess Ω) t ω

/--
Integration-ready audit boundary for the one-dimensional Brownian Ito special
case after stochastic-integral and quadratic-variation APIs are available.

This narrows the finite-dimensional Ito statement to a scalar Brownian process
and records the exact remaining construction obligations: derivative agreement,
domain membership for the first- and second-order integrands, and the actual
Ito identity.  It deliberately does not prove those obligations.
-/
structure OneDimensionalBrownianItoSpecialCaseData
    {Ω : Type u} [MeasurableSpace Ω] (μ : Measure Ω)
    (filtration : Filtration ℝ ‹MeasurableSpace Ω›) (B : RealProcess Ω) :
    Type u where
  testFunction : ℝ → ℝ
  firstDerivative : ℝ → ℝ
  secondDerivative : ℝ → ℝ
  stochasticIntegral : RealProcess Ω → RealProcess Ω → RealProcess Ω
  finiteVariationIntegral : RealProcess Ω → RealProcess Ω → RealProcess Ω
  quadraticCovariation : RealProcess Ω → RealProcess Ω → RealProcess Ω
  brownian : OneDimensionalBrownianData μ filtration B
  stochasticIntegralAPI :
    SemimartingaleStochasticIntegralAPI μ filtration stochasticIntegral
  quadraticCovariationAPI :
    QuadraticCovariationFiniteVariationAPI μ filtration
      quadraticCovariation finiteVariationIntegral
  testFunctionC2 : ContDiff ℝ 2 testFunction
  firstDerivativeBoundary : Prop
  firstDerivativeBoundary_holds : firstDerivativeBoundary
  secondDerivativeBoundary : Prop
  secondDerivativeBoundary_holds : secondDerivativeBoundary
  firstIntegrandInDomain :
    stochasticIntegralAPI.predictableIntegrandDomain
      (oneDimensionalItoFirstIntegrand firstDerivative B)
  secondIntegrandInDomain :
    quadraticCovariationAPI.integrandDomain
      (oneDimensionalItoSecondIntegrand secondDerivative B)
  timeProcessInFiniteVariationDomain :
    quadraticCovariationAPI.finiteVariationIntegratorDomain
      (deterministicTimeProcess Ω)
  quadraticCovariationAgreesWithTime :
    ∀ t : ℝ, quadraticCovariation B B t =ᵐ[μ]
      fun ω => deterministicTimeProcess Ω t ω
  identityBoundary : Prop
  identityBoundary_holds : identityBoundary

/-- Projection wrapper: Brownian boundary data is strongly adapted. -/
theorem OneDimensionalBrownianData.stronglyAdapted_process
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianData μ filtration B) :
    StronglyAdapted filtration B :=
  D.stronglyAdapted

/-- Projection wrapper: Brownian boundary data includes the Gaussian-process anchor. -/
theorem OneDimensionalBrownianData.gaussian_process
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianData μ filtration B) :
    IsGaussianProcess B μ :=
  D.gaussianProcess

/-- Projection wrapper: Brownian boundary data includes independent increments. -/
theorem OneDimensionalBrownianData.independent_increments
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianData μ filtration B) :
    HasIndepIncrements B μ :=
  D.independentIncrements

/-- Projection wrapper: Brownian boundary data includes semimartingale closure. -/
theorem OneDimensionalBrownianData.semimartingale_process
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianData μ filtration B) :
    SemimartingaleProcess μ filtration B :=
  D.semimartingale

/-- Projection wrapper: Brownian quadratic variation is represented by the clock. -/
def OneDimensionalBrownianData.quadraticVariation_time
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianData μ filtration B) :
    QuadraticVariationData μ filtration B (deterministicTimeProcess Ω) :=
  D.quadraticVariationIsTime

/-- Projection wrapper: the Brownian continuous-path obligation is present. -/
theorem OneDimensionalBrownianData.continuous_path_boundary
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianData μ filtration B) :
    D.continuousPathBoundary :=
  D.continuousPathBoundary_holds

/-- Projection wrapper: the first-order Brownian Ito integrand is in domain. -/
theorem OneDimensionalBrownianItoSpecialCaseData.first_integrand_mem
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianItoSpecialCaseData μ filtration B) :
    D.stochasticIntegralAPI.predictableIntegrandDomain
      (oneDimensionalItoFirstIntegrand D.firstDerivative B) :=
  D.firstIntegrandInDomain

/-- Projection wrapper: the second-order Brownian Ito integrand is in domain. -/
theorem OneDimensionalBrownianItoSpecialCaseData.second_integrand_mem
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianItoSpecialCaseData μ filtration B) :
    D.quadraticCovariationAPI.integrandDomain
      (oneDimensionalItoSecondIntegrand D.secondDerivative B) :=
  D.secondIntegrandInDomain

/-- Projection wrapper: the Brownian Ito audit carries its identity obligation. -/
theorem OneDimensionalBrownianItoSpecialCaseData.identity_boundary
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {filtration : Filtration ℝ ‹MeasurableSpace Ω›} {B : RealProcess Ω}
    (D : OneDimensionalBrownianItoSpecialCaseData μ filtration B) :
    D.identityBoundary :=
  D.identityBoundary_holds

section MathlibProcessAnchors

variable {Ω : Type u} {mΩ : MeasurableSpace Ω}

/-- Checked mathlib wrapper: the natural filtration makes a strongly measurable process adapted. -/
theorem natural_filtration_stronglyAdapted_real
    (u : ℝ → Ω → ℝ) (hum : ∀ t : ℝ, StronglyMeasurable (u t)) :
    StronglyAdapted (Filtration.natural u hum) u :=
  Filtration.stronglyAdapted_natural hum

/-- Checked mathlib wrapper: strong adaptedness exposes coordinate strong measurability. -/
theorem stronglyAdapted_stronglyMeasurable_real
    {𝓕 : Filtration ℝ mΩ} {u : ℝ → Ω → ℝ}
    (hu : StronglyAdapted 𝓕 u) (t : ℝ) :
    StronglyMeasurable (u t) :=
  hu.stronglyMeasurable

/-- Checked mathlib wrapper: a martingale has integrable time slices. -/
theorem martingale_integrable_time
    {𝓕 : Filtration ℝ mΩ} {P : Measure Ω} {M : ℝ → Ω → ℝ}
    (hM : Martingale M 𝓕 P) (t : ℝ) :
    Integrable (M t) P :=
  hM.integrable t

/-- Checked mathlib wrapper: a predictable discrete process is strongly adapted. -/
theorem predictable_stronglyAdapted_nat
    {𝓕 : Filtration ℕ mΩ} {u : ℕ → Ω → ℝ}
    (hu : IsPredictable 𝓕 u) :
    StronglyAdapted 𝓕 u :=
  hu.adapted

/-- Checked mathlib wrapper: a stopped discrete strongly adapted process remains strongly adapted. -/
theorem stronglyAdapted_stoppedProcess_nat
    {𝓕 : Filtration ℕ mΩ} {u : ℕ → Ω → ℝ} {τ : Ω → WithTop ℕ}
    (hu : StronglyAdapted 𝓕 u) (hτ : IsStoppingTime 𝓕 τ) :
    StronglyAdapted 𝓕 (stoppedProcess u τ) :=
  hu.stoppedProcess_of_discrete hτ

/-- Checked mathlib wrapper: the independent-increments predicate is a well-typed process API. -/
def HasIndepIncrementsShape (X : ℝ → Ω → ℝ) (P : Measure Ω) : Prop :=
  HasIndepIncrements X P

/-- Checked mathlib wrapper: the Gaussian-process predicate is a well-typed process API. -/
def IsGaussianProcessShape (X : ℝ → Ω → ℝ) (P : Measure Ω) : Prop :=
  IsGaussianProcess X P

end MathlibProcessAnchors

/-- Pinned mathlib revision used for this Stage1 anchor audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Predictable",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Process.Basic",
  "Mathlib.Probability.Independence.Process.HasIndepIncrements",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
  "Mathlib.Probability.HasLaw",
  "Mathlib.MeasureTheory.Function.L1Space.Integrable"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.Filtration.natural",
  "MeasureTheory.Filtration.stronglyAdapted_natural",
  "MeasureTheory.Adapted",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.StronglyAdapted.stronglyMeasurable",
  "MeasureTheory.IsPredictable",
  "MeasureTheory.IsPredictable.adapted",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.stoppedProcess",
  "MeasureTheory.StronglyAdapted.stoppedProcess_of_discrete",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "ProbabilityTheory.HasIndepIncrements",
  "ProbabilityTheory.IsGaussianProcess",
  "ContDiff"
]

/-- Exact public child-task anchor list for `S1-M-225`. -/
def requestedMathlibAuditAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.IsPredictable",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.stoppedProcess",
  "MeasureTheory.Martingale",
  "ProbabilityTheory.HasIndepIncrements",
  "ProbabilityTheory.IsGaussianProcess"
]

/-- One row in the integration-ready public mathlib anchor table. -/
structure MathlibAnchorTableRow where
  requestedAnchor : String
  checkedName : String
  moduleName : String
  sourceLocation : String
  repoLocalEvidence : String

/--
Integration-ready public mathlib anchor table for the Ito-formula Stage1 slot.

The table is metadata: it records checked mathlib substrate anchors at the
pinned revision and does not claim a completed Ito-formula proof.
-/
def publicMathlibAnchorTable : List MathlibAnchorTableRow := [
  {
    requestedAnchor := "Filtration",
    checkedName := "MeasureTheory.Filtration",
    moduleName := "Mathlib.Probability.Process.Filtration",
    sourceLocation := "Mathlib/Probability/Process/Filtration.lean:50",
    repoLocalEvidence := "#check MeasureTheory.Filtration"
  },
  {
    requestedAnchor := "StronglyAdapted",
    checkedName := "MeasureTheory.StronglyAdapted",
    moduleName := "Mathlib.Probability.Process.Adapted",
    sourceLocation := "Mathlib/Probability/Process/Adapted.lean:103",
    repoLocalEvidence := "stronglyAdapted_stronglyMeasurable_real"
  },
  {
    requestedAnchor := "IsPredictable",
    checkedName := "MeasureTheory.IsPredictable",
    moduleName := "Mathlib.Probability.Process.Predictable",
    sourceLocation := "Mathlib/Probability/Process/Predictable.lean:63",
    repoLocalEvidence := "predictable_stronglyAdapted_nat"
  },
  {
    requestedAnchor := "IsStoppingTime",
    checkedName := "MeasureTheory.IsStoppingTime",
    moduleName := "Mathlib.Probability.Process.Stopping",
    sourceLocation := "Mathlib/Probability/Process/Stopping.lean:75",
    repoLocalEvidence := "#check MeasureTheory.IsStoppingTime"
  },
  {
    requestedAnchor := "stoppedProcess",
    checkedName := "MeasureTheory.stoppedProcess",
    moduleName := "Mathlib.Probability.Process.Stopping",
    sourceLocation := "Mathlib/Probability/Process/Stopping.lean:801",
    repoLocalEvidence := "stronglyAdapted_stoppedProcess_nat"
  },
  {
    requestedAnchor := "Martingale",
    checkedName := "MeasureTheory.Martingale",
    moduleName := "Mathlib.Probability.Martingale.Basic",
    sourceLocation := "Mathlib/Probability/Martingale/Basic.lean:53",
    repoLocalEvidence := "martingale_integrable_time"
  },
  {
    requestedAnchor := "HasIndepIncrements",
    checkedName := "ProbabilityTheory.HasIndepIncrements",
    moduleName := "Mathlib.Probability.Independence.Process.HasIndepIncrements",
    sourceLocation := "Mathlib/Probability/Independence/Process/HasIndepIncrements.lean:57",
    repoLocalEvidence := "HasIndepIncrementsShape"
  },
  {
    requestedAnchor := "IsGaussianProcess",
    checkedName := "ProbabilityTheory.IsGaussianProcess",
    moduleName := "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
    sourceLocation := "Mathlib/Probability/Distributions/Gaussian/IsGaussianProcess/Def.lean:30",
    repoLocalEvidence := "IsGaussianProcessShape"
  }
]

/--
Search terms that did not locate a terminal Ito-formula theorem in the pinned
local mathlib snapshot.
-/
def absentTerminalSearchTerms : List String := [
  "Ito",
  "Itô",
  "ItoFormula",
  "Itô formula",
  "stochastic integral",
  "StochasticIntegral",
  "semimartingale",
  "Semimartingale",
  "quadratic covariation",
  "quadratic variation",
  "Brownian",
  "continuous semimartingale",
  "Càdlàg",
  "Cadlag"
]

/--
External Lean 4 stochastic-calculus projects found during the Stage1 anchor
audit.  These are not imported by this repository, so they are blockers/candidate
dependencies rather than completion evidence for this slot.
-/
def externalAnchorCandidates : List String := [
  "RemyDegenne/brownian-motion: BrownianMotion Lean project; README says stochastic integrals and Ito's lemma are in progress.",
  "RemyDegenne/brownian-motion blueprint: section 13.5 lists integration by parts and Ito's formula targets for continuous semimartingales."
]

/--
Concrete integration blockers for any future attempt to close this theorem via
an external Lean dependency.
-/
def externalAnchorIntegrationBlockers : List String := [
  "No external Ito-formula theorem from BrownianMotion is pinned in this Lake workspace.",
  "No repo-local import path or wrapper theorem has been validated against BrownianMotion.",
  "The candidate upstream project describes the Ito-lemma work as in progress, so it is not completion evidence."
]

/-!
## Child C007 external Brownian-motion tracking

This metadata records the public Stage1 requirement to track
`RemyDegenne/brownian-motion` at tag `v4.30.0-rc1` or newer as a relevant
primary-source Lean project, while preventing anchor-only evidence from being
counted as terminal closure for Ito's formula.
-/

/-- External project tracked by child `S1-M-225-C007`. -/
def brownianMotionTrackedRepository : String :=
  "https://github.com/RemyDegenne/brownian-motion"

/-- Minimum audited upstream tag required by the public child task. -/
def brownianMotionTrackedMinimumTag : String :=
  "v4.30.0-rc1"

/-- Primary-source tag URL used for the child `S1-M-225-C007` audit. -/
def brownianMotionTrackedTagReadmeUrl : String :=
  "https://raw.githubusercontent.com/RemyDegenne/brownian-motion/v4.30.0-rc1/README.md"

/--
Repo-local evidence for the tracked external tag.

This is anchor metadata only.  It records the external project as relevant
stochastic-calculus infrastructure, not as a checked dependency in this Lake
workspace.
-/
def brownianMotionTrackedTagEvidence : List String := [
  "Repository: RemyDegenne/brownian-motion",
  "Tracked minimum tag: v4.30.0-rc1",
  "Primary-source README URL: https://raw.githubusercontent.com/RemyDegenne/brownian-motion/v4.30.0-rc1/README.md",
  "README status recorded by the parent audit: Brownian motion is complete, while stochastic integrals and Ito's lemma are still being developed.",
  "Relevant adjacent project scope: Brownian motion, stochastic-integral scaffolding, local martingales, and quadratic-variation scaffolding."
]

/--
Concrete blockers that prevent `brownian-motion@v4.30.0-rc1` anchor evidence
from being counted as terminal Ito-formula closure in this repository.
-/
def brownianMotionTrackedTagIntegrationBlockers : List String := [
  "Ito's lemma is not recorded as present in the audited upstream README evidence; it is described as still being developed.",
  "No Lean theorem named as a terminal Ito-formula/Ito-lemma closure has been imported into this repository from the external project.",
  "No Lake dependency pin or vendored proof body for brownian-motion is present in this repository's validation closure.",
  "No repo-local wrapper theorem around a brownian-motion Ito formula has been checked by `lake env lean`.",
  "Therefore the tracked external project remains `external_upstream_anchor_only` for this parent theorem."
]

/-- Child C007 external anchor status: relevant, but not terminal closure. -/
def brownianMotionTrackedTagIsTerminalItoProof : Bool :=
  false

/-- Checked guard against treating the C007 tracked tag as terminal closure. -/
theorem brownianMotionTrackedTagIsTerminalItoProof_eq_false :
    brownianMotionTrackedTagIsTerminalItoProof = false :=
  rfl

/-- Child C008 resolved Git tag object for `RemyDegenne/brownian-motion@v4.30.0-rc1`. -/
def brownianMotionAuditedTagObject : String :=
  "74d80593f8721bd15d7935653f0ebe2e73dd49c2"

/-- Child C008 resolved peeled commit for `RemyDegenne/brownian-motion@v4.30.0-rc1`. -/
def brownianMotionAuditedTagPeeledCommit : String :=
  "35122bd024c5ba8ac52945097f514647880c923c"

/-- Child C008 network command used to resolve the audited external tag. -/
def brownianMotionAuditedTagResolutionCommand : String :=
  "git ls-remote --tags https://github.com/RemyDegenne/brownian-motion.git 'refs/tags/v4.30.0-rc1*'"

/-- Child C008 resolved tag evidence for serial public audit backfill. -/
def brownianMotionAuditedTagResolutionEvidence : List String := [
  "refs/tags/v4.30.0-rc1 = tag object 74d80593f8721bd15d7935653f0ebe2e73dd49c2",
  "refs/tags/v4.30.0-rc1^{} = peeled commit 35122bd024c5ba8ac52945097f514647880c923c",
  "Network resolution succeeded on 2026-05-01 from the Stage1 child workspace.",
  "This is external-anchor metadata only; the external project is not pinned/imported into this Lake validation closure."
]

/-- Child C008 status: resolving the external tag SHA is not terminal Ito closure. -/
def brownianMotionAuditedTagResolutionIsTerminalItoProof : Bool :=
  false

/-- Checked guard against treating the C008 tag-SHA resolution as terminal closure. -/
theorem brownianMotionAuditedTagResolutionIsTerminalItoProof_eq_false :
    brownianMotionAuditedTagResolutionIsTerminalItoProof = false :=
  rfl

/-- Child C003 decision: define a repo-local semimartingale decomposition boundary now. -/
def semimartingaleApiDecision : String :=
  "Define repo-local LocalMartingaleData, FiniteVariationData, and SemimartingaleDecomposition boundaries; do not claim a terminal Ito-formula proof."

/-- The C003 semimartingale API boundary is not itself a proof of Ito's formula. -/
def semimartingaleApiIsTerminalItoProof : Bool :=
  false

/-- Checked guard against treating the semimartingale API boundary as terminal closure. -/
theorem semimartingaleApiIsTerminalItoProof_eq_false :
    semimartingaleApiIsTerminalItoProof = false :=
  rfl

/--
Child C004 decision: expose a repo-local stochastic-integral API boundary from
predictable finite-step integrands to semimartingale integrators.
-/
def stochasticIntegralApiDecision : String :=
  "Define repo-local PredictableSimpleProcessData, SimpleStochasticIntegralData, and SemimartingaleStochasticIntegralAPI boundaries; keep real-time predictability as an explicit construction obligation."

/--
Concrete blockers left before the stochastic-integral boundary can become a
terminal construction.
-/
def stochasticIntegralApiIntegrationBlockers : List String := [
  "Pinned mathlib `MeasureTheory.IsPredictable` requires an `OrderBot` time index, so it does not directly instantiate the existing `ℝ`-indexed semimartingale boundary.",
  "No repo-local construction proves the predictable simple-process boundary from mathlib measurable/predictable primitives for continuous time.",
  "No extension theorem constructs stochastic integrals for general predictable integrands from the simple-process formula.",
  "No local uniqueness, localization, isometry, convergence, or semimartingale-integral calculus theorem has been proved."
]

/-- The C004 stochastic-integral API boundary is not itself a proof of Ito's formula. -/
def stochasticIntegralApiIsTerminalItoProof : Bool :=
  false

/-- Checked guard against treating the stochastic-integral API boundary as terminal closure. -/
theorem stochasticIntegralApiIsTerminalItoProof_eq_false :
    stochasticIntegralApiIsTerminalItoProof = false :=
  rfl

/--
Child C005 decision: expose a repo-local quadratic-covariation API boundary
and a finite-variation integration boundary for Ito's second-order term.
-/
def quadraticCovariationApiDecision : String :=
  "Define repo-local QuadraticVariationData, QuadraticCovariationData, FiniteVariationIntegralData, and QuadraticCovariationFiniteVariationAPI boundaries; keep partition-limit, polarization, bilinearity, and Stieltjes-construction obligations explicit."

/--
Concrete blockers left before the quadratic-covariation boundary can become a
terminal Ito-formula ingredient.
-/
def quadraticCovariationApiIntegrationBlockers : List String := [
  "Pinned mathlib has no canonical continuous-time quadratic variation or covariation API for semimartingales.",
  "No repo-local theorem constructs quadratic variation as a partition limit for semimartingales.",
  "No repo-local theorem proves quadratic covariation by polarization, symmetry, or bilinearity for the selected semimartingale boundary.",
  "No repo-local Stieltjes/Lebesgue--Stieltjes construction proves finite-variation integration against covariation processes.",
  "The Ito second-order term still depends on explicit well-formedness hypotheses rather than constructed integral and covariation theorems."
]

/-- The C005 quadratic-covariation API boundary is not itself a proof of Ito's formula. -/
def quadraticCovariationApiIsTerminalItoProof : Bool :=
  false

/-- Checked guard against treating the C005 API boundary as terminal closure. -/
theorem quadraticCovariationApiIsTerminalItoProof_eq_false :
    quadraticCovariationApiIsTerminalItoProof = false :=
  rfl

/--
Child C006 decision: expose a one-dimensional Brownian/Ito special-case audit
boundary after the stochastic-integral and quadratic-covariation APIs exist.
-/
def oneDimensionalBrownianItoSpecialCaseAuditDecision : String :=
  "Define repo-local OneDimensionalBrownianData and OneDimensionalBrownianItoSpecialCaseData boundaries; keep Brownian path/normalization, integrand-domain, quadratic-variation clock, and identity obligations explicit."

/--
Concrete blockers left before the one-dimensional Brownian/Ito audit can become
a terminal special-case theorem.
-/
def oneDimensionalBrownianItoSpecialCaseIntegrationBlockers : List String := [
  "Pinned mathlib has Gaussian-process and independent-increment predicates, but no canonical continuous-time standard Brownian-motion structure with continuous paths and normalized stationary increments.",
  "No repo-local construction proves that the audited Brownian process is a semimartingale in the selected decomposition boundary.",
  "No repo-local theorem proves Brownian quadratic variation equals the deterministic clock process.",
  "No repo-local proof places the derivative-composed integrands in the stochastic-integral and finite-variation-integral domains.",
  "No repo-local theorem proves the one-dimensional Brownian Ito identity from the API boundaries."
]

/-- The C006 one-dimensional Brownian audit is not itself a proof of Ito's formula. -/
def oneDimensionalBrownianItoSpecialCaseIsTerminalItoProof : Bool :=
  false

/-- Checked guard against treating the C006 audit boundary as terminal closure. -/
theorem oneDimensionalBrownianItoSpecialCaseIsTerminalItoProof_eq_false :
    oneDimensionalBrownianItoSpecialCaseIsTerminalItoProof = false :=
  rfl

#check StatementShape
#check ItoFormulaData
#check ItoFormulaIdentity
#check ItoFormulaConclusion
#check deterministicTimeProcess
#check LocalMartingaleData
#check LocalMartingaleProcess
#check FiniteVariationData
#check FiniteVariationProcess
#check SemimartingaleDecomposition
#check SemimartingaleProcess
#check LocalMartingaleData.stoppedMartingale
#check FiniteVariationData.boundedVariationOn_uIcc
#check semimartingaleProcess_iff_nonempty_decomposition
#check SemimartingaleDecomposition.semimartingaleProcess
#check ItoFormulaData.coordinate_semimartingale
#check PredictableSimpleProcessData
#check PredictableSimpleProcess
#check SimpleStochasticIntegralData
#check SemimartingaleStochasticIntegralAPI
#check PredictableSimpleProcessData.predictable_boundary
#check PredictableSimpleProcessData.step_representation
#check SimpleStochasticIntegralData.stronglyAdapted_integral
#check SimpleStochasticIntegralData.formula
#check SemimartingaleStochasticIntegralAPI.predictableSimple_mem
#check SemimartingaleStochasticIntegralAPI.semimartingale_mem
#check SemimartingaleStochasticIntegralAPI.simpleIntegral_eq
#check ItoFormulaData.stochasticIntegral_api
#check QuadraticVariationData
#check QuadraticVariationProcess
#check QuadraticCovariationData
#check QuadraticCovariationProcess
#check FiniteVariationIntegralData
#check QuadraticCovariationFiniteVariationAPI
#check QuadraticVariationData.finiteVariation_process
#check QuadraticVariationData.partition_limit_boundary
#check QuadraticCovariationData.finiteVariation_process
#check QuadraticCovariationData.polarization_boundary
#check FiniteVariationIntegralData.stronglyAdapted_integral
#check FiniteVariationIntegralData.stieltjes_boundary
#check QuadraticCovariationFiniteVariationAPI.covariation_process
#check QuadraticCovariationFiniteVariationAPI.covariation_integrator_mem
#check QuadraticCovariationFiniteVariationAPI.finiteVariationIntegral_eq
#check ItoFormulaData.quadraticCovariation_api
#check hypotheses_finiteVariationIntegralWellDefined
#check OneDimensionalBrownianData
#check oneDimensionalItoFirstIntegrand
#check oneDimensionalItoSecondIntegrand
#check OneDimensionalBrownianItoIdentity
#check OneDimensionalBrownianItoSpecialCaseData
#check OneDimensionalBrownianData.stronglyAdapted_process
#check OneDimensionalBrownianData.gaussian_process
#check OneDimensionalBrownianData.independent_increments
#check OneDimensionalBrownianData.semimartingale_process
#check OneDimensionalBrownianData.quadraticVariation_time
#check OneDimensionalBrownianData.continuous_path_boundary
#check OneDimensionalBrownianItoSpecialCaseData.first_integrand_mem
#check OneDimensionalBrownianItoSpecialCaseData.second_integrand_mem
#check OneDimensionalBrownianItoSpecialCaseData.identity_boundary
#check natural_filtration_stronglyAdapted_real
#check stronglyAdapted_stronglyMeasurable_real
#check martingale_integrable_time
#check predictable_stronglyAdapted_nat
#check stronglyAdapted_stoppedProcess_nat
#check ProbabilityTheory.HasIndepIncrements
#check ProbabilityTheory.IsGaussianProcess
#check MeasureTheory.Filtration
#check MeasureTheory.StronglyAdapted
#check MeasureTheory.Martingale
#check MeasureTheory.IsPredictable
#check MeasureTheory.IsStoppingTime
#check MeasureTheory.stoppedProcess
#check mathlibPinnedRevision
#check requestedMathlibAuditAnchorNames
#check publicMathlibAnchorTable
#check externalAnchorCandidates
#check externalAnchorIntegrationBlockers
#check brownianMotionTrackedRepository
#check brownianMotionTrackedMinimumTag
#check brownianMotionTrackedTagReadmeUrl
#check brownianMotionTrackedTagEvidence
#check brownianMotionTrackedTagIntegrationBlockers
#check brownianMotionTrackedTagIsTerminalItoProof_eq_false
#check brownianMotionAuditedTagObject
#check brownianMotionAuditedTagPeeledCommit
#check brownianMotionAuditedTagResolutionCommand
#check brownianMotionAuditedTagResolutionEvidence
#check brownianMotionAuditedTagResolutionIsTerminalItoProof_eq_false
#check semimartingaleApiDecision
#check semimartingaleApiIsTerminalItoProof_eq_false
#check stochasticIntegralApiDecision
#check stochasticIntegralApiIntegrationBlockers
#check stochasticIntegralApiIsTerminalItoProof_eq_false
#check quadraticCovariationApiDecision
#check quadraticCovariationApiIntegrationBlockers
#check quadraticCovariationApiIsTerminalItoProof_eq_false
#check oneDimensionalBrownianItoSpecialCaseAuditDecision
#check oneDimensionalBrownianItoSpecialCaseIntegrationBlockers
#check oneDimensionalBrownianItoSpecialCaseIsTerminalItoProof_eq_false

end S1_M_225
end Stage1
end AwesomeTheorems
