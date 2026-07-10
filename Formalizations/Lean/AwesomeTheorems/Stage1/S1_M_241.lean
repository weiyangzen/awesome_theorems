import Mathlib.Probability.HasLaw
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.Kernel.Composition.Comp
import Mathlib.Probability.Kernel.CondDistrib
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Filtration

/-!
# S1-M-241 / THM-M-1048: Martingale problem and Markov characterization

This Stage1 artifact records a conservative Lean 4 statement boundary for the
martingale-problem characterization of Markov processes.

The pinned mathlib snapshot has probability measures, laws of random variables,
filtrations, adapted processes, martingales, conditional expectations, Markov
kernels, and kernel composition.  It does not expose a terminal theorem saying
that well-posedness of a martingale problem yields the corresponding Markov
process/transition-kernel characterization.  The declarations below therefore
freeze the statement shape and add checked wrappers around the available
mathlib anchors.  No terminal martingale-problem theorem is claimed here.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_241

universe uΩ uS uT

/-- The default time index for the normalized martingale-problem statement. -/
abbrev Time : Type :=
  ℝ≥0

/-- State-valued stochastic processes indexed by nonnegative real time. -/
abbrev StateProcess (Ω : Type uΩ) (State : Type uS) : Type (max uΩ uS) :=
  Time → Ω → State

/--
Test functions in the domain of a generator.

The generator is represented as a second real-valued function on the state
space.  A later integrator can specialize this structure to a Feller generator,
diffusion operator, finite-state `Q`-matrix, or another concrete domain API.
-/
structure GeneratorTestFunction
    (State : Type uS) [MeasurableSpace State] : Type uS where
  toFun : State → ℝ
  measurable_toFun : Measurable toFun
  generator : State → ℝ
  measurable_generator : Measurable generator

instance {State : Type uS} [MeasurableSpace State] :
    CoeFun (GeneratorTestFunction State) (fun _ => State → ℝ) where
  coe f := f.toFun

/--
Boundary data for a future martingale-problem characterization theorem.

`additiveGeneratorIntegral f t` represents the time integral
`∫_0^t A f (X_s) ds`.  It is kept as data at Stage1 because the local
dependency closure has no canonical continuous-time stochastic-integral or
generator-domain interface for this theorem.
-/
structure MartingaleProblemData
    (Ω : Type uΩ) (State : Type uS)
    [MeasurableSpace Ω] [MeasurableSpace State] : Type (max uΩ uS) where
  probabilityMeasure : Measure Ω
  initialLaw : Measure State
  process : StateProcess Ω State
  filtration : Filtration Time (inferInstance : MeasurableSpace Ω)
  transitionKernel : Time → Time → Kernel State State
  additiveGeneratorIntegral : GeneratorTestFunction State → Time → Ω → ℝ
  initialLaw_isProbability : IsProbabilityMeasure initialLaw

/--
The compensated real process attached to a test function:
`f(X_t) - f(X_0) - ∫_0^t A f(X_s) ds`.
-/
def MartingaleObservable
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State)
    (f : GeneratorTestFunction State) : Time → Ω → ℝ :=
  fun t ω =>
    f (D.process t ω) - f (D.process 0 ω) - D.additiveGeneratorIntegral f t ω

/-- The process is adapted to the supplied filtration. -/
def ProcessAdapted
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop :=
  Adapted D.filtration D.process

/-- The initial coordinate has the declared initial law. -/
def InitialLawMatches
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop :=
  HasLaw (D.process 0) D.initialLaw D.probabilityMeasure

/-- All declared transition objects are Markov kernels. -/
def TransitionKernelsMarkov
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop :=
  ∀ s t : Time, s ≤ t → IsMarkovKernel (D.transitionKernel s t)

/--
Each test function produces a martingale after subtracting the generator
compensator.
-/
def SolvesMartingaleProblem
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop :=
  ∀ f : GeneratorTestFunction State,
    Martingale (MartingaleObservable D f) D.filtration D.probabilityMeasure

/--
The finite-dimensional law of a process at a finite family of observation times.

For `times : Fin n → Time`, this is the push-forward of the ambient probability
measure along the coordinate map `ω ↦ fun i => X (times i) ω`.
-/
def FiniteDimensionalLaw
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (P : Measure Ω) (X : StateProcess Ω State)
    {n : ℕ} (times : Fin n → Time) : Measure (Fin n → State) :=
  Measure.map (fun ω i => X (times i) ω) P

