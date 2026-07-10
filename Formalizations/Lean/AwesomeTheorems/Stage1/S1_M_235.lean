import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.Kernel.Composition.Comp
import Mathlib.Probability.Process.Filtration
import Mathlib.Probability.Process.FiniteDimensionalLaws
import Mathlib.Probability.Process.Kolmogorov

/-!
# S1-M-235 / THM-M-1042: Dynkin formula

This Stage1 artifact records a conservative Lean 4 statement boundary for
Dynkin's formula for Markov processes and their infinitesimal generators.

The pinned mathlib snapshot has Markov kernels, kernel composition,
Chapman-Kolmogorov identities for powers of a discrete-time kernel,
filtrations, finite-dimensional process laws, calculus, and Bochner/time
integrals.  It does not expose a terminal continuous-time Markov-process
generator API or a checked Dynkin formula theorem.

Accordingly this file gives a typed semigroup/expectation statement shape and
low-risk wrappers around existing mathlib kernel/process anchors.  It does not
prove Dynkin's formula.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_235

universe u v w

/-- Continuous nonnegative time is represented by real times with explicit `0 ≤ t` hypotheses. -/
abbrev Time : Type := ℝ

/--
Boundary data for a future Dynkin formula formalization.

`transitionKernel t` is the Markov transition kernel at time `t`; `generator`
is the infinitesimal generator on real-valued test functions.  The generator
domain and Markov/process assumptions are predicates rather than bundled APIs
because the pinned mathlib dependency does not yet provide a canonical
continuous-time Markov-generator object.
-/
structure DynkinFormulaData
    (State : Type u) [MeasurableSpace State] : Type (u + 1) where
  transitionKernel : Time → Kernel State State
  generator : (State → ℝ) → State → ℝ
  generatorDomain : (State → ℝ) → Prop
  markovProcessRealization : Prop

/-- The time-zero transition kernel is the identity kernel. -/
def InitialKernel
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) : Prop :=
  D.transitionKernel 0 = Kernel.id

/-- Nonnegative-time transition kernels are Markov kernels. -/
def MarkovKernelFamily
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) : Prop :=
  ∀ t : Time, 0 ≤ t → IsMarkovKernel (D.transitionKernel t)

/-- Continuous-time Chapman-Kolmogorov semigroup law for transition kernels. -/
def SemigroupLaw
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) : Prop :=
  ∀ s t : Time, 0 ≤ s → 0 ≤ t →
    D.transitionKernel (s + t) = D.transitionKernel t ∘ₖ D.transitionKernel s

/-- Expected value of a state test function after applying the transition kernel. -/
def transitionExpectation
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) (f : State → ℝ) (t : Time) (x : State) : ℝ :=
  ∫ y, f y ∂(D.transitionKernel t x)

/--
Integrability side conditions for the semigroup form of Dynkin's formula.

This predicate deliberately records only the analytic obligations needed for
the displayed formula to be meaningful.  Later work can strengthen it to a
canonical Feller-domain or martingale-problem API.
-/
def DynkinFormulaIntegrable
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) (f : State → ℝ) (x : State) (t : Time) : Prop :=
  Integrable f (D.transitionKernel t x) ∧
    (∀ s : Time, 0 ≤ s → s ≤ t →
      Integrable (fun y : State => D.generator f y) (D.transitionKernel s x)) ∧
      Integrable
        (fun s : Time =>
          transitionExpectation D (D.generator f) s x)
        (volume.restrict (Set.Icc (0 : Time) t))

/--
Semigroup/expectation form of Dynkin's formula:

`E_x[f(X_t)] = f x + ∫_0^t E_x[(A f)(X_s)] ds`.

