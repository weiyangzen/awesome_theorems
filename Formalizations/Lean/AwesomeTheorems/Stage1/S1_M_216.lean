import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.Kernel.Composition.Comp
import Mathlib.Probability.Process.Filtration
import Mathlib.Probability.Process.FiniteDimensionalLaws
import Mathlib.Probability.Process.Kolmogorov

/-!
# S1-M-216 / THM-M-1092: Kolmogorov forward/backward equations

This Stage1 artifact records a conservative Lean 4 boundary for the
Kolmogorov forward and backward equations for transition densities.

The local mathlib snapshot has Markov kernels, kernel composition, the
Chapman-Kolmogorov equation for powers of a kernel, filtrations, stochastic
process law/finitary-distribution infrastructure, and calculus/integration
APIs.  It does not expose a terminal continuous-time Markov semigroup API with
infinitesimal generator and transition-density forward/backward PDE theorems.

The terminal theorem is therefore represented as an explicit statement shape.
The checked content below wraps mathlib's Markov-kernel and
Chapman-Kolmogorov substrate without claiming proof of the continuous-time
Kolmogorov equations.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_216

universe u v w

/--
Boundary data for a future continuous-time Markov transition-density theorem.

`transitionKernel t` is the time-`t` Markov kernel and `transitionDensity t x y`
is its density relative to `referenceMeasure`.  The generators are kept as
operators on real-valued state functions; later work can replace this by a
concrete Feller-semigroup, matrix-generator, or diffusion-generator API.
-/
structure KolmogorovEquationData
    (State : Type u) [MeasurableSpace State] : Type (u + 1) where
  referenceMeasure : Measure State
  transitionKernel : ℝ → Kernel State State
  transitionDensity : ℝ → State → State → ℝ
  backwardGenerator : (State → ℝ) → State → ℝ
  forwardGenerator : (State → ℝ) → State → ℝ

/-- The time-zero transition kernel is the identity kernel. -/
def InitialKernel
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  D.transitionKernel 0 = Kernel.id

/-- Nonnegative-time transition kernels are Markov kernels. -/
def MarkovKernelFamily
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  ∀ t : ℝ, 0 ≤ t → IsMarkovKernel (D.transitionKernel t)

/-- Continuous-time Chapman-Kolmogorov semigroup law for transition kernels. -/
def SemigroupLaw
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  ∀ s t : ℝ, 0 ≤ s → 0 ≤ t →
    D.transitionKernel (s + t) = D.transitionKernel t ∘ₖ D.transitionKernel s

/-- Measurability of transition densities in the terminal state variable. -/
def TransitionDensityMeasurable
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  ∀ t x, 0 ≤ t → Measurable fun y : State => D.transitionDensity t x y

/-- Nonnegativity of transition densities for nonnegative times. -/
def TransitionDensityNonnegative
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  ∀ t x y, 0 ≤ t → 0 ≤ D.transitionDensity t x y

/-- The transition density represents the transition kernel relative to a reference measure. -/
def DensityRepresentsKernel
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  ∀ t x, 0 ≤ t →
    D.transitionKernel t x =
      D.referenceMeasure.withDensity
        (fun y : State => ENNReal.ofReal (D.transitionDensity t x y))

/-- Time differentiability of transition densities on positive time. -/
def DifferentiableInTime
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  ∀ x y, DifferentiableOn ℝ (fun t : ℝ => D.transitionDensity t x y) (Set.Ioi 0)

/-- Kolmogorov backward equation statement for the supplied generator. -/
def BackwardEquation
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  ∀ t x y, 0 < t →
    HasDerivAt (fun τ : ℝ => D.transitionDensity τ x y)
      (D.backwardGenerator (fun z : State => D.transitionDensity t z y) x) t

/-- Kolmogorov forward equation statement for the supplied generator. -/
def ForwardEquation
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  ∀ t x y, 0 < t →
    HasDerivAt (fun τ : ℝ => D.transitionDensity τ x y)
      (D.forwardGenerator (D.transitionDensity t x) y) t