/--
Equality of all finite-dimensional laws for two processes, allowing the two
processes to live on different probability spaces.
-/
def SameFiniteDimensionalLaws
    {Ω₁ Ω₂ : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω₁] [MeasurableSpace Ω₂] [MeasurableSpace State]
    (D₁ : MartingaleProblemData Ω₁ State)
    (D₂ : MartingaleProblemData Ω₂ State) : Prop :=
  ∀ (n : ℕ) (times : Fin n → Time),
    FiniteDimensionalLaw D₁.probabilityMeasure D₁.process times =
      FiniteDimensionalLaw D₂.probabilityMeasure D₂.process times

/--
Well-posedness of the martingale problem as finite-dimensional-law uniqueness.

Any two martingale-problem solution packages whose initial coordinates have the
same declared initial law as `D` must have identical finite-dimensional laws.
This is still a Stage1 assumption rather than a terminal proof, but it is no
longer an opaque placeholder proposition.
-/
def MartingaleProblemWellPosed
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop :=
  ∀ (Ω₁ Ω₂ : Type uΩ) [MeasurableSpace Ω₁] [MeasurableSpace Ω₂],
    ∀ (D₁ : MartingaleProblemData Ω₁ State)
      (D₂ : MartingaleProblemData Ω₂ State),
      D₁.initialLaw = D.initialLaw →
        D₂.initialLaw = D.initialLaw →
          InitialLawMatches D₁ →
            InitialLawMatches D₂ →
              SolvesMartingaleProblem D₁ →
                SolvesMartingaleProblem D₂ →
                  SameFiniteDimensionalLaws D₁ D₂

/--
Hypothesis package for the normalized statement boundary.

The `wellPosed` field is the high-risk mathematical/formalization bridge; the
other fields are current mathlib-facing process, law, kernel, and martingale
interfaces.
-/
structure MartingaleProblemHypotheses
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop where
  process_adapted : ProcessAdapted D
  initial_law : InitialLawMatches D
  transition_kernels : TransitionKernelsMarkov D
  martingale_problem : SolvesMartingaleProblem D
  wellPosed : MartingaleProblemWellPosed D

/--
Kernel-level Chapman-Kolmogorov law for the transition family.

The order follows mathlib's kernel-composition convention:
`η ∘ₖ κ` first uses `κ`, then uses `η`.
-/
def ChapmanKolmogorovLaw
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop :=
  ∀ r s t : Time, r ≤ s → s ≤ t →
    D.transitionKernel r t = D.transitionKernel s t ∘ₖ D.transitionKernel r s

/--
Conditional-law Markov property in test-function form.

For every real-valued measurable test function `g`, the conditional expectation
of `g(X_t)` given the filtration at time `s` is the transition-kernel average
of `g` from the current state `X_s`.
-/
def ConditionalLawMarkovProperty
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop :=
  ∀ s t : Time, s ≤ t →
    ∀ g : State → ℝ, Measurable g →
      Integrable (fun ω => g (D.process t ω)) D.probabilityMeasure →
        D.probabilityMeasure[fun ω => g (D.process t ω) | D.filtration s]
          =ᵐ[D.probabilityMeasure]
            fun ω => ∫ y, g y ∂(D.transitionKernel s t (D.process s ω))

/--
Preferred regular-conditional-law Markov property using mathlib's
`ProbabilityTheory.condDistrib` API.

When the state space is standard Borel and the ambient process measure is
finite, `condDistrib (X_t) (X_s) P` is the regular conditional distribution of
`X_t` given `X_s`.  The Markov property says that this conditional law is
almost surely the declared transition kernel `P_{s,t}` as a kernel-valued
function of the current state.
-/
def RegularConditionalLawMarkovProperty
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    [StandardBorelSpace State] [Nonempty State]
    (D : MartingaleProblemData Ω State) [IsFiniteMeasure D.probabilityMeasure] : Prop :=
  ∀ s t : Time, s ≤ t →
    ProbabilityTheory.condDistrib (D.process t) (D.process s) D.probabilityMeasure
      =ᵐ[D.probabilityMeasure.map (D.process s)]
        D.transitionKernel s t

/-- One-time marginal law obtained by pushing the initial law through the transition kernel. -/
def OneTimeMarginalLaw
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop :=
  ∀ t : Time, HasLaw (D.process t) (D.initialLaw.bind (D.transitionKernel 0 t))
    D.probabilityMeasure

/--
Conclusion package expected from a terminal martingale-problem
characterization theorem.
-/
structure MarkovCharacterizationConclusion
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : MartingaleProblemData Ω State) : Prop where
  regular_conditional_law_markov :
    ∀ [StandardBorelSpace State] [Nonempty State] [IsFiniteMeasure D.probabilityMeasure],
      RegularConditionalLawMarkovProperty D
  conditional_law_markov : ConditionalLawMarkovProperty D
  chapman_kolmogorov : ChapmanKolmogorovLaw D
  one_time_marginals : OneTimeMarginalLaw D
  transition_kernels : TransitionKernelsMarkov D

