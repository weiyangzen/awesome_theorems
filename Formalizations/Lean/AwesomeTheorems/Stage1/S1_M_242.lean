import Mathlib.Probability.HasLaw
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Adapted
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# S1-M-242 / THM-M-1049: Stroock-Varadhan martingale problem

This Stage1 artifact records a conservative Lean 4 boundary for the
Stroock-Varadhan martingale-problem characterization of diffusion processes.

Informally, a diffusion with generator `L` is characterized by the requirement
that, for each admissible test function `f`,

`f(X_t) - f(X_0) - ∫_0^t L f (X_s) ds`

is a martingale.  Well-posedness of this martingale problem then identifies the
law/transition structure of the diffusion.

The pinned mathlib snapshot has probability laws, Markov kernels, filtrations,
adapted processes, conditional expectations, and martingales.  It does not
expose a terminal diffusion-generator API, stochastic integral API, or
Stroock-Varadhan theorem.  The declarations below therefore freeze a typed
statement shape and expose low-risk wrappers around the available substrate.
No terminal proof of the Stroock-Varadhan theorem is claimed here.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory
open intervalIntegral

namespace AwesomeTheorems.Stage1.S1_M_242

universe uΩ uE

/-- Continuous time index used by this normalized Stage1 boundary. -/
abbrev Time : Type :=
  ℝ

/-- A state-valued stochastic process indexed by continuous time. -/
abbrev StochasticProcess (Ω : Type uΩ) (E : Type uE) : Type (max uΩ uE) :=
  Time → Ω → E

/-- Real-valued test functions on the state space. -/
abbrev TestFunction (E : Type uE) : Type uE :=
  E → ℝ

/--
Candidate roots for the future diffusion-generator branch.

The Stage1 branch decision is intentionally represented as data, not prose, so
later workers can point to a checked repo-local declaration when replacing the
placeholder `diffusionGeneratorShape`.
-/
inductive DiffusionGeneratorBranch : Type where
  | sdeCoefficients
  | fellerSemigroup
  | separateDiffusionGeneratorStructure
  deriving DecidableEq

/--
Selected root for `THM-M-1049.diffusion_generator`.

The martingale-problem statement is generator-first: SDE coefficients can later
instantiate the operator, and Feller semigroups belong to the transition-law
side, but the local branch should be built around a separate diffusion-generator
structure.
-/
def selectedDiffusionGeneratorBranch : DiffusionGeneratorBranch :=
  .separateDiffusionGeneratorStructure

/--
Repo-local shell for the separate diffusion-generator structure selected by
`THM-M-1049.diffusion_generator`.

This is still a statement boundary.  It records the objects a future concrete
branch must replace: a test-function domain, an operator on test functions, and
the analytic side conditions needed to feed the compensated martingale process.
-/
structure DiffusionGeneratorStructure
    (E : Type uE) [TopologicalSpace E] [MeasurableSpace E] :
    Type uE where
  domain : Set (TestFunction E)
  operator : TestFunction E → TestFunction E
  admissible : Prop
  domainClosedUnderOperator : Prop
  pathwiseCompensatorCompatible : Prop

/--
Data for a future Stroock-Varadhan martingale-problem statement.

The field `accumulatedGenerator` stands for
`∫_0^t generator f (process s) ds`.  It is explicit because the current local
dependency closure does not contain the diffusion-generator and stochastic
calculus API needed to define the classical integral package canonically.
-/
structure MartingaleProblemData
    (Ω : Type uΩ) (E : Type uE)
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E] :
    Type (max uΩ uE) where
  probabilityMeasure : Measure Ω
  isProbability : IsProbabilityMeasure probabilityMeasure
  process : StochasticProcess Ω E
  filtration : Filtration Time (inferInstance : MeasurableSpace Ω)
  adapted : Adapted filtration process
  initialLaw : Measure E
  initialHasLaw : HasLaw (process 0) initialLaw probabilityMeasure
  testFunctions : Set (TestFunction E)
  generator : TestFunction E → TestFunction E
  accumulatedGenerator : TestFunction E → Time → Ω → ℝ
  transitionKernel : Time → Kernel E E
  transitionKernelMarkov : ∀ t : Time, 0 ≤ t → IsMarkovKernel (transitionKernel t)
  diffusionGeneratorShape : Prop
  accumulatedGeneratorIsIntegral : Prop
  pathRegularity : Prop
  martingaleProblemWellPosed : Prop
  transitionLawCharacterizesProcess : Prop

/--
A separate diffusion-generator package realizes the legacy generator fields in
`MartingaleProblemData`.

This keeps C004's branch choice integration-ready without changing the existing
data constructor used by the sibling Stage1 children.
-/
structure DiffusionGeneratorBranchRealization
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E)
    (G : DiffusionGeneratorStructure E) : Prop where
  testFunctions_subset_domain : D.testFunctions ⊆ G.domain
  generator_eq_operator : D.generator = G.operator
  diffusion_generator_shape : D.diffusionGeneratorShape
  admissible : G.admissible
  domain_closed_under_operator : G.domainClosedUnderOperator
  pathwise_compensator_compatible : G.pathwiseCompensatorCompatible

/-- The selected diffusion-generator branch is the separate structure branch. -/
theorem selectedDiffusionGeneratorBranch_eq :
    selectedDiffusionGeneratorBranch = .separateDiffusionGeneratorStructure :=
  rfl

/-- A realized separate generator package supplies the legacy generator field. -/
theorem diffusionGeneratorRealization_generator_eq
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E} {G : DiffusionGeneratorStructure E}
    (hG : DiffusionGeneratorBranchRealization D G) :
    D.generator = G.operator :=
  hG.generator_eq_operator