/-- Well-formedness assumptions for the normalized Stage1 statement boundary. -/
def KolmogorovEquationHypotheses
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop :=
  InitialKernel D ∧
    MarkovKernelFamily D ∧
      SemigroupLaw D ∧
        TransitionDensityMeasurable D ∧
          TransitionDensityNonnegative D ∧
            DensityRepresentsKernel D ∧
              DifferentiableInTime D

/--
Terminal conclusion package for Kolmogorov's forward and backward equations.

The forward/backward equations are the missing continuous-time generator facts.
The semigroup and density clauses are included so that a later proof exposes
the Chapman-Kolmogorov and transition-density interfaces at the same boundary.
-/
structure KolmogorovForwardBackwardConclusion
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop where
  backward_equation : BackwardEquation D
  forward_equation : ForwardEquation D
  semigroup_law : SemigroupLaw D
  density_representation : DensityRepresentsKernel D

/--
Stage1 normalized statement shape for the Kolmogorov forward/backward equation
slot.

This is intentionally a proposition-valued target, not a local proof of the
continuous-time theorem.  It freezes the explicit Lean boundary a later
formalization must close: Markov kernels, density representation, time
differentiability, semigroup law, and generator equations.
-/
def StatementShape : Prop :=
  ∀ (State : Type u) [MeasurableSpace State],
    ∀ D : KolmogorovEquationData State,
      KolmogorovEquationHypotheses D → KolmogorovForwardBackwardConclusion D

/-- The normalized statement unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (State : Type u) [MeasurableSpace State],
        ∀ D : KolmogorovEquationData State,
          KolmogorovEquationHypotheses D → KolmogorovForwardBackwardConclusion D :=
  Iff.rfl

/-! ## Public statement-normalization boundary -/

/--
Public Stage1 boundary for `THM-M-1092`.

This deliberately aliases `AwesomeTheorems.Stage1.S1_M_216.StatementShape`.
It is the current repo-local Lean statement shape for Kolmogorov's forward and
backward equations, not a terminal proof of the continuous-time generator
equations.
-/
abbrev PublicStatementNormalization : Prop :=
  StatementShape.{u}

/-- The public-normalization boundary is definitionally the same as `StatementShape`. -/
theorem publicStatementNormalization_iff_statementShape :
    PublicStatementNormalization.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/-- Canonical checked name for the current repo-local statement boundary. -/
def publicStatementBoundaryName : String :=
  "AwesomeTheorems.Stage1.S1_M_216.StatementShape"

/-- Checked metadata for the public Stage1 backfill note. -/
def publicStatementNormalizationNotes : List String := [
  "Use AwesomeTheorems.Stage1.S1_M_216.StatementShape as the current repo-local Lean statement boundary for THM-M-1092.",
  "The checked artifact provides Markov-kernel, density-representation, semigroup-law, differentiability, and generator-equation statement shapes.",
  "This is not a terminal Kolmogorov forward/backward theorem: concrete continuous-time Markov semigroup, transition-density, Feller or finite-state generator, and forward/backward PDE proof packages remain formalization debt."
]

/-- The public statement-normalization metadata is explicitly non-terminal. -/
def publicStatementNormalizationIsTerminal : Bool := false

/-- Sanity check for the non-terminal public-normalization gate. -/
theorem publicStatementNormalizationIsTerminal_eq_false :
    publicStatementNormalizationIsTerminal = false :=
  rfl

/-! ## External anchor integration gate -/

/--
Audit shape for a possible future external Lean 4 terminal proof of the
Kolmogorov forward/backward equations.
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

/-- Projection wrapper: a conclusion package exposes the backward equation. -/
theorem conclusion_backwardEquation
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : KolmogorovForwardBackwardConclusion D) :
    BackwardEquation D :=
  h.backward_equation

/-- Projection wrapper: a conclusion package exposes the forward equation. -/
theorem conclusion_forwardEquation
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : KolmogorovForwardBackwardConclusion D) :
    ForwardEquation D :=
  h.forward_equation

/-- Projection wrapper: the hypotheses include Markov-kernel structure. -/
theorem hypotheses_markovKernel
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : KolmogorovEquationHypotheses D) :
    ∀ t : ℝ, 0 ≤ t → IsMarkovKernel (D.transitionKernel t) :=
  h.2.1