/--
Stage1 normalized statement shape for THM-M-1048.

For every stochastic process solving a well-posed martingale problem, a future
terminal theorem should produce the Markov characterization package: conditional
law Markov property, Chapman-Kolmogorov law, transition-kernel Markovness, and
one-time marginal laws.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) (State : Type uS)
    [MeasurableSpace Ω] [MeasurableSpace State],
    ∀ D : MartingaleProblemData Ω State,
      MartingaleProblemHypotheses D → MarkovCharacterizationConclusion D

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type uΩ) (State : Type uS)
      [MeasurableSpace Ω] [MeasurableSpace State],
      ∀ D : MartingaleProblemData Ω State,
        MartingaleProblemHypotheses D → MarkovCharacterizationConclusion D) :
    StatementShape.{uΩ, uS} :=
  h

/-- Projection wrapper: hypotheses expose the martingale-problem property. -/
theorem hypotheses_martingaleProblem
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (h : MartingaleProblemHypotheses D) :
    SolvesMartingaleProblem D :=
  h.martingale_problem

/-- Projection wrapper: hypotheses expose the well-posedness placeholder. -/
theorem hypotheses_wellPosed
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (h : MartingaleProblemHypotheses D) :
    MartingaleProblemWellPosed D :=
  h.wellPosed

/-- Apply well-posedness to two solution packages with the same initial law. -/
theorem wellPosed_sameFiniteDimensionalLaws
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (h : MartingaleProblemWellPosed D)
    (Ω₁ Ω₂ : Type uΩ) [MeasurableSpace Ω₁] [MeasurableSpace Ω₂]
    (D₁ : MartingaleProblemData Ω₁ State)
    (D₂ : MartingaleProblemData Ω₂ State)
    (hD₁ : D₁.initialLaw = D.initialLaw)
    (hD₂ : D₂.initialLaw = D.initialLaw)
    (hinit₁ : InitialLawMatches D₁)
    (hinit₂ : InitialLawMatches D₂)
    (hmp₁ : SolvesMartingaleProblem D₁)
    (hmp₂ : SolvesMartingaleProblem D₂) :
    SameFiniteDimensionalLaws D₁ D₂ :=
  h Ω₁ Ω₂ D₁ D₂ hD₁ hD₂ hinit₁ hinit₂ hmp₁ hmp₂

/-- Projection wrapper: a test function's compensated process is a martingale. -/
theorem observable_martingale
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (h : MartingaleProblemHypotheses D)
    (f : GeneratorTestFunction State) :
    Martingale (MartingaleObservable D f) D.filtration D.probabilityMeasure :=
  h.martingale_problem f

/-- Checked martingale anchor: each compensated coordinate is integrable. -/
theorem observable_integrable
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (h : MartingaleProblemHypotheses D)
    (f : GeneratorTestFunction State) (t : Time) :
    Integrable (MartingaleObservable D f t) D.probabilityMeasure :=
  (observable_martingale h f).integrable t

/-- Checked martingale anchor: each compensated process is strongly adapted. -/
theorem observable_stronglyAdapted
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (h : MartingaleProblemHypotheses D)
    (f : GeneratorTestFunction State) :
    StronglyAdapted D.filtration (MartingaleObservable D f) :=
  (observable_martingale h f).stronglyAdapted

/-- Checked martingale anchor: conditional expectation recovers earlier compensated values. -/
theorem observable_condExp_ae_eq
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (h : MartingaleProblemHypotheses D)
    (f : GeneratorTestFunction State) {s t : Time} (hst : s ≤ t) :
    D.probabilityMeasure[MartingaleObservable D f t | D.filtration s]
      =ᵐ[D.probabilityMeasure] MartingaleObservable D f s :=
  (observable_martingale h f).condExp_ae_eq hst

/-- Projection wrapper: hypotheses expose Markovness of transition kernels. -/
theorem hypotheses_transitionKernels
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (h : MartingaleProblemHypotheses D) :
    TransitionKernelsMarkov D :=
  h.transition_kernels

/-- Projection wrapper: conclusions expose the conditional-law Markov property. -/
theorem conclusion_conditionalLawMarkov
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (C : MarkovCharacterizationConclusion D) :
    ConditionalLawMarkovProperty D :=
  C.conditional_law_markov