The time integral is encoded as an integral against restricted Lebesgue measure
on `Set.Icc 0 t`; the explicit `0 ≤ t` premise keeps the real-time convention
unambiguous.
-/
def ExpectedDynkinFormula
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) (f : State → ℝ) (x : State) (t : Time) : Prop :=
  0 ≤ t →
    transitionExpectation D f t x =
      f x +
        ∫ s : Time,
          transitionExpectation D (D.generator f) s x
        ∂(volume.restrict (Set.Icc (0 : Time) t))

/--
Generator identification by the right derivative at time zero of the transition
semigroup on the test function `f`.
-/
def GeneratorAtZero
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) (f : State → ℝ) : Prop :=
  ∀ x : State,
    HasDerivWithinAt
      (fun t : Time => transitionExpectation D f t x)
      (D.generator f x) (Set.Ici 0) 0

/-- Normalized hypotheses for the Dynkin formula statement boundary. -/
def DynkinFormulaHypotheses
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) (f : State → ℝ) : Prop :=
  InitialKernel D ∧
    MarkovKernelFamily D ∧
      SemigroupLaw D ∧
        D.generatorDomain f ∧
          D.markovProcessRealization ∧
            GeneratorAtZero D f ∧
              ∀ x : State, ∀ t : Time, 0 ≤ t → DynkinFormulaIntegrable D f x t

/-- Terminal conclusion package for Dynkin's formula over all states and nonnegative times. -/
def DynkinFormulaConclusion
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) (f : State → ℝ) : Prop :=
  ∀ x : State, ∀ t : Time, ExpectedDynkinFormula D f x t

/--
Stage1 normalized statement shape for Dynkin's formula.

The real theorem should eventually derive `DynkinFormulaConclusion` from a
concrete Markov process/generator API.  This declaration freezes the expected
Lean boundary without claiming a terminal proof.
-/
def StatementShape : Prop :=
  ∀ (State : Type u) [MeasurableSpace State],
    ∀ D : DynkinFormulaData State,
      ∀ f : State → ℝ,
        DynkinFormulaHypotheses D f → DynkinFormulaConclusion D f

/-- The normalized statement unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (State : Type u) [MeasurableSpace State],
        ∀ D : DynkinFormulaData State,
          ∀ f : State → ℝ,
            DynkinFormulaHypotheses D f → DynkinFormulaConclusion D f :=
  Iff.rfl

/-- Projection wrapper: the hypotheses include nonnegative-time Markov kernels. -/
theorem hypotheses_markovKernel
    {State : Type u} [MeasurableSpace State]
    {D : DynkinFormulaData State} {f : State → ℝ}
    (h : DynkinFormulaHypotheses D f) :
    ∀ t : Time, 0 ≤ t → IsMarkovKernel (D.transitionKernel t) :=
  h.2.1

/-- Projection wrapper: the hypotheses include the Chapman-Kolmogorov semigroup law. -/
theorem hypotheses_semigroupLaw
    {State : Type u} [MeasurableSpace State]
    {D : DynkinFormulaData State} {f : State → ℝ}
    (h : DynkinFormulaHypotheses D f) :
    SemigroupLaw D :=
  h.2.2.1

/-- Projection wrapper: the hypotheses include generator-domain membership for the test function. -/
theorem hypotheses_generatorDomain
    {State : Type u} [MeasurableSpace State]
    {D : DynkinFormulaData State} {f : State → ℝ}
    (h : DynkinFormulaHypotheses D f) :
    D.generatorDomain f :=
  h.2.2.2.1

/-- Projection wrapper: the hypotheses include generator identification at time zero. -/
theorem hypotheses_generatorAtZero
    {State : Type u} [MeasurableSpace State]
    {D : DynkinFormulaData State} {f : State → ℝ}
    (h : DynkinFormulaHypotheses D f) :
    GeneratorAtZero D f :=
  h.2.2.2.2.2.1

