import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.Kernel.Composition.Comp
import Mathlib.Probability.Kernel.Integral
import Mathlib.Probability.Process.Filtration

/-!
# S1-M-236 / THM-M-1043: Feynman-Kac formula

This Stage1 artifact records a conservative Lean 4 boundary for the
Feynman-Kac formula: a probabilistic representation of solutions to a
parabolic PDE with generator, potential, source term, and terminal/initial
payoff data.

The pinned mathlib snapshot has strong measure-theory, integration,
Markov-kernel, filtration, and derivative APIs.  It does not expose a terminal
Feynman-Kac theorem, a canonical diffusion-generator API, or the stochastic
calculus/path-integral infrastructure needed for the full continuous-time
formula.

Accordingly this file provides a typed statement shape and low-risk wrappers
around existing mathlib kernel and integration facts.  It does not prove the
Feynman-Kac formula.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_236

universe u v w

/-- Nonnegative time for the forward Feynman-Kac boundary. -/
abbrev Time : Type := ℝ≥0

/--
Chosen time orientation for the Stage1 Feynman-Kac convention.

`forwardTimeToMaturity` means the formal time variable is elapsed
time-to-maturity `τ = T - t`.  Thus the same convention is backward in calendar
time `t`, but forward in the nonnegative Lean variable used below.
-/
inductive TimeOrientation where
  | forwardTimeToMaturity

/-- Chosen sign convention for the infinitesimal generator term. -/
inductive GeneratorSign where
  | positiveGenerator

/-- Chosen sign convention for the potential term. -/
inductive PotentialSign where
  | killingMinus

/-- Chosen sign convention for the source term. -/
inductive SourceSign where
  | additiveSource

/-- Chosen location of the payoff boundary condition. -/
inductive PayoffBoundary where
  | initialAtZeroMaturity

/--
Repo-local convention record for the normalized Feynman-Kac statement.

The selected convention is the time-to-maturity form
`∂_τ u = L u - V u + f`, with payoff at `τ = 0`.  Equivalently, in calendar
time it is a backward terminal-value convention with generator sign `+L`,
killing potential sign `-V u`, and additive source `+f`.
-/
structure FeynmanKacConvention : Type where
  timeOrientation : TimeOrientation
  generatorSign : GeneratorSign
  potentialSign : PotentialSign
  sourceSign : SourceSign
  payoffBoundary : PayoffBoundary

/-- Canonical convention selected for this Stage1 slot. -/
def canonicalFeynmanKacConvention : FeynmanKacConvention where
  timeOrientation := TimeOrientation.forwardTimeToMaturity
  generatorSign := GeneratorSign.positiveGenerator
  potentialSign := PotentialSign.killingMinus
  sourceSign := SourceSign.additiveSource
  payoffBoundary := PayoffBoundary.initialAtZeroMaturity

/-- Checked projection: the canonical convention is forward in time-to-maturity. -/
theorem canonicalConvention_timeOrientation :
    canonicalFeynmanKacConvention.timeOrientation =
      TimeOrientation.forwardTimeToMaturity :=
  rfl

/-- Checked projection: the canonical convention uses the generator with positive sign. -/
theorem canonicalConvention_generatorSign :
    canonicalFeynmanKacConvention.generatorSign =
      GeneratorSign.positiveGenerator :=
  rfl

/-- Checked projection: the canonical convention uses the potential as a killing term. -/
theorem canonicalConvention_potentialSign :
    canonicalFeynmanKacConvention.potentialSign =
      PotentialSign.killingMinus :=
  rfl

/-- Checked projection: the canonical convention uses an additive source term. -/
theorem canonicalConvention_sourceSign :
    canonicalFeynmanKacConvention.sourceSign =
      SourceSign.additiveSource :=
  rfl

/--
Candidate first closure targets for the Stage1 Feynman-Kac line.

The first target is about which theorem family should be closed first in this
repository, not about changing the final mathematical goal.
-/
inductive FirstClosureTarget where
  | finiteStateContinuousTimeMarkovChain
  | discreteTimeDynamicProgrammingAnalogue
  | generalDiffusionFellerSemigroup
  deriving DecidableEq

/--
Checked decision record for the first repo-local closure target.