/-- A realized separate generator package supplies the old shape predicate. -/
theorem diffusionGeneratorRealization_shape
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E} {G : DiffusionGeneratorStructure E}
    (hG : DiffusionGeneratorBranchRealization D G) :
    D.diffusionGeneratorShape :=
  hG.diffusion_generator_shape

/--
The generator-compensated process associated to a test function.

For a completed formalization, `accumulatedGenerator f t ω` should be replaced
or justified by the integral of `generator f` along the sample path up to time
`t`.
-/
def GeneratorCompensated
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (f : TestFunction E) :
    Time → Ω → ℝ :=
  fun t ω => f (D.process t ω) - f (D.process 0 ω) - D.accumulatedGenerator f t ω

/--
The selected deterministic time-integrand for the generator bridge.

This is the concrete path API chosen for replacing the placeholder
`accumulatedGenerator`: for a fixed sample point `ω`, integrate the real-valued
path `s ↦ generator f (process s ω)` over the deterministic time interval.
-/
def generatorPathIntegrand
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (f : TestFunction E) (ω : Ω) :
    Time → ℝ :=
  fun s => D.generator f (D.process s ω)

/--
Canonical accumulated generator selected by `THM-M-1049.generator_bridge`.

The bridge uses mathlib's real interval-integral API
`∫ s in 0..t, ...`, not a stochastic integral.  Stochastic calculus remains a
separate future branch; the Stroock-Varadhan compensator itself is the
deterministic time integral of the generator evaluated along each sample path.
-/
def canonicalAccumulatedGenerator
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (f : TestFunction E) :
    Time → Ω → ℝ :=
  fun t ω => ∫ s in (0 : Time)..t, generatorPathIntegrand D f ω s

/--
Concrete replacement predicate for `accumulatedGeneratorIsIntegral`.

It records both local interval-integrability of the pathwise generator and the
repo-local equality requirement saying that the legacy placeholder field
`D.accumulatedGenerator` agrees almost everywhere with the canonical interval
integral for each admissible test function and time.
-/
def AccumulatedGeneratorIsIntervalIntegral
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Prop :=
  (∀ f : TestFunction E,
      f ∈ D.testFunctions →
        ∀ ω : Ω, ∀ t : Time,
          IntervalIntegrable (generatorPathIntegrand D f ω) volume (0 : Time) t) ∧
    ∀ f : TestFunction E,
      f ∈ D.testFunctions →
        ∀ t : Time,
          D.accumulatedGenerator f t =ᵐ[D.probabilityMeasure]
            canonicalAccumulatedGenerator D f t

/-- The canonical accumulated generator unfolds to the chosen interval integral. -/
theorem canonicalAccumulatedGenerator_apply
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (f : TestFunction E) (t : Time) (ω : Ω) :
    canonicalAccumulatedGenerator D f t ω =
      ∫ s in (0 : Time)..t, generatorPathIntegrand D f ω s :=
  rfl

/--
The selected bridge turns the legacy `accumulatedGenerator` field into the
canonical interval integral, almost everywhere under the packaged law.
-/
theorem accumulatedGenerator_ae_eq_canonical
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (hD : AccumulatedGeneratorIsIntervalIntegral D)
    {f : TestFunction E} (hf : f ∈ D.testFunctions) (t : Time) :
    D.accumulatedGenerator f t =ᵐ[D.probabilityMeasure]
      canonicalAccumulatedGenerator D f t :=
  hD.2 f hf t

/-- The selected bridge records pathwise interval-integrability of the generator. -/
theorem generatorPathIntegrable
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (hD : AccumulatedGeneratorIsIntervalIntegral D)
    {f : TestFunction E} (hf : f ∈ D.testFunctions) (ω : Ω) (t : Time) :
    IntervalIntegrable (generatorPathIntegrand D f ω) volume (0 : Time) t :=
  hD.1 f hf ω t

/-- The martingale-problem condition for all admissible test functions. -/
def SolvesMartingaleProblem
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Prop :=
  ∀ f : TestFunction E,
    f ∈ D.testFunctions →
      Martingale (GeneratorCompensated D f) D.filtration D.probabilityMeasure

/--
Leaf obligations for one admissible test function in the martingale-problem
proof tree.

This mirrors mathlib's `Martingale` definition for the compensated real-valued
process: prove strong adaptedness of the compensated process, then prove the
conditional-expectation identity for every ordered time pair.  Integrability is
kept as a downstream consequence of the assembled martingale, matching the
current mathlib API.
-/
structure CompensatedMartingaleLeafObligations
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (f : TestFunction E) : Prop where
  stronglyAdapted :
    StronglyAdapted D.filtration (GeneratorCompensated D f)
  condExp_ae_eq :
    ∀ s t : Time,
      s ≤ t →
        D.probabilityMeasure[GeneratorCompensated D f t | D.filtration s]
          =ᵐ[D.probabilityMeasure] GeneratorCompensated D f s

/--
Universal leaf package for `THM-M-1049.martingale_problem`.

The package is intentionally indexed by the admissibility proof `f ∈
D.testFunctions`; future workers can refine each admissibility branch without
changing the public `SolvesMartingaleProblem` predicate.
-/
def MartingaleProblemLeafPackage
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Prop :=
  ∀ f : TestFunction E,
    f ∈ D.testFunctions → CompensatedMartingaleLeafObligations D f