/-- Projection wrapper: a terminal conclusion package exposes the formula at each state and time. -/
theorem conclusion_expectedDynkinFormula
    {State : Type u} [MeasurableSpace State]
    {D : DynkinFormulaData State} {f : State → ℝ}
    (h : DynkinFormulaConclusion D f) (x : State) (t : Time) :
    ExpectedDynkinFormula D f x t :=
  h x t

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
has measurable coordinate maps.  This is not Dynkin's formula, but it is
relevant process-law substrate for this Stage1 slot.
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

/-! ## Audit probes retained in the checked file. -/

#check ProbabilityTheory.Kernel
#check ProbabilityTheory.IsMarkovKernel
#check ProbabilityTheory.Kernel.deterministic
#check ProbabilityTheory.Kernel.comp
#check ProbabilityTheory.Kernel.comp_apply'
#check ProbabilityTheory.Kernel.lintegral_comp
#check ProbabilityTheory.Kernel.pow_add
#check ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral
#check MeasureTheory.Filtration
#check ProbabilityTheory.IsKolmogorovProcess
#check ProbabilityTheory.IsAEKolmogorovProcess
#check ProbabilityTheory.IsKolmogorovProcess.measurable
#check ProbabilityTheory.IsAEKolmogorovProcess.aemeasurable
#check HasDerivWithinAt
#check Integrable
#check transitionExpectation
#check ExpectedDynkinFormula
#check StatementShape

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
  "Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic",
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
  "MeasureTheory.Filtration",
  "ProbabilityTheory.isProjectiveMeasureFamily_map_restrict",
  "ProbabilityTheory.map_eq_iff_forall_finset_map_restrict_eq",
  "ProbabilityTheory.IsKolmogorovProcess",
  "ProbabilityTheory.IsAEKolmogorovProcess",
  "ProbabilityTheory.IsKolmogorovProcess.measurable",
  "ProbabilityTheory.IsAEKolmogorovProcess.aemeasurable",
  "HasDerivWithinAt",
  "MeasureTheory.Integrable"
]

/--
Search terms that did not locate a terminal Dynkin formula theorem in the local
pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Dynkin formula",
  "DynkinFormula",
  "Dynkin's formula",
  "Markov generator",
  "infinitesimal generator",
  "Markov semigroup",
  "transition semigroup",
  "Feller semigroup",
  "martingale problem",
  "Ito formula",
  "Itô formula",
  "continuous-time Markov"
]

/--
External Lean 4 projects and pinned revisions audited for this slot.

These entries are evidence targets only.  They are not terminal theorem anchors,
and they are not imported dependencies of this repository.
-/
def externalLeanAuditTargets : List String := [
  "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "RemyDegenne/brownian-motion@91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "RemyDegenne/kolmogorov_extension4@e236e968c2b038b952444df54075a6e8b1058380"
]

/--
Concrete blockers recorded by the external audit.

The Brownian-motion project has relevant stochastic-process and stochastic-
integral development, but its public README marks the Ito-lemma branch as in
progress and its blueprint theorem for Ito's formula is not a checked Lean
theorem body.  The Kolmogorov-extension project supplies construction
substrate, not a Dynkin-formula/generator theorem.  The pinned mathlib tree has
kernel/process substrate but no terminal continuous-time generator/Dynkin
formula theorem found by the search terms above.
-/
def externalAuditBlockers : List String := [
  "No checked external Lean 4 theorem named DynkinFormula was found.",
  "No checked external Lean 4 MarkovSemigroup/FellerSemigroup/InfinitesimalGenerator API was found that proves Dynkin formula.",
  "RemyDegenne/brownian-motion records stochastic integrals and Ito's lemma as in progress, not terminal Lean closure.",
  "RemyDegenne/kolmogorov_extension4 records Kolmogorov-extension substrate, not a Dynkin-formula theorem.",
  "No external proof was pinned, imported, or checked by this child."
]

/-! ## S1-M-235-C003 first closure-target decision -/

/-- Candidate scopes for the first terminal proof attempt after the statement-shape boundary. -/
inductive FirstClosureTarget where
  | finiteStateContinuousTimeMarkovChain
  | fellerSemigroup
  | martingaleProblem

