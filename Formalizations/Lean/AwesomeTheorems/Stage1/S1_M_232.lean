import Mathlib.Probability.Kernel.CondDistrib
import Mathlib.Probability.Process.Filtration
import Mathlib.Probability.Process.Stopping
import Mathlib.Probability.Independence.Process.Basic
import Mathlib.Probability.Independence.Conditional

/-!
# S1-M-232 / THM-M-1039: Markov property of SDE solutions

This Stage1 artifact records a conservative Lean 4 statement-shape boundary
for the theorem that solutions of stochastic differential equations are Markov
processes.

The pinned mathlib snapshot provides Markov kernels, regular conditional
distributions, filtrations, stopping-time infrastructure, conditional
expectations, and independence predicates for random variables/processes.  This
audit did not find a terminal SDE, Brownian motion, stochastic integral, or
Itô-map theorem in the local Lean dependency closure.

The declarations below therefore keep the SDE equation, coefficient
assumptions, strong uniqueness, and noise-increment hypotheses as explicit
proposition fields, while expressing the Markov conclusion with concrete
mathlib objects: filtrations, transition kernels, conditional expectations, and
regular conditional distributions.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped ENNReal ProbabilityTheory

namespace AwesomeTheorems.Stage1.S1_M_232

universe u v w

/--
Input data for a future formal theorem asserting that an SDE solution is Markov.

The fields `sdeIntegralEquation`, `coefficientsMeasurable`,
`strongExistenceUniqueness`, `drivingNoiseIndependentIncrements`, and
`transitionSemigroupIdentified` are intentionally abstract: the current local
mathlib closure has no canonical SDE/stochastic-integral/Brownian API.  The
probability-space, process, filtration, and transition-kernel boundary is
expressed with concrete mathlib types.
-/
structure SDEMarkovData (Time : Type u) (Ω : Type v) (State : Type w)
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State] where
  μ : Measure Ω
  process : Time → Ω → State
  filtration : Filtration Time (inferInstance : MeasurableSpace Ω)
  transitionKernel : Time → Time → Kernel State State
  processMeasurable : ∀ t, Measurable (process t)
  processAdapted : ∀ t, Measurable[filtration t] (process t)
  finiteMeasure : IsFiniteMeasure μ
  transitionMarkov : ∀ s t, s ≤ t → IsMarkovKernel (transitionKernel s t)
  sdeIntegralEquation : Prop
  coefficientsMeasurable : Prop
  strongExistenceUniqueness : Prop
  drivingNoiseIndependentIncrements : Prop
  transitionSemigroupIdentified : Prop

attribute [instance] SDEMarkovData.finiteMeasure

/-- The abstract SDE-side hypotheses needed before the Markov conclusion. -/
def SDEHypotheses {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : SDEMarkovData Time Ω State) : Prop :=
  D.sdeIntegralEquation ∧ D.coefficientsMeasurable ∧
    D.strongExistenceUniqueness ∧ D.drivingNoiseIndependentIncrements ∧
      D.transitionSemigroupIdentified

/--
The regular-conditional-distribution version of the transition-law statement.

For `s ≤ t`, the conditional distribution of `X_t` given `X_s` is the transition
kernel `P_{s,t}`.  This is weaker than a full filtration-relative Markov
property, but it is a concrete mathlib-facing anchor.
-/
def ConditionalTransitionLaw {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State] [StandardBorelSpace State]
    [Nonempty State] (D : SDEMarkovData Time Ω State) : Prop :=
  ∀ s t, s ≤ t →
    condDistrib (D.process t) (D.process s) D.μ = D.transitionKernel s t

/-- Bounded measurable real-valued test functions on the state space. -/
def BoundedMeasurableTest (State : Type*) [MeasurableSpace State]
    (f : State → ℝ) : Prop :=
  Measurable f ∧ ∃ C : ℝ, 0 ≤ C ∧ ∀ x, |f x| ≤ C

