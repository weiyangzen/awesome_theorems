import Mathlib.Probability.HasLaw
import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Process.Stopping
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# S1-M-228 / THM-M-1035: Stratonovich integral

This Stage1 artifact records a conservative Lean 4 boundary for the
Stratonovich stochastic integral slot summarized as "another definition of
stochastic integral".

The pinned mathlib snapshot has measure theory, probability laws, independence,
filtrations, adapted processes, stopping times, stopped values, and Bochner
integrability.  This audit did not find a canonical stochastic-integral API or
a terminal Stratonovich integral theorem.  The declarations below therefore
freeze a statement shape around midpoint Riemann sums and convergence
interfaces, and provide only checked low-risk wrappers around available
mathlib process and law infrastructure.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

open scoped BigOperators ENNReal NNReal MeasureTheory ProbabilityTheory

namespace AwesomeTheorems.Stage1.S1_M_228

universe uΩ uX

/-- Midpoint average used by finite Stratonovich Riemann sums. -/
def midpointAverage (x y : ℝ) : ℝ :=
  (x + y) / 2

/--
Discrete midpoint Riemann sum
`sum_i ((Y_i + Y_{i+1}) / 2) * (X_{i+1} - X_i)`.

This is only the finite-sum skeleton of the Stratonovich construction.  A full
formalization must replace the convergence fields below by the chosen
continuous-time stochastic-integral object model.
-/
def stratonovichRiemannSum {Ω : Type uΩ}
    (Y X : ℕ → Ω → ℝ) (N : ℕ) (ω : Ω) : ℝ :=
  Finset.sum (Finset.range N) fun i =>
    midpointAverage (Y i ω) (Y (i + 1) ω) * (X (i + 1) ω - X i ω)

/-- The midpoint average of equal values is that value. -/
theorem midpointAverage_self (x : ℝ) :
    midpointAverage x x = x := by
  unfold midpointAverage
  ring

/-- If the integrand is identically zero, every finite midpoint sum is zero. -/
theorem stratonovichRiemannSum_zero_integrand {Ω : Type uΩ}
    (X : ℕ → Ω → ℝ) (N : ℕ) (ω : Ω) :
    stratonovichRiemannSum (fun _ _ => 0) X N ω = 0 := by
  simp [stratonovichRiemannSum, midpointAverage]

/-- If the integrator is identically zero, every finite midpoint sum is zero. -/
theorem stratonovichRiemannSum_zero_integrator {Ω : Type uΩ}
    (Y : ℕ → Ω → ℝ) (N : ℕ) (ω : Ω) :
    stratonovichRiemannSum Y (fun _ _ => 0) N ω = 0 := by
  simp [stratonovichRiemannSum, midpointAverage]

/--
Boundary data for a future Stratonovich integral theorem.

The real-valued discrete skeleton records the midpoint sums that should
converge to `stratonovichIntegral`.  The abstract proposition fields mark the
continuous-time stochastic-process assumptions still missing from the local
object model, such as semimartingale hypotheses, mesh convergence, and the
Itô/Stratonovich conversion interface.
-/
structure StratonovichIntegralData (Ω : Type uΩ) [MeasurableSpace Ω]
    (P : Measure Ω) : Type uΩ where
  integrand : ℕ → Ω → ℝ
  integrator : ℕ → Ω → ℝ
  filtration : Filtration ℕ (inferInstance : MeasurableSpace Ω)
  stratonovichIntegral : Ω → ℝ
  meshSize : ℕ → ℝ
  stochasticBasisHypotheses : Prop
  semimartingaleInterface : Prop
  integrabilityHypotheses : Prop
  meshTendsToZero : Prop
  midpointSumConverges : Prop
  itoConversionInterface : Prop
  chainRuleInterface : Prop

/--
Conclusion package expected from a completed Stratonovich integral
formalization.