The selected first target is the discrete-time dynamic-programming analogue:
it can use the kernel-power and deterministic-kernel facts already checked in
this file.  The finite-state continuous-time Markov-chain target remains the
next faithful continuous-time specialization after a finite generator/matrix
semigroup package is selected.  The general diffusion/Feller-semigroup theorem
is deferred until stochastic calculus, generator-domain, and path-functional
integrability APIs exist in the local validation closure.
-/
structure FirstClosureTargetDecision where
  selected : FirstClosureTarget
  nextContinuousTimeTarget : FirstClosureTarget
  deferredTarget : FirstClosureTarget
  checkedSubstrate : List String
  blockerForFiniteStateCTMC : String
  blockerForGeneralDiffusion : String

/-- Canonical first closure target selected for this Stage1 slot. -/
def firstClosureTargetDecision : FirstClosureTargetDecision where
  selected := FirstClosureTarget.discreteTimeDynamicProgrammingAnalogue
  nextContinuousTimeTarget := FirstClosureTarget.finiteStateContinuousTimeMarkovChain
  deferredTarget := FirstClosureTarget.generalDiffusionFellerSemigroup
  checkedSubstrate := [
    "Kernel.pow_add",
    "Kernel.pow_add_apply_eq_lintegral",
    "Kernel.integral_deterministic",
    "FeynmanKacConvention with forward time-to-maturity and killing sign"
  ]
  blockerForFiniteStateCTMC :=
    "Needs a selected finite generator/matrix-semigroup package and checked finite-sum path functional before it can be the first closed theorem."
  blockerForGeneralDiffusion :=
    "Needs diffusion/Feller semigroup, stochastic-integral/Ito, generator-domain, measurability, and integrability infrastructure not present in the repo-local Lean closure."

/-- Checked gate: the first repo-local closure target is the discrete-time DP analogue. -/
theorem firstClosureTarget_selected :
    firstClosureTargetDecision.selected =
      FirstClosureTarget.discreteTimeDynamicProgrammingAnalogue :=
  rfl

/-- Checked gate: the first continuous-time specialization is finite-state CTMC, not diffusion. -/
theorem firstClosureTarget_nextContinuousTime :
    firstClosureTargetDecision.nextContinuousTimeTarget =
      FirstClosureTarget.finiteStateContinuousTimeMarkovChain :=
  rfl

/--
Boundary data for a future Feynman-Kac theorem.

`transitionKernel t` is the time-`t` Markov kernel.  The expression
`probabilisticRepresentation t x` is the expected exponential path functional
starting at `x`; it is intentionally a field because the pinned dependency
closure does not yet provide a canonical diffusion/path-integral API for the
continuous-time Feynman-Kac expression.  The scalar `potential` is the killing
rate in the selected convention, so it appears as `- potential * solution` in
the PDE clause below.
-/
structure FeynmanKacData
    (State : Type u) [MeasurableSpace State] : Type (u + 1) where
  initialMeasure : Measure State
  transitionKernel : Time → Kernel State State
  generator : (State → ℝ) → State → ℝ
  potential : State → ℝ
  source : Time → State → ℝ
  payoff : State → ℝ
  solution : Time → State → ℝ
  timeDerivative : Time → State → ℝ
  probabilisticRepresentation : Time → State → ℝ
  pathFunctionalWellFormed : Prop

/--
Concrete path-functional expectation package for the probabilistic side of
Feynman-Kac.

`pathLaw t x` is the law of paths started at `x` and observed up to
time-to-maturity `t`.  `pathFunctional t x` is the discounted/killed payoff
plus source contribution along such a path.  The final field ties the abstract
representation already present in `FeynmanKacData` to the Bochner expectation
of that path functional.

This is still a boundary package, not a diffusion construction: later workers
must instantiate `Path`, `pathLaw`, and `pathFunctional` from a selected
discrete-time, finite-state CTMC, or diffusion/Feller API.
-/
structure PathFunctionalExpectationPackage
    (State : Type u) [MeasurableSpace State]
    (Path : Type v) [MeasurableSpace Path]
    (D : FeynmanKacData State) : Type (max (u + 1) (v + 1)) where
  pathLaw : Time → State → Measure Path
  pathFunctional : Time → State → Path → ℝ
  pathFunctional_measurable :
    ∀ t x, Measurable (pathFunctional t x)
  pathFunctional_integrable :
    ∀ t x, Integrable (pathFunctional t x) (pathLaw t x)
  expectation_eq :
    ∀ t x, D.probabilisticRepresentation t x =
      ∫ ω, pathFunctional t x ω ∂pathLaw t x
  wellFormed : D.pathFunctionalWellFormed