/-- The two local leaves assemble into mathlib's martingale predicate. -/
theorem compensatedMartingale_of_leafObligations
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E} {f : TestFunction E}
    (h : CompensatedMartingaleLeafObligations D f) :
    Martingale (GeneratorCompensated D f) D.filtration D.probabilityMeasure :=
  ⟨h.stronglyAdapted, h.condExp_ae_eq⟩

/-- Any mathlib martingale proof splits into the two local martingale leaves. -/
theorem leafObligations_of_compensatedMartingale
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E} {f : TestFunction E}
    (h : Martingale (GeneratorCompensated D f) D.filtration D.probabilityMeasure) :
    CompensatedMartingaleLeafObligations D f :=
  ⟨h.1, h.2⟩

/--
For a fixed test function, the local leaf obligations are definitionally
equivalent to mathlib's martingale predicate.
-/
theorem compensatedMartingale_iff_leafObligations
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E} {f : TestFunction E} :
    Martingale (GeneratorCompensated D f) D.filtration D.probabilityMeasure ↔
      CompensatedMartingaleLeafObligations D f :=
  ⟨leafObligations_of_compensatedMartingale, compensatedMartingale_of_leafObligations⟩

/-- The universal leaf package assembles into `SolvesMartingaleProblem`. -/
theorem solvesMartingaleProblem_of_leafPackage
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (h : MartingaleProblemLeafPackage D) :
    SolvesMartingaleProblem D :=
  fun f hf => compensatedMartingale_of_leafObligations (h f hf)

/-- A solved martingale problem splits into the universal local leaf package. -/
theorem leafPackage_of_solvesMartingaleProblem
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (h : SolvesMartingaleProblem D) :
    MartingaleProblemLeafPackage D :=
  fun f hf => leafObligations_of_compensatedMartingale (h f hf)

/--
Checked split for `THM-M-1049.martingale_problem`: proving every admissible
compensated test-function process is a martingale is equivalent to providing
the two-leaf package for every admissible test function.
-/
theorem solvesMartingaleProblem_iff_leafPackage
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E} :
    SolvesMartingaleProblem D ↔ MartingaleProblemLeafPackage D :=
  ⟨leafPackage_of_solvesMartingaleProblem, solvesMartingaleProblem_of_leafPackage⟩

/-- M0387-level child status for the martingale-problem proof split. -/
def martingaleProblemLeafSplitStatus : String :=
  "checked_split_into_strong_adaptedness_and_conditional_expectation_leaves; terminal_theorem_not_claimed"

/--
One-time marginal law of the process under its packaged probability measure.

This is only a law-comparison boundary.  A future transition-law child must
replace or extend it with finite-dimensional/path-law APIs.
-/
def oneTimeMarginalLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (t : Time) : Measure E :=
  D.probabilityMeasure.map (D.process t)

/--
Repo-local equality boundary for the normalized martingale-problem
specification shared by two candidate solutions.

Only the fields that live on the common state space are compared here.  Process
paths, filtrations, probability spaces, and accumulated-generator sample paths
may live on different spaces and are handled by the solution predicates.
-/
def SameMartingaleProblemSpecification
    {Ω₁ Ω₂ : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω₁] [MeasurableSpace Ω₂]
    [TopologicalSpace E] [MeasurableSpace E]
    (D₁ : MartingaleProblemData Ω₁ E)
    (D₂ : MartingaleProblemData Ω₂ E) : Prop :=
  D₁.initialLaw = D₂.initialLaw ∧
    D₁.testFunctions = D₂.testFunctions ∧
      D₁.generator = D₂.generator

/--
Current repo-local law-equality target for uniqueness in law.

This records equality of all one-time marginal laws.  It is deliberately weaker
than full finite-dimensional or path-law equality, which belongs to the
`THM-M-1049.transition_law` branch.
-/
def SameOneTimeMarginalLaws
    {Ω₁ Ω₂ : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω₁] [MeasurableSpace Ω₂]
    [TopologicalSpace E] [MeasurableSpace E]
    (D₁ : MartingaleProblemData Ω₁ E)
    (D₂ : MartingaleProblemData Ω₂ E) : Prop :=
  ∀ t : Time, oneTimeMarginalLaw D₁ t = oneTimeMarginalLaw D₂ t

/--
Path-valued realization of the packaged stochastic process.

This is the process-law carrier for `THM-M-1049.transition_law`: it turns the
curried process `Time → Ω → E` into a random variable from the probability
space to the path space `Time → E`.
-/
def processPath
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) :
    Ω → Time → E :=
  fun ω t => D.process t ω

/-- Process law obtained by pushing the packaged probability measure to path space. -/
def processLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) :
    Measure (Time → E) :=
  D.probabilityMeasure.map (processPath D)

/-- Evaluation of a path along a finite list of observation times. -/
def finiteDimensionalEvaluation
    {E : Type uE} (n : ℕ) (times : Fin n → Time) :
    (Time → E) → Fin n → E :=
  fun path i => path (times i)

/-- Finite-dimensional law of the process at a finite observation grid. -/
def finiteDimensionalLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (n : ℕ) (times : Fin n → Time) :
    Measure (Fin n → E) :=
  D.probabilityMeasure.map (fun ω i => D.process (times i) ω)

/--
One-time law predicted by the transition kernel from the initial law.

For a homogeneous transition family this is the expected `μ₀ P_t` marginal.
The full finite-dimensional transition-kernel construction remains a package
field below because the local artifact does not yet choose a canonical
continuous-time Chapman-Kolmogorov/Ionescu-Tulcea API.
-/
def transitionKernelMarginalLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (t : Time) :
    Measure E :=
  D.initialLaw.bind (D.transitionKernel t)