The fields are all checkable propositions over the selected object model.  A
later proof should derive them from concrete stochastic-process assumptions and
from the actual construction of the Stratonovich integral.
-/
structure StratonovichIntegralConclusion {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : StratonovichIntegralData Ω P) : Prop where
  integrand_aestronglyMeasurable :
    ∀ n, AEStronglyMeasurable (D.integrand n) P
  integrator_aestronglyMeasurable :
    ∀ n, AEStronglyMeasurable (D.integrator n) P
  integrand_adapted : Adapted D.filtration D.integrand
  integrator_adapted : Adapted D.filtration D.integrator
  integral_aestronglyMeasurable :
    AEStronglyMeasurable D.stratonovichIntegral P
  integral_integrable : Integrable D.stratonovichIntegral P
  mesh_tends_to_zero : D.meshTendsToZero
  midpoint_sum_converges : D.midpointSumConverges
  ito_conversion_interface : D.itoConversionInterface
  chain_rule_interface : D.chainRuleInterface

/--
Normalized Stage1 statement shape for the Stratonovich integral slot.

For every probability space and data package satisfying the stochastic-basis,
semimartingale, integrability, and mesh/convergence hypotheses, a future
terminal theorem should provide the measurability, adaptedness,
integrability, convergence, conversion, and chain-rule conclusion package.
This file records the boundary and checked substrate only.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P],
    ∀ D : StratonovichIntegralData Ω P,
      D.stochasticBasisHypotheses →
        D.semimartingaleInterface →
          D.integrabilityHypotheses →
            D.meshTendsToZero →
              D.midpointSumConverges →
                StratonovichIntegralConclusion D

/-- Project the integrability obligation from a future conclusion package. -/
theorem conclusion_integrable {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : StratonovichIntegralData Ω P}
    (h : StratonovichIntegralConclusion D) :
    Integrable D.stratonovichIntegral P :=
  h.integral_integrable

/-- Project the midpoint-sum convergence obligation from a future conclusion package. -/
theorem conclusion_midpoint_sum_converges {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : StratonovichIntegralData Ω P}
    (h : StratonovichIntegralConclusion D) :
    D.midpointSumConverges :=
  h.midpoint_sum_converges

/-- Project the adaptedness obligation for the integrand. -/
theorem conclusion_integrand_adapted {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : StratonovichIntegralData Ω P}
    (h : StratonovichIntegralConclusion D) :
    Adapted D.filtration D.integrand :=
  h.integrand_adapted

/-- Project the Itô/Stratonovich conversion-interface obligation. -/
theorem conclusion_ito_conversion_interface {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : StratonovichIntegralData Ω P}
    (h : StratonovichIntegralConclusion D) :
    D.itoConversionInterface :=
  h.ito_conversion_interface

section MathlibAnchors

variable {Ω : Type uΩ} [MeasurableSpace Ω]

/-- Checked mathlib wrapper: deterministic times are stopping times. -/
theorem const_stopping_time_wrapper
    (ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)) (n : ℕ) :
    IsStoppingTime ℱ (fun _ : Ω => (n : WithTop ℕ)) :=
  isStoppingTime_const ℱ n

omit [MeasurableSpace Ω] in
/-- Checked mathlib wrapper: stopping at a deterministic time returns that process value. -/
theorem stoppedValue_const_wrapper {X : Type uX} (u : ℕ → Ω → X) (n : ℕ) :
    stoppedValue u (fun _ : Ω => (n : WithTop ℕ)) = u n :=
  stoppedValue_const u n

/-- Checked mathlib wrapper: the identity random variable has its source measure as its law. -/
theorem hasLaw_id_wrapper {X : Type uX} [MeasurableSpace X] (μ : Measure X) :
    HasLaw (id : X → X) μ μ :=
  HasLaw.id

/-- Checked mathlib wrapper: measure-preserving maps induce `HasLaw`. -/
theorem measurePreserving_hasLaw_wrapper {X : Type uX} [MeasurableSpace X]
    {μ : Measure Ω} {ν : Measure X} {f : Ω → X}
    (h : MeasurePreserving f μ ν) :
    HasLaw f ν μ :=
  h.hasLaw

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Function.AEEqFun",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure"
]

/-- Checked local names used as anchors for the Stratonovich statement boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.ProgMeasurable",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.isStoppingTime_const",
  "MeasureTheory.stoppedValue",
  "MeasureTheory.stoppedValue_const",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.HasLaw.id",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.iIndepFun",
  "MeasureTheory.AEStronglyMeasurable",
  "MeasureTheory.Integrable",
  "MeasureTheory.MeasurePreserving.hasLaw"
]