/-- Existence of a typed path-functional package in a fixed path universe. -/
def HasPathFunctionalExpectationPackage
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  ∃ (Path : Type v) (mPath : MeasurableSpace Path),
    Nonempty (@PathFunctionalExpectationPackage State _ Path mPath D)

/-- Measurability leaf for a concrete path-functional package. -/
def PathFunctionalMeasurableLeaf
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) : Prop :=
  ∀ t x, Measurable (P.pathFunctional t x)

/-- Integrability leaf for a concrete path-functional package. -/
def PathFunctionalIntegrableLeaf
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) : Prop :=
  ∀ t x, Integrable (P.pathFunctional t x) (P.pathLaw t x)

/-- Expectation-identification leaf for a concrete path-functional package. -/
def PathFunctionalExpectationLeaf
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) : Prop :=
  ∀ t x, D.probabilisticRepresentation t x =
    ∫ ω, P.pathFunctional t x ω ∂P.pathLaw t x

/--
Checked package of the local path-functional leaves.

Each projection below is intentionally a one-step field projection, keeping the
leaf proof budget comfortably below the `<=100` M0387 requirement.
-/
def PathFunctionalExpectationLeaves
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) : Prop :=
  PathFunctionalMeasurableLeaf P ∧
    PathFunctionalIntegrableLeaf P ∧
      PathFunctionalExpectationLeaf P ∧
        D.pathFunctionalWellFormed

/-- `<=100` leaf: package field projection for path-functional measurability. -/
theorem pathFunctional_measurable_leaf
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) :
    PathFunctionalMeasurableLeaf P :=
  P.pathFunctional_measurable

/-- `<=100` leaf: package field projection for path-functional integrability. -/
theorem pathFunctional_integrable_leaf
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) :
    PathFunctionalIntegrableLeaf P :=
  P.pathFunctional_integrable

/-- `<=100` leaf: package field projection for expectation identification. -/
theorem pathFunctional_expectation_leaf
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) :
    PathFunctionalExpectationLeaf P :=
  P.expectation_eq

/-- `<=100` leaf: the concrete package supplies the legacy well-formedness gate. -/
theorem pathFunctional_wellFormed_leaf
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) :
    D.pathFunctionalWellFormed :=
  P.wellFormed

/-- `<=100` package gate combining the local path-functional leaves. -/
theorem pathFunctional_expectation_leaves
    {State : Type u} [MeasurableSpace State]
    {Path : Type v} [MeasurableSpace Path]
    {D : FeynmanKacData State}
    (P : PathFunctionalExpectationPackage State Path D) :
    PathFunctionalExpectationLeaves P :=
  ⟨pathFunctional_measurable_leaf P,
    pathFunctional_integrable_leaf P,
    pathFunctional_expectation_leaf P,
    pathFunctional_wellFormed_leaf P⟩

/-- Nonnegative-time transition kernels are Markov kernels. -/
def MarkovKernelFamily
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  ∀ t : Time, IsMarkovKernel (D.transitionKernel t)

/-- The time-zero transition kernel is the identity kernel. -/
def InitialKernel
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  D.transitionKernel 0 = Kernel.id

/-- Continuous-time Chapman-Kolmogorov semigroup law for transition kernels. -/
def SemigroupLaw
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  ∀ s t : Time, D.transitionKernel (s + t) = D.transitionKernel t ∘ₖ D.transitionKernel s

/-- Measurability obligations for the scalar data in the Feynman-Kac boundary. -/
def ScalarDataMeasurable
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  Measurable D.potential ∧
    Measurable D.payoff ∧
      (∀ t : Time, Measurable (D.source t)) ∧
        (∀ t : Time, Measurable (D.solution t)) ∧
          ∀ t : Time, Measurable (D.probabilisticRepresentation t)

/-- Integrability obligations for the payoff and represented solution. -/
def KernelIntegrability
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  ∀ t x, Integrable D.payoff (D.transitionKernel t x)