/-- Projection wrapper: the hypotheses include the transition-density representation. -/
theorem hypotheses_densityRepresentsKernel
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : KolmogorovEquationHypotheses D) :
    DensityRepresentsKernel D :=
  h.2.2.2.2.2.1

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

end KernelAnchors

section ProcessAnchors

variable {T Ω E : Type u}
variable [PseudoEMetricSpace T] {mΩ : MeasurableSpace Ω}
variable [PseudoEMetricSpace E] [MeasurableSpace E] [BorelSpace E]
variable {p q : ℝ} {M : ℝ≥0} {P : Measure Ω} {X : T → Ω → E}

/--
Checked mathlib wrapper: a process satisfying mathlib's Kolmogorov condition
has measurable coordinate maps.  This is not the Kolmogorov forward/backward
equation, but it is relevant stochastic-process substrate for this Stage1 slot.
-/
theorem kolmogorovProcess_measurable_coordinate_wrapper
    (hX : IsKolmogorovProcess X P p q M) (t : T) :
    Measurable (X t) :=
  hX.measurable t

/--
Checked mathlib wrapper: the a.e. Kolmogorov-process condition provides
a.e.-measurable coordinate maps.
-/
theorem aeKolmogorovProcess_aemeasurable_coordinate_wrapper
    (hX : IsAEKolmogorovProcess X P p q M) (t : T) :
    AEMeasurable (X t) P :=
  hX.aemeasurable t

end ProcessAnchors

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Kernel.Defs",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Composition.Comp",
  "Mathlib.Probability.Kernel.Composition.MeasureComp",
  "Mathlib.Probability.Kernel.Category.Stoch",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.FiniteDimensionalLaws",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.WithDensity",
  "Mathlib.Analysis.Calculus.Deriv.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.Kernel.deterministic",
  "ProbabilityTheory.Kernel.comp",
  "ProbabilityTheory.Kernel.comp_apply'",
  "ProbabilityTheory.Kernel.lintegral_comp",
  "ProbabilityTheory.Kernel.pow_add",
  "ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral",
  "ProbabilityTheory.Kernel.pow_succ_apply_eq_lintegral",
  "MeasureTheory.Measure.comp_assoc",
  "MeasureTheory.Measure.isProbabilityMeasure_bind",
  "MeasureTheory.ProbabilityMeasure",
  "MeasureTheory.ProbabilityMeasure.map",
  "MeasureTheory.Filtration",
  "ProbabilityTheory.isProjectiveMeasureFamily_map_restrict",
  "ProbabilityTheory.map_eq_iff_forall_finset_map_restrict_eq",
  "ProbabilityTheory.IsKolmogorovProcess",
  "ProbabilityTheory.IsAEKolmogorovProcess",
  "ProbabilityTheory.IsKolmogorovProcess.measurable",
  "ProbabilityTheory.IsAEKolmogorovProcess.aemeasurable",
  "HasDerivAt",
  "DifferentiableOn",
  "MeasureTheory.Measure.withDensity"
]

/--
Search terms that did not locate a terminal continuous-time
Kolmogorov-forward/backward-equation theorem in the local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Kolmogorov forward equation",
  "Kolmogorov backward equation",
  "forward equation",
  "backward equation",
  "transition density",
  "transition semigroup",
  "Markov semigroup",
  "infinitesimal generator",
  "continuous-time Markov",
  "Feller semigroup",
  "KolmogorovForward",
  "KolmogorovBackward"
]

/-! ## S1-M-216-C002 external Lean 4 audit boundary -/

/--
Exact external Lean 4 search tokens assigned to child task `S1-M-216-C002`.

These names are audit metadata, not theorem constants imported from another
project.  The current repo-local closure has no pinned external terminal proof
for these tokens.
-/
def c002ExternalLeanAuditTokens : List String := [
  "KolmogorovForward",
  "KolmogorovBackward",
  "FellerSemigroup",
  "MarkovSemigroup",
  "TransitionDensity",
  "InfinitesimalGenerator"
]

/--
Current C002 repo-local integration-debt flag.