/--
C003 decision: use finite-state continuous-time Markov chains as the first
closure target.

This is narrower than a general Feller-semigroup theorem and avoids making the
martingale-problem formulation the first dependency-heavy object model.  The
finite-state route can build a concrete rate-matrix/generator package before
lifting the result back toward the existing kernel-semigroup statement shape.
-/
def c003SelectedFirstClosureTarget : FirstClosureTarget :=
  FirstClosureTarget.finiteStateContinuousTimeMarkovChain

/-- Checked sanity gate for the C003 closure-target decision. -/
theorem c003SelectedFirstClosureTarget_eq_finiteStateCTMC :
    c003SelectedFirstClosureTarget =
      FirstClosureTarget.finiteStateContinuousTimeMarkovChain :=
  rfl

/-- C003 decision metadata for later public backfill. -/
def c003ClosureTargetDecisionNotes : List String := [
  "First closure target: finite-state continuous-time Markov chains.",
  "Reason: the repo-local artifact already has kernel, semigroup, derivative, and integral statement-shape substrate but no terminal Feller-semigroup/generator-domain API.",
  "Finite-state CTMCs give the smallest honest terminal branch: rate matrix, finite sums for expectations, transition semigroup, generator-at-zero, and integral formula.",
  "Feller semigroups remain the broader later target after a concrete bounded-continuous-function and generator-domain API exists.",
  "The martingale-problem formulation remains a later bridge from the semigroup formula, not the first closure target for this slot."
]

/-! ## S1-M-235-C004 independent theorem-tree packages -/

/--
The five C004 packages requested by the public Stage1 line.  Each constructor is
kept independent so later workers can replace the current statement-boundary
predicate with a concrete proof package without changing the public names.
-/
inductive DynkinTheoremTreePackage where
  | initialKernel
  | markovKernelFamily
  | semigroupLaw
  | generatorAtZero
  | dynkinFormulaIntegrable
  deriving DecidableEq, Repr

/--
Package-local target for the C004 split.  The first three packages are
kernel-semigroup obligations; the last two package the generator and analytic
integrability obligations for the chosen test function.
-/
def DynkinTheoremTreePackageTarget
    {State : Type u} [MeasurableSpace State]
    (D : DynkinFormulaData State) (f : State → ℝ) :
    DynkinTheoremTreePackage → Prop
  | .initialKernel => InitialKernel D
  | .markovKernelFamily => MarkovKernelFamily D
  | .semigroupLaw => SemigroupLaw D
  | .generatorAtZero => GeneratorAtZero D f
  | .dynkinFormulaIntegrable =>
      ∀ x : State, ∀ t : Time, 0 ≤ t → DynkinFormulaIntegrable D f x t

/-- C004-local status vocabulary; none of these rows is a terminal Dynkin proof. -/
inductive DynkinPackageStatus where
  | checkedStatementBoundary
  | formalizationDebt
  deriving DecidableEq, Repr

/-- One independently budgeted theorem-tree leaf for the C004 package split. -/
structure DynkinPackageLeafBudget where
  package : DynkinTheoremTreePackage
  leafId : String
  obligation : String
  upstreamInputs : String
  downstreamInterface : String
  budgetStepLimit : Nat
  status : DynkinPackageStatus
  completionBoundary : String

/-- M0387 local proof-leaf budget limit used by the C004 split. -/
def c004LeafBudgetLimit : Nat :=
  100

/--
Integration-ready package ledger for C004.