/-- Projection wrapper: conclusions expose the preferred regular conditional law. -/
theorem conclusion_regularConditionalLawMarkov
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    [StandardBorelSpace State] [Nonempty State]
    {D : MartingaleProblemData Ω State} [IsFiniteMeasure D.probabilityMeasure]
    (C : MarkovCharacterizationConclusion D) :
    RegularConditionalLawMarkovProperty D :=
  C.regular_conditional_law_markov

/-- Projection wrapper: conclusions expose the Chapman-Kolmogorov law. -/
theorem conclusion_chapmanKolmogorov
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (C : MarkovCharacterizationConclusion D) :
    ChapmanKolmogorovLaw D :=
  C.chapman_kolmogorov

/-- Projection wrapper: conclusions expose the one-time marginal law. -/
theorem conclusion_oneTimeMarginalLaw
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (C : MarkovCharacterizationConclusion D) :
    OneTimeMarginalLaw D :=
  C.one_time_marginals

/-- Projection wrapper: conclusions expose Markovness of transition kernels. -/
theorem conclusion_transitionKernels
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : MartingaleProblemData Ω State}
    (C : MarkovCharacterizationConclusion D) :
    TransitionKernelsMarkov D :=
  C.transition_kernels

section KernelAnchors

variable {α : Type uS} [MeasurableSpace α]
variable {β : Type uT} [MeasurableSpace β]
variable {γ : Type uΩ} [MeasurableSpace γ]

/-- Checked mathlib wrapper: deterministic kernels are Markov kernels. -/
theorem deterministicKernel_isMarkov
    (f : α → β) (hf : Measurable f) :
    IsMarkovKernel (Kernel.deterministic f hf) :=
  inferInstance

/-- Checked mathlib wrapper: Markov kernels are closed under kernel composition. -/
theorem compKernel_isMarkov
    (κ : Kernel α β) (η : Kernel β γ)
    [IsMarkovKernel κ] [IsMarkovKernel η] :
    IsMarkovKernel (η ∘ₖ κ) :=
  inferInstance

/-- Checked mathlib wrapper: Chapman-Kolmogorov equation for powers of one kernel. -/
theorem kernel_pow_add_wrapper
    (κ : Kernel α α) (m n : ℕ) :
    κ ^ (m + n) = (κ ^ m) ∘ₖ (κ ^ n) :=
  Kernel.pow_add κ m n

/--
Checked mathlib wrapper: the conditional distribution of `X_t` given `X_s`
pushes the one-time law of `X_s` forward to the one-time law of `X_t`.
-/
theorem process_condDistrib_comp_map
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    [StandardBorelSpace State] [Nonempty State]
    {D : MartingaleProblemData Ω State} [IsFiniteMeasure D.probabilityMeasure]
    {s t : Time}
    (hs : AEMeasurable (D.process s) D.probabilityMeasure)
    (ht : AEMeasurable (D.process t) D.probabilityMeasure) :
    ProbabilityTheory.condDistrib (D.process t) (D.process s) D.probabilityMeasure ∘ₘ
        D.probabilityMeasure.map (D.process s) =
      D.probabilityMeasure.map (D.process t) :=
  ProbabilityTheory.condDistrib_comp_map hs ht

/--
Checked mathlib wrapper: for scalar test functions, regular conditional
distributions realize conditional expectation with respect to the
current-state sigma-algebra.
-/
theorem process_condExp_ae_eq_integral_condDistrib
    {Ω : Type uΩ} {State : Type uS}
    [MeasurableSpace Ω] [MeasurableSpace State]
    [StandardBorelSpace State] [Nonempty State]
    {D : MartingaleProblemData Ω State} [IsFiniteMeasure D.probabilityMeasure]
    {s t : Time} {g : State → ℝ}
    (hs : Measurable (D.process s))
    (ht : AEMeasurable (D.process t) D.probabilityMeasure)
    (hg : StronglyMeasurable g)
    (hgint : Integrable (fun ω => g (D.process t ω)) D.probabilityMeasure) :
    D.probabilityMeasure[fun ω => g (D.process t ω) |
        MeasurableSpace.comap (D.process s) inferInstance]
      =ᵐ[D.probabilityMeasure]
        fun ω =>
          ∫ y, g y ∂(ProbabilityTheory.condDistrib
            (D.process t) (D.process s) D.probabilityMeasure (D.process s ω)) :=
  ProbabilityTheory.condExp_ae_eq_integral_condDistrib hs ht hg hgint

end KernelAnchors

/-! ## S1-M-241-C006 discrete-time kernel special case -/

section DiscreteTimeSpecialCase

variable {α : Type uS} [MeasurableSpace α]

