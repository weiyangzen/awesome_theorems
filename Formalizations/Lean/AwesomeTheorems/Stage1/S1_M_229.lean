import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Independence
import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.HasLaw
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Process.Stopping
import Mathlib.Topology.Basic
import Mathlib.Topology.MetricSpace.Lipschitz

/-!
# S1-M-229 / THM-M-1036: Existence and uniqueness for stochastic differential equations

This Stage1 artifact records a conservative Lean 4 boundary for the theorem
summarized as existence and uniqueness of solutions to stochastic differential
equations.

The pinned mathlib snapshot has probability laws, Gaussian processes,
filtrations, adapted and progressively measurable processes, stopping times,
martingales, and integration infrastructure.  It does not expose a terminal
stochastic integral, Brownian-motion, Ito-process, or SDE
existence-and-uniqueness theorem.  The main result is therefore represented as
an explicit statement shape.  The checked declarations below are only
repo-local wrappers around available substrate or projections from local
statement packages.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

open scoped ENNReal NNReal MeasureTheory ProbabilityTheory Topology

namespace AwesomeTheorems.Stage1.S1_M_229

universe uΩ

/-- Continuous time index for the normalized one-dimensional Stage1 SDE boundary. -/
abbrev Time : Type :=
  ℝ

/-- One-dimensional state space used by this Stage1 boundary artifact. -/
abbrev State : Type :=
  ℝ

/-- A real-valued stochastic process indexed by continuous time. -/
abbrev StochasticProcess (Ω : Type uΩ) : Type uΩ :=
  Time → Ω → State

/-- A deterministic scalar drift or diffusion coefficient `c(t, x)`. -/
abbrev SdeCoefficient : Type :=
  Time → State → State

/--
Coefficient-side hypotheses for a future one-dimensional strong SDE theorem.

The fields use concrete mathlib metric predicates for state-variable
regularity.  They do not claim the classical SDE theorem; they only package the
deterministic coefficient assumptions that such a theorem would consume.
-/
structure SdeCoefficientData : Type where
  drift : SdeCoefficient
  diffusion : SdeCoefficient
  driftMeasurable : Measurable fun z : Time × State => drift z.1 z.2
  diffusionMeasurable : Measurable fun z : Time × State => diffusion z.1 z.2
  driftGlobalLipschitzConstant : ℝ≥0
  diffusionGlobalLipschitzConstant : ℝ≥0
  driftGlobalLipschitz :
    ∀ t : Time, LipschitzWith driftGlobalLipschitzConstant fun x : State => drift t x
  diffusionGlobalLipschitz :
    ∀ t : Time, LipschitzWith diffusionGlobalLipschitzConstant fun x : State => diffusion t x
  driftLocalLipschitz : ∀ t : Time, LocallyLipschitz fun x : State => drift t x
  diffusionLocalLipschitz : ∀ t : Time, LocallyLipschitz fun x : State => diffusion t x
  linearGrowthConstant : ℝ≥0
  driftLinearGrowth :
    ∀ t : Time, ∀ x : State, ‖drift t x‖ ≤ (linearGrowthConstant : ℝ) * (1 + ‖x‖)
  diffusionLinearGrowth :
    ∀ t : Time, ∀ x : State, ‖diffusion t x‖ ≤ (linearGrowthConstant : ℝ) * (1 + ‖x‖)

/--
Concrete Brownian-motion boundary over currently selected mathlib APIs.

Mathlib does not yet provide a canonical Brownian-motion object in this local
closure, so this structure records the standard one-dimensional Brownian
properties directly in terms of checked probability-process APIs.
-/
structure BrownianMotionData (Ω : Type uΩ) [MeasurableSpace Ω]
    (P : Measure Ω) : Type (max uΩ 1) where
  process : StochasticProcess Ω
  filtration : Filtration Time (inferInstance : MeasurableSpace Ω)
  gaussian : IsGaussianProcess process P
  adapted : Adapted filtration process
  stronglyAdapted : StronglyAdapted filtration process
  progressivelyMeasurable : ProgMeasurable filtration process
  continuousPaths : ∀ ω : Ω, Continuous fun t : Time => process t ω
  startsAtZero : process 0 =ᵐ[P] fun _ : Ω => (0 : State)
  independentIncrements :
    ∀ ⦃s t u v : Time⦄,
      0 ≤ s → s ≤ t → t ≤ u → u ≤ v →
        IndepFun (fun ω : Ω => process t ω - process s ω)
          (fun ω : Ω => process v ω - process u ω) P
  covariance :
    ∀ s t : Time,
      0 ≤ s → 0 ≤ t →
        (∫ ω, process s ω * process t ω ∂P) = min s t

/-- First-moment integrability for every time slice of a process. -/
def SdeFirstMomentEstimate {Ω : Type uΩ} [MeasurableSpace Ω]
    (P : Measure Ω) (X : StochasticProcess Ω) : Prop :=
  ∀ t : Time, Integrable (X t) P

/-- Second-moment integrability for every time slice of a process. -/
def SdeSecondMomentEstimate {Ω : Type uΩ} [MeasurableSpace Ω]
    (P : Measure Ω) (X : StochasticProcess Ω) : Prop :=
  ∀ t : Time, Integrable (fun ω : Ω => (X t ω) ^ 2) P

/--
Local Ito/time-integral API boundary needed by the SDE statement.

The fields name the deterministic time integral and stochastic Ito integral
used in the equation
`X_t = X_0 + ∫ b(s, X_s) ds + ∫ σ(s, X_s) dW_s`.  The adaptedness and moment
fields are obligations supplied by a future mathlib API or pinned external
dependency; this structure is not a construction theorem for stochastic
integrals.
-/
structure SdeIntegralAPI (Ω : Type uΩ) [MeasurableSpace Ω]
    (P : Measure Ω) (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω))
    (W : StochasticProcess Ω) : Type (max uΩ 1) where
  timeIntegral : StochasticProcess Ω → StochasticProcess Ω
  itoIntegral : StochasticProcess Ω → StochasticProcess Ω → StochasticProcess Ω
  timeIntegral_adapted :
    ∀ {H : StochasticProcess Ω}, Adapted ℱ H → Adapted ℱ (timeIntegral H)
  itoIntegral_adapted :
    ∀ {H M : StochasticProcess Ω},
      Adapted ℱ H → Adapted ℱ M → Adapted ℱ (itoIntegral H M)
  timeIntegral_firstMoment :
    ∀ {H : StochasticProcess Ω},
      SdeFirstMomentEstimate P H → SdeFirstMomentEstimate P (timeIntegral H)
  itoIntegral_firstMoment :
    ∀ {H M : StochasticProcess Ω},
      SdeFirstMomentEstimate P H → SdeFirstMomentEstimate P M →
        SdeFirstMomentEstimate P (itoIntegral H M)
  timeIntegral_secondMoment :
    ∀ {H : StochasticProcess Ω},
      SdeSecondMomentEstimate P H → SdeSecondMomentEstimate P (timeIntegral H)
  itoIntegral_secondMoment :
    ∀ {H M : StochasticProcess Ω},
      SdeSecondMomentEstimate P H → SdeSecondMomentEstimate P M →
        SdeSecondMomentEstimate P (itoIntegral H M)
  drivingIntegrator : W = W

/--
Problem data for a future strong SDE existence-and-uniqueness theorem.