The entries record checked local statement boundaries and the next concrete
proof obligations.  They do not claim that Dynkin's formula is proved: the
terminal finite-state CTMC/Feller/martingale proof body remains open
formalization debt until a repo-local validation command checks it.
-/
def c004DynkinPackageLeafBudgets : List DynkinPackageLeafBudget := [
  {
    package := .initialKernel,
    leafId := "S1-M-235-C004-L001-initial-kernel",
    obligation := "Prove that the transition kernel at time zero is the identity kernel for the selected continuous-time Markov model.",
    upstreamInputs := "future finite-state CTMC transition kernel or pinned continuous-time Markov semigroup API",
    downstreamInterface := "InitialKernel D",
    budgetStepLimit := c004LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "statement-boundary checked only: InitialKernel is typed, but no concrete CTMC kernel proof is present"
  },
  {
    package := .markovKernelFamily,
    leafId := "S1-M-235-C004-L002-markov-kernel-family",
    obligation := "Show every nonnegative-time transition kernel is an IsMarkovKernel instance or theorem.",
    upstreamInputs := "mathlib Kernel/IsMarkovKernel substrate plus future transition-kernel construction",
    downstreamInterface := "MarkovKernelFamily D",
    budgetStepLimit := c004LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "statement-boundary checked only: deterministic/composition Markov-kernel wrappers are local anchors, not a continuous-time family proof"
  },
  {
    package := .semigroupLaw,
    leafId := "S1-M-235-C004-L003-semigroup-law",
    obligation := "Prove the continuous-time Chapman-Kolmogorov law with the repository's kernel-composition order fixed.",
    upstreamInputs := "mathlib kernel composition and discrete-time Kernel.pow_add_apply_eq_lintegral substrate",
    downstreamInterface := "SemigroupLaw D",
    budgetStepLimit := c004LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "statement-boundary checked only: discrete-time kernel powers are anchored, but no continuous-time semigroup proof is present"
  },
  {
    package := .generatorAtZero,
    leafId := "S1-M-235-C004-L004-generator-at-zero",
    obligation := "Identify the generator as the right derivative at zero of the transition expectation for each state.",
    upstreamInputs := "HasDerivWithinAt, transitionExpectation, and future concrete generator/domain construction",
    downstreamInterface := "GeneratorAtZero D f",
    budgetStepLimit := c004LeafBudgetLimit,
    status := .formalizationDebt,
    completionBoundary := "unchecked formalization debt: no finite-state rate-matrix or Feller-generator derivative proof is present"
  },
  {
    package := .dynkinFormulaIntegrable,
    leafId := "S1-M-235-C004-L005-dynkin-formula-integrable",
    obligation := "Discharge the test-function, generator, and time-integrand integrability side conditions needed by the displayed Dynkin formula.",
    upstreamInputs := "Integrable, transitionExpectation, restricted Lebesgue time integral, and future boundedness/measurability hypotheses",
    downstreamInterface := "∀ x t, 0 ≤ t → DynkinFormulaIntegrable D f x t",
    budgetStepLimit := c004LeafBudgetLimit,
    status := .formalizationDebt,
    completionBoundary := "unchecked formalization debt: the analytic integrability proof is not supplied by the current statement-shape artifact"
  }
]

/-- The C004 package split contains exactly the five requested independent leaves. -/
theorem c004DynkinPackageLeafBudgets_length :
    c004DynkinPackageLeafBudgets.length = 5 := by
  native_decide

/-- Every C004 local leaf is explicitly budgeted at the M0387 `<= 100` threshold. -/
theorem c004DynkinPackageLeafBudgets_all_le_100 :
    c004DynkinPackageLeafBudgets.all
      (fun row => row.budgetStepLimit ≤ c004LeafBudgetLimit) = true := by
  native_decide

/-- The normalized hypotheses expose the C004 initial-kernel package. -/
theorem hypotheses_initialKernel
    {State : Type u} [MeasurableSpace State]
    {D : DynkinFormulaData State} {f : State → ℝ}
    (h : DynkinFormulaHypotheses D f) :
    InitialKernel D :=
  h.1