/--
Transition-law package connecting the martingale-problem data to path laws and
finite-dimensional laws.

The package deliberately separates the checked objects available now from the
future hard theorem.  It records:

* the one-time marginal law obtained from the transition kernel,
* a finite-dimensional transition-kernel law family,
* equality of process finite-dimensional laws with that family,
* consistency of the finite-dimensional transition laws, and
* the existing process-characterization conclusion field.
-/
structure TransitionLawPackage
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Type (max uΩ uE) where
  one_time_marginal_from_transition :
    ∀ t : Time, 0 ≤ t →
      oneTimeMarginalLaw D t = transitionKernelMarginalLaw D t
  kernel_finite_dimensional_law :
    ∀ n : ℕ, (Fin n → Time) → Measure (Fin n → E)
  finite_dimensional_law_from_transition :
    ∀ (n : ℕ) (times : Fin n → Time),
      finiteDimensionalLaw D n times = kernel_finite_dimensional_law n times
  finite_dimensional_projective_consistency :
    Prop
  process_law_has_finite_dimensional_marginals :
    ∀ (n : ℕ) (times : Fin n → Time),
      (processLaw D).map (finiteDimensionalEvaluation n times) =
        finiteDimensionalLaw D n times
  transition_law_characterizes_process :
    D.transitionLawCharacterizesProcess

/-- The process path unfolds to the original process at each time. -/
theorem processPath_apply
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (ω : Ω) (t : Time) :
    processPath D ω t = D.process t ω :=
  rfl

/-- Finite-dimensional evaluation is path evaluation on the selected grid. -/
theorem finiteDimensionalEvaluation_apply
    {E : Type uE} (n : ℕ) (times : Fin n → Time)
    (path : Time → E) (i : Fin n) :
    finiteDimensionalEvaluation n times path i = path (times i) :=
  rfl

/-- The finite-dimensional law unfolds to the corresponding push-forward law. -/
theorem finiteDimensionalLaw_eq_map
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (n : ℕ) (times : Fin n → Time) :
    finiteDimensionalLaw D n times =
      D.probabilityMeasure.map (fun ω i => D.process (times i) ω) :=
  rfl

/-- The initial law is a probability measure because it is the law of `process 0`. -/
theorem initialLaw_isProbability
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) :
    IsProbabilityMeasure D.initialLaw :=
  D.initialHasLaw.isProbabilityMeasure_iff.1 D.isProbability

/-- The transition-kernel marginal unfolds to integration against the kernel. -/
theorem transitionKernelMarginalLaw_apply
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (t : Time)
    {s : Set E} (hs : MeasurableSet s) :
    transitionKernelMarginalLaw D t s =
      ∫⁻ x, D.transitionKernel t x s ∂D.initialLaw :=
  Measure.bind_apply hs (Kernel.aemeasurable _)

/-- Nonnegative-time transition-kernel marginals are probability measures. -/
theorem transitionKernelMarginalLaw_isProbability
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (t : Time) (ht : 0 ≤ t) :
    IsProbabilityMeasure (transitionKernelMarginalLaw D t) := by
  letI : IsProbabilityMeasure D.initialLaw := initialLaw_isProbability D
  exact MeasureTheory.isProbabilityMeasure_bind (Kernel.aemeasurable _)
    (ae_of_all _ fun x => (D.transitionKernelMarkov t ht).isProbabilityMeasure x)

/-- A transition-law package exposes one-time marginal identification. -/
theorem oneTimeMarginalLaw_eq_transitionKernelMarginalLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (h : TransitionLawPackage D) (t : Time) (ht : 0 ≤ t) :
    oneTimeMarginalLaw D t = transitionKernelMarginalLaw D t :=
  h.one_time_marginal_from_transition t ht

/-- A transition-law package exposes finite-dimensional law identification. -/
theorem finiteDimensionalLaw_eq_kernelFiniteDimensionalLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (h : TransitionLawPackage D) (n : ℕ) (times : Fin n → Time) :
    finiteDimensionalLaw D n times = h.kernel_finite_dimensional_law n times :=
  h.finite_dimensional_law_from_transition n times

/-- A transition-law package exposes process-law finite-dimensional marginals. -/
theorem processLaw_finiteDimensionalMarginal
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (h : TransitionLawPackage D) (n : ℕ) (times : Fin n → Time) :
    (processLaw D).map (finiteDimensionalEvaluation n times) =
      finiteDimensionalLaw D n times :=
  h.process_law_has_finite_dimensional_marginals n times

/-- A transition-law package supplies the legacy characterization boundary. -/
theorem transitionLawCharacterizesProcess_of_transitionLawPackage
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (h : TransitionLawPackage D) :
    D.transitionLawCharacterizesProcess :=
  h.transition_law_characterizes_process

/-- M0387-level child status for the transition-law package. -/
def transitionLawPackageStatus : String :=
  "checked_process_law_finite_dimensional_law_and_transition_kernel_package; terminal_theorem_not_claimed"

/--
Existence leaves for a concrete candidate solving the martingale problem.

The candidate data package already supplies the probability space and initial
law; the remaining leaves expose the integral compensator, path regularity, and
martingale-problem solution obligations.
-/
structure MartingaleProblemExistenceLeaves
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Prop where
  probability :
    IsProbabilityMeasure D.probabilityMeasure
  initial_law :
    HasLaw (D.process 0) D.initialLaw D.probabilityMeasure
  accumulated_generator_is_integral :
    D.accumulatedGeneratorIsIntegral
  path_regular :
    D.pathRegularity
  solves_martingale_problem :
    SolvesMartingaleProblem D