/--
Search terms that did not locate a terminal Stratonovich integral theorem in
the local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Stratonovich",
  "Stratonovich integral",
  "Ito integral",
  "Itô integral",
  "stochastic integral",
  "StochasticIntegral",
  "BrownianMotion",
  "IsBrownianMotion",
  "semimartingale",
  "quadratic variation"
]

/--
Integration-ready public audit note for the Stage1 backfill surface.

This records only the local mathlib anchor status; it is not a terminal
Stratonovich theorem or a stochastic-integral construction.
-/
def publicMathlibAnchorAuditNote : String :=
  "local mathlib has Filtration, Adapted, IsStoppingTime, stoppedValue, HasLaw, \
  AEStronglyMeasurable, and Integrable, but no canonical Stratonovich, Ito \
  integral, stochastic integral, BrownianMotion, semimartingale, or quadratic \
  variation terminal API was found."

/--
Machine status for the terminal Stratonovich integral theorem.

This is deliberately not a completion claim: the local artifact only records a
statement boundary and checked substrate wrappers.
-/
def terminalStratonovichMachineStatus : String := "not_repo_local_closed"

/--
Machine status for the checked stopping-time, stopped-value, and law wrappers.

Those wrappers are local declarations whose proof bodies are immediate calls to
pinned mathlib theorems.
-/
def substrateWrapperMachineStatus : String := "local_wrapper_upstream_mathlib"

/-- Debt class for the terminal theorem after the local mathlib anchor audit. -/
def terminalStratonovichDebtClass : String := "formalization_debt"

/--
Formalization-debt child task required before attempting the terminal
Stratonovich theorem.

The existing `StratonovichIntegralData` boundary is only a discrete
midpoint-sum skeleton.  A future closure must first select or build a
continuous-time stochastic-integral object model and validate it repo-locally.
-/
def continuousTimeStochasticIntegralObjectModelDebtTask : String :=
  "Define or import a continuous-time stochastic-integral object model before \
  attempting the terminal Stratonovich theorem."

/--
Open status for the continuous-time stochastic-integral object-model gap.

This marker is intentionally not a completion claim; it records the next
formalization-debt leaf for serial public backfill.
-/
def continuousTimeStochasticIntegralObjectModelStatus : String :=
  "formalization_debt_open"

/-- Minimal prerequisites expected from the future continuous-time object model. -/
def continuousTimeStochasticIntegralObjectModelPrerequisites : List String := [
  "continuous-time stochastic basis and filtration",
  "adapted integrand and integrator processes",
  "stochastic integral object with convergence semantics",
  "compatibility with semimartingale and quadratic-variation APIs",
  "repo-local validation through a local proof body, mathlib wrapper, or pinned dependency"
]

/--
Formalization-debt child task for the semimartingale and variation layer.

This is the child requested by the public backfill row: define or import
semimartingales and quadratic/cross variation, then prove midpoint
Riemann-sum convergence.  It is intentionally an open debt marker, not a
terminal Stratonovich theorem.
-/
def semimartingaleQuadraticVariationDebtTask : String :=
  "Define or import semimartingales and quadratic/cross variation, then prove \
  midpoint Riemann-sum convergence."

/--
Open status for the semimartingale, quadratic/cross-variation, and midpoint
Riemann-sum convergence gap.
-/
def semimartingaleQuadraticVariationStatus : String := "formalization_debt_open"

/--
Statement-boundary data for the future semimartingale and variation layer.

The fields are propositions until a canonical local or pinned upstream API is
selected.  This prevents the Stage1 artifact from pretending that the current
mathlib snapshot already supplies semimartingales, quadratic variation, cross
variation, or the convergence theorem needed by the Stratonovich construction.
-/
structure SemimartingaleQuadraticVariationData (Ω : Type uΩ)
    [MeasurableSpace Ω] (P : Measure Ω) : Type uΩ where
  integrand : ℝ → Ω → ℝ
  integrator : ℝ → Ω → ℝ
  filtration : Filtration ℝ (inferInstance : MeasurableSpace Ω)
  semimartingaleAPI : Prop
  integrandSemimartingale : Prop
  integratorSemimartingale : Prop
  quadraticVariationAPI : Prop
  crossVariationAPI : Prop
  midpointPartitionMeshAPI : Prop
  midpointRiemannSumConvergence : Prop