/-- The solution starts from the supplied payoff at time zero. -/
def InitialCondition
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  ∀ x : State, D.solution 0 x = D.payoff x

/-- Time differentiability of the represented solution at positive times. -/
def DifferentiableInTime
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  ∀ (t : ℝ) (x : State) (ht : 0 < t),
    HasDerivAt (fun τ : ℝ => D.solution (Real.toNNReal τ) x)
      (D.timeDerivative ⟨t, le_of_lt ht⟩ x) t

/--
Parabolic PDE clause associated to the selected Feynman-Kac convention.

The Lean time variable is forward time-to-maturity `τ`; the canonical PDE is
`∂_τ u = L u - V u + f`.  Calendar-time presentations are recovered by
substituting `τ = T - t`, giving the usual backward terminal-value orientation.
-/
def ParabolicPDE
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  ∀ t x,
    D.timeDerivative t x =
      D.generator (D.solution t) x - D.potential x * D.solution t x + D.source t x

/-- The PDE clause unfolds with the canonical generator, killing, and source signs. -/
theorem parabolicPDE_iff_canonicalSigns
    {State : Type u} [MeasurableSpace State]
    {D : FeynmanKacData State} :
    ParabolicPDE D ↔
      ∀ t x,
        D.timeDerivative t x =
          D.generator (D.solution t) x - D.potential x * D.solution t x + D.source t x :=
  Iff.rfl

/--
The probabilistic representation clause expected from the full Feynman-Kac
formula.
-/
def FeynmanKacRepresentation
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  ∀ t x, D.solution t x = D.probabilisticRepresentation t x

/-- Boundary facts not currently supplied by a local stochastic-analysis API. -/
def PathFunctionalWellFormed
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  D.pathFunctionalWellFormed

/-- Well-formedness assumptions for the normalized Stage1 statement boundary. -/
def FeynmanKacHypotheses
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop :=
  InitialKernel D ∧
    MarkovKernelFamily D ∧
      SemigroupLaw D ∧
        ScalarDataMeasurable D ∧
          KernelIntegrability D ∧
            InitialCondition D ∧
              DifferentiableInTime D ∧
                ParabolicPDE D ∧
                  PathFunctionalWellFormed D

/--
Terminal conclusion package for the Feynman-Kac formula.

The representation equality is the missing continuous-time theorem.  The PDE,
semigroup, and initial-condition clauses are repeated so later proof work keeps
the analytic and probabilistic sides aligned at the same boundary.
-/
structure FeynmanKacConclusion
    {State : Type u} [MeasurableSpace State]
    (D : FeynmanKacData State) : Prop where
  representation : FeynmanKacRepresentation D
  parabolic_pde : ParabolicPDE D
  initial_condition : InitialCondition D
  semigroup_law : SemigroupLaw D

/--
Stage1 normalized statement shape for the Feynman-Kac formula.

This proposition-valued target freezes the Lean boundary a later formalization
must close: Markov transition kernels, PDE/generator side conditions,
measurability/integrability, and the expected exponential path-functional
representation.
-/
def StatementShape : Prop :=
  ∀ (State : Type u) [MeasurableSpace State],
    ∀ D : FeynmanKacData State,
      FeynmanKacHypotheses D → FeynmanKacConclusion D

/-- The normalized statement unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (State : Type u) [MeasurableSpace State],
        ∀ D : FeynmanKacData State,
          FeynmanKacHypotheses D → FeynmanKacConclusion D :=
  Iff.rfl

/-- Projection wrapper: a conclusion package exposes the representation equality. -/
theorem conclusion_representation
    {State : Type u} [MeasurableSpace State]
    {D : FeynmanKacData State}
    (h : FeynmanKacConclusion D) :
    FeynmanKacRepresentation D :=
  h.representation

/-- Projection wrapper: a conclusion package exposes the parabolic PDE clause. -/
theorem conclusion_parabolicPDE
    {State : Type u} [MeasurableSpace State]
    {D : FeynmanKacData State}
    (h : FeynmanKacConclusion D) :
    ParabolicPDE D :=
  h.parabolic_pde

/-- Projection wrapper: the hypotheses include Markov-kernel structure. -/
theorem hypotheses_markovKernel
    {State : Type u} [MeasurableSpace State]
    {D : FeynmanKacData State}
    (h : FeynmanKacHypotheses D) :
    ∀ t : Time, IsMarkovKernel (D.transitionKernel t) :=
  h.2.1