/--
The elapsed-time transition kernel generated by one discrete-time Markov
kernel.

At Stage1 this is the finite/discrete-time special case requested before the
continuous-time generator theorem: time is `ℕ`, and the `n`-step transition is
the `n`th power of one kernel.
-/
def DiscreteTimeTransitionKernel (κ : Kernel α α) (n : ℕ) : Kernel α α :=
  κ ^ n

/-- Discrete-time Chapman-Kolmogorov law for one kernel-powered transition family. -/
def DiscreteTimeChapmanKolmogorovLaw (κ : Kernel α α) : Prop :=
  ∀ m n : ℕ,
    DiscreteTimeTransitionKernel κ (m + n) =
      DiscreteTimeTransitionKernel κ m ∘ₖ DiscreteTimeTransitionKernel κ n

/-- Powers of a Markov kernel are Markov kernels. -/
theorem discreteTimeTransitionKernel_isMarkov
    (κ : Kernel α α) [IsMarkovKernel κ] (n : ℕ) :
    IsMarkovKernel (DiscreteTimeTransitionKernel κ n) := by
  dsimp [DiscreteTimeTransitionKernel]
  induction n with
  | zero =>
      change IsMarkovKernel (Kernel.id : Kernel α α)
      infer_instance
  | succ n hn =>
      rw [pow_succ]
      haveI : IsMarkovKernel (κ ^ n : Kernel α α) := hn
      exact Kernel.IsMarkovKernel.comp (η := (κ ^ n : Kernel α α)) (κ := κ)

/--
Checked discrete-time Chapman-Kolmogorov identity, proved by mathlib's
`Kernel.pow_add`.
-/
theorem discreteTimeTransitionKernel_chapmanKolmogorov
    (κ : Kernel α α) :
    DiscreteTimeChapmanKolmogorovLaw κ := by
  intro m n
  exact Kernel.pow_add κ m n

/--
Integral form of the same discrete-time Chapman-Kolmogorov identity.

This leaf states the eventwise transition probability after `m + n` steps as
the integral of the `n`-step event probability against the `m`-step transition.
-/
theorem discreteTimeTransitionKernel_apply_eq_lintegral
    (κ : Kernel α α) (m n : ℕ) (a : α) {s : Set α}
    (hs : MeasurableSet s) :
    DiscreteTimeTransitionKernel κ (m + n) a s =
      ∫⁻ b, DiscreteTimeTransitionKernel κ n b s
        ∂(DiscreteTimeTransitionKernel κ m a) := by
  dsimp [DiscreteTimeTransitionKernel]
  exact Kernel.pow_add_apply_eq_lintegral κ m n a hs

/--
C006 package: the discrete-time special case closed locally for kernel powers.

This is a substrate package for the martingale-problem entry.  It does not
prove that well-posed continuous-time martingale problems are Markov.
-/
structure DiscreteTimeKernelSpecialCase
    (α : Type uS) [MeasurableSpace α] : Prop where
  kernel_power_markov_leaf :
    ∀ (κ : Kernel α α), IsMarkovKernel κ →
      ∀ n : ℕ, IsMarkovKernel (DiscreteTimeTransitionKernel κ n)
  kernel_power_chapman_kolmogorov_leaf :
    ∀ κ : Kernel α α, DiscreteTimeChapmanKolmogorovLaw κ
  integral_kernel_power_leaf :
    ∀ (κ : Kernel α α) (m n : ℕ) (a : α) {s : Set α},
      MeasurableSet s →
        DiscreteTimeTransitionKernel κ (m + n) a s =
          ∫⁻ b, DiscreteTimeTransitionKernel κ n b s
            ∂(DiscreteTimeTransitionKernel κ m a)

/-- Checked C006 package instance. -/
theorem c006DiscreteTimeKernelSpecialCase
    (α : Type uS) [MeasurableSpace α] :
    DiscreteTimeKernelSpecialCase α where
  kernel_power_markov_leaf := by
    intro κ hκ n
    haveI : IsMarkovKernel κ := hκ
    exact discreteTimeTransitionKernel_isMarkov κ n
  kernel_power_chapman_kolmogorov_leaf := by
    intro κ
    exact discreteTimeTransitionKernel_chapmanKolmogorov κ
  integral_kernel_power_leaf := by
    intro κ m n a s hs
    exact discreteTimeTransitionKernel_apply_eq_lintegral κ m n a hs

/--
`false` records that C006 is not a terminal martingale-problem
characterization theorem.
-/
def c006DiscreteTimeSpecialCaseIsTerminalMartingaleProblemTheorem : Bool := false