/--
The semimartingale/variation boundary exposes the exact convergence obligation
needed by the future Stratonovich theorem.
-/
theorem SemimartingaleQuadraticVariationData.midpoint_convergence_obligation
    {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : SemimartingaleQuadraticVariationData Ω P) :
    D.midpointRiemannSumConvergence →
      D.midpointRiemannSumConvergence :=
  id

/-- M0387-level child leaves for the semimartingale/variation debt task. -/
def semimartingaleQuadraticVariationDebtLeaves : List (String × String) := [
  ("SMQV228.L001.open.semimartingale_api",
    "Define or import a semimartingale predicate over a continuous-time filtered probability space."),
  ("SMQV228.L002.open.quadratic_variation_api",
    "Define or import quadratic variation for the selected semimartingale/local-martingale domain."),
  ("SMQV228.L003.open.cross_variation_api",
    "Define or import cross variation/covariation and prove compatibility with quadratic variation."),
  ("SMQV228.L004.open.partition_mesh_api",
    "Define tagged partitions and mesh convergence for midpoint stochastic Riemann sums."),
  ("SMQV228.L005.open.midpoint_sum_convergence",
    "Prove convergence of midpoint Riemann sums under the selected semimartingale and variation hypotheses."),
  ("SMQV228.L006.open.stratonovich_integration_bridge",
    "Connect the midpoint convergence theorem to the `StratonovichIntegralData.midpointSumConverges` field.")
]

/--
Formalization-debt child task for the Ito/Stratonovich conversion and
Stratonovich chain-rule layer.

This child can only close after the stochastic-integral and
quadratic/cross-variation APIs are present and repo-locally validated.  Until
then, it is an open interface obligation and not a terminal theorem proof.
-/
def itoStratonovichConversionChainRuleDebtTask : String :=
  "Prove Itô/Stratonovich conversion and the Stratonovich chain rule once \
  stochastic integral and quadratic-variation APIs exist."

/-- Open status for the Ito/Stratonovich conversion and chain-rule gap. -/
def itoStratonovichConversionChainRuleStatus : String :=
  "formalization_debt_open"

/--
Statement-boundary data for the future Ito/Stratonovich conversion and
Stratonovich chain rule.

The formula fields remain propositions because the current repo-local API does
not yet provide stochastic integrals, semimartingales, quadratic/cross
variation, or a differentiability interface specialized to stochastic chain
rules.
-/
structure ItoStratonovichConversionChainRuleData (Ω : Type uΩ)
    [MeasurableSpace Ω] (P : Measure Ω) : Type uΩ where
  process : ℝ → Ω → ℝ
  integrand : ℝ → Ω → ℝ
  integrator : ℝ → Ω → ℝ
  filtration : Filtration ℝ (inferInstance : MeasurableSpace Ω)
  stochasticIntegralAPI : Prop
  itoIntegralAPI : Prop
  stratonovichIntegralAPI : Prop
  quadraticVariationAPI : Prop
  crossVariationAPI : Prop
  semimartingaleHypotheses : Prop
  smoothChainRuleFunctionAPI : Prop
  itoStratonovichConversionFormula : Prop
  stratonovichChainRuleFormula : Prop
  terminalConclusionBridge : Prop

/-- Project the future Ito/Stratonovich conversion obligation. -/
theorem ItoStratonovichConversionChainRuleData.conversion_obligation
    {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ItoStratonovichConversionChainRuleData Ω P) :
    D.itoStratonovichConversionFormula →
      D.itoStratonovichConversionFormula :=
  id

/-- Project the future Stratonovich chain-rule obligation. -/
theorem ItoStratonovichConversionChainRuleData.chain_rule_obligation
    {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ItoStratonovichConversionChainRuleData Ω P) :
    D.stratonovichChainRuleFormula →
      D.stratonovichChainRuleFormula :=
  id