/-- Projection wrapper: the hypotheses include the parabolic PDE clause. -/
theorem hypotheses_parabolicPDE
    {State : Type u} [MeasurableSpace State]
    {D : FeynmanKacData State}
    (h : FeynmanKacHypotheses D) :
    ParabolicPDE D :=
  h.2.2.2.2.2.2.2.1

section KernelAnchors

variable {α : Type u} [MeasurableSpace α]
variable {β : Type v} [MeasurableSpace β]
variable {γ : Type w} [MeasurableSpace γ]

/-- Checked mathlib wrapper: deterministic kernels are Markov kernels. -/
theorem deterministic_isMarkovKernel_wrapper
    (f : α → β) (hf : Measurable f) :
    IsMarkovKernel (Kernel.deterministic f hf) :=
  inferInstance

/-- Checked mathlib wrapper: Markov kernels are closed under kernel composition. -/
theorem comp_isMarkovKernel_wrapper
    (κ : Kernel α β) (η : Kernel β γ)
    [IsMarkovKernel κ] [IsMarkovKernel η] :
    IsMarkovKernel (η ∘ₖ κ) :=
  inferInstance

/--
Checked mathlib wrapper: Chapman-Kolmogorov equation for powers of one
discrete-time transition kernel.
-/
theorem chapmanKolmogorov_kernel_pow_wrapper
    (κ : Kernel α α) (m n : ℕ) :
    κ ^ (m + n) = (κ ^ m) ∘ₖ (κ ^ n) :=
  Kernel.pow_add κ m n

/--
Checked mathlib wrapper: integral form of the Chapman-Kolmogorov equation for
the `m+n` step transition kernel.
-/
theorem chapmanKolmogorov_kernel_pow_apply_wrapper
    (κ : Kernel α α) (m n : ℕ) (a : α) {s : Set α}
    (hs : MeasurableSet s) :
    (κ ^ (m + n)) a s = ∫⁻ b, (κ ^ n) b s ∂((κ ^ m) a) :=
  Kernel.pow_add_apply_eq_lintegral κ m n a hs

/-- Checked mathlib wrapper: deterministic kernels evaluate Bochner integrals by substitution. -/
theorem deterministic_kernel_integral_wrapper
    [MeasurableSingletonClass β]
    (g : α → β) (hg : Measurable g) (f : β → ℝ) (a : α) :
    ∫ b, f b ∂Kernel.deterministic g hg a = f (g a) :=
  Kernel.integral_deterministic hg

/--
Public theorem-tree substrate leaf for S1-M-236-C006.

This is the checked discrete-time kernel-power law supplied by mathlib.  It is
recorded as reusable substrate for a future dynamic-programming/Feynman-Kac
approximation tree, not as the continuous-time Feynman-Kac theorem.
-/
theorem publicTree_kernel_pow_add_checked
    (κ : Kernel α α) (m n : ℕ) :
    κ ^ (m + n) = (κ ^ m) ∘ₖ (κ ^ n) :=
  chapmanKolmogorov_kernel_pow_wrapper κ m n

/--
Public theorem-tree substrate leaf for S1-M-236-C006.

This is the checked integral Chapman-Kolmogorov form for kernel powers.  It is
kernel substrate only; it does not provide path-functional integrability,
stochastic calculus, generator-domain, or parabolic-PDE closure.
-/
theorem publicTree_kernel_pow_add_apply_eq_lintegral_checked
    (κ : Kernel α α) (m n : ℕ) (a : α) {s : Set α}
    (hs : MeasurableSet s) :
    (κ ^ (m + n)) a s = ∫⁻ b, (κ ^ n) b s ∂((κ ^ m) a) :=
  chapmanKolmogorov_kernel_pow_apply_wrapper κ m n a hs

/--
Public theorem-tree substrate leaf for S1-M-236-C006.

This is the checked deterministic-kernel integral reduction supplied by
mathlib.  It is useful for deterministic transitions or boundary/payoff
substitution leaves, but it is not a terminal Feynman-Kac representation.
-/
theorem publicTree_kernel_integral_deterministic_checked
    [MeasurableSingletonClass β]
    (g : α → β) (hg : Measurable g) (f : β → ℝ) (a : α) :
    ∫ b, f b ∂Kernel.deterministic g hg a = f (g a) :=
  deterministic_kernel_integral_wrapper g hg f a