`false` records that this partial Stage1 artifact is not citing an external
Lean 4 terminal proof as completed while leaving it outside the Lake closure.
It does not claim terminal proof completion.
-/
def c002RepoLocalIntegrationDebtRetained : Bool := false

/-- Checked sanity gate for the C002 integration-debt flag. -/
theorem c002RepoLocalIntegrationDebtRetained_eq_false :
    c002RepoLocalIntegrationDebtRetained = false :=
  rfl

/-- Human-readable C002 audit conclusion metadata. -/
def c002ExternalLeanAuditConclusion : List String := [
  "No repo-local pinned/imported external Lean 4 terminal proof is present for the C002 exact token set.",
  "The local checked artifact remains a StatementShape plus mathlib substrate wrapper, not a terminal Kolmogorov forward/backward theorem.",
  "If a true external Lean 4 proof is later found, this slot must pin/import/check it or record a concrete integration blocker before any completed status."
]

/-! ## S1-M-216-C003 first closure-target decision -/

/--
Candidate scopes for the first theorem-closure attempt after the current
statement-shape boundary.
-/
inductive FirstClosureTarget where
  | finiteStateContinuousTimeMarkovChain
  | generalFellerSemigroup

/--
C003 decision: start with the finite-state continuous-time Markov-chain
special case, not the fully general Feller-semigroup theorem.

The general Feller branch remains important, but it depends on a wider
semigroup/generator-domain API than the current repo-local Lean artifact
exposes.  The finite-state CTMC branch is the narrower first closure target for
building checked transition-density, generator, forward-equation, and
backward-equation packages.
-/
def c003SelectedFirstClosureTarget : FirstClosureTarget :=
  FirstClosureTarget.finiteStateContinuousTimeMarkovChain

/-- Checked sanity gate for the C003 target decision. -/
theorem c003SelectedFirstClosureTarget_eq_finiteStateCTMC :
    c003SelectedFirstClosureTarget =
      FirstClosureTarget.finiteStateContinuousTimeMarkovChain :=
  rfl

/-- C003 decision metadata for public backfill. -/
def c003ClosureTargetDecisionNotes : List String := [
  "First closure target: finite-state continuous-time Markov chains.",
  "Reason: the current repo-local Lean closure has Markov-kernel and Chapman-Kolmogorov substrate but no terminal Feller-semigroup/generator-domain API.",
  "The finite-state branch should define a concrete rate-matrix/generator package, transition probabilities or densities against counting measure, and separate forward/backward equation leaves.",
  "The general Feller-semigroup theorem remains a later broader formalization branch and must not be claimed complete from this finite-state decision."
]

/-! ## S1-M-216-C004 independent theorem-tree packages -/

/--
Independent theorem-tree package for transition-density measurability.

This package freezes the local leaf that a later CTMC or Feller-semigroup proof
must close.  It is a package boundary, not a proof that an arbitrary
`KolmogorovEquationData` satisfies the leaf.
-/
structure TransitionDensityMeasurablePackage
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop where
  measurable_terminal_state_leaf : TransitionDensityMeasurable D

/--
Independent theorem-tree package for representing kernels by densities with
respect to the selected reference measure.
-/
structure DensityRepresentsKernelPackage
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop where
  withDensity_kernel_leaf : DensityRepresentsKernel D

/--
Independent theorem-tree package for the backward Kolmogorov equation.

The leaf states the positive-time derivative in the initial-state variable via
the backward generator.
-/
structure BackwardEquationPackage
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop where
  backward_generator_derivative_leaf : BackwardEquation D

/--
Independent theorem-tree package for the forward Kolmogorov equation.

The leaf states the positive-time derivative in the terminal-state variable via
the forward generator.
-/
structure ForwardEquationPackage
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop where
  forward_generator_derivative_leaf : ForwardEquation D

/-- C004 package bundle: the four requested packages remain independent fields. -/
structure C004IndependentTheoremTreePackages
    {State : Type u} [MeasurableSpace State]
    (D : KolmogorovEquationData State) : Prop where
  transition_density_measurable : TransitionDensityMeasurablePackage D
  density_represents_kernel : DensityRepresentsKernelPackage D
  backward_equation : BackwardEquationPackage D
  forward_equation : ForwardEquationPackage D