The Brownian package records the available mathlib interfaces for Gaussian
processes, filtrations, adapted/progressive measurability, independent
increments, path continuity, and covariance.  Initial-data hypotheses are also
stated against the selected filtration and independence API.
-/
structure SdeProblemData (Ω : Type uΩ) [MeasurableSpace Ω]
    (P : Measure Ω) : Type (max uΩ 1) where
  initial : Ω → State
  initialLaw : Measure State
  initialHasLaw : HasLaw initial initialLaw P
  brownian : BrownianMotionData Ω P
  integralApi : SdeIntegralAPI Ω P brownian.filtration brownian.process
  coefficients : SdeCoefficientData
  initialMeasurableAtZero : Measurable[brownian.filtration 0] initial
  initialIndependentOfDrivingNoise :
    ∀ t : Time, IndepFun initial (brownian.process t) P

/-- The driving process selected in `SdeProblemData`. -/
def SdeProblemData.drivingNoise {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) : StochasticProcess Ω :=
  D.brownian.process

/-- The filtration selected in `SdeProblemData`. -/
def SdeProblemData.filtration {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) : Filtration Time (inferInstance : MeasurableSpace Ω) :=
  D.brownian.filtration

/-- Deterministic time integral selected by the SDE problem data. -/
def SdeProblemData.timeIntegral {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) : StochasticProcess Ω → StochasticProcess Ω :=
  D.integralApi.timeIntegral

/-- Ito integral selected by the SDE problem data. -/
def SdeProblemData.itoIntegral {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) :
    StochasticProcess Ω → StochasticProcess Ω → StochasticProcess Ω :=
  D.integralApi.itoIntegral

/-- Drift coefficient evaluated along a candidate solution path. -/
def SdeProblemData.driftIntegrand {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) (X : StochasticProcess Ω) : StochasticProcess Ω :=
  fun t ω => D.coefficients.drift t (X t ω)

/-- Diffusion coefficient evaluated along a candidate solution path. -/
def SdeProblemData.diffusionIntegrand {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) (X : StochasticProcess Ω) :
    StochasticProcess Ω :=
  fun t ω => D.coefficients.diffusion t (X t ω)

/-- The drift term `∫ b(s, X_s) ds` selected by the local integral API. -/
def SdeProblemData.driftIntegralTerm {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) (X : StochasticProcess Ω) :
    StochasticProcess Ω :=
  D.timeIntegral (D.driftIntegrand X)

/-- The diffusion term `∫ σ(s, X_s) dW_s` selected by the local Ito API. -/
def SdeProblemData.diffusionIntegralTerm {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) (X : StochasticProcess Ω) :
    StochasticProcess Ω :=
  D.itoIntegral (D.diffusionIntegrand X) D.drivingNoise

/-- One Picard update for the selected SDE boundary. -/
def SdeProblemData.picardStep {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) (X : StochasticProcess Ω) :
    StochasticProcess Ω :=
  fun t ω => D.initial ω + D.driftIntegralTerm X t ω +
    D.diffusionIntegralTerm X t ω

/--
Picard iteration package for the existence branch.

This is not a construction of the iterates.  It records the independently
checkable obligations that a future Picard proof must close after the Brownian
and Ito-integral APIs are available.
-/
structure PicardIterationData {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) : Type (max uΩ 1) where
  seed : StochasticProcess Ω
  iterate : ℕ → StochasticProcess Ω
  zero_eq_seed : iterate 0 = seed
  seedAdapted : Adapted D.filtration seed
  seedFirstMoment : SdeFirstMomentEstimate P seed
  seedSecondMoment : SdeSecondMomentEstimate P seed
  stepEquation :
    ∀ n : ℕ, ∀ t : Time,
      iterate (n + 1) t =ᵐ[P] D.picardStep (iterate n) t
  iterateAdapted : ∀ n : ℕ, Adapted D.filtration (iterate n)
  iterateFirstMoment : ∀ n : ℕ, SdeFirstMomentEstimate P (iterate n)
  iterateSecondMoment : ∀ n : ℕ, SdeSecondMomentEstimate P (iterate n)

/--
Contraction-estimate package for the Picard existence branch.

The `distance` field is deliberately local to the package because the final
process-space norm depends on the stochastic-integral API selected later
(typically a stopped/supremum L² norm on a finite horizon).
-/
structure PicardContractionData {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) : Type (max uΩ 1) where
  distance : StochasticProcess Ω → StochasticProcess Ω → ℝ
  contractionFactor : ℝ
  distance_nonneg : ∀ X Y : StochasticProcess Ω, 0 ≤ distance X Y
  contractionFactor_nonneg : 0 ≤ contractionFactor
  contractionFactor_lt_one : contractionFactor < 1
  picardStep_contraction :
    ∀ X Y : StochasticProcess Ω,
      distance (D.picardStep X) (D.picardStep Y) ≤
        contractionFactor * distance X Y

/--
Limit package for the Picard existence branch.

The convergence statement is pointwise almost-everywhere at every fixed time.
It is intentionally weaker than a final stopped-process or pathwise uniform
convergence theorem; selecting that stronger topology is a remaining proof leaf.
-/
structure PicardLimitData {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) (I : PicardIterationData D) :
    Type (max uΩ 1) where
  limit : StochasticProcess Ω
  adapted : Adapted D.filtration limit
  progressivelyMeasurable : ProgMeasurable D.filtration limit
  integrableSlices : ∀ t : Time, Integrable (limit t) P
  initialCondition : limit 0 =ᵐ[P] D.initial
  driftIntegrandAdapted : Adapted D.filtration (D.driftIntegrand limit)
  diffusionIntegrandAdapted : Adapted D.filtration (D.diffusionIntegrand limit)
  driftIntegrandFirstMoment : SdeFirstMomentEstimate P (D.driftIntegrand limit)
  diffusionIntegrandFirstMoment : SdeFirstMomentEstimate P (D.diffusionIntegrand limit)
  driftIntegrandSecondMoment : SdeSecondMomentEstimate P (D.driftIntegrand limit)
  diffusionIntegrandSecondMoment : SdeSecondMomentEstimate P (D.diffusionIntegrand limit)
  convergesAtSlices :
    ∀ t : Time, ∀ᵐ ω ∂P,
      Filter.Tendsto (fun n : ℕ => I.iterate n t ω) Filter.atTop
        (𝓝 (limit t ω))
  fixedPoint : ∀ t : Time, limit t =ᵐ[P] D.picardStep limit t

/--
Candidate strong-solution package for the normalized SDE boundary.

The two integral terms stand for the deterministic drift integral and the
stochastic Ito integral.  They are data plus obligations rather than definitions
because the pinned mathlib snapshot does not expose a stochastic-integral API.
-/
structure StrongSdeSolution {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) : Type (max uΩ 1) where
  process : StochasticProcess Ω
  adapted : Adapted D.filtration process
  progressivelyMeasurable : ProgMeasurable D.filtration process
  integrableSlices : ∀ t : Time, Integrable (process t) P
  initialCondition : process 0 =ᵐ[P] D.initial
  driftIntegrandAdapted : Adapted D.filtration (D.driftIntegrand process)
  diffusionIntegrandAdapted : Adapted D.filtration (D.diffusionIntegrand process)
  driftIntegrandFirstMoment : SdeFirstMomentEstimate P (D.driftIntegrand process)
  diffusionIntegrandFirstMoment : SdeFirstMomentEstimate P (D.diffusionIntegrand process)
  driftIntegrandSecondMoment : SdeSecondMomentEstimate P (D.driftIntegrand process)
  diffusionIntegrandSecondMoment : SdeSecondMomentEstimate P (D.diffusionIntegrand process)
  integralEquation :
    ∀ t : Time,
      process t =ᵐ[P]
      fun ω => D.initial ω + D.driftIntegralTerm process t ω +
        D.diffusionIntegralTerm process t ω