/--
The conversion/chain-rule boundary exposes the two obligations needed by
`StratonovichIntegralConclusion`.
-/
theorem ItoStratonovichConversionChainRuleData.conversion_chain_rule_obligations
    {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (D : ItoStratonovichConversionChainRuleData Ω P) :
    D.itoStratonovichConversionFormula →
      D.stratonovichChainRuleFormula →
        D.itoStratonovichConversionFormula ∧
          D.stratonovichChainRuleFormula :=
  fun hConversion hChainRule => ⟨hConversion, hChainRule⟩

/-- M0387-level child leaves for the conversion/chain-rule debt task. -/
def itoStratonovichConversionChainRuleDebtLeaves : List (String × String) := [
  ("ISCC228.L001.open.ito_integral_api",
    "Define or import an Ito stochastic integral API compatible with the selected semimartingale model."),
  ("ISCC228.L002.open.stratonovich_integral_api",
    "Define or import a Stratonovich integral API and align it with midpoint-sum convergence."),
  ("ISCC228.L003.open.quadratic_cross_variation_bridge",
    "Connect quadratic and cross variation to the correction term in the conversion formula."),
  ("ISCC228.L004.open.ito_stratonovich_conversion",
    "Prove the Ito/Stratonovich conversion formula under the selected API hypotheses."),
  ("ISCC228.L005.open.smooth_chain_rule_api",
    "Select differentiability hypotheses for the scalar functions used in the chain rule."),
  ("ISCC228.L006.open.stratonovich_chain_rule",
    "Prove the Stratonovich chain rule from the conversion theorem and variation calculus."),
  ("ISCC228.L007.open.terminal_conclusion_bridge",
    "Connect the conversion and chain-rule theorems to `StratonovichIntegralConclusion` fields.")
]

/--
M0387 completion gate: this artifact does not treat any anchor-only external
evidence as a completed repo-local theorem closure.
-/
def completedStateRetainsRepoLocalIntegrationDebt : Bool := false

/--
C008 Stage1 checkbox gate.

The public checkbox must remain open until the terminal theorem has a
repo-local proof body, a mathlib wrapper theorem, or a pinned external
dependency, and the public proof-tree ledger has been merged by a serialized
integrator pass.
-/
def c008Stage1CheckboxGate : String :=
  "keep_open_until_repo_local_closure_and_public_proof_tree_ledger_merge"

/-- The public proof-tree ledger has not been merged by this child worker. -/
def c008PublicProofTreeLedgerMerged : Bool := false

/-- The Stage1 checkbox remains open for this child gate. -/
def c008Stage1CheckboxOpen : Bool := true

/-- Checked status split required by the Stage1 child integration gate. -/
theorem terminalStratonovichMachineStatus_eq :
    terminalStratonovichMachineStatus = "not_repo_local_closed" := rfl

/-- Checked wrapper-status split required by the Stage1 child integration gate. -/
theorem substrateWrapperMachineStatus_eq :
    substrateWrapperMachineStatus = "local_wrapper_upstream_mathlib" := rfl

/-- Checked debt-class marker for the terminal Stratonovich theorem. -/
theorem terminalStratonovichDebtClass_eq :
    terminalStratonovichDebtClass = "formalization_debt" := rfl

/-- Checked formalization-debt task marker for serial public backfill. -/
theorem continuousTimeStochasticIntegralObjectModelDebtTask_eq :
    continuousTimeStochasticIntegralObjectModelDebtTask =
      "Define or import a continuous-time stochastic-integral object model before \
      attempting the terminal Stratonovich theorem." := rfl

/-- Checked open-status marker for the continuous-time stochastic-integral model gap. -/
theorem continuousTimeStochasticIntegralObjectModelStatus_eq :
    continuousTimeStochasticIntegralObjectModelStatus =
      "formalization_debt_open" := rfl

/-- Checked formalization-debt task marker for the semimartingale/variation gap. -/
theorem semimartingaleQuadraticVariationDebtTask_eq :
    semimartingaleQuadraticVariationDebtTask =
      "Define or import semimartingales and quadratic/cross variation, then prove \
      midpoint Riemann-sum convergence." := rfl

/-- Checked open-status marker for the semimartingale/variation gap. -/
theorem semimartingaleQuadraticVariationStatus_eq :
    semimartingaleQuadraticVariationStatus = "formalization_debt_open" := rfl

/-- Checked formalization-debt task marker for the conversion/chain-rule gap. -/
theorem itoStratonovichConversionChainRuleDebtTask_eq :
    itoStratonovichConversionChainRuleDebtTask =
      "Prove Itô/Stratonovich conversion and the Stratonovich chain rule once \
      stochastic integral and quadratic-variation APIs exist." := rfl

/-- Checked open-status marker for the conversion/chain-rule gap. -/
theorem itoStratonovichConversionChainRuleStatus_eq :
    itoStratonovichConversionChainRuleStatus =
      "formalization_debt_open" := rfl

/-- Checked public-audit note marker for the Stage1 child integration gate. -/
theorem publicMathlibAnchorAuditNote_eq :
    publicMathlibAnchorAuditNote =
      "local mathlib has Filtration, Adapted, IsStoppingTime, stoppedValue, HasLaw, \
      AEStronglyMeasurable, and Integrable, but no canonical Stratonovich, Ito \
      integral, stochastic integral, BrownianMotion, semimartingale, or quadratic \
      variation terminal API was found." := rfl

/-- Checked M0387 gate marker: no completed state retains integration debt. -/
theorem completedStateRetainsRepoLocalIntegrationDebt_eq_false :
    completedStateRetainsRepoLocalIntegrationDebt = false := rfl

/-- Checked C008 marker: the checkbox gate is an explicit keep-open condition. -/
theorem c008Stage1CheckboxGate_eq :
    c008Stage1CheckboxGate =
      "keep_open_until_repo_local_closure_and_public_proof_tree_ledger_merge" := rfl

/-- Checked C008 marker: this child did not merge the public proof-tree ledger. -/
theorem c008PublicProofTreeLedgerMerged_eq_false :
    c008PublicProofTreeLedgerMerged = false := rfl

/-- Checked C008 marker: the Stage1 checkbox remains open. -/
theorem c008Stage1CheckboxOpen_eq_true :
    c008Stage1CheckboxOpen = true := rfl

end MathlibAnchors

/-! ## Audit probes -/

#check midpointAverage
#check stratonovichRiemannSum
#check stratonovichRiemannSum_zero_integrand
#check stratonovichRiemannSum_zero_integrator
#check StratonovichIntegralData
#check StratonovichIntegralConclusion
#check StatementShape
#check conclusion_integrable
#check conclusion_midpoint_sum_converges
#check conclusion_integrand_adapted
#check conclusion_ito_conversion_interface
#check const_stopping_time_wrapper
#check stoppedValue_const_wrapper
#check hasLaw_id_wrapper
#check measurePreserving_hasLaw_wrapper
#check Filtration
#check Adapted
#check IsStoppingTime
#check stoppedValue
#check HasLaw
#check AEStronglyMeasurable
#check Integrable
#check terminalStratonovichMachineStatus_eq
#check substrateWrapperMachineStatus_eq
#check terminalStratonovichDebtClass_eq
#check continuousTimeStochasticIntegralObjectModelDebtTask_eq
#check continuousTimeStochasticIntegralObjectModelStatus_eq
#check semimartingaleQuadraticVariationDebtTask
#check semimartingaleQuadraticVariationStatus
#check SemimartingaleQuadraticVariationData
#check SemimartingaleQuadraticVariationData.midpoint_convergence_obligation
#check semimartingaleQuadraticVariationDebtLeaves
#check semimartingaleQuadraticVariationDebtTask_eq
#check semimartingaleQuadraticVariationStatus_eq
#check itoStratonovichConversionChainRuleDebtTask
#check itoStratonovichConversionChainRuleStatus
#check ItoStratonovichConversionChainRuleData
#check ItoStratonovichConversionChainRuleData.conversion_obligation
#check ItoStratonovichConversionChainRuleData.chain_rule_obligation
#check ItoStratonovichConversionChainRuleData.conversion_chain_rule_obligations
#check itoStratonovichConversionChainRuleDebtLeaves
#check itoStratonovichConversionChainRuleDebtTask_eq
#check itoStratonovichConversionChainRuleStatus_eq
#check publicMathlibAnchorAuditNote_eq
#check completedStateRetainsRepoLocalIntegrationDebt_eq_false
#check c008Stage1CheckboxGate_eq
#check c008PublicProofTreeLedgerMerged_eq_false
#check c008Stage1CheckboxOpen_eq_true

end AwesomeTheorems.Stage1.S1_M_228