/-- Projection leaf: the measurability package exposes `TransitionDensityMeasurable`. -/
theorem transitionDensityMeasurable_of_package
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : TransitionDensityMeasurablePackage D) :
    TransitionDensityMeasurable D :=
  h.measurable_terminal_state_leaf

/-- Constructor leaf: `TransitionDensityMeasurable` closes its package boundary. -/
theorem transitionDensityMeasurablePackage_of_statement
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : TransitionDensityMeasurable D) :
    TransitionDensityMeasurablePackage D :=
  ⟨h⟩

/-- Projection leaf: the density package exposes `DensityRepresentsKernel`. -/
theorem densityRepresentsKernel_of_package
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : DensityRepresentsKernelPackage D) :
    DensityRepresentsKernel D :=
  h.withDensity_kernel_leaf

/-- Constructor leaf: `DensityRepresentsKernel` closes its package boundary. -/
theorem densityRepresentsKernelPackage_of_statement
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : DensityRepresentsKernel D) :
    DensityRepresentsKernelPackage D :=
  ⟨h⟩

/-- Projection leaf: the backward-equation package exposes `BackwardEquation`. -/
theorem backwardEquation_of_package
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : BackwardEquationPackage D) :
    BackwardEquation D :=
  h.backward_generator_derivative_leaf

/-- Constructor leaf: `BackwardEquation` closes its package boundary. -/
theorem backwardEquationPackage_of_statement
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : BackwardEquation D) :
    BackwardEquationPackage D :=
  ⟨h⟩

/-- Projection leaf: the forward-equation package exposes `ForwardEquation`. -/
theorem forwardEquation_of_package
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : ForwardEquationPackage D) :
    ForwardEquation D :=
  h.forward_generator_derivative_leaf

/-- Constructor leaf: `ForwardEquation` closes its package boundary. -/
theorem forwardEquationPackage_of_statement
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (h : ForwardEquation D) :
    ForwardEquationPackage D :=
  ⟨h⟩

/--
Checked assembly leaf: the existing Stage1 hypotheses and terminal conclusion,
if supplied by a later proof, populate the four independent C004 packages.

This theorem is only an interface check.  It does not construct the hypotheses
or the terminal forward/backward conclusion for a concrete process.
-/
theorem c004IndependentPackages_of_hypotheses_conclusion
    {State : Type u} [MeasurableSpace State]
    {D : KolmogorovEquationData State}
    (hh : KolmogorovEquationHypotheses D)
    (hc : KolmogorovForwardBackwardConclusion D) :
    C004IndependentTheoremTreePackages D where
  transition_density_measurable := ⟨hh.2.2.2.1⟩
  density_represents_kernel := ⟨hh.2.2.2.2.2.1⟩
  backward_equation := ⟨hc.backward_equation⟩
  forward_equation := ⟨hc.forward_equation⟩

/--
C004 child status flag.

`false` records that the package split is not terminal proof completion for the
continuous-time Kolmogorov theorem.
-/
def c004IndependentPackagesAreTerminal : Bool := false

/-- Checked sanity gate for the C004 non-terminal status flag. -/
theorem c004IndependentPackagesAreTerminal_eq_false :
    c004IndependentPackagesAreTerminal = false :=
  rfl

/-- C004 package names exposed for public backfill. -/
def c004IndependentPackageNames : List String := [
  "TransitionDensityMeasurablePackage",
  "DensityRepresentsKernelPackage",
  "BackwardEquationPackage",
  "ForwardEquationPackage"
]

/-- C004 local leaf-budget ledger for the package split. -/
def c004LocalLeafBudgetLedger : List String := [
  "C004-L01 checked-interface: TransitionDensityMeasurablePackage projection/constructor leaves compile locally and are under 100 proof steps.",
  "C004-L02 checked-interface: DensityRepresentsKernelPackage projection/constructor leaves compile locally and are under 100 proof steps.",
  "C004-L03 checked-interface: BackwardEquationPackage projection/constructor leaves compile locally and are under 100 proof steps.",
  "C004-L04 checked-interface: ForwardEquationPackage projection/constructor leaves compile locally and are under 100 proof steps.",
  "C004-L05 unchecked-terminal: prove the four package assumptions for a concrete finite-state CTMC or pinned external closure before claiming theorem completion."
]