/-- Checked sanity gate for the C006 non-terminal status flag. -/
theorem c006DiscreteTimeSpecialCaseIsTerminalMartingaleProblemTheorem_eq_false :
    c006DiscreteTimeSpecialCaseIsTerminalMartingaleProblemTheorem = false :=
  rfl

/-- C006 checked anchor names for serial public backfill. -/
def c006DiscreteTimeSpecialCaseAnchorNames : List String := [
  "ProbabilityTheory.Kernel.pow_add",
  "ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral",
  "AwesomeTheorems.Stage1.S1_M_241.DiscreteTimeTransitionKernel",
  "AwesomeTheorems.Stage1.S1_M_241.discreteTimeTransitionKernel_isMarkov",
  "AwesomeTheorems.Stage1.S1_M_241.discreteTimeTransitionKernel_chapmanKolmogorov",
  "AwesomeTheorems.Stage1.S1_M_241.discreteTimeTransitionKernel_apply_eq_lintegral",
  "AwesomeTheorems.Stage1.S1_M_241.c006DiscreteTimeKernelSpecialCase"
]

/-- C006 local leaf-budget ledger. -/
def c006LocalLeafBudgetLedger : List String := [
  "C006-L01 checked-definition: DiscreteTimeTransitionKernel defines the n-step kernel as κ^n.",
  "C006-L02 checked-leaf: discreteTimeTransitionKernel_isMarkov proves kernel powers are Markov under IsMarkovKernel κ and is under 100 proof steps.",
  "C006-L03 checked-leaf: discreteTimeTransitionKernel_chapmanKolmogorov proves the discrete Chapman-Kolmogorov law by Kernel.pow_add and is under 100 proof steps.",
  "C006-L04 checked-leaf: discreteTimeTransitionKernel_apply_eq_lintegral proves the eventwise integral form by Kernel.pow_add_apply_eq_lintegral and is under 100 proof steps.",
  "C006-L05 non-terminal boundary: c006DiscreteTimeSpecialCaseIsTerminalMartingaleProblemTheorem_eq_false records that this substrate is not the continuous-time martingale-problem theorem."
]

/--
C006 repo-local integration-debt flag.

The proof bodies used here are local wrappers around pinned mathlib kernel
facts inside the Lake closure, so this child retains no anchor-only external
integration debt.
-/
def c006RepoLocalIntegrationDebtRetained : Bool := false

/-- Checked sanity gate for the C006 integration-debt flag. -/
theorem c006RepoLocalIntegrationDebtRetained_eq_false :
    c006RepoLocalIntegrationDebtRetained = false :=
  rfl

end DiscreteTimeSpecialCase

/-! ## S1-M-241-C007 theorem-tree leaf ledger -/

/--
C007 theorem-tree package split for the martingale-problem entry.

This is checked metadata, not a terminal proof.  It fixes the package names an
integrator should use when serially backfilling the public Stage1 surface.
-/
def c007TheoremTreePackages : List String := [
  "S1-M-241.P1.statement_normalization",
  "S1-M-241.P2.mathlib_object_model",
  "S1-M-241.P3.martingale_problem_branch",
  "S1-M-241.P4.wellposedness_branch",
  "S1-M-241.P5.regular_conditional_law_bridge",
  "S1-M-241.P6.discrete_kernel_substrate",
  "S1-M-241.P7.transition_semigroup_branch",
  "S1-M-241.P8.repo_local_closure_gate"
]

/--
Checked local leaves already available in this artifact.

Each listed item is either a definition/projection wrapper or a proof wrapper
whose Lean body is below the M0387 100-step leaf budget and is validated by the
file-level Lean command.  These leaves do not prove the terminal martingale
problem characterization.
-/
def c007CheckedLocalLeafLedger : List String := [
  "C007-L01 checked-definition: Time and StateProcess fix the nonnegative-real time index and state-valued process shape.",
  "C007-L02 checked-definition: GeneratorTestFunction records measurable test functions and measurable generator images.",
  "C007-L03 checked-definition: MartingaleProblemData records process, filtration, initial law, transition kernels, and Stage1 compensator data.",
  "C007-L04 checked-definition: MartingaleObservable defines the compensated test-function process.",
  "C007-L05 checked-definition: ProcessAdapted, InitialLawMatches, TransitionKernelsMarkov, and SolvesMartingaleProblem align the statement with mathlib anchors.",
  "C007-L06 checked-definition: FiniteDimensionalLaw and SameFiniteDimensionalLaws provide the finite-dimensional-law uniqueness target.",
  "C007-L07 checked-definition: MartingaleProblemWellPosed is no longer an opaque Prop placeholder; it is finite-dimensional-law uniqueness for all solution packages with the same initial law.",
  "C007-L08 checked-definition: RegularConditionalLawMarkovProperty records the preferred condDistrib Markov-property target.",
  "C007-L09 checked-wrapper: observable_martingale, observable_integrable, observable_stronglyAdapted, and observable_condExp_ae_eq expose mathlib martingale consequences.",
  "C007-L10 checked-wrapper: deterministicKernel_isMarkov, compKernel_isMarkov, kernel_pow_add_wrapper, process_condDistrib_comp_map, and process_condExp_ae_eq_integral_condDistrib expose kernel and conditional-law anchors.",
  "C007-L11 checked-package: c006DiscreteTimeKernelSpecialCase closes the discrete-time kernel-power substrate by local wrappers around pinned mathlib facts."
]