/--
Uniqueness-in-law leaves for the martingale problem.

Given any second candidate on any measurable probability space with the same
state-space specification and a solved martingale problem, prove equality of
the current repo-local law target.
-/
structure MartingaleProblemUniquenessInLawLeaves
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Prop where
  one_time_marginal_law_eq :
    ∀ (Ω₂ : Type uΩ) [MeasurableSpace Ω₂],
      ∀ D₂ : MartingaleProblemData Ω₂ E,
        SameMartingaleProblemSpecification D D₂ →
          SolvesMartingaleProblem D₂ →
            SameOneTimeMarginalLaws D D₂

/--
Checked well-posedness split for `THM-M-1049.well_posedness`.

The split separates existence of a candidate solution from uniqueness in the
current law-equality target.  It does not prove the classical
Stroock-Varadhan well-posedness theorem.
-/
structure MartingaleProblemWellPosedLeafPackage
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Prop where
  existence :
    MartingaleProblemExistenceLeaves D
  uniqueness_in_law :
    MartingaleProblemUniquenessInLawLeaves D

/-- The data package supplies the probability leaf of the existence branch. -/
theorem existenceProbabilityLeaf
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) :
    IsProbabilityMeasure D.probabilityMeasure :=
  D.isProbability

/-- The data package supplies the initial-law leaf of the existence branch. -/
theorem existenceInitialLawLeaf
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) :
    HasLaw (D.process 0) D.initialLaw D.probabilityMeasure :=
  D.initialHasLaw

/-- The checked well-posedness package exposes its existence branch. -/
theorem existenceLeaves_of_wellPosedLeafPackage
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (h : MartingaleProblemWellPosedLeafPackage D) :
    MartingaleProblemExistenceLeaves D :=
  h.existence

/-- The checked well-posedness package exposes its uniqueness-in-law branch. -/
theorem uniquenessInLawLeaves_of_wellPosedLeafPackage
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (h : MartingaleProblemWellPosedLeafPackage D) :
    MartingaleProblemUniquenessInLawLeaves D :=
  h.uniqueness_in_law

/-- Uniqueness leaves apply to any second solution with the same specification. -/
theorem sameOneTimeMarginalLaws_of_uniquenessLeaves
    {Ω₁ Ω₂ : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω₁] [MeasurableSpace Ω₂]
    [TopologicalSpace E] [MeasurableSpace E]
    {D₁ : MartingaleProblemData Ω₁ E}
    {D₂ : MartingaleProblemData Ω₂ E}
    (h : MartingaleProblemUniquenessInLawLeaves D₁)
    (hSpec : SameMartingaleProblemSpecification D₁ D₂)
    (hSolves : SolvesMartingaleProblem D₂) :
    SameOneTimeMarginalLaws D₁ D₂ :=
  h.one_time_marginal_law_eq Ω₂ D₂ hSpec hSolves

/-- M0387-level child status for the well-posedness proof split. -/
def wellPosednessLeafSplitStatus : String :=
  "checked_split_into_existence_and_uniqueness_in_one_time_law_leaves; terminal_theorem_not_claimed"

/-- Hypotheses outside the bare martingale predicate in the normalized boundary. -/
def StroockVaradhanHypotheses
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Prop :=
  D.diffusionGeneratorShape ∧
    D.accumulatedGeneratorIsIntegral ∧
      D.pathRegularity ∧
        D.martingaleProblemWellPosed ∧
          SolvesMartingaleProblem D

/-- Stroock-Varadhan hypotheses expose the legacy well-posedness field. -/
theorem martingaleProblemWellPosed_of_hypotheses
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (hD : StroockVaradhanHypotheses D) :
    D.martingaleProblemWellPosed :=
  hD.2.2.2.1

/-- Stroock-Varadhan hypotheses assemble the existence leaves. -/
theorem existenceLeaves_of_hypotheses
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (hD : StroockVaradhanHypotheses D) :
    MartingaleProblemExistenceLeaves D :=
  ⟨D.isProbability, D.initialHasLaw, hD.2.1, hD.2.2.1, hD.2.2.2.2⟩

/--
Conclusion package for the martingale-problem characterization.

The hard theorem should derive law/transition identification from the
martingale problem and well-posedness assumptions.  These conclusion fields
remain proposition boundaries until the diffusion-generator and process-law
APIs are available in the local Lean closure.
-/
structure StroockVaradhanConclusion
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) : Prop where
  martingale_problem_characterizes_diffusion : D.transitionLawCharacterizesProcess
  uniqueness_in_law : D.martingaleProblemWellPosed
  martingale_problem_holds : SolvesMartingaleProblem D

/--
Stage1 normalized statement shape for the Stroock-Varadhan martingale problem.

For every measurable probability space and state space, a process equipped with
a diffusion generator, integral compensator, path regularity, and a well-posed
martingale problem should be characterized by the corresponding diffusion
transition law.  This is a formalization target only, not a local proof of the
classical theorem.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) (E : Type uE)
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E],
      ∀ D : MartingaleProblemData Ω E,
        StroockVaradhanHypotheses D → StroockVaradhanConclusion D

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h :
      ∀ (Ω : Type uΩ) (E : Type uE)
        [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E],
          ∀ D : MartingaleProblemData Ω E,
            StroockVaradhanHypotheses D → StroockVaradhanConclusion D) :
    StatementShape.{uΩ, uE} :=
  fun Ω E _ _ _ D hD => h Ω E D hD