/--
Checked non-completion gate for S1-M-236-C006.

The public-tree kernel substrate above closes three mathlib wrapper leaves.
It deliberately does not assert `StatementShape`, `FeynmanKacRepresentation`,
or any continuous-time PDE/path-functional theorem.
-/
theorem publicTree_kernel_substrate_not_statementShape_completion :
    True :=
  trivial

end KernelAnchors

/-! ## Audit probes retained in the checked file. -/

#check Kernel
#check IsMarkovKernel
#check Kernel.id
#check Kernel.deterministic
#check Kernel.comp
#check Kernel.pow_add
#check Kernel.pow_add_apply_eq_lintegral
#check Kernel.integral_deterministic
#check publicTree_kernel_pow_add_checked
#check publicTree_kernel_pow_add_apply_eq_lintegral_checked
#check publicTree_kernel_integral_deterministic_checked
#check publicTree_kernel_substrate_not_statementShape_completion
#check MeasureTheory.Integrable
#check MeasureTheory.Filtration
#check HasDerivAt
#check DifferentiableOn
#check canonicalFeynmanKacConvention
#check parabolicPDE_iff_canonicalSigns
#check firstClosureTargetDecision
#check firstClosureTarget_selected
#check firstClosureTarget_nextContinuousTime
#check PathFunctionalExpectationPackage
#check HasPathFunctionalExpectationPackage
#check pathFunctional_measurable_leaf
#check pathFunctional_integrable_leaf
#check pathFunctional_expectation_leaf
#check pathFunctional_expectation_leaves

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Composition.Comp",
  "Mathlib.Probability.Kernel.Integral",
  "Mathlib.Probability.Kernel.MeasurableIntegral",
  "Mathlib.Probability.Kernel.WithDensity",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic",
  "Mathlib.Analysis.Calculus.Deriv.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.Kernel.id",
  "ProbabilityTheory.Kernel.deterministic",
  "ProbabilityTheory.Kernel.comp",
  "ProbabilityTheory.Kernel.pow_add",
  "ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral",
  "ProbabilityTheory.Kernel.integral_deterministic",
  "AwesomeTheorems.Stage1.S1_M_236.publicTree_kernel_pow_add_checked",
  "AwesomeTheorems.Stage1.S1_M_236.publicTree_kernel_pow_add_apply_eq_lintegral_checked",
  "AwesomeTheorems.Stage1.S1_M_236.publicTree_kernel_integral_deterministic_checked",
  "AwesomeTheorems.Stage1.S1_M_236.publicTree_kernel_substrate_not_statementShape_completion",
  "ProbabilityTheory.Kernel.withDensity",
  "ProbabilityTheory.Kernel.lintegral_withDensity",
  "MeasureTheory.Integrable",
  "MeasureTheory.Filtration",
  "HasDerivAt",
  "DifferentiableOn"
]

/--
Search terms that did not locate a terminal continuous-time Feynman-Kac theorem
in the local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Feynman",
  "Kac",
  "Feynman-Kac",
  "FeynmanKac",
  "stochastic integral",
  "diffusion generator",
  "Markov semigroup",
  "parabolic PDE",
  "heat semigroup",
  "exponential path functional"
]

/-! ## External Lean 4 audit record for child S1-M-236-C003. -/

/--
Primary-source Lean repository audit row for the Feynman-Kac external-anchor
search.  A row is evidence only; it is not theorem closure unless
`terminalFeynmanKacProof` is true and the project is pinned/imported/checked in
this repository.
-/
structure ExternalLeanAuditRecord where
  repoUrl : String
  commit : String
  leanToolchain : String
  license : String
  matchingAnchors : List String
  blocker : String
  terminalFeynmanKacProof : Bool