/--
Filtration-relative Markov property, stated through conditional expectations of
measurable indicator tests.

For every measurable state set `A`, the conditional probability of `X_t ∈ A`
given the past filtration at time `s` is the transition kernel evaluated at the
current state `X_s`.
-/
def FiltrationMarkovProperty {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : SDEMarkovData Time Ω State) : Prop :=
  ∀ s t, s ≤ t → ∀ A : Set State, MeasurableSet A →
    D.μ[(D.process t ⁻¹' A).indicator (fun _ => (1 : ℝ)) | D.filtration s]
      =ᵐ[D.μ] fun ω => (D.transitionKernel s t (D.process s ω)).real A

/--
Filtration-relative Markov property for bounded measurable real-valued tests.

For every bounded measurable `f`, the conditional expectation of `f X_t` given
the past filtration at time `s` is the transition-kernel integral of `f`
evaluated at the current state `X_s`.
-/
def FiltrationMarkovPropertyBoundedTests {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : SDEMarkovData Time Ω State) : Prop :=
  ∀ s t, s ≤ t → ∀ f : State → ℝ, BoundedMeasurableTest State f →
    D.μ[(fun ω => f (D.process t ω)) | D.filtration s]
      =ᵐ[D.μ] fun ω => ∫ x, f x ∂(D.transitionKernel s t (D.process s ω))

/-- Concrete conclusion package expected from a terminal SDE Markov theorem. -/
structure SDEMarkovConclusion {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State] [StandardBorelSpace State]
    [Nonempty State] (D : SDEMarkovData Time Ω State) : Type _ where
  conditionalTransitionLaw : ConditionalTransitionLaw D
  filtrationMarkovProperty : FiltrationMarkovProperty D
  boundedMeasurableMarkovProperty : FiltrationMarkovPropertyBoundedTests D

/--
Normalized Stage1 statement shape for THM-M-1039.

Given an SDE data package satisfying the abstract equation, coefficient,
strong-uniqueness, independent-increment, and transition-identification
hypotheses, the solution should produce the Markov conclusion package above.
-/
def StatementShape (Time Ω State : Type*) [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State] [StandardBorelSpace State]
    [Nonempty State] : Prop :=
  ∀ D : SDEMarkovData Time Ω State,
    SDEHypotheses D → Nonempty (SDEMarkovConclusion D)

/-- The normalized statement shape unfolds to the expected data-package target. -/
theorem statementShape_iff (Time Ω State : Type*) [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State] [StandardBorelSpace State]
    [Nonempty State] :
    StatementShape Time Ω State ↔
      ∀ D : SDEMarkovData Time Ω State,
        SDEHypotheses D → Nonempty (SDEMarkovConclusion D) :=
  Iff.rfl

/-- Checked wrapper: every packaged transition kernel is a Markov kernel. -/
theorem transitionKernel_isMarkov {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : SDEMarkovData Time Ω State) {s t : Time} (hst : s ≤ t) :
    IsMarkovKernel (D.transitionKernel s t) :=
  D.transitionMarkov s t hst

/-- Checked wrapper: the packaged filtration is monotone in time. -/
theorem filtration_mono {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    (D : SDEMarkovData Time Ω State) {s t : Time} (hst : s ≤ t) :
    D.filtration s ≤ D.filtration t :=
  D.filtration.mono hst

/-- Checked wrapper: the regular conditional law given a state is a Markov kernel. -/
theorem condDistrib_process_isMarkovKernel {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State] [StandardBorelSpace State]
    [Nonempty State] (D : SDEMarkovData Time Ω State) (s t : Time) :
    IsMarkovKernel (condDistrib (D.process t) (D.process s) D.μ) := by
  infer_instance

/--
Checked mathlib anchor: composing the conditional distribution of `X_t` given
`X_s` with the law of `X_s` recovers the law of `X_t`.
-/
theorem condDistrib_process_comp_map {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State] [StandardBorelSpace State]
    [Nonempty State] (D : SDEMarkovData Time Ω State) (s t : Time) :
    condDistrib (D.process t) (D.process s) D.μ ∘ₘ (D.μ.map (D.process s)) =
      D.μ.map (D.process t) := by
  exact condDistrib_comp_map (D.processMeasurable s).aemeasurable
    (D.processMeasurable t).aemeasurable

/--
Checked mathlib anchor: conditional distributions agree a.e. with conditional
expectations of indicator tests given the current state.
-/
theorem condDistrib_process_ae_eq_condExp {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State] [StandardBorelSpace State]
    [Nonempty State] (D : SDEMarkovData Time Ω State) (s t : Time)
    {A : Set State} (hA : MeasurableSet A) :
    (fun ω => (condDistrib (D.process t) (D.process s) D.μ (D.process s ω)).real A)
      =ᵐ[D.μ] D.μ[(D.process t ⁻¹' A).indicator (fun _ => (1 : ℝ)) |
        MeasurableSpace.comap (D.process s) (inferInstance : MeasurableSpace State)] := by
  exact condDistrib_ae_eq_condExp (D.processMeasurable s) (D.processMeasurable t) hA

/-- A bounded measurable test carries its measurable-function component. -/
theorem BoundedMeasurableTest.measurable {State : Type*} [MeasurableSpace State]
    {f : State → ℝ} (hf : BoundedMeasurableTest State f) :
    Measurable f :=
  hf.1

/-- A bounded measurable test carries a uniform real bound. -/
theorem BoundedMeasurableTest.exists_bound {State : Type*} [MeasurableSpace State]
    {f : State → ℝ} (hf : BoundedMeasurableTest State f) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ x, |f x| ≤ C :=
  hf.2

/-- The SDE-side hypotheses project to the abstract SDE equation field. -/
theorem SDEHypotheses.sdeIntegralEquation {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : SDEMarkovData Time Ω State} (h : SDEHypotheses D) :
    D.sdeIntegralEquation :=
  h.1

/-- The SDE-side hypotheses project to the coefficient-measurability field. -/
theorem SDEHypotheses.coefficientsMeasurable {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : SDEMarkovData Time Ω State} (h : SDEHypotheses D) :
    D.coefficientsMeasurable :=
  h.2.1

/-- The SDE-side hypotheses project to the strong existence/uniqueness field. -/
theorem SDEHypotheses.strongExistenceUniqueness {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : SDEMarkovData Time Ω State} (h : SDEHypotheses D) :
    D.strongExistenceUniqueness :=
  h.2.2.1

/-- The SDE-side hypotheses project to the independent-increment field. -/
theorem SDEHypotheses.drivingNoiseIndependentIncrements {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : SDEMarkovData Time Ω State} (h : SDEHypotheses D) :
    D.drivingNoiseIndependentIncrements :=
  h.2.2.2.1

/-- The SDE-side hypotheses project to the transition-identification field. -/
theorem SDEHypotheses.transitionSemigroupIdentified {Time Ω State : Type*} [Preorder Time]
    [MeasurableSpace Ω] [MeasurableSpace State]
    {D : SDEMarkovData Time Ω State} (h : SDEHypotheses D) :
    D.transitionSemigroupIdentified :=
  h.2.2.2.2

/-- mathlib modules checked while locating repo-local anchors for this SDE slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Kernel.CondDistrib",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Composition.MeasureComp",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Independence.Process.Basic",
  "Mathlib.Probability.Independence.Process.HasIndepIncrements",
  "Mathlib.Probability.Independence.Conditional",
  "Mathlib.Probability.ConditionalExpectation",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.Filtration.mono",
  "MeasureTheory.IsStoppingTime",
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.condDistrib",
  "ProbabilityTheory.condDistrib_comp_map",
  "ProbabilityTheory.condDistrib_ae_eq_condExp",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.condIndepFun_iff_condDistrib_prod_ae_eq_prodMkRight"
]

/--
Search terms that did not locate a terminal SDE Markov-property theorem in the
pinned local mathlib snapshot.
-/
def absentTerminalSearchTerms : List String := [
  "SDE",
  "stochastic differential equation",
  "Ito",
  "Itô",
  "Brownian",
  "Markov property",
  "strong Markov",
  "stochastic integral",
  "semimartingale",
  "diffusion process"
]

/-!
## External Brownian-motion audit

Child audit `S1-M-232-C002` inspected `RemyDegenne/brownian-motion` at
commit `91885e6172648ea7f9c6a16b3a7069f92c88e023`. The project is a useful
upstream API anchor for Brownian motion and early stochastic-integral
infrastructure, but it is not imported here: its toolchain is
`leanprover/lean4:v4.30.0-rc1`, while this repository is pinned to
`leanprover/lean4:v4.29.0`, and the audited stochastic-integral files still
contain upstream placeholder proof terms. The lists below are compile-checked
metadata only; they do not claim repo-local theorem completion.
-/

/-- Exact upstream repository audited for Brownian/stochastic-integral APIs. -/
def brownianMotionAuditRepo : String :=
  "https://github.com/RemyDegenne/brownian-motion"

/-- Exact upstream commit audited for child task `S1-M-232-C002`. -/
def brownianMotionAuditCommit : String :=
  "91885e6172648ea7f9c6a16b3a7069f92c88e023"

/-- Upstream toolchain recorded at the audited commit. -/
def brownianMotionAuditToolchain : String :=
  "leanprover/lean4:v4.30.0-rc1"

/-- This repository's Lean toolchain at audit time. -/
def repoAuditToolchain : String :=
  "leanprover/lean4:v4.29.0"

/-- Mathlib revisions compared during the external audit. -/
def brownianMotionAuditMathlibRevisions : List String := [
  "brownian-motion: f23306121184717ace04f3ac514be974e3224c8b",
  "awesome_theorems: 8a178386ffc0f5fef0b77738bb5449d50efeea95"
]

/-- Upstream dependency pins recorded from the audited `lake-manifest.json`. -/
def brownianMotionAuditDependencyPins : List String := [
  "RemyDegenne/kolmogorov_extension4@e236e968c2b038b952444df54075a6e8b1058380",
  "PatrickMassot/checkdecls@3d425859e73fcfbef85b9638c2a91708ef4a22d4",
  "leanprover/subverso@52b9dfbd2658408e37ae6e8b72601ddeaaa25a0c"
]

/--
Upstream Brownian-motion API names found at the audited commit. These are
external anchors only because the project is not pinned/imported in this repo.
-/
def brownianMotionAuditBrownianAnchors : List String := [
  "ProbabilityTheory.IsPreBrownian",
  "ProbabilityTheory.IsPreBrownian.shift",
  "ProbabilityTheory.IsPreBrownian.indepFun_shift",
  "ProbabilityTheory.IsFilteredPreBrownian",
  "ProbabilityTheory.IsPreBrownian.isMartingale",
  "ProbabilityTheory.IsBrownian",
  "ProbabilityTheory.brownian",
  "ProbabilityTheory.IsBrownian_brownian",
  "ProbabilityTheory.hasIndepIncrements_brownian",
  "ProbabilityTheory.wienerMeasure"
]

/--
Upstream stochastic-integral/local-martingale API names found at the audited
commit. These remain external anchors and include in-progress files upstream.
-/
def brownianMotionAuditStochasticIntegralAnchors : List String := [
  "ProbabilityTheory.ElementaryPredictableSet",
  "ProbabilityTheory.SimpleProcess",
  "ProbabilityTheory.SimpleProcess.integral",
  "ProbabilityTheory.SimpleProcess.integralEval",
  "ProbabilityTheory.SimpleProcess.integral_assoc",
  "ProbabilityTheory.IsLocalMartingale",
  "ProbabilityTheory.IsLocalSubmartingale",
  "ProbabilityTheory.doob_meyer",
  "ProbabilityTheory.quadraticVariation"
]

/--
Concrete blockers preventing this external project from being treated as a
completed repo-local dependency for THM-M-1039 in the current repository.
-/
def brownianMotionAuditIntegrationBlockers : List String := [
  "toolchain_mismatch: upstream leanprover/lean4:v4.30.0-rc1 vs repo leanprover/lean4:v4.29.0",
  "mathlib_mismatch: upstream f23306121184717ace04f3ac514be974e3224c8b vs repo 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "upstream_stochastic_integral_in_progress: README says stochastic integrals and Ito lemma are in progress",
  "upstream_placeholder_proofs: audited BrownianMotion/StochasticIntegral and Choquet files contain placeholder proof terms",
  "no_terminal_sde_markov_theorem_found: audit found Brownian weak-Markov-style anchors, but no SDE Markov-property theorem"
]

/-!
## External SDE Markov theorem integration gate

Child `S1-M-232-C005` is the non-completion gate for external Lean evidence.
The audited Brownian-motion project provides useful stochastic-process anchors,
but no terminal theorem proving the Markov property of SDE solutions was found
at the audited commit.  Therefore there is no external theorem to pin, import,
and check in this repository for the terminal THM-M-1039 conclusion.
-/

/-- Repo-local status for a searched external SDE Markov-property theorem. -/
inductive ExternalSDEMarkovProofStatus where
  /-- The audit did not locate a terminal theorem for the SDE Markov property. -/
  | noTerminalTheoremLocated
  /-- A terminal theorem was located, but concrete blockers prevent integration. -/
  | terminalTheoremLocatedButBlocked
  /-- A terminal theorem is pinned/imported/checked in this repo's closure. -/
  | pinnedImportedChecked
  deriving DecidableEq, Repr

/-- One checked row for the external SDE Markov-property integration gate. -/
structure ExternalSDEMarkovIntegrationGate where
  repository : String
  auditedCommit : String
  terminalTheoremName : Option String
  status : ExternalSDEMarkovProofStatus
  blockers : List String
  completionClaimAllowed : Bool
  deriving Repr

/--
Gate row for `RemyDegenne/brownian-motion`: no terminal SDE Markov theorem was
located, so anchor-only Brownian/stochastic-integral evidence cannot complete
THM-M-1039.
-/
def brownianMotionTerminalSDEMarkovGate : ExternalSDEMarkovIntegrationGate := {
  repository := brownianMotionAuditRepo
  auditedCommit := brownianMotionAuditCommit
  terminalTheoremName := none
  status := .noTerminalTheoremLocated
  blockers := brownianMotionAuditIntegrationBlockers
  completionClaimAllowed := false
}

/-- Concrete integration blocker text for public C005 backfill. -/
def terminalSDEMarkovExternalIntegrationBlocker : String :=
  "No terminal SDE Markov-property theorem was located in RemyDegenne/brownian-motion at commit 91885e6172648ea7f9c6a16b3a7069f92c88e023; direct integration is also blocked by Lean/mathlib mismatch and upstream stochastic-integral placeholders."

/-- Completion is allowed exactly when a terminal external theorem is checked locally. -/
def TerminalSDEMarkovExternalCompletionAllowed : Prop :=
  brownianMotionTerminalSDEMarkovGate.completionClaimAllowed = true

/-- Checked C005 gate: the audited external anchor does not permit completion. -/
theorem brownianMotionTerminalSDEMarkovCompletionDisallowed :
    ¬ TerminalSDEMarkovExternalCompletionAllowed := by
  intro h
  cases h

/-- Repo-local integration-debt gate summary for the current open theorem state. -/
def terminalSDEMarkovRepoLocalIntegrationDebtGate : String :=
  "pass_open_only: no external terminal SDE Markov theorem is counted as completed; THM-M-1039 remains formalization_debt, not repo_local_integration_debt in a completed state."

/-!
## Canonical object-model decision

For the current repo-local Stage1 artifact, the canonical SDE object model is
the local abstract `SDEMarkovData` structure above.  The pinned external
Brownian-motion route and a future mathlib route are useful follow-up routes,
but neither is a completed dependency in this repository's current validation
closure.
-/

/-- Candidate object-model routes considered for the SDE Markov-property slot. -/
inductive SDEObjectModelRoute where
  /-- Use the local abstract structure already checked in this artifact. -/
  | localAbstractStructure
  /-- Pin and import an external Brownian/stochastic-integral project. -/
  | pinnedExternalBrownianProject
  /-- Wait for or contribute a future canonical mathlib SDE API. -/
  | futureMathlibAPI
  deriving DecidableEq, Repr

/--
Selected canonical route for the current repo-local artifact.

This chooses the local abstract `SDEMarkovData` boundary because it is the only
route that currently validates under this repository's Lean toolchain without
adding an unpinned or incomplete dependency.
-/
def canonicalSDEObjectModelRoute : SDEObjectModelRoute :=
  .localAbstractStructure

/-- Non-selected routes and their current integration status. -/
def nonSelectedSDEObjectModelRoutes : List String := [
  "pinned_external_brownian_project: blocked by toolchain/mathlib mismatch and no located terminal SDE Markov theorem",
  "future_mathlib_api: blocked because no canonical SDE/stochastic-integral/Brownian API is in the pinned local mathlib closure"
]

/-- Public-audit summary of the selected repo-local SDE object model. -/
def canonicalSDEObjectModelSummary : String :=
  "Use local abstract SDEMarkovData for Stage1 statement-shape work; keep terminal theorem open."

/-- Checked marker that the current artifact selects the local abstract route. -/
def UsesLocalAbstractSDEObjectModel : Prop :=
  canonicalSDEObjectModelRoute = .localAbstractStructure

/-- The selected SDE object model is the local abstract `SDEMarkovData` route. -/
theorem canonicalSDEObjectModelRoute_isLocal :
    UsesLocalAbstractSDEObjectModel :=
  rfl

/-!
## Public theorem-tree leaf backfill

Child `S1-M-232-C004` records the currently unchecked leaves `L008` through
`L022` as integration-ready public checklist rows.  These rows are deliberately
unchecked: they preserve the `<=100` local proof budget while making clear that
the terminal SDE Markov-property theorem is still formalization debt.
-/

/-- Status values used by the SDE Markov-property public leaf backfill. -/
inductive SDEMarkovLeafStatus where
  /-- A statement-shape or wrapper leaf already checked by this repo-local file. -/
  | checkedLocal
  /-- A terminal theorem or integration leaf still open as formalization debt. -/
  | uncheckedFormalizationDebt
  deriving DecidableEq, Repr

/-- One public theorem-tree leaf row for the SDE Markov-property slot. -/
structure SDEMarkovLeafLedgerRow where
  leafId : String
  packageId : String
  maxProofSteps : Nat
  status : SDEMarkovLeafStatus
  task : String
  completionClaimed : Bool
  deriving Repr

/-- Public backfill rows for unchecked leaves `S1_M_232.L008` through `L022`. -/
def uncheckedLeafBackfillL008ToL022 : List SDEMarkovLeafLedgerRow := [
  { leafId := "S1_M_232.L008_sde_equation_api",
    packageId := "P03_sde_object_model",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Choose or import a canonical SDE or stochastic-integral equation API.",
    completionClaimed := false },
  { leafId := "S1_M_232.L009_brownian_or_noise_api",
    packageId := "P03_sde_object_model",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Choose or import Brownian/noise process and independent-increment APIs.",
    completionClaimed := false },
  { leafId := "S1_M_232.L010_adapted_progressive_bridge",
    packageId := "P03_sde_object_model",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Bridge adapted/progressive measurability to the chosen SDE solution API.",
    completionClaimed := false },
  { leafId := "S1_M_232.L011_strong_solution_uniqueness",
    packageId := "P03_sde_object_model",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Formalize strong existence and uniqueness hypotheses sufficient for flow representation.",
    completionClaimed := false },
  { leafId := "S1_M_232.L012_future_increment_independence",
    packageId := "P04_noise_increment_independence",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Prove future noise increments are independent of the past filtration at time s.",
    completionClaimed := false },
  { leafId := "S1_M_232.L013_solution_flow_measurable",
    packageId := "P05_flow_solution_map",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Prove the post-s solution is measurable in the current state and future noise.",
    completionClaimed := false },
  { leafId := "S1_M_232.L014_flow_conditional_distribution",
    packageId := "P06_conditional_law_bridge",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Identify the conditional law through the solution-flow representation.",
    completionClaimed := false },
  { leafId := "S1_M_232.L015_transition_kernel_construction",
    packageId := "P07_transition_kernel_identification",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Construct P_{s,t} from the solution flow and future-noise distribution.",
    completionClaimed := false },
  { leafId := "S1_M_232.L016_transition_kernel_measurability",
    packageId := "P07_transition_kernel_identification",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Prove the constructed transition object is measurable as a kernel.",
    completionClaimed := false },
  { leafId := "S1_M_232.L017_transition_kernel_markov",
    packageId := "P07_transition_kernel_identification",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Prove each constructed transition kernel is a probability/Markov kernel.",
    completionClaimed := false },
  { leafId := "S1_M_232.L018_semigroup_or_time_inhomogeneous_consistency",
    packageId := "P07_transition_kernel_identification",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Prove Chapman-Kolmogorov or time-inhomogeneous transition consistency if required.",
    completionClaimed := false },
  { leafId := "S1_M_232.L019_conditional_law_to_filtration_markov",
    packageId := "P08_filtration_markov_property",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Lift the current-state conditional law to the filtration-relative Markov property.",
    completionClaimed := false },
  { leafId := "S1_M_232.L020_indicator_tests_to_bounded_tests",
    packageId := "P08_filtration_markov_property",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Extend indicator-test Markov statements to bounded measurable test functions.",
    completionClaimed := false },
  { leafId := "S1_M_232.L021_strong_markov_extension",
    packageId := "P08_filtration_markov_property",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "Add the stopping-time strong Markov variant only if this Stage1 slot is broadened.",
    completionClaimed := false },
  { leafId := "S1_M_232.L022_dependency_pin_check",
    packageId := "P09_wrapper_or_dependency_closure",
    maxProofSteps := 100,
    status := .uncheckedFormalizationDebt,
    task := "If an external Lean theorem is found, pin/import/check it before any completion claim.",
    completionClaimed := false }
]

/-- Stable ids for the unchecked public backfill leaves. -/
def uncheckedLeafBackfillIdsL008ToL022 : List String :=
  uncheckedLeafBackfillL008ToL022.map (fun row => row.leafId)

/--
Public backfill gate: the leaf rows above may be copied to the public theorem
tree, but every row remains unchecked and no terminal theorem completion is
claimed by this artifact.
-/
def publicLeafBackfillL008ToL022Gate : String :=
  "Backfill S1_M_232.L008 through S1_M_232.L022 as unchecked <=100 leaves; keep THM-M-1039 open until terminal SDE Markov proof closure validates repo-locally."

/-!
## Bounded measurable test-function extension

Child `S1-M-232-C006` extends the repo-local statement shape from measurable
indicator tests to bounded measurable real-valued test functions.  The selected
statement bridge is the conditional-expectation identity whose right-hand side
is the transition-kernel integral.  This is a typed target only: the theorem
that derives the bounded-test identity from indicator tests remains an
unchecked formalization leaf until a monotone-class or simple-function bridge is
implemented locally.
-/

/-- Public status for the bounded-test extension child. -/
inductive BoundedTestExtensionStatus where
  /-- The bounded-test statement shape is present and Lean-checked. -/
  | statementShapeChecked
  /-- The derivation from indicator tests is still open formalization debt. -/
  | bridgeProofOpen
  deriving DecidableEq, Repr

/-- Statement-shape gate for child `S1-M-232-C006`. -/
def boundedMeasurableTestExtensionStatus : List BoundedTestExtensionStatus := [
  .statementShapeChecked,
  .bridgeProofOpen
]

/-- Public-audit summary for the bounded measurable test-function extension. -/
def boundedMeasurableTestExtensionSummary : String :=
  "FiltrationMarkovPropertyBoundedTests is now a checked repo-local statement-shape target; the indicator-to-bounded-test monotone-class/simple-function proof remains open formalization debt."

/--
Completion gate for the bounded-test child: the statement extension is checked,
but the terminal theorem is not completed by this artifact.
-/
def boundedMeasurableTestExtensionCompletionClaimAllowed : Bool :=
  false

/-! ## Audit probes -/

#check StatementShape
#check SDEMarkovData
#check ConditionalTransitionLaw
#check BoundedMeasurableTest
#check FiltrationMarkovProperty
#check FiltrationMarkovPropertyBoundedTests
#check transitionKernel_isMarkov
#check filtration_mono
#check condDistrib_process_isMarkovKernel
#check condDistrib_process_comp_map
#check condDistrib_process_ae_eq_condExp
#check BoundedMeasurableTest.measurable
#check BoundedMeasurableTest.exists_bound
#check Filtration
#check Filtration.mono
#check IsStoppingTime
#check Kernel
#check IsMarkovKernel
#check condDistrib
#check condDistrib_comp_map
#check condDistrib_ae_eq_condExp
#check IndepFun
#check iIndepFun
#check condIndepFun_iff_condDistrib_prod_ae_eq_prodMkRight
#check mathlibAnchorModules
#check mathlibAnchorNames
#check absentTerminalSearchTerms
#check brownianMotionAuditRepo
#check brownianMotionAuditCommit
#check brownianMotionAuditToolchain
#check repoAuditToolchain
#check brownianMotionAuditMathlibRevisions
#check brownianMotionAuditDependencyPins
#check brownianMotionAuditBrownianAnchors
#check brownianMotionAuditStochasticIntegralAnchors
#check brownianMotionAuditIntegrationBlockers
#check ExternalSDEMarkovProofStatus
#check ExternalSDEMarkovIntegrationGate
#check brownianMotionTerminalSDEMarkovGate
#check terminalSDEMarkovExternalIntegrationBlocker
#check TerminalSDEMarkovExternalCompletionAllowed
#check brownianMotionTerminalSDEMarkovCompletionDisallowed
#check terminalSDEMarkovRepoLocalIntegrationDebtGate
#check SDEObjectModelRoute
#check canonicalSDEObjectModelRoute
#check nonSelectedSDEObjectModelRoutes
#check canonicalSDEObjectModelSummary
#check UsesLocalAbstractSDEObjectModel
#check canonicalSDEObjectModelRoute_isLocal
#check SDEMarkovLeafStatus
#check SDEMarkovLeafLedgerRow
#check uncheckedLeafBackfillL008ToL022
#check uncheckedLeafBackfillIdsL008ToL022
#check publicLeafBackfillL008ToL022Gate
#check BoundedTestExtensionStatus
#check boundedMeasurableTestExtensionStatus
#check boundedMeasurableTestExtensionSummary
#check boundedMeasurableTestExtensionCompletionClaimAllowed

end AwesomeTheorems.Stage1.S1_M_232