/--
C004 repo-local integration-debt flag.

No external terminal proof is cited by this package split, so no anchor-only
repo-local integration debt is retained as completed evidence.
-/
def c004RepoLocalIntegrationDebtRetained : Bool := false

/-- Checked sanity gate for the C004 integration-debt flag. -/
theorem c004RepoLocalIntegrationDebtRetained_eq_false :
    c004RepoLocalIntegrationDebtRetained = false :=
  rfl

/-! ## S1-M-216-C005 discrete-time Chapman-Kolmogorov substrate -/

/--
Discrete-time Chapman-Kolmogorov substrate package for powers of one Markov
kernel.

This is intentionally separated from `SemigroupLaw D`, which is the
continuous-time transition-kernel semigroup statement needed by the terminal
Kolmogorov forward/backward theorem.
-/
structure DiscreteTimeChapmanKolmogorovSubstrate
    (α : Type u) [MeasurableSpace α] : Prop where
  integral_kernel_power_leaf :
    ∀ (κ : Kernel α α) (m n : ℕ) (a : α) {s : Set α},
      MeasurableSet s →
        (κ ^ (m + n)) a s = ∫⁻ b, (κ ^ n) b s ∂((κ ^ m) a)

/--
Checked C005 package instance, proved directly by mathlib's
`Kernel.pow_add_apply_eq_lintegral`.
-/
theorem c005DiscreteTimeChapmanKolmogorovSubstrate
    (α : Type u) [MeasurableSpace α] :
    DiscreteTimeChapmanKolmogorovSubstrate α where
  integral_kernel_power_leaf := by
    intro κ m n a s hs
    exact Kernel.pow_add_apply_eq_lintegral κ m n a hs

/--
C005 bridge to the pre-existing local wrapper name.

This keeps the theorem-tree package connected to the audited wrapper while
making clear that both names cover the same discrete-time kernel-power fact.
-/
theorem c005_integral_leaf_eq_wrapper
    {α : Type u} [MeasurableSpace α]
    (κ : Kernel α α) (m n : ℕ) (a : α) {s : Set α}
    (hs : MeasurableSet s) :
    (κ ^ (m + n)) a s = ∫⁻ b, (κ ^ n) b s ∂((κ ^ m) a) :=
  chapmanKolmogorov_kernel_pow_apply_wrapper κ m n a hs

/--
C005 status flag.

`false` records that the checked discrete-time Chapman-Kolmogorov substrate is
not the terminal continuous-time Kolmogorov forward/backward theorem.
-/
def c005DiscreteTimeSubstrateIsTerminalKolmogorovTheorem : Bool := false

/-- Checked sanity gate for the C005 non-terminal status flag. -/
theorem c005DiscreteTimeSubstrateIsTerminalKolmogorovTheorem_eq_false :
    c005DiscreteTimeSubstrateIsTerminalKolmogorovTheorem = false :=
  rfl

/-- C005 checked anchor names for public backfill. -/
def c005DiscreteTimeChapmanKolmogorovAnchorNames : List String := [
  "ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral",
  "AwesomeTheorems.Stage1.S1_M_216.chapmanKolmogorov_kernel_pow_apply_wrapper",
  "AwesomeTheorems.Stage1.S1_M_216.c005DiscreteTimeChapmanKolmogorovSubstrate"
]

/-- C005 local leaf-budget ledger. -/
def c005LocalLeafBudgetLedger : List String := [
  "C005-L01 checked-substrate: c005DiscreteTimeChapmanKolmogorovSubstrate compiles locally by Kernel.pow_add_apply_eq_lintegral and is under 100 proof steps.",
  "C005-L02 checked-bridge: c005_integral_leaf_eq_wrapper compiles locally and links the C005 tree leaf to chapmanKolmogorov_kernel_pow_apply_wrapper under 100 proof steps.",
  "C005-L03 non-terminal boundary: c005DiscreteTimeSubstrateIsTerminalKolmogorovTheorem_eq_false compiles locally; the discrete-time kernel-power fact is not a proof of the continuous-time forward/backward equations."
]