/-- The normalized hypotheses expose the C004 integrability package. -/
theorem hypotheses_dynkinFormulaIntegrable
    {State : Type u} [MeasurableSpace State]
    {D : DynkinFormulaData State} {f : State → ℝ}
    (h : DynkinFormulaHypotheses D f) :
    ∀ x : State, ∀ t : Time, 0 ≤ t → DynkinFormulaIntegrable D f x t :=
  h.2.2.2.2.2.2

/-- Every package-local target is available from the normalized hypothesis bundle. -/
theorem packageTarget_of_hypotheses
    {State : Type u} [MeasurableSpace State]
    {D : DynkinFormulaData State} {f : State → ℝ}
    (h : DynkinFormulaHypotheses D f) (package : DynkinTheoremTreePackage) :
    DynkinTheoremTreePackageTarget D f package := by
  cases package
  · exact hypotheses_initialKernel h
  · exact hypotheses_markovKernel h
  · exact hypotheses_semigroupLaw h
  · exact hypotheses_generatorAtZero h
  · exact hypotheses_dynkinFormulaIntegrable h

/--
The C004 split is ready for public backfill as an open package ledger, not as a
completion claim.
-/
def c004PackageSplitReadyForPublicBackfill : Bool :=
  true

/-- C004 does not close Dynkin's formula. -/
def c004ClosesDynkinFormula : Bool :=
  false

/--
No completed state in the C004 package ledger retains repo-local integration
debt: there is no completed state at all.
-/
def c004NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c004PackageSplitReadyForPublicBackfill_eq_true :
    c004PackageSplitReadyForPublicBackfill = true :=
  rfl

theorem c004ClosesDynkinFormula_eq_false :
    c004ClosesDynkinFormula = false :=
  rfl

theorem c004NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c004NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check DynkinTheoremTreePackage
#check DynkinTheoremTreePackageTarget
#check c004DynkinPackageLeafBudgets
#check c004DynkinPackageLeafBudgets_length
#check c004DynkinPackageLeafBudgets_all_le_100
#check packageTarget_of_hypotheses

/-! ## S1-M-235-C005 discrete-time Chapman-Kolmogorov substrate -/

/--
C005 role tags for the checked discrete-time Chapman-Kolmogorov substrate.
The continuous-time boundary row is deliberately separate from the checked
mathlib wrappers.
-/
inductive C005ChapmanKolmogorovRole where
  | kernelPowerEquation
  | integralKernelPowerEquation
  | continuousTimeBoundary
  deriving DecidableEq, Repr

/-- C005 status tags; no row here is a terminal continuous-time Dynkin theorem. -/
inductive C005ChapmanKolmogorovStatus where
  | checkedDiscreteTimeSubstrate
  | boundaryOnlyNotContinuousTime
  deriving DecidableEq, Repr

/-- One M0387-budgeted C005 leaf connecting mathlib kernel powers to the theorem tree. -/
structure C005ChapmanKolmogorovLeafBudget where
  role : C005ChapmanKolmogorovRole
  leafId : String
  mathlibAnchor : String
  repoLocalAnchor : String
  theoremTreeUse : String
  budgetStepLimit : Nat
  status : C005ChapmanKolmogorovStatus
  completionBoundary : String

/-- M0387 local proof-leaf budget limit used by the C005 discrete-time substrate split. -/
def c005LeafBudgetLimit : Nat :=
  100

/--
Integration-ready C005 ledger.