/--
Open M0387 leaves remaining before the parent package can be completed.

These are deliberately recorded as unchecked/open because no repo-local proof
body or pinned external dependency currently closes the terminal theorem.
-/
def c007OpenLeafLedger : List String := [
  "C007-L12 open-formalization: prove or import the continuous-time generator-domain bridge from martingale-problem well-posedness to Markov characterization.",
  "C007-L13 open-formalization: derive ConditionalLawMarkovProperty over the supplied filtration from the regular conditional-law Markov property or replace it with a canonical mathlib conditional-distribution API.",
  "C007-L14 open-formalization: prove OneTimeMarginalLaw for the declared transition kernels from initial law plus the Markov characterization.",
  "C007-L15 open-formalization: prove ChapmanKolmogorovLaw for the continuous-time transition family, not just the discrete kernel-power substrate.",
  "C007-L16 open-external-audit: rerun authenticated Lean 4 primary-source search for terminal martingale-problem proofs and pin/import/check any exact proof found, or record a concrete integration blocker.",
  "C007-L17 open-public-integration: serially merge the checked leaf ledger and validation record into the authoritative public blueprint/todo surfaces."
]

/-- C007 checked anchor names for serial public backfill. -/
def c007LeafLedgerAnchorNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_241.c007TheoremTreePackages",
  "AwesomeTheorems.Stage1.S1_M_241.c007CheckedLocalLeafLedger",
  "AwesomeTheorems.Stage1.S1_M_241.c007OpenLeafLedger",
  "AwesomeTheorems.Stage1.S1_M_241.c007AllParentLeavesClosed",
  "AwesomeTheorems.Stage1.S1_M_241.c007RepoLocalIntegrationDebtRetained_eq_false"
]

/--
C007 completion gate for the full parent theorem.

The value is intentionally false: the parent still has open formalization and
public-integration leaves, so this child must not mark the package complete.
-/
def c007AllParentLeavesClosed : Bool := false

/-- Checked sanity gate: C007 does not close all parent leaves. -/
theorem c007AllParentLeavesClosed_eq_false :
    c007AllParentLeavesClosed = false :=
  rfl

/--
C007 repo-local integration-debt flag.

No external Lean 4 terminal proof is used as anchor-only completion evidence in
this child, and the parent is kept non-complete.  If a later audit finds an
external proof, it must be pinned/imported/checked or listed as a concrete
blocker before any completion claim.
-/
def c007RepoLocalIntegrationDebtRetained : Bool := false

/-- Checked sanity gate for the C007 integration-debt flag. -/
theorem c007RepoLocalIntegrationDebtRetained_eq_false :
    c007RepoLocalIntegrationDebtRetained = false :=
  rfl

/-- Public Stage1 boundary names that the serial integrator should surface. -/
def publicStatementBoundaryNames : List String := [
  "MartingaleProblemData",
  "MartingaleObservable",
  "SolvesMartingaleProblem",
  "FiniteDimensionalLaw",
  "SameFiniteDimensionalLaws",
  "MartingaleProblemWellPosed",
  "RegularConditionalLawMarkovProperty",
  "ConditionalLawMarkovProperty",
  "MarkovCharacterizationConclusion",
  "StatementShape"
]

/--
Pinned mathlib revision audited for the Stage1 martingale-problem substrate.

This records the local Lake dependency revision used for the anchor checks
below; it is not a terminal martingale-problem theorem claim.
-/
def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Composition.Comp",
  "Mathlib.Probability.Kernel.Composition.MeasureComp",
  "Mathlib.Probability.Kernel.CondDistrib",
  "Mathlib.Probability.Kernel.Condexp",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Independence.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.stronglyAdapted",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.Martingale.condExp_ae_eq",
  "MeasureTheory.IsStoppingTime",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.condDistrib",
  "ProbabilityTheory.condDistrib_comp_map",
  "ProbabilityTheory.condExp_ae_eq_integral_condDistrib",
  "ProbabilityTheory.Kernel.deterministic",
  "ProbabilityTheory.Kernel.comp",
  "ProbabilityTheory.Kernel.pow_add",
  "ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral",
  "MeasureTheory.Measure.bind",
  "MeasureTheory.IsProbabilityMeasure"
]