/--
C005 repo-local integration-debt flag.

The checked proof body comes from pinned mathlib inside the local Lake closure,
so this child does not retain anchor-only external integration debt.
-/
def c005RepoLocalIntegrationDebtRetained : Bool := false

/-- Checked sanity gate for the C005 integration-debt flag. -/
theorem c005RepoLocalIntegrationDebtRetained_eq_false :
    c005RepoLocalIntegrationDebtRetained = false :=
  rfl

/-! ## S1-M-216-C006 completion and public-surface gate -/

/-- File-level completion gate row for the C006 child task. -/
structure CompletionValidationGateRow where
  gateName : String
  requiredEvidence : String
  currentEvidence : String
  completionStatus : String

/--
C006 records the M0387 completion gates that must all close before this Stage1
slot can leave open status.

The current file validates as a non-terminal statement-shape artifact with
checked mathlib substrate wrappers.  It does not provide a terminal local proof
of the continuous-time Kolmogorov forward/backward equations, and this worker
does not merge public planning documents.
-/
def c006CompletionValidationGates : List CompletionValidationGateRow :=
  [ { gateName := "repo_local_lean_validation"
      requiredEvidence :=
        "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_216.lean passes after any terminal proof or wrapper lands"
      currentEvidence :=
        "owned Stage1 artifact validates as StatementShape plus checked mathlib kernel/process substrate wrappers, not as terminal theorem completion"
      completionStatus := "necessary_artifact_gate_only_not_terminal_completion" },
    { gateName := "terminal_kolmogorov_forward_backward_closure"
      requiredEvidence :=
        "local proof body or pinned imported dependency proves the continuous-time transition-density forward and backward equations with no sorry/admit/axiom placeholders"
      currentEvidence :=
        "no terminal continuous-time Markov semigroup/generator/density proof is present in the local Lake closure"
      completionStatus := "open_formalization_debt" },
    { gateName := "external_anchor_integration"
      requiredEvidence :=
        "any exact external Lean 4 terminal proof is pinned/imported/checked locally, or a concrete integration blocker is recorded before any completion claim"
      currentEvidence :=
        "no exact external terminal proof is cited as completed evidence, so no completed-state repo_local_integration_debt is retained"
      completionStatus := "open_external_audit_gate" },
    { gateName := "public_checklist_synchronization"
      requiredEvidence :=
        "serial integrator updates Docs/Stage1_Blueprint.md and associated todo/checklist surfaces after machine and public backfill gates are satisfied"
      currentEvidence :=
        "this child worker does not edit public planning documents; it provides integration-ready backfill text only"
      completionStatus := "open_public_doc_integration_gate" } ]

/-- C006 keeps exactly the four validation/synchronization gates above. -/
theorem c006CompletionValidationGates_length :
    c006CompletionValidationGates.length = 4 :=
  rfl

/-- Current C006 status flag: this slot must remain open after this child pass. -/
def c006Stage1StatusRemainsOpen : Bool := true

/-- Checked sanity gate for the C006 open-status flag. -/
theorem c006Stage1StatusRemainsOpen_eq_true :
    c006Stage1StatusRemainsOpen = true :=
  rfl

/--
Public backfill sentence for the C006 completion gate.

This is deliberately metadata for the serial public-doc integrator; it is not a
claim that the terminal Kolmogorov theorem is locally proved.
-/
def c006PublicBackfill : String :=
  "Keep S1-M-216 / THM-M-1092 open until `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_216.lean` validates with a terminal local proof body or pinned imported Lean closure for the continuous-time Kolmogorov forward/backward equations, no sorry/admit/axiom placeholders are present, any external Lean proof is pin/import/check integrated or blocked concretely, and Docs/Stage1_Blueprint.md plus todo/checklist surfaces are merged consistently in a serial integration patch."

end S1_M_216
end Stage1
end AwesomeTheorems