The first two rows are checked mathlib-backed discrete-time kernel-power
identities.  The third row prevents this substrate from being read as a proof
of the continuous-time semigroup law or Dynkin's formula.
-/
def c005ChapmanKolmogorovLeafBudgets : List C005ChapmanKolmogorovLeafBudget := [
  {
    role := .kernelPowerEquation,
    leafId := "S1-M-235-C005-L001-kernel-pow-add",
    mathlibAnchor := "ProbabilityTheory.Kernel.pow_add",
    repoLocalAnchor := "chapmanKolmogorov_kernel_pow_wrapper",
    theoremTreeUse := "Discrete-time Chapman-Kolmogorov equality for powers of a single Markov transition kernel.",
    budgetStepLimit := c005LeafBudgetLimit,
    status := .checkedDiscreteTimeSubstrate,
    completionBoundary := "checked repo-local wrapper only: discrete-time kernel powers, not continuous-time Dynkin formula"
  },
  {
    role := .integralKernelPowerEquation,
    leafId := "S1-M-235-C005-L002-kernel-pow-add-apply-lintegral",
    mathlibAnchor := "ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral",
    repoLocalAnchor := "chapmanKolmogorov_kernel_pow_apply_wrapper",
    theoremTreeUse := "Integral form of discrete-time Chapman-Kolmogorov for the m+n step transition probability of a measurable set.",
    budgetStepLimit := c005LeafBudgetLimit,
    status := .checkedDiscreteTimeSubstrate,
    completionBoundary := "checked repo-local wrapper only: integral kernel-power substrate, not a generator or continuous-time semigroup proof"
  },
  {
    role := .continuousTimeBoundary,
    leafId := "S1-M-235-C005-L003-continuous-time-boundary",
    mathlibAnchor := "none",
    repoLocalAnchor := "SemigroupLaw",
    theoremTreeUse := "Boundary marker saying the checked discrete-time substrate can inform the future SemigroupLaw package but does not discharge it.",
    budgetStepLimit := c005LeafBudgetLimit,
    status := .boundaryOnlyNotContinuousTime,
    completionBoundary := "open formalization debt: continuous-time Chapman-Kolmogorov and Dynkin formula remain unproved"
  }
]

/-- The C005 substrate ledger has exactly the three intended theorem-tree rows. -/
theorem c005ChapmanKolmogorovLeafBudgets_length :
    c005ChapmanKolmogorovLeafBudgets.length = 3 := by
  native_decide

/-- Every C005 row is explicitly budgeted at the M0387 `<= 100` threshold. -/
theorem c005ChapmanKolmogorovLeafBudgets_all_le_100 :
    c005ChapmanKolmogorovLeafBudgets.all
      (fun row => row.budgetStepLimit ≤ c005LeafBudgetLimit) = true := by
  native_decide

/--
C005 checked substrate theorem: mathlib's integral Chapman-Kolmogorov identity
for powers of one discrete-time transition kernel is available repo-locally.
-/
theorem c005_kernel_pow_add_apply_eq_lintegral_substrate
    {α : Type u} [MeasurableSpace α]
    (κ : Kernel α α) (m n : ℕ) (a : α) {s : Set α}
    (hs : MeasurableSet s) :
    (κ ^ (m + n)) a s = ∫⁻ b, (κ ^ n) b s ∂((κ ^ m) a) :=
  chapmanKolmogorov_kernel_pow_apply_wrapper κ m n a hs

/--
C005 checked substrate theorem: the corresponding kernel-power composition
identity is available repo-locally.
-/
theorem c005_kernel_pow_add_substrate
    {α : Type u} [MeasurableSpace α]
    (κ : Kernel α α) (m n : ℕ) :
    κ ^ (m + n) = (κ ^ m) ∘ₖ (κ ^ n) :=
  chapmanKolmogorov_kernel_pow_wrapper κ m n

/-- C005 supplies checked discrete-time substrate for `SemigroupLaw`. -/
def c005SuppliesDiscreteTimeChapmanKolmogorovSubstrate : Bool :=
  true

/-- C005 does not supply a continuous-time Chapman-Kolmogorov proof. -/
def c005SuppliesContinuousTimeSemigroupLaw : Bool :=
  false

/-- C005 does not close Dynkin's formula. -/
def c005ClosesDynkinFormula : Bool :=
  false

/--
No completed C005 state retains repo-local integration debt: the checked rows
are repo-local mathlib wrappers, and the continuous-time/Dynkin rows remain
open formalization debt rather than completed states.
-/
def c005NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c005SuppliesDiscreteTimeChapmanKolmogorovSubstrate_eq_true :
    c005SuppliesDiscreteTimeChapmanKolmogorovSubstrate = true :=
  rfl