/-- The normalized statement unfolds to the expected data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{uΩ, uE} ↔
      ∀ (Ω : Type uΩ) (E : Type uE)
        [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E],
          ∀ D : MartingaleProblemData Ω E,
            StroockVaradhanHypotheses D → StroockVaradhanConclusion D :=
  Iff.rfl

/-- The data package exposes its probability-measure instance. -/
theorem probabilityMeasure_isProbability
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) :
    IsProbabilityMeasure D.probabilityMeasure :=
  D.isProbability

/-- The data package exposes adaptedness of the process. -/
theorem process_adapted
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) :
    Adapted D.filtration D.process :=
  D.adapted

/-- With a Borel state space, adaptedness gives measurability of each time slice. -/
theorem process_measurable_time
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E] [BorelSpace E]
    (D : MartingaleProblemData Ω E) (t : Time) :
    Measurable (D.process t) :=
  D.adapted.measurable

/-- The data package exposes the initial law of the process. -/
theorem initial_hasLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) :
    HasLaw (D.process 0) D.initialLaw D.probabilityMeasure :=
  D.initialHasLaw

/-- A transition kernel is Markov at each nonnegative time. -/
theorem transitionKernel_isMarkov
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : MartingaleProblemData Ω E) (t : Time) (ht : 0 ≤ t) :
    IsMarkovKernel (D.transitionKernel t) :=
  D.transitionKernelMarkov t ht

/-- The hypotheses expose the martingale-problem predicate. -/
theorem solvesMartingaleProblem_of_hypotheses
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (hD : StroockVaradhanHypotheses D) :
    SolvesMartingaleProblem D :=
  hD.2.2.2.2

/-- A process solving the martingale problem supplies each compensated martingale. -/
theorem compensated_martingale
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (hD : SolvesMartingaleProblem D) {f : TestFunction E}
    (hf : f ∈ D.testFunctions) :
    Martingale (GeneratorCompensated D f) D.filtration D.probabilityMeasure :=
  hD f hf

/-- mathlib's martingale API gives integrability of each compensated time slice. -/
theorem compensated_integrable
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (hD : SolvesMartingaleProblem D) {f : TestFunction E}
    (hf : f ∈ D.testFunctions) (t : Time) :
    Integrable (GeneratorCompensated D f t) D.probabilityMeasure :=
  (hD f hf).integrable t

/-- mathlib's martingale API gives the conditional-expectation characterization. -/
theorem compensated_condExp_ae_eq
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (hD : SolvesMartingaleProblem D) {f : TestFunction E}
    (hf : f ∈ D.testFunctions) {s t : Time} (hst : s ≤ t) :
    D.probabilityMeasure[GeneratorCompensated D f t | D.filtration s]
      =ᵐ[D.probabilityMeasure] GeneratorCompensated D f s :=
  (hD f hf).condExp_ae_eq hst

/-- A conclusion package exposes the transition-law characterization boundary. -/
theorem conclusion_transitionLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (C : StroockVaradhanConclusion D) :
    D.transitionLawCharacterizesProcess :=
  C.martingale_problem_characterizes_diffusion

/-- A conclusion package exposes well-posedness/uniqueness in law. -/
theorem conclusion_uniquenessInLaw
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : MartingaleProblemData Ω E}
    (C : StroockVaradhanConclusion D) :
    D.martingaleProblemWellPosed :=
  C.uniqueness_in_law

/-- Checked mathlib wrapper: `HasLaw` exposes the defining map equality. -/
theorem hasLaw_map_eq
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {μ : Measure E} {X : Ω → E}
    (hX : HasLaw X μ P) :
    P.map X = μ :=
  hX.map_eq

/-- Checked mathlib wrapper: `HasLaw` exposes almost-everywhere measurability. -/
theorem hasLaw_aemeasurable
    {Ω : Type uΩ} {E : Type uE}
    [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {μ : Measure E} {X : Ω → E}
    (hX : HasLaw X μ P) :
    AEMeasurable X P :=
  hX.aemeasurable

/-- Checked mathlib wrapper: deterministic kernels are Markov kernels. -/
theorem deterministicKernel_isMarkov
    {E F : Type*} [MeasurableSpace E] [MeasurableSpace F]
    {f : E → F} (hf : Measurable f) :
    IsMarkovKernel (Kernel.deterministic f hf) :=
  inferInstance

/-- Pinned mathlib revision used for the Stage1 martingale-problem API audit. -/
def mathlibAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact mathlib anchors requested for the `THM-M-1049.mathlib_audit` child task. -/
def checkedMathlibAuditAnchors : List String := [
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.IsMarkovKernel",
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.Martingale.condExp_ae_eq"
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Composition.Comp",
  "Mathlib.Probability.Kernel.Invariance",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.MeasureTheory.Function.ConditionalExpectation.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure"
]

/-- Pinned declaration names used or audited for this Stage1 boundary. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.HasLaw.map_eq",
  "ProbabilityTheory.HasLaw.aemeasurable",
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.Kernel.deterministic",
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "MeasureTheory.Adapted.measurable",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.Martingale.condExp_ae_eq",
  "MeasureTheory.IsProbabilityMeasure",
  "MeasureTheory.Integrable",
  "IntervalIntegrable",
  "intervalIntegral.integral_of_le"
]

/-- The generator bridge API selected in this child pass. -/
def generatorBridgeSelectedAPI : String :=
  "pathwise deterministic real interval integral: fun t omega => ∫ s in (0 : Time)..t, D.generator f (D.process s omega)"

/--
M0387-level local status for `THM-M-1049.generator_bridge`.