/--
Search terms that did not locate a terminal martingale-problem Markov
characterization theorem in the pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "martingale problem",
  "MartingaleProblem",
  "Markov process",
  "MarkovProcess",
  "Markov property",
  "conditional law Markov",
  "well-posed martingale problem",
  "Dynkin formula",
  "infinitesimal generator",
  "Feller semigroup"
]

/--
External Lean 4 primary-source search terms required before upgrading this slot.

The authenticated GitHub code-search pass could not be completed in the
2026-05-01 child run because the local `gh` client had no authenticated host
and the GitHub REST code-search endpoint returned `401 Requires authentication`.
This is an integration blocker, not evidence of theorem absence.
-/
def externalPrimarySourceSearchTerms : List String := [
  "MartingaleProblem",
  "martingale problem",
  "MarkovProcess",
  "Dynkin formula",
  "Feller semigroup",
  "infinitesimal generator"
]

/-- Checked status note for the external-audit child pass. -/
def externalPrimarySourceAuditStatus : String :=
  "blocked: authenticated GitHub Lean code search unavailable locally; no external terminal proof was pinned, imported, or checked"

/-- Concrete blocker that prevents marking the external audit complete. -/
def externalPrimarySourceIntegrationBlocker : String :=
  "Provide GH_TOKEN or run gh auth login, rerun authenticated code search for the required Lean 4 terms, then pin/import/check any terminal martingale-problem proof found."

/-! ## Audit probes -/

#check Time
#check StateProcess
#check GeneratorTestFunction
#check MartingaleProblemData
#check MartingaleObservable
#check SolvesMartingaleProblem
#check FiniteDimensionalLaw
#check SameFiniteDimensionalLaws
#check MartingaleProblemWellPosed
#check MartingaleProblemHypotheses
#check RegularConditionalLawMarkovProperty
#check ConditionalLawMarkovProperty
#check MarkovCharacterizationConclusion
#check StatementShape
#check publicStatementBoundaryNames
#check auditedMathlibRevision
#check externalPrimarySourceSearchTerms
#check externalPrimarySourceAuditStatus
#check externalPrimarySourceIntegrationBlocker
#check observable_martingale
#check observable_integrable
#check observable_stronglyAdapted
#check observable_condExp_ae_eq
#check hypotheses_wellPosed
#check wellPosed_sameFiniteDimensionalLaws
#check deterministicKernel_isMarkov
#check compKernel_isMarkov
#check kernel_pow_add_wrapper
#check process_condDistrib_comp_map
#check process_condExp_ae_eq_integral_condDistrib
#check DiscreteTimeTransitionKernel
#check DiscreteTimeChapmanKolmogorovLaw
#check discreteTimeTransitionKernel_isMarkov
#check discreteTimeTransitionKernel_chapmanKolmogorov
#check discreteTimeTransitionKernel_apply_eq_lintegral
#check DiscreteTimeKernelSpecialCase
#check c006DiscreteTimeKernelSpecialCase
#check c006DiscreteTimeSpecialCaseAnchorNames
#check c006LocalLeafBudgetLedger
#check c006RepoLocalIntegrationDebtRetained_eq_false
#check c007TheoremTreePackages
#check c007CheckedLocalLeafLedger
#check c007OpenLeafLedger
#check c007LeafLedgerAnchorNames
#check c007AllParentLeavesClosed_eq_false
#check c007RepoLocalIntegrationDebtRetained_eq_false
#check conclusion_regularConditionalLawMarkov
#check conclusion_oneTimeMarginalLaw
#check conclusion_transitionKernels
#check MeasureTheory.Filtration
#check MeasureTheory.Adapted
#check MeasureTheory.StronglyAdapted
#check MeasureTheory.Martingale
#check MeasureTheory.Martingale.condExp_ae_eq
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.Kernel
#check ProbabilityTheory.IsMarkovKernel
#check ProbabilityTheory.condDistrib
#check ProbabilityTheory.condDistrib_comp_map
#check ProbabilityTheory.condExp_ae_eq_integral_condDistrib
#check ProbabilityTheory.Kernel.pow_add
#check ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral

end S1_M_241
end Stage1
end AwesomeTheorems