/--
Pathwise uniqueness estimate package for two candidate strong solutions.

The analytic proof should construct `differenceEnergy` from the stopped or
fixed-time moment of `X - Y`, prove the displayed estimate from the SDE
integral equation plus Lipschitz/Ito bounds, and show that zero energy implies
fixed-time almost-everywhere equality.  This structure is only the checked
boundary for that estimate.
-/
structure PathwiseUniquenessEstimateData {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) (X Y : StrongSdeSolution D) :
    Type (max uΩ 1) where
  differenceEnergy : Time → ℝ
  gronwallBound : Time → ℝ
  differenceEnergy_nonneg : ∀ t : Time, 0 ≤ differenceEnergy t
  pathwiseEstimate : ∀ t : Time, differenceEnergy t ≤ gronwallBound t
  zeroEnergy_imp_aeEq :
    ∀ t : Time, differenceEnergy t = 0 → X.process t =ᵐ[P] Y.process t

/--
Gronwall closure package for a pathwise uniqueness estimate.

In a terminal proof this field should come from a checked Gronwall lemma
applied to the estimate kernel selected for the SDE.  Here it isolates the
closure obligation from the preceding stochastic estimate.
-/
structure GronwallClosureData {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) (X Y : StrongSdeSolution D)
    (E : PathwiseUniquenessEstimateData D X Y) : Type where
  gronwallBound_zero : ∀ t : Time, E.gronwallBound t = 0

/-- A checked uniqueness package bundles estimate leaves and Gronwall leaves. -/
structure SdeUniquenessPackage {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) : Type (max uΩ 1) where
  estimate : ∀ X Y : StrongSdeSolution D, PathwiseUniquenessEstimateData D X Y
  gronwall :
    ∀ X Y : StrongSdeSolution D, GronwallClosureData D X Y (estimate X Y)

/-- A completed Picard limit package gives the strong-solution existence conclusion. -/
theorem picardLimitData_existsStrongSolution {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} {I : PicardIterationData D}
    (L : PicardLimitData D I) :
    Nonempty (StrongSdeSolution D) :=
  ⟨{
    process := L.limit
    adapted := L.adapted
    progressivelyMeasurable := L.progressivelyMeasurable
    integrableSlices := L.integrableSlices
    initialCondition := L.initialCondition
    driftIntegrandAdapted := L.driftIntegrandAdapted
    diffusionIntegrandAdapted := L.diffusionIntegrandAdapted
    driftIntegrandFirstMoment := L.driftIntegrandFirstMoment
    diffusionIntegrandFirstMoment := L.diffusionIntegrandFirstMoment
    driftIntegrandSecondMoment := L.driftIntegrandSecondMoment
    diffusionIntegrandSecondMoment := L.diffusionIntegrandSecondMoment
    integralEquation := by
      intro t
      simpa [SdeProblemData.picardStep] using L.fixedPoint t
  }⟩

/--
Conclusion package expected from a completed SDE existence-and-uniqueness
formalization.

`pathwiseUnique` is stated as indistinguishability at each fixed time.  A later
formalization may strengthen this to process-level indistinguishability after
choosing the final stochastic-process API.
-/
structure SdeExistUniqueConclusion {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SdeProblemData Ω P) : Prop where
  existsStrongSolution : Nonempty (StrongSdeSolution D)
  pathwiseUnique :
    ∀ X Y : StrongSdeSolution D, ∀ t : Time, X.process t =ᵐ[P] Y.process t
  uniquenessInLaw :
    ∀ X Y : StrongSdeSolution D, ∀ t : Time,
      P.map (X.process t) = P.map (Y.process t)

/--
Stage1 normalized statement shape for THM-M-1036.

For a probability space, initial random variable, Gaussian driving process, and
deterministic coefficients satisfying the chosen Brownian/noise, measurability,
local-Lipschitz, linear-growth, stochastic-integral, and independence
hypotheses, a completed formalization should construct a strong solution and
prove pathwise uniqueness and uniqueness in law.  This file does not prove that
terminal theorem.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P],
    ∀ D : SdeProblemData Ω P, SdeExistUniqueConclusion D

/-- Project existence of a strong solution from the future conclusion package. -/
theorem conclusion_existsStrongSolution {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SdeProblemData Ω P} (h : SdeExistUniqueConclusion D) :
    Nonempty (StrongSdeSolution D) :=
  h.existsStrongSolution

/-- Project pathwise uniqueness from the future conclusion package. -/
theorem conclusion_pathwiseUnique {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SdeProblemData Ω P} (h : SdeExistUniqueConclusion D) :
    ∀ X Y : StrongSdeSolution D, ∀ t : Time, X.process t =ᵐ[P] Y.process t :=
  h.pathwiseUnique

/-- Project uniqueness in law from the future conclusion package. -/
theorem conclusion_uniquenessInLaw {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SdeProblemData Ω P} (h : SdeExistUniqueConclusion D) :
    ∀ X Y : StrongSdeSolution D, ∀ t : Time,
      P.map (X.process t) = P.map (Y.process t) :=
  h.uniquenessInLaw

/-- Project the stochastic pathwise uniqueness estimate from its package. -/
theorem pathwiseUniquenessEstimate_bound {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} {X Y : StrongSdeSolution D}
    (E : PathwiseUniquenessEstimateData D X Y) (t : Time) :
    E.differenceEnergy t ≤ E.gronwallBound t :=
  E.pathwiseEstimate t

/-- Project nonnegativity of the difference energy from its package. -/
theorem pathwiseUniquenessEstimate_nonneg {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} {X Y : StrongSdeSolution D}
    (E : PathwiseUniquenessEstimateData D X Y) (t : Time) :
    0 ≤ E.differenceEnergy t :=
  E.differenceEnergy_nonneg t

/-- Gronwall closure forces the packaged difference energy to vanish. -/
theorem gronwallClosure_differenceEnergy_eq_zero {Ω : Type uΩ}
    [MeasurableSpace Ω] {P : Measure Ω} {D : SdeProblemData Ω P}
    {X Y : StrongSdeSolution D} (E : PathwiseUniquenessEstimateData D X Y)
    (G : GronwallClosureData D X Y E) (t : Time) :
    E.differenceEnergy t = 0 := by
  refine le_antisymm ?_ (E.differenceEnergy_nonneg t)
  simpa [G.gronwallBound_zero t] using E.pathwiseEstimate t

/-- Estimate plus Gronwall closure gives fixed-time pathwise uniqueness. -/
theorem gronwallClosure_pathwiseUnique {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} {X Y : StrongSdeSolution D}
    (E : PathwiseUniquenessEstimateData D X Y)
    (G : GronwallClosureData D X Y E) (t : Time) :
    X.process t =ᵐ[P] Y.process t :=
  E.zeroEnergy_imp_aeEq t (gronwallClosure_differenceEnergy_eq_zero E G t)