The bridge selection itself is checked repo-local statement/proof work.  It is
not a terminal Stroock-Varadhan theorem and does not close the future
diffusion-generator, well-posedness, transition-law, or external-audit leaves.
-/
def generatorBridgeStatus : String :=
  "selected_api_local_statement_shape_checked; terminal_theorem_not_claimed"

/-- The diffusion-generator branch selected in the C004 child pass. -/
def diffusionGeneratorBranchSelectedAPI : String :=
  "separate_diffusion_generator_structure; SDE coefficients are later adapters; Feller semigroups are transition-law adapters"

/--
M0387-level local status for `THM-M-1049.diffusion_generator`.

The branch choice is checked repo-local statement-shape work.  It does not
construct a classical second-order differential operator, prove Feller
semigroup generation, or close the Stroock-Varadhan theorem.
-/
def diffusionGeneratorBranchStatus : String :=
  "selected_separate_diffusion_generator_structure_checked; terminal_theorem_not_claimed"

/--
Search terms that did not locate a terminal Stroock-Varadhan theorem in the
pinned local mathlib snapshot.
-/
def absentTerminalSearchTerms : List String := [
  "Stroock",
  "Varadhan",
  "martingale problem",
  "MartingaleProblem",
  "diffusion generator",
  "Diffusion",
  "stochastic differential equation",
  "SDE",
  "Feller semigroup",
  "continuous-time Markov",
  "BrownianMotion",
  "StochasticIntegral"
]

/-- Date of the rerun external Lean 4 audit for `THM-M-1049.external_audit`. -/
def externalAuditDate : String :=
  "2026-05-01"

/--
Primary-source search surfaces rerun for the external audit.

The audit found no Lean 4 theorem/module that states or proves the terminal
Stroock-Varadhan martingale-problem theorem.  Therefore there is currently no
external proof artifact to pin/import/check for this parent theorem.
-/
def externalAuditPrimarySourceSearches : List String := [
  "pinned local mathlib package at 8a178386ffc0f5fef0b77738bb5449d50efeea95: rg for Stroock, Varadhan, MartingaleProblem, and martingale problem returned no terminal theorem",
  "pinned local Lean dependency closure under Formalizations/Lean/.lake/packages: rg for Stroock, Varadhan, MartingaleProblem, and martingale problem returned no terminal theorem",
  "GitHub web/source search queries for Lean 4 Stroock Varadhan martingale problem and MartingaleProblem Lean 4: no terminal Stroock-Varadhan Lean theorem located",
  "RemyDegenne/brownian-motion primary repository shallow clone: rg for Stroock, Varadhan, MartingaleProblem, and martingale problem returned no terminal theorem"
]

/--
External terminal Lean 4 proof discovery result for this audit.

`false` means the audit did not locate a concrete theorem/module that can be
pinned into this repository.  It is not a mathematical disproof and not a
terminal formalization claim.
-/
def externalAuditTerminalProofFound : Bool :=
  false

/-- The external audit currently has no upstream proof body to integrate. -/
theorem externalAuditTerminalProofFound_eq_false :
    externalAuditTerminalProofFound = false :=
  rfl

/--
Concrete M0387 integration blocker for the external-audit child.

Because no terminal external Lean 4 Stroock-Varadhan theorem was located, there
is no upstream module/theorem/revision that can be added as a pinned dependency
or wrapped locally in this pass.
-/
def externalAuditIntegrationBlocker : String :=
  "no concrete external Lean 4 terminal Stroock-Varadhan martingale-problem theorem/module was located; integration can resume only after a specific upstream repo, commit, module, and theorem name are found"

/--
M0387 repo-local integration-debt gate for the external audit.

This is a pass only for the C008 audit scope: no external proof was found, so no
anchor-only external proof is being treated as completed.  The parent theorem
remains open formalization debt and no terminal theorem completion is claimed.
-/
def externalAuditRepoLocalIntegrationDebtGate : String :=
  "pass_for_audit_scope_no_external_terminal_proof_found_no_anchor_only_completion_claim"

/-- Four M0387 prerequisites for closing the Stage1 Stroock-Varadhan slot. -/
def StatusGatePrerequisites
    (localValidationPassed publicMergeBackDone leafLedgerClosed
      noCompletedStateRepoLocalIntegrationDebt : Prop) : Prop :=
  localValidationPassed ∧
    publicMergeBackDone ∧
      leafLedgerClosed ∧
        noCompletedStateRepoLocalIntegrationDebt

/-- The status gate requires a repo-local Lean validation pass. -/
theorem statusGate_requires_localValidation
    {localValidationPassed publicMergeBackDone leafLedgerClosed
      noCompletedStateRepoLocalIntegrationDebt : Prop}
    (h :
      StatusGatePrerequisites localValidationPassed publicMergeBackDone
        leafLedgerClosed noCompletedStateRepoLocalIntegrationDebt) :
    localValidationPassed :=
  h.1

/-- The status gate requires serial public-document merge-back. -/
theorem statusGate_requires_publicMergeBack
    {localValidationPassed publicMergeBackDone leafLedgerClosed
      noCompletedStateRepoLocalIntegrationDebt : Prop}
    (h :
      StatusGatePrerequisites localValidationPassed publicMergeBackDone
        leafLedgerClosed noCompletedStateRepoLocalIntegrationDebt) :
    publicMergeBackDone :=
  h.2.1