/--
External Lean projects audited for the search terms `FeynmanKac`,
`ItoFormula`, `StochasticIntegral`, `DiffusionGenerator`,
`MarkovSemigroup`, and `ParabolicPDE`.
-/
def externalLeanAuditRecords : List ExternalLeanAuditRecord := [
  {
    repoUrl := "https://github.com/RemyDegenne/brownian-motion"
    commit := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    license := "Apache-2.0"
    matchingAnchors := [
      "BrownianMotion.lean imports BrownianMotion.StochasticIntegral.*",
      "BrownianMotion/StochasticIntegral/SimpleProcess.lean defines elementary stochastic integrals",
      "BrownianMotion/StochasticIntegral/QuadraticVariation.lean defines quadraticVariation",
      "blueprint/src/chapters/stochastic_integral.tex includes an Ito formula target"
    ]
    blocker :=
      "No FeynmanKac/ParabolicPDE terminal theorem; README says stochastic integrals and Ito's lemma are in progress, the audited stochastic-integral tree contains unfinished proof placeholders, and the toolchain/mathlib commit differs from this repository."
    terminalFeynmanKacProof := false
  },
  {
    repoUrl := "https://github.com/mrdouglasny/markov-semigroups"
    commit := "eed89fc1bb5df45a1cde511bd4fea59235a80563"
    leanToolchain := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    matchingAnchors := [
      "MarkovSemigroups/Abstract/Hypercontractivity.lean: structure MarkovSemigroup",
      "MarkovSemigroups/Diffusion/CarreDuChamp.lean: class BakryEmerySpace",
      "MarkovSemigroups/Instances/WorkInProgress/Euclidean.lean: def ouSemigroup"
    ]
    blocker :=
      "Relevant Markov-semigroup and diffusion-generator adjacent infrastructure only; no FeynmanKac/ItoFormula/StochasticIntegral/ParabolicPDE terminal proof, and the project declares custom postulates plus quarantined unfinished proofs."
    terminalFeynmanKacProof := false
  },
  {
    repoUrl := "https://github.com/catskillsresearch/grundbegriffe"
    commit := "e8aa4fe66308d9e6e85d5bdedd9d981af99f17f7"
    leanToolchain := "leanprover-community/lean:3.24.0"
    license := "Apache-2.0"
    matchingAnchors := [
      "src/stochastic_process.lean defines probability_space, random_variable, stochastic_process"
    ]
    blocker :=
      "Lean 3 exploratory stochastic-process definitions only; no Lean 4 project, no stochastic integral, Markov semigroup, parabolic PDE, or Feynman-Kac terminal theorem."
    terminalFeynmanKacProof := false
  }
]

/-- The C003 external audit found no terminal proof that can close S1-M-236. -/
def terminalExternalFeynmanKacProofLocated : Bool := false

/--
Checked gate: the external audit does not create completed-state
repo-local integration debt, because no external terminal Feynman-Kac proof is
being claimed.
-/
theorem terminalExternalFeynmanKacProofLocated_eq_false :
    terminalExternalFeynmanKacProofLocated = false :=
  rfl

/-! ## Stage1 open-status gate for child S1-M-236-C007. -/

/--
Repo-local completion gate for this Stage1 slot.

The slot can leave `open` only after either a terminal local proof validates or
a pinned external Lean closure validates, and the public docs have been merged
consistently with that validation result.
-/
structure Stage1OpenStatusGate where
  terminalLocalProofValidated : Bool
  pinnedExternalClosureValidated : Bool
  publicDocsMergedConsistently : Bool
  stage1StatusOpen : Bool

/--
Current C007 gate record: no terminal local proof or pinned external closure
has passed validation, and the public backfill remains an integrator task.
-/
def c007Stage1OpenStatusGate : Stage1OpenStatusGate where
  terminalLocalProofValidated := false
  pinnedExternalClosureValidated := false
  publicDocsMergedConsistently := false
  stage1StatusOpen := true

/--
Checked C007 gate: S1-M-236 remains open until terminal repo-local or pinned
external Lean closure and public-doc consistency are both available.
-/
theorem c007_stage1_status_remains_open :
    c007Stage1OpenStatusGate.terminalLocalProofValidated = false ∧
      c007Stage1OpenStatusGate.pinnedExternalClosureValidated = false ∧
        c007Stage1OpenStatusGate.publicDocsMergedConsistently = false ∧
          c007Stage1OpenStatusGate.stage1StatusOpen = true :=
  ⟨rfl, rfl, rfl, rfl⟩

#check c007Stage1OpenStatusGate
#check c007_stage1_status_remains_open

end S1_M_236
end Stage1
end AwesomeTheorems