theorem c005SuppliesContinuousTimeSemigroupLaw_eq_false :
    c005SuppliesContinuousTimeSemigroupLaw = false :=
  rfl

theorem c005ClosesDynkinFormula_eq_false :
    c005ClosesDynkinFormula = false :=
  rfl

theorem c005NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c005NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check C005ChapmanKolmogorovRole
#check C005ChapmanKolmogorovStatus
#check c005ChapmanKolmogorovLeafBudgets
#check c005ChapmanKolmogorovLeafBudgets_length
#check c005ChapmanKolmogorovLeafBudgets_all_le_100
#check c005_kernel_pow_add_apply_eq_lintegral_substrate
#check c005_kernel_pow_add_substrate

/-! ## S1-M-235-C006 Stage1 completion gate -/

/--
C006 status gate for the public Stage1 checkbox.

The current artifact has checked statement-shape and substrate rows, but it has
neither a terminal repo-local Dynkin proof nor a pinned external Lean closure.
The public Stage1 status must therefore remain open until a future patch
changes these gate inputs and validates the file locally.
-/
structure C006Stage1CompletionGate where
  terminalLocalProofValidated : Bool
  pinnedExternalLeanClosureValidated : Bool
  publicDocsMergedConsistently : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool

/-- Current C006 gate values for this Stage1 slot. -/
def c006Stage1CompletionGate : C006Stage1CompletionGate where
  terminalLocalProofValidated := false
  pinnedExternalLeanClosureValidated := false
  publicDocsMergedConsistently := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true

/--
Stage1 may close only after a terminal local proof or pinned external Lean
closure validates and the public documentation has been merged consistently.
-/
def C006Stage1CompletionGate.closureAllowed
    (gate : C006Stage1CompletionGate) : Bool :=
  (gate.terminalLocalProofValidated ||
      gate.pinnedExternalLeanClosureValidated) &&
    gate.publicDocsMergedConsistently &&
      gate.noCompletedStateRetainsRepoLocalIntegrationDebt

/-- C006 records that the Stage1 status must remain open in the current artifact. -/
def c006Stage1StatusMustRemainOpen : Bool :=
  !C006Stage1CompletionGate.closureAllowed c006Stage1CompletionGate

/-- C006 does not close Dynkin's formula. -/
def c006ClosesDynkinFormula : Bool :=
  false

/--
No completed C006 state retains repo-local integration debt: there is no
completed Dynkin formula state, and no external terminal proof was left as an
anchor-only completion.
-/
def c006NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c006_terminalLocalProofValidated_eq_false :
    c006Stage1CompletionGate.terminalLocalProofValidated = false :=
  rfl

theorem c006_pinnedExternalLeanClosureValidated_eq_false :
    c006Stage1CompletionGate.pinnedExternalLeanClosureValidated = false :=
  rfl

theorem c006_publicDocsMergedConsistently_eq_false :
    c006Stage1CompletionGate.publicDocsMergedConsistently = false :=
  rfl

theorem c006_closureAllowed_eq_false :
    C006Stage1CompletionGate.closureAllowed c006Stage1CompletionGate = false :=
  rfl

theorem c006Stage1StatusMustRemainOpen_eq_true :
    c006Stage1StatusMustRemainOpen = true :=
  rfl

theorem c006ClosesDynkinFormula_eq_false :
    c006ClosesDynkinFormula = false :=
  rfl

theorem c006NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c006NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check C006Stage1CompletionGate
#check C006Stage1CompletionGate.closureAllowed
#check c006Stage1CompletionGate
#check c006Stage1StatusMustRemainOpen
#check c006_closureAllowed_eq_false

end S1_M_235
end Stage1
end AwesomeTheorems