/-- The status gate requires closure of the child leaf ledgers. -/
theorem statusGate_requires_leafLedgerClosure
    {localValidationPassed publicMergeBackDone leafLedgerClosed
      noCompletedStateRepoLocalIntegrationDebt : Prop}
    (h :
      StatusGatePrerequisites localValidationPassed publicMergeBackDone
        leafLedgerClosed noCompletedStateRepoLocalIntegrationDebt) :
    leafLedgerClosed :=
  h.2.2.1

/-- The status gate forbids completed-state repo-local integration debt. -/
theorem statusGate_requires_noCompletedStateRepoLocalIntegrationDebt
    {localValidationPassed publicMergeBackDone leafLedgerClosed
      noCompletedStateRepoLocalIntegrationDebt : Prop}
    (h :
      StatusGatePrerequisites localValidationPassed publicMergeBackDone
        leafLedgerClosed noCompletedStateRepoLocalIntegrationDebt) :
    noCompletedStateRepoLocalIntegrationDebt :=
  h.2.2.2

/-- Required local validation command for this Stage1 status gate. -/
def statusGateValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_242.lean"

/--
Current M0387 status-gate result for `THM-M-1049.status_gate`.

The local Lean artifact may validate, and no completed-state
`repo_local_integration_debt` is introduced, but completion remains blocked
until serial public merge-back and leaf-ledger closure are both recorded.
-/
def statusGateCurrentResult : String :=
  "open_until_local_validation_public_merge_back_leaf_ledger_closure_and_no_completed_state_repo_local_integration_debt_are_all_satisfied"

/--
Checked Boolean summary of the current completion gate.

`false` is intentional: this child is the gatekeeper and cannot claim terminal
completion before public merge-back and leaf-ledger closure happen.
-/
def statusGateCompletionAllowed : Bool :=
  false

/-- The current C009 pass leaves the Stage1 status gate open. -/
theorem statusGateCompletionAllowed_eq_false :
    statusGateCompletionAllowed = false :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check MartingaleProblemData
#check DiffusionGeneratorBranch
#check selectedDiffusionGeneratorBranch
#check DiffusionGeneratorStructure
#check DiffusionGeneratorBranchRealization
#check selectedDiffusionGeneratorBranch_eq
#check diffusionGeneratorRealization_generator_eq
#check diffusionGeneratorRealization_shape
#check GeneratorCompensated
#check generatorPathIntegrand
#check canonicalAccumulatedGenerator
#check AccumulatedGeneratorIsIntervalIntegral
#check canonicalAccumulatedGenerator_apply
#check accumulatedGenerator_ae_eq_canonical
#check generatorPathIntegrable
#check SolvesMartingaleProblem
#check CompensatedMartingaleLeafObligations
#check MartingaleProblemLeafPackage
#check compensatedMartingale_of_leafObligations
#check leafObligations_of_compensatedMartingale
#check compensatedMartingale_iff_leafObligations
#check solvesMartingaleProblem_of_leafPackage
#check leafPackage_of_solvesMartingaleProblem
#check solvesMartingaleProblem_iff_leafPackage
#check oneTimeMarginalLaw
#check SameMartingaleProblemSpecification
#check SameOneTimeMarginalLaws
#check processPath
#check processLaw
#check finiteDimensionalEvaluation
#check finiteDimensionalLaw
#check transitionKernelMarginalLaw
#check TransitionLawPackage
#check processPath_apply
#check finiteDimensionalEvaluation_apply
#check finiteDimensionalLaw_eq_map
#check initialLaw_isProbability
#check transitionKernelMarginalLaw_apply
#check transitionKernelMarginalLaw_isProbability
#check oneTimeMarginalLaw_eq_transitionKernelMarginalLaw
#check finiteDimensionalLaw_eq_kernelFiniteDimensionalLaw
#check processLaw_finiteDimensionalMarginal
#check transitionLawCharacterizesProcess_of_transitionLawPackage
#check MartingaleProblemExistenceLeaves
#check MartingaleProblemUniquenessInLawLeaves
#check MartingaleProblemWellPosedLeafPackage
#check existenceProbabilityLeaf
#check existenceInitialLawLeaf
#check martingaleProblemWellPosed_of_hypotheses
#check existenceLeaves_of_hypotheses
#check existenceLeaves_of_wellPosedLeafPackage
#check uniquenessInLawLeaves_of_wellPosedLeafPackage
#check sameOneTimeMarginalLaws_of_uniquenessLeaves
#check StroockVaradhanHypotheses
#check StroockVaradhanConclusion
#check compensated_martingale
#check compensated_integrable
#check compensated_condExp_ae_eq
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.Kernel
#check ProbabilityTheory.IsMarkovKernel
#check MeasureTheory.Filtration
#check MeasureTheory.Adapted
#check MeasureTheory.Martingale
#check MeasureTheory.Martingale.integrable
#check MeasureTheory.Martingale.condExp_ae_eq
#check IntervalIntegrable
#check intervalIntegral.integral_of_le
#check absentTerminalSearchTerms
#check externalAuditDate
#check externalAuditPrimarySourceSearches
#check externalAuditTerminalProofFound
#check externalAuditTerminalProofFound_eq_false
#check externalAuditIntegrationBlocker
#check externalAuditRepoLocalIntegrationDebtGate
#check StatusGatePrerequisites
#check statusGate_requires_localValidation
#check statusGate_requires_publicMergeBack
#check statusGate_requires_leafLedgerClosure
#check statusGate_requires_noCompletedStateRepoLocalIntegrationDebt
#check statusGateValidationCommand
#check statusGateCurrentResult
#check statusGateCompletionAllowed
#check statusGateCompletionAllowed_eq_false

end AwesomeTheorems.Stage1.S1_M_242