/-- Almost-everywhere equality transports fixed-time laws. -/
theorem law_eq_of_ae_eq {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {X Y : Ω → State} (h : X =ᵐ[P] Y) :
    P.map X = P.map Y :=
  Measure.map_congr h

/-- Fixed-time pathwise uniqueness transports to fixed-time uniqueness in law. -/
theorem pathwiseUnique_to_uniquenessInLaw {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P}
    (h : ∀ X Y : StrongSdeSolution D, ∀ t : Time,
      X.process t =ᵐ[P] Y.process t) :
    ∀ X Y : StrongSdeSolution D, ∀ t : Time,
      P.map (X.process t) = P.map (Y.process t) := by
  intro X Y t
  exact law_eq_of_ae_eq (h X Y t)

/-- A completed uniqueness package gives fixed-time pathwise uniqueness. -/
theorem sdeUniquenessPackage_pathwiseUnique {Ω : Type uΩ}
    [MeasurableSpace Ω] {P : Measure Ω} {D : SdeProblemData Ω P}
    (U : SdeUniquenessPackage D) :
    ∀ X Y : StrongSdeSolution D, ∀ t : Time, X.process t =ᵐ[P] Y.process t := by
  intro X Y t
  exact gronwallClosure_pathwiseUnique (U.estimate X Y) (U.gronwall X Y) t

/-- A completed uniqueness package gives fixed-time uniqueness in law. -/
theorem sdeUniquenessPackage_uniquenessInLaw {Ω : Type uΩ}
    [MeasurableSpace Ω] {P : Measure Ω} {D : SdeProblemData Ω P}
    (U : SdeUniquenessPackage D) :
    ∀ X Y : StrongSdeSolution D, ∀ t : Time,
      P.map (X.process t) = P.map (Y.process t) :=
  pathwiseUnique_to_uniquenessInLaw (sdeUniquenessPackage_pathwiseUnique U)

/--
Existence plus a completed uniqueness package assembles the current conclusion
shape.  The existence input is intentionally separate so this theorem does not
hide the open Picard/external-existence branch.
-/
theorem existence_and_uniquenessPackage_conclusion {Ω : Type uΩ}
    [MeasurableSpace Ω] {P : Measure Ω} {D : SdeProblemData Ω P}
    (hExists : Nonempty (StrongSdeSolution D)) (U : SdeUniquenessPackage D) :
    SdeExistUniqueConclusion D where
  existsStrongSolution := hExists
  pathwiseUnique := sdeUniquenessPackage_pathwiseUnique U
  uniquenessInLaw := sdeUniquenessPackage_uniquenessInLaw U

/-- A solution package exposes adaptedness of the solution process. -/
theorem solution_adapted {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SdeProblemData Ω P} (X : StrongSdeSolution D) :
    Adapted D.filtration X.process :=
  X.adapted

/-- A solution package exposes progressive measurability of the solution process. -/
theorem solution_progressivelyMeasurable {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SdeProblemData Ω P} (X : StrongSdeSolution D) :
    ProgMeasurable D.filtration X.process :=
  X.progressivelyMeasurable

/-- A solution package exposes the initial condition. -/
theorem solution_initialCondition {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SdeProblemData Ω P} (X : StrongSdeSolution D) :
    X.process 0 =ᵐ[P] D.initial :=
  X.initialCondition

/-- A solution package exposes its integral-equation boundary. -/
theorem solution_integralEquation {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SdeProblemData Ω P} (X : StrongSdeSolution D) (t : Time) :
    X.process t =ᵐ[P]
      fun ω => D.initial ω + D.driftIntegralTerm X.process t ω +
        D.diffusionIntegralTerm X.process t ω :=
  X.integralEquation t

/-- A solution process is a fixed point of the Picard update map. -/
theorem solution_picardStep_fixedPoint {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (X : StrongSdeSolution D)
    (t : Time) :
    X.process t =ᵐ[P] D.picardStep X.process t := by
  simpa [SdeProblemData.picardStep] using X.integralEquation t

/-- A Picard iteration package exposes its step equation. -/
theorem picardIteration_stepEquation {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (I : PicardIterationData D)
    (n : ℕ) (t : Time) :
    I.iterate (n + 1) t =ᵐ[P] D.picardStep (I.iterate n) t :=
  I.stepEquation n t

/-- A Picard iteration package exposes adaptedness of every iterate. -/
theorem picardIteration_iterateAdapted {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (I : PicardIterationData D)
    (n : ℕ) :
    Adapted D.filtration (I.iterate n) :=
  I.iterateAdapted n

/-- A Picard contraction package exposes the strict contraction estimate. -/
theorem picardContraction_estimate {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (C : PicardContractionData D)
    (X Y : StochasticProcess Ω) :
    C.distance (D.picardStep X) (D.picardStep Y) ≤
      C.contractionFactor * C.distance X Y :=
  C.picardStep_contraction X Y

/-- A Picard limit package exposes fixed-point closure of the limit. -/
theorem picardLimit_fixedPoint {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} {I : PicardIterationData D}
    (L : PicardLimitData D I) (t : Time) :
    L.limit t =ᵐ[P] D.picardStep L.limit t :=
  L.fixedPoint t

/-- The selected time-integral API preserves adaptedness. -/
theorem timeIntegral_adapted {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) {H : StochasticProcess Ω}
    (hH : Adapted D.filtration H) :
    Adapted D.filtration (D.timeIntegral H) :=
  D.integralApi.timeIntegral_adapted hH

/-- The selected Ito-integral API preserves adaptedness. -/
theorem itoIntegral_adapted {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) {H M : StochasticProcess Ω}
    (hH : Adapted D.filtration H) (hM : Adapted D.filtration M) :
    Adapted D.filtration (D.itoIntegral H M) :=
  D.integralApi.itoIntegral_adapted hH hM

/-- The selected time-integral API preserves first-moment estimates. -/
theorem timeIntegral_firstMoment {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) {H : StochasticProcess Ω}
    (hH : SdeFirstMomentEstimate P H) :
    SdeFirstMomentEstimate P (D.timeIntegral H) :=
  D.integralApi.timeIntegral_firstMoment hH

/-- The selected Ito-integral API preserves first-moment estimates. -/
theorem itoIntegral_firstMoment {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) {H M : StochasticProcess Ω}
    (hH : SdeFirstMomentEstimate P H) (hM : SdeFirstMomentEstimate P M) :
    SdeFirstMomentEstimate P (D.itoIntegral H M) :=
  D.integralApi.itoIntegral_firstMoment hH hM

/-- The selected time-integral API preserves second-moment estimates. -/
theorem timeIntegral_secondMoment {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) {H : StochasticProcess Ω}
    (hH : SdeSecondMomentEstimate P H) :
    SdeSecondMomentEstimate P (D.timeIntegral H) :=
  D.integralApi.timeIntegral_secondMoment hH

/-- The selected Ito-integral API preserves second-moment estimates. -/
theorem itoIntegral_secondMoment {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) {H M : StochasticProcess Ω}
    (hH : SdeSecondMomentEstimate P H) (hM : SdeSecondMomentEstimate P M) :
    SdeSecondMomentEstimate P (D.itoIntegral H M) :=
  D.integralApi.itoIntegral_secondMoment hH hM

/-- A strong solution exposes adaptedness of its drift integral. -/
theorem solution_driftIntegralAdapted {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (X : StrongSdeSolution D) :
    Adapted D.filtration (D.driftIntegralTerm X.process) :=
  D.integralApi.timeIntegral_adapted X.driftIntegrandAdapted

/-- A strong solution exposes adaptedness of its diffusion Ito integral. -/
theorem solution_diffusionIntegralAdapted {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (X : StrongSdeSolution D) :
    Adapted D.filtration (D.diffusionIntegralTerm X.process) :=
  D.integralApi.itoIntegral_adapted X.diffusionIntegrandAdapted D.brownian.adapted

/-- A strong solution exposes first-moment estimates for its drift integral. -/
theorem solution_driftIntegralFirstMoment {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (X : StrongSdeSolution D) :
    SdeFirstMomentEstimate P (D.driftIntegralTerm X.process) :=
  D.integralApi.timeIntegral_firstMoment X.driftIntegrandFirstMoment

/-- A strong solution exposes first-moment estimates for its diffusion Ito integral. -/
theorem solution_diffusionIntegralFirstMoment {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (X : StrongSdeSolution D)
    (hW : SdeFirstMomentEstimate P D.drivingNoise) :
    SdeFirstMomentEstimate P (D.diffusionIntegralTerm X.process) :=
  D.integralApi.itoIntegral_firstMoment X.diffusionIntegrandFirstMoment hW

/-- A strong solution exposes second-moment estimates for its drift integral. -/
theorem solution_driftIntegralSecondMoment {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (X : StrongSdeSolution D) :
    SdeSecondMomentEstimate P (D.driftIntegralTerm X.process) :=
  D.integralApi.timeIntegral_secondMoment X.driftIntegrandSecondMoment

/-- A strong solution exposes second-moment estimates for its diffusion Ito integral. -/
theorem solution_diffusionIntegralSecondMoment {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SdeProblemData Ω P} (X : StrongSdeSolution D)
    (hW : SdeSecondMomentEstimate P D.drivingNoise) :
    SdeSecondMomentEstimate P (D.diffusionIntegralTerm X.process) :=
  D.integralApi.itoIntegral_secondMoment X.diffusionIntegrandSecondMoment hW

/-- The problem package exposes the law of the initial random variable. -/
theorem initial_hasLaw {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) :
    HasLaw D.initial D.initialLaw P :=
  D.initialHasLaw

/-- The coefficient package exposes global Lipschitz control for the drift. -/
theorem coefficients_driftGlobalLipschitz (C : SdeCoefficientData) (t : Time) :
    LipschitzWith C.driftGlobalLipschitzConstant fun x : State => C.drift t x :=
  C.driftGlobalLipschitz t

/-- The coefficient package exposes global Lipschitz control for the diffusion. -/
theorem coefficients_diffusionGlobalLipschitz (C : SdeCoefficientData) (t : Time) :
    LipschitzWith C.diffusionGlobalLipschitzConstant fun x : State => C.diffusion t x :=
  C.diffusionGlobalLipschitz t

/-- The coefficient package exposes local Lipschitz control for the drift. -/
theorem coefficients_driftLocalLipschitz (C : SdeCoefficientData) (t : Time) :
    LocallyLipschitz fun x : State => C.drift t x :=
  C.driftLocalLipschitz t

/-- The coefficient package exposes local Lipschitz control for the diffusion. -/
theorem coefficients_diffusionLocalLipschitz (C : SdeCoefficientData) (t : Time) :
    LocallyLipschitz fun x : State => C.diffusion t x :=
  C.diffusionLocalLipschitz t

/-- The coefficient package exposes linear growth for the drift. -/
theorem coefficients_driftLinearGrowth (C : SdeCoefficientData) (t : Time) (x : State) :
    ‖C.drift t x‖ ≤ (C.linearGrowthConstant : ℝ) * (1 + ‖x‖) :=
  C.driftLinearGrowth t x

/-- The coefficient package exposes linear growth for the diffusion. -/
theorem coefficients_diffusionLinearGrowth (C : SdeCoefficientData) (t : Time) (x : State) :
    ‖C.diffusion t x‖ ≤ (C.linearGrowthConstant : ℝ) * (1 + ‖x‖) :=
  C.diffusionLinearGrowth t x

/-- The problem package exposes Gaussianity of the Brownian boundary process. -/
theorem driving_gaussianProcess {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) :
    IsGaussianProcess D.drivingNoise P :=
  D.brownian.gaussian

/-- The problem package exposes adaptedness of the Brownian boundary process. -/
theorem driving_adapted {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) :
    Adapted D.filtration D.drivingNoise :=
  D.brownian.adapted

/-- The problem package exposes progressive measurability of the Brownian boundary process. -/
theorem driving_progressivelyMeasurable {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) :
    ProgMeasurable D.filtration D.drivingNoise :=
  D.brownian.progressivelyMeasurable

/-- The problem package exposes Brownian path continuity. -/
theorem driving_continuousPaths {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) (ω : Ω) :
    Continuous fun t : Time => D.drivingNoise t ω :=
  D.brownian.continuousPaths ω

/-- The problem package exposes Brownian independent increments. -/
theorem driving_independentIncrements {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) ⦃s t u v : Time⦄
    (hs : 0 ≤ s) (hst : s ≤ t) (htu : t ≤ u) (huv : u ≤ v) :
    IndepFun (fun ω : Ω => D.drivingNoise t ω - D.drivingNoise s ω)
      (fun ω : Ω => D.drivingNoise v ω - D.drivingNoise u ω) P :=
  D.brownian.independentIncrements hs hst htu huv

/-- The problem package exposes the Brownian covariance identity. -/
theorem driving_covariance {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) (s t : Time) (hs : 0 ≤ s) (ht : 0 ≤ t) :
    (∫ ω, D.drivingNoise s ω * D.drivingNoise t ω ∂P) = min s t :=
  D.brownian.covariance s t hs ht

/-- The initial random variable is measurable at time zero in the chosen filtration. -/
theorem initial_measurableAtZero {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) :
    Measurable[D.filtration 0] D.initial :=
  D.initialMeasurableAtZero

/-- The initial random variable is independent of each one-time Brownian coordinate. -/
theorem initial_independentOfDrivingNoise {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SdeProblemData Ω P) (t : Time) :
    IndepFun D.initial (D.drivingNoise t) P :=
  D.initialIndependentOfDrivingNoise t

/-- Checked mathlib wrapper: `HasLaw` exposes the map equality defining a law. -/
theorem hasLaw_map_eq {Ω X : Type*} [MeasurableSpace Ω] [MeasurableSpace X]
    {P : Measure Ω} {μ : Measure X} {Z : Ω → X} (hZ : HasLaw Z μ P) :
    P.map Z = μ :=
  hZ.map_eq

/-- Checked mathlib wrapper: `HasLaw` exposes almost-everywhere measurability. -/
theorem hasLaw_aemeasurable {Ω X : Type*} [MeasurableSpace Ω] [MeasurableSpace X]
    {P : Measure Ω} {μ : Measure X} {Z : Ω → X} (hZ : HasLaw Z μ P) :
    AEMeasurable Z P :=
  hZ.aemeasurable

/-- Checked mathlib wrapper: a Gaussian process has almost-everywhere measurable slices. -/
theorem gaussianProcess_aemeasurable {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {X : StochasticProcess Ω} (hX : IsGaussianProcess X P) (t : Time) :
    AEMeasurable (X t) P :=
  hX.aemeasurable t

/-- Checked mathlib wrapper: progressive measurability implies strong adaptedness. -/
theorem progMeasurable_stronglyAdapted {Ω : Type uΩ} [MeasurableSpace Ω]
    {ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)} {X : StochasticProcess Ω}
    (hX : ProgMeasurable ℱ X) :
    StronglyAdapted ℱ X :=
  hX.stronglyAdapted

/-- Checked mathlib wrapper: adapted processes have globally measurable slices. -/
theorem adapted_measurable_slice {Ω : Type uΩ} [MeasurableSpace Ω]
    {ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)} {X : StochasticProcess Ω}
    (hX : Adapted ℱ X) (t : Time) :
    Measurable (X t) :=
  hX.measurable

/-- Checked mathlib wrapper: constant processes are adapted. -/
theorem const_process_adapted {Ω : Type uΩ} [MeasurableSpace Ω]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) (x : State) :
    Adapted ℱ (fun _ _ => x : StochasticProcess Ω) :=
  adapted_const ℱ x

/-- Checked mathlib wrapper: constant processes are progressively measurable. -/
theorem const_process_progMeasurable {Ω : Type uΩ} [MeasurableSpace Ω]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) (x : State) :
    ProgMeasurable ℱ (fun _ _ => x : StochasticProcess Ω) :=
  progMeasurable_const ℱ x

/-- Checked mathlib wrapper: deterministic times are stopping times. -/
theorem const_stopping_time_wrapper {Ω : Type uΩ} [MeasurableSpace Ω]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) (t : Time) :
    IsStoppingTime ℱ (fun _ : Ω => (t : WithTop Time)) :=
  isStoppingTime_const ℱ t

/-- mathlib modules checked while locating repo-local anchors for this SDE slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic",
  "Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Independence",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.HittingTime",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.Topology.MetricSpace.Lipschitz"
]

/-- Pinned declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.HasLaw.map_eq",
  "ProbabilityTheory.HasLaw.aemeasurable",
  "ProbabilityTheory.IsGaussianProcess",
  "ProbabilityTheory.IsGaussianProcess.aemeasurable",
  "ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_eval",
  "ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_increments",
  "ProbabilityTheory.IsGaussianProcess.iIndepFun_of_covariance_eq_zero",
  "ProbabilityTheory.IsGaussianProcess.indepFun_of_covariance_eq_zero",
  "ProbabilityTheory.HasGaussianLaw",
  "ProbabilityTheory.HasGaussianLaw.aemeasurable",
  "ProbabilityTheory.HasGaussianLaw.integrable",
  "ProbabilityTheory.HasGaussianLaw.memLp_two",
  "ProbabilityTheory.HasGaussianLaw.iIndepFun_of_covariance_eq_zero",
  "ProbabilityTheory.HasGaussianLaw.indepFun_of_covariance_eq_zero",
  "ProbabilityTheory.iIndepFun.hasGaussianLaw",
  "ProbabilityTheory.IndepFun.hasGaussianLaw_sub_of_sub",
  "ProbabilityTheory.IndepFun",
  "Measure.map_congr",
  "LipschitzWith",
  "LocallyLipschitz",
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "MeasureTheory.Adapted.measurable",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.ProgMeasurable",
  "MeasureTheory.ProgMeasurable.stronglyAdapted",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.isStoppingTime_const",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.Submartingale.stoppedProcess",
  "AwesomeTheorems.Stage1.S1_M_229.SdeProblemData.picardStep",
  "AwesomeTheorems.Stage1.S1_M_229.PicardIterationData",
  "AwesomeTheorems.Stage1.S1_M_229.PicardContractionData",
  "AwesomeTheorems.Stage1.S1_M_229.PicardLimitData",
  "AwesomeTheorems.Stage1.S1_M_229.picardLimitData_existsStrongSolution",
  "AwesomeTheorems.Stage1.S1_M_229.PathwiseUniquenessEstimateData",
  "AwesomeTheorems.Stage1.S1_M_229.GronwallClosureData",
  "AwesomeTheorems.Stage1.S1_M_229.SdeUniquenessPackage",
  "AwesomeTheorems.Stage1.S1_M_229.law_eq_of_ae_eq",
  "AwesomeTheorems.Stage1.S1_M_229.pathwiseUnique_to_uniquenessInLaw",
  "AwesomeTheorems.Stage1.S1_M_229.existence_and_uniquenessPackage_conclusion"
]

/-- Checked Stage1 decision for this child: use a local SDE integral API boundary. -/
def sdeIntegralApiDecision : String :=
  "Expose SdeIntegralAPI with timeIntegral and itoIntegral operations, adaptedness, and first/second moment obligations; no terminal Ito construction is claimed."

/-- Concrete blockers before the local integral API can count as terminal SDE proof evidence. -/
def sdeIntegralApiIntegrationBlockers : List String := [
  "No repo-local construction of the Ito integral from predictable simple processes is available in this Lean closure.",
  "No Ito isometry or Brownian stochastic-integral moment estimate theorem is imported or pinned.",
  "The external Brownian-motion candidate is not in the Lake dependency closure and targets a different Lean/mathlib dependency set."
]

/-- The local SDE integral API boundary is not a terminal SDE existence proof. -/
def sdeIntegralApiIsTerminalExistenceProof : Bool :=
  false

/-- Checked guard against treating the local integral API boundary as terminal closure. -/
theorem sdeIntegralApiIsTerminalExistenceProof_eq_false :
    sdeIntegralApiIsTerminalExistenceProof = false :=
  rfl

/-- Checked Stage1 decision for the Picard existence child. -/
def picardExistenceDecision : String :=
  "Expose Picard step, iteration, contraction, and limit data packages; prove that a completed Picard limit package yields a StrongSdeSolution; do not claim terminal SDE existence."

/--
Picard-existence leaf ledger for the local Stage1 artifact.

The boolean component means that the leaf is closed in this repository now.
Only boundary/projection leaves are closed; analytic Picard estimates remain
open formalization debt.
-/
def picardExistenceLeafLedger : List (String × Nat × Bool) := [
  ("S1-M-229-C004-L001.picard-step-map", 12, true),
  ("S1-M-229-C004-L002.solution-fixed-point-projection", 8, true),
  ("S1-M-229-C004-L003.iteration-data-boundary", 18, true),
  ("S1-M-229-C004-L004.contraction-data-boundary", 20, true),
  ("S1-M-229-C004-L005.limit-data-boundary", 28, true),
  ("S1-M-229-C004-L006.limit-data-to-strong-solution", 18, true),
  ("S1-M-229-C004-L007.construct-picard-seed", 0, false),
  ("S1-M-229-C004-L008.iterate-adaptedness-induction", 0, false),
  ("S1-M-229-C004-L009.iterate-moment-induction", 0, false),
  ("S1-M-229-C004-L010.ito-estimate-for-step-differences", 0, false),
  ("S1-M-229-C004-L011.contraction-or-cauchy-estimate", 0, false),
  ("S1-M-229-C004-L012.limit-passage-through-integrals", 0, false),
  ("S1-M-229-C004-L013.limit-progressive-measurability", 0, false),
  ("S1-M-229-C004-L014.limit-integral-equation", 0, false)
]

/-- The Picard existence branch is not repo-locally complete. -/
def picardExistenceIsRepoLocalComplete : Bool :=
  false

/-- Checked guard against treating the Picard boundary split as terminal closure. -/
theorem picardExistenceIsRepoLocalComplete_eq_false :
    picardExistenceIsRepoLocalComplete = false :=
  rfl

/-- Concrete blockers before the Picard existence branch can be completed. -/
def picardExistenceIntegrationBlockers : List String := [
  "No repo-local Ito construction or Ito-isometry theorem is available for the Picard estimates.",
  "No selected stopped-process or finite-horizon L2 metric has been connected to the local integral API.",
  "No proof that Picard iterates converge in a topology strong enough to pass through both integral terms is in the repo-local closure.",
  "No pinned/imported external Lean 4 SDE existence theorem has been validated in this repository."
]

/-- Checked Stage1 decision for the uniqueness child. -/
def sdeUniquenessDecision : String :=
  "Expose checked pathwise-uniqueness estimate, Gronwall closure, and fixed-time law-transport packages; do not claim the analytic SDE uniqueness theorem is complete."

/--
Uniqueness leaf ledger for the local Stage1 artifact.

The boolean component means that the leaf is closed in this repository now.
Only boundary/projection/transport leaves are closed; stochastic estimates and
the real Gronwall lemma application remain open formalization debt.
-/
def sdeUniquenessLeafLedger : List (String × Nat × Bool) := [
  ("S1-M-229-C005-L001.pathwise-estimate-boundary", 24, true),
  ("S1-M-229-C005-L002.gronwall-closure-boundary", 10, true),
  ("S1-M-229-C005-L003.estimate-bound-projection", 6, true),
  ("S1-M-229-C005-L004.nonnegativity-projection", 6, true),
  ("S1-M-229-C005-L005.gronwall-zero-energy", 12, true),
  ("S1-M-229-C005-L006.gronwall-to-pathwise-uniqueness", 10, true),
  ("S1-M-229-C005-L007.ae-equality-to-law-equality", 6, true),
  ("S1-M-229-C005-L008.pathwise-uniqueness-to-law-uniqueness", 8, true),
  ("S1-M-229-C005-L009.uniqueness-package-boundary", 16, true),
  ("S1-M-229-C005-L010.uniqueness-package-to-conclusion", 18, true),
  ("S1-M-229-C005-L011.derive-difference-energy-estimate", 0, false),
  ("S1-M-229-C005-L012.drift-difference-bound", 0, false),
  ("S1-M-229-C005-L013.ito-difference-bound", 0, false),
  ("S1-M-229-C005-L014.apply-real-gronwall-lemma", 0, false),
  ("S1-M-229-C005-L015.zero-energy-to-ae-equality", 0, false),
  ("S1-M-229-C005-L016.upgrade-fixed-time-law-to-process-law-if-required", 0, false)
]

/-- The uniqueness branch is not repo-locally complete. -/
def sdeUniquenessIsRepoLocalComplete : Bool :=
  false

/-- Checked guard against treating the uniqueness split as terminal closure. -/
theorem sdeUniquenessIsRepoLocalComplete_eq_false :
    sdeUniquenessIsRepoLocalComplete = false :=
  rfl

/-- Concrete blockers before the uniqueness branch can be completed. -/
def sdeUniquenessIntegrationBlockers : List String := [
  "No repo-local derivation of the stopped or fixed-time L2 difference-energy estimate from the two SDE integral equations is available.",
  "No Ito isometry or stochastic-integral difference estimate is pinned/imported/checked for the diffusion term.",
  "No deterministic Gronwall lemma has been connected to the selected difference-energy inequality.",
  "The current conclusion transports fixed-time almost-everywhere equality to fixed-time laws; process-level uniqueness in law would need a finite-dimensional-law or path-space law upgrade."
]

/--
Search terms that did not locate a terminal SDE existence-and-uniqueness theorem
in the pinned local mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "SDE",
  "StochasticDifferential",
  "stochastic differential equation",
  "StrongSolution",
  "WeakSolution",
  "Ito process",
  "Itô process",
  "StochasticIntegral",
  "stochastic integral",
  "BrownianMotion",
  "Brownian motion",
  "existence and uniqueness SDE",
  "pathwise uniqueness"
]

/-- External Brownian-motion candidate audited for this Stage1 slot. -/
def externalBrownianMotionRepository : String :=
  "https://github.com/RemyDegenne/brownian-motion"

/-- External Brownian-motion repository HEAD audited on 2026-05-01. -/
def externalBrownianMotionCommit : String :=
  "91885e6172648ea7f9c6a16b3a7069f92c88e023"

/--
External declarations found in the Brownian-motion candidate repository.

These names are anchor metadata only; the external project is not pinned,
imported, or checked in this repository's Lean closure.
-/
def externalBrownianMotionAnchorNames : List String := [
  "ProbabilityTheory.IsBrownian",
  "ProbabilityTheory.IsPreBrownian",
  "ProbabilityTheory.preBrownian",
  "ProbabilityTheory.IsPreBrownian.isGaussianProcess",
  "ProbabilityTheory.IsPreBrownian.hasLaw",
  "ProbabilityTheory.IsPreBrownian.hasIndepIncrements",
  "ProbabilityTheory.isBrownian_iff_isPreBrownian_continuous",
  "ProbabilityTheory.isBrownian_iff_isPreBrownian_continuous'",
  "ProbabilityTheory.IsBrownian.isPreBrownian",
  "ProbabilityTheory.IsBrownian.isGaussianProcess",
  "ProbabilityTheory.IsBrownian.hasLaw",
  "ProbabilityTheory.IsBrownian.hasIndepIncrements"
]

/--
External integration blocker for the Brownian-motion candidate.

At commit `externalBrownianMotionCommit`, the external project targets Lean
`v4.30.0-rc1` and a different mathlib/kolmogorov-extension dependency closure
than this repository's current Lean `v4.29.0` and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.
-/
def externalBrownianMotionIntegrationBlocker : String :=
  "toolchain/dependency mismatch; not pinned or imported into this repo-local Lean closure"

/-- Audit date for the external SDE existence/uniqueness integration gate. -/
def externalSdeExistenceUniquenessAuditDate : String :=
  "2026-05-01"

/--
Checked Stage1 decision for the external SDE existence/uniqueness integration
gate.

The current bounded audit found Brownian-motion infrastructure, but no external
Lean 4 terminal theorem proving the classical SDE existence-and-uniqueness
statement.  Therefore there is no external terminal proof to pin/import/check
in this child, and the public completion gate must remain open.
-/
def externalSdeExistenceUniquenessGateDecision : String :=
  "No external Lean 4 terminal SDE existence-and-uniqueness proof was found in the audited closure; do not mark completed from anchor-only evidence."

/-- No audited external terminal SDE existence/uniqueness proof is currently repo-local. -/
def externalSdeExistenceUniquenessTerminalProofFound : Bool :=
  false

/-- Checked guard against treating the external-anchor audit as terminal closure. -/
theorem externalSdeExistenceUniquenessTerminalProofFound_eq_false :
    externalSdeExistenceUniquenessTerminalProofFound = false :=
  rfl

/-- External/proof-search sources audited for the integration gate. -/
def externalSdeExistenceUniquenessAuditSources : List String := [
  "pinned mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 local tree search",
  "RemyDegenne/brownian-motion commit 91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "web search for Lean 4 stochastic differential equation existence uniqueness proof",
  "GitHub unauthenticated code search attempt returned 401 Requires authentication"
]

/--
Concrete blockers before any external SDE proof can close this Stage1 slot.

If a later worker identifies a terminal Lean 4 theorem, the next step is not an
anchor-only citation: it must be a compatible Lake dependency pin, vendored
proof body, or repo-local wrapper theorem that validates in this repository.
-/
def externalSdeExistenceUniquenessIntegrationBlockers : List String := [
  "No terminal SDE existence-and-uniqueness theorem was found in the pinned local mathlib closure.",
  "The audited external Brownian-motion project supplies Brownian infrastructure only; it does not provide a checked SDE existence-and-uniqueness theorem for this repository.",
  "The audited external Brownian-motion project targets Lean v4.30.0-rc1, mathlib f2330615d77de0c9a2f5cb56bb6eda8c52c7f92d, and kolmogorov_extension4 b0771387813dca0b08715e4a5a944d457ebd92e0, while this repository targets Lean v4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "If a terminal external Lean 4 SDE proof is later found, the public slot must stay open until it is pinned/imported/vendored and checked locally, or until an explicit compatibility/license/dependency blocker is recorded."
]

/--
Checked Stage1 decision for the public merge gate.

This child is allowed to record an integration-ready public backfill plan, but
it does not edit shared public planning documents.  Therefore the public Stage1
checkbox must remain open after local Lean validation.
-/
def publicMergeGateDecision : String :=
  "Keep S1-M-229.public-merge open until local validation, serial public backfill, and independent <=100 leaf ledgers are synchronized."

/-- Public surfaces that require a later serialized integrator patch. -/
def publicMergeRequiredSurfaces : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md or the authoritative public progress surface selected by the supervisor"
]

/--
Public-merge gate leaf ledger for this local artifact.

The boolean component records whether the leaf is closed by this child in the
repo-local checked artifact.  Public-document leaves remain open because this
worker does not own shared public surfaces.
-/
def publicMergeGateLeafLedger : List (String × Nat × Bool) := [
  ("S1-M-229-C007-L001.local-lean-artifact-validation", 4, true),
  ("S1-M-229-C007-L002.child-ledger-public-backfill-plan", 12, true),
  ("S1-M-229-C007-L003.serial-blueprint-merge-back", 0, false),
  ("S1-M-229-C007-L004.public-todo-and-readme-synchronization", 0, false),
  ("S1-M-229-C007-L005.parent-independent-leaf-ledger-synchronization", 0, false),
  ("S1-M-229-C007-L006.terminal-completion-gate-recheck", 0, false)
]

/-- Numeric proof-step budgets appearing in the C007 public-merge ledger. -/
def publicMergeGateLeafBudgetValues : List Nat := [
  4, 12, 0, 0, 0, 0
]

/-- All C007 public-merge leaves are budgeted within the M0387 `<=100` limit. -/
def publicMergeGateLeafBudgetsWithinLimit : Bool :=
  publicMergeGateLeafBudgetValues.all fun n => decide (n <= 100)

/-- The public merge-back is not completed by this child. -/
def publicMergeBackCompleted : Bool :=
  false

/-- The parent public surfaces and independent leaf ledgers are not synchronized yet. -/
def publicMergeLeafLedgersSynchronized : Bool :=
  false

/-- Checked guard: this child cannot close the public Stage1 checkbox. -/
def publicMergeCanCloseNow : Bool :=
  false

/-- Checked guard for the C007 M0387 leaf-budget ledger. -/
theorem publicMergeGateLeafBudgetsWithinLimit_eq_true :
    publicMergeGateLeafBudgetsWithinLimit = true :=
  rfl

/-- Checked guard that no public merge-back completion is claimed. -/
theorem publicMergeBackCompleted_eq_false :
    publicMergeBackCompleted = false :=
  rfl

/-- Checked guard that parent public/leaf synchronization is still open. -/
theorem publicMergeLeafLedgersSynchronized_eq_false :
    publicMergeLeafLedgersSynchronized = false :=
  rfl

/-- Checked guard that the public Stage1 checkbox must remain open. -/
theorem publicMergeCanCloseNow_eq_false :
    publicMergeCanCloseNow = false :=
  rfl

#check StatementShape
#check SdeCoefficientData
#check BrownianMotionData
#check SdeFirstMomentEstimate
#check SdeSecondMomentEstimate
#check SdeIntegralAPI
#check SdeProblemData
#check SdeProblemData.driftIntegralTerm
#check SdeProblemData.diffusionIntegralTerm
#check SdeProblemData.picardStep
#check PicardIterationData
#check PicardContractionData
#check PicardLimitData
#check StrongSdeSolution
#check PathwiseUniquenessEstimateData
#check GronwallClosureData
#check SdeUniquenessPackage
#check SdeExistUniqueConclusion
#check picardLimitData_existsStrongSolution
#check solution_picardStep_fixedPoint
#check picardIteration_stepEquation
#check picardIteration_iterateAdapted
#check picardContraction_estimate
#check picardLimit_fixedPoint
#check solution_driftIntegralAdapted
#check solution_diffusionIntegralAdapted
#check solution_driftIntegralFirstMoment
#check solution_diffusionIntegralFirstMoment
#check solution_driftIntegralSecondMoment
#check solution_diffusionIntegralSecondMoment
#check sdeIntegralApiIsTerminalExistenceProof_eq_false
#check picardExistenceIsRepoLocalComplete_eq_false
#check pathwiseUniquenessEstimate_bound
#check pathwiseUniquenessEstimate_nonneg
#check gronwallClosure_differenceEnergy_eq_zero
#check gronwallClosure_pathwiseUnique
#check law_eq_of_ae_eq
#check pathwiseUnique_to_uniquenessInLaw
#check sdeUniquenessPackage_pathwiseUnique
#check sdeUniquenessPackage_uniquenessInLaw
#check existence_and_uniquenessPackage_conclusion
#check sdeUniquenessIsRepoLocalComplete_eq_false
#check externalSdeExistenceUniquenessTerminalProofFound_eq_false
#check publicMergeGateLeafBudgetsWithinLimit_eq_true
#check publicMergeBackCompleted_eq_false
#check publicMergeLeafLedgersSynchronized_eq_false
#check publicMergeCanCloseNow_eq_false
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.IsGaussianProcess
#check ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_increments
#check ProbabilityTheory.IsGaussianProcess.iIndepFun_of_covariance_eq_zero
#check ProbabilityTheory.IsGaussianProcess.indepFun_of_covariance_eq_zero
#check ProbabilityTheory.HasGaussianLaw.iIndepFun_of_covariance_eq_zero
#check ProbabilityTheory.HasGaussianLaw.indepFun_of_covariance_eq_zero
#check ProbabilityTheory.iIndepFun.hasGaussianLaw
#check ProbabilityTheory.IndepFun.hasGaussianLaw_sub_of_sub
#check ProbabilityTheory.IndepFun
#check Measure.map_congr
#check LipschitzWith
#check LocallyLipschitz
#check MeasureTheory.Filtration
#check MeasureTheory.Adapted
#check MeasureTheory.ProgMeasurable
#check MeasureTheory.IsStoppingTime
#check MeasureTheory.Martingale

end AwesomeTheorems.Stage1.S1_M_229
