import Mathlib.Probability.Martingale.Convergence

/-!
# S1-M-281 / THM-M-1001: Martingale convergence theorem

This Stage1 artifact records a checked Lean 4 wrapper for the discrete-time,
real-valued, `L¹`-bounded martingale almost-sure convergence theorem.

At the pinned mathlib revision used by this repository, the terminal theorem is
available for real-valued submartingales indexed by `ℕ`:
`MeasureTheory.Submartingale.ae_tendsto_limitProcess`.  Since every martingale
is a submartingale, the declarations below package the usual martingale
statement and prove it locally by importing the mathlib theorem.

The file does not claim continuous-time, vector-valued, stopped/localized, or
stochastic-integral variants of the martingale convergence theorem.  Those
remain separate formalization/integration targets until their exact APIs are
selected and locally checked.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_281

universe u

/--
Normalized data for the checked discrete-time martingale convergence wrapper.

The field `isFiniteMeasure` is explicit because the imported mathlib theorem is
stated under `[IsFiniteMeasure μ]`.  `isProbability` records the source theorem's
probability-space reading, while keeping the wrapper usable for any finite
measure satisfying the same hypotheses.
-/
structure L1BoundedMartingaleData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  filtration : Filtration ℕ ‹MeasurableSpace Ω›
  process : ℕ → Ω → ℝ
  isProbability : IsProbabilityMeasure μ
  isFiniteMeasure : IsFiniteMeasure μ
  martingale : Martingale process filtration μ
  l1Bound : ℝ≥0
  eLpNorm_le : ∀ n : ℕ, eLpNorm (process n) 1 μ ≤ l1Bound

/--
Conclusion of the discrete `L¹`-bounded martingale convergence theorem:
the sample paths converge almost everywhere to mathlib's `Filtration.limitProcess`.
-/
def AlmostSureConvergenceConclusion
    {Ω : Type u} [MeasurableSpace Ω] (D : L1BoundedMartingaleData Ω) : Prop :=
  ∀ᵐ ω ∂D.μ,
    Filter.Tendsto (fun n : ℕ => D.process n ω) Filter.atTop
      (𝓝 (Filtration.limitProcess D.process D.filtration D.μ ω))

/--
Stage1 normalized statement shape for the checked martingale convergence
wrapper.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : L1BoundedMartingaleData Ω,
      AlmostSureConvergenceConclusion D

/--
Repo-local statement-scope decision for `S1-M-281.statement-scope`.

The public Stage1 theorem should be backfilled as the checked discrete-time,
real-valued, `L¹`-bounded martingale convergence theorem represented by
`StatementShape`, not as a broader family of continuous-time, local-martingale,
vector-valued, stopped/localized, or stochastic-integral convergence variants.
-/
inductive StatementScopeDecision where
  | checkedDiscreteRealL1Bounded
  deriving DecidableEq, Repr

/-- The selected public scope for this Stage1 slot. -/
def statementScopeDecision : StatementScopeDecision :=
  .checkedDiscreteRealL1Bounded

/-- Machine-readable in-scope statement families for this local artifact. -/
def inScopeStatementFamilies : List String := [
  "discrete-time indexed by Nat",
  "real-valued process",
  "finite/probability-measure martingale",
  "uniform L1-bound via eLpNorm",
  "almost-sure convergence to Filtration.limitProcess",
  "uniform-integrability companion wrappers already checked below"
]

/-- Machine-readable out-of-scope theorem families for this local artifact. -/
def outOfScopeStatementFamilies : List String := [
  "continuous-time martingale convergence",
  "local-martingale convergence",
  "Banach/vector-valued martingale convergence",
  "stopped/localized martingale convergence families",
  "stochastic-integral convergence variants"
]

/-- The scope decision is definitionally the checked discrete real `L¹` theorem. -/
theorem statementScopeDecision_eq_checkedDiscreteRealL1Bounded :
    statementScopeDecision = .checkedDiscreteRealL1Bounded :=
  rfl

/-- The normalized statement unfolds to the explicit data-parametrized theorem. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : L1BoundedMartingaleData Ω,
          AlmostSureConvergenceConclusion D :=
  Iff.rfl

/--
Checked local wrapper: a discrete real-valued `L¹`-bounded martingale converges
almost everywhere to its mathlib limit process.
-/
theorem martingale_ae_tendsto_limitProcess
    {Ω : Type u} [MeasurableSpace Ω] (D : L1BoundedMartingaleData Ω) :
    AlmostSureConvergenceConclusion D := by
  letI := D.isFiniteMeasure
  exact D.martingale.submartingale.ae_tendsto_limitProcess D.eLpNorm_le

/--
The full normalized wrapper theorem is closed locally by the imported mathlib
submartingale convergence theorem.
-/
theorem statementShape_holds : StatementShape.{u} := by
  intro Ω _ D
  exact martingale_ae_tendsto_limitProcess D

/-- Project the martingale predicate from the normalized data. -/
theorem process_martingale
    {Ω : Type u} [MeasurableSpace Ω] (D : L1BoundedMartingaleData Ω) :
    Martingale D.process D.filtration D.μ :=
  D.martingale

/-- mathlib converts every martingale into a submartingale. -/
theorem process_submartingale
    {Ω : Type u} [MeasurableSpace Ω] (D : L1BoundedMartingaleData Ω) :
    Submartingale D.process D.filtration D.μ :=
  D.martingale.submartingale

/--
Anchor-audit bridge wrapper: `MeasureTheory.Martingale.submartingale`, declared
in `Mathlib.Probability.Martingale.Basic`, is the exact theorem used to pass
from the martingale statement to mathlib's submartingale convergence theorem.
-/
theorem anchorAudit_martingale_submartingale
    {Ω : Type u} [MeasurableSpace Ω] (D : L1BoundedMartingaleData Ω) :
    Submartingale D.process D.filtration D.μ :=
  D.martingale.submartingale

/--
Anchor-audit terminal wrapper: `MeasureTheory.Submartingale.ae_tendsto_limitProcess`,
declared in `Mathlib.Probability.Martingale.Convergence`, is the terminal
mathlib theorem for the checked discrete-time `L¹`-bounded convergence leaf.
-/
theorem anchorAudit_submartingale_ae_tendsto_limitProcess
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {ℱ : Filtration ℕ ‹MeasurableSpace Ω›} {X : ℕ → Ω → ℝ} {R : ℝ≥0}
    (hX : Submartingale X ℱ μ) (hR : ∀ n : ℕ, eLpNorm (X n) 1 μ ≤ R) :
    ∀ᵐ ω ∂μ,
      Filter.Tendsto (fun n : ℕ => X n ω) Filter.atTop
        (𝓝 (Filtration.limitProcess X ℱ μ ω)) :=
  hX.ae_tendsto_limitProcess hR

/-- mathlib's martingale API supplies integrability of each time slice. -/
theorem process_integrable
    {Ω : Type u} [MeasurableSpace Ω] (D : L1BoundedMartingaleData Ω) (n : ℕ) :
    Integrable (D.process n) D.μ :=
  D.martingale.integrable n

/-- The imported convergence theorem also supplies `L¹` membership of the limit process. -/
theorem limitProcess_memLp_one
    {Ω : Type u} [MeasurableSpace Ω] (D : L1BoundedMartingaleData Ω) :
    MemLp (Filtration.limitProcess D.process D.filtration D.μ) 1 D.μ :=
  D.martingale.submartingale.memLp_limitProcess D.eLpNorm_le

/--
Uniform-integrability variant exposed by mathlib: a uniformly integrable
martingale converges almost everywhere to the same limit process.
-/
theorem martingale_ae_tendsto_limitProcess_of_uniformIntegrable
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {ℱ : Filtration ℕ ‹MeasurableSpace Ω›} {X : ℕ → Ω → ℝ}
    (hX : Martingale X ℱ μ) (hUI : UniformIntegrable X 1 μ) :
    ∀ᵐ ω ∂μ,
      Filter.Tendsto (fun n : ℕ => X n ω) Filter.atTop
        (𝓝 (Filtration.limitProcess X ℱ μ ω)) :=
  hX.submartingale.ae_tendsto_limitProcess_of_uniformIntegrable hUI

/--
Uniform-integrability `L¹` convergence wrapper for the same mathlib limit
process.
-/
theorem martingale_tendsto_eLpNorm_one_limitProcess_of_uniformIntegrable
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {ℱ : Filtration ℕ ‹MeasurableSpace Ω›} {X : ℕ → Ω → ℝ}
    (hX : Martingale X ℱ μ) (hUI : UniformIntegrable X 1 μ) :
    Filter.Tendsto
      (fun n : ℕ => eLpNorm (X n - Filtration.limitProcess X ℱ μ) 1 μ)
      Filter.atTop (𝓝 0) :=
  hX.submartingale.tendsto_eLpNorm_one_limitProcess hUI

/--
L¹ martingale convergence, conditional-expectation form: under uniform
integrability, each martingale time slice is the conditional expectation of the
limit process.
-/
theorem martingale_ae_eq_condExp_limitProcess_of_uniformIntegrable
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {ℱ : Filtration ℕ ‹MeasurableSpace Ω›} {X : ℕ → Ω → ℝ}
    (hX : Martingale X ℱ μ) (hUI : UniformIntegrable X 1 μ) (n : ℕ) :
    X n =ᵐ[μ] μ[Filtration.limitProcess X ℱ μ | ℱ n] :=
  hX.ae_eq_condExp_limitProcess hUI n

/-! ## Continuous-time audit result for `S1-M-281.continuous-time-audit`. -/

/--
Shape of a continuous-time real-valued martingale datum supported by the
current mathlib process APIs.  This intentionally records API availability
only: `Martingale` and `Filtration` are generic enough to use index `ℝ≥0`, and
mathlib supplies right-continuous filtrations, but no terminal convergence
theorem below closes this shape in the current imported module.
-/
structure ContinuousTimeMartingaleData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›
  process : ℝ≥0 → Ω → ℝ
  martingale : Martingale process filtration μ
  rightContinuous : Filtration.IsRightContinuous filtration

/--
The natural continuous-time analogue that would have to be proved or imported
before this Stage1 slot could claim a continuous-time martingale convergence
branch.
-/
def ContinuousTimeAlmostSureConvergenceTarget
    {Ω : Type u} [MeasurableSpace Ω] (D : ContinuousTimeMartingaleData Ω) : Prop :=
  ∀ᵐ ω ∂D.μ,
    Filter.Tendsto (fun t : ℝ≥0 => D.process t ω) Filter.atTop
      (𝓝 (Filtration.limitProcess D.process D.filtration D.μ ω))

/-- Repo-local result of the continuous-time audit. -/
inductive ContinuousTimeAuditStatus where
  | outOfScopeForCheckedWrapper
  | integrationBlocker
  deriving DecidableEq, Repr

/--
Continuous-time convergence is not part of the checked local theorem scope, and
the primary local Lean 4 sources do not expose a terminal continuous-time
martingale convergence theorem to pin/import/check here.
-/
def continuousTimeAuditStatus : ContinuousTimeAuditStatus :=
  .integrationBlocker

/-- The exact repo-local continuous-time audit result. -/
theorem continuousTimeAuditStatus_eq_integrationBlocker :
    continuousTimeAuditStatus = .integrationBlocker :=
  rfl

/-- Primary local sources inspected for the continuous-time audit. -/
def continuousTimeAuditPrimarySources : List String := [
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Martingale.Upcrossing",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.BorelCantelli",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping"
]

/-- Positive continuous-time API findings that typecheck at the pinned mathlib revision. -/
def continuousTimePositiveApiFindings : List String := [
  "MeasureTheory.Martingale is generic in a preorder index type",
  "MeasureTheory.Submartingale is generic in a preorder index type",
  "MeasureTheory.Filtration supports index type NNReal",
  "MeasureTheory.Filtration.rightCont is available",
  "MeasureTheory.Filtration.IsRightContinuous is available"
]

/--
Concrete blocker for continuous-time completion: mathlib's currently pinned
terminal convergence theorems are specialized to `ℕ`-indexed real processes.
-/
def continuousTimeIntegrationBlockers : List String := [
  "MeasureTheory.Submartingale.ae_tendsto_limitProcess has index Nat, not NNReal or Real",
  "MeasureTheory.Submartingale.tendsto_eLpNorm_one_limitProcess has index Nat",
  "MeasureTheory.Martingale.ae_eq_condExp_limitProcess has index Nat",
  "No LocalMartingale, Semimartingale, cadlag/cadlàg process, or continuous-time convergence terminal theorem was found in the inspected primary mathlib sources"
]

/-! ## Vector-valued audit result for `S1-M-281.vector-valued-audit`. -/

/--
Shape of a discrete Banach-valued martingale datum supported by mathlib's
generic martingale API.  This records only the available API boundary:
`Martingale` is stated for complete real normed spaces, but the convergence
theorems audited below do not close a Banach-valued convergence statement.
-/
structure BanachValuedDiscreteMartingaleData
    (Ω : Type u) [MeasurableSpace Ω] (E : Type*) [NormedAddCommGroup E]
    [NormedSpace ℝ E] [CompleteSpace E] where
  μ : Measure Ω
  filtration : Filtration ℕ ‹MeasurableSpace Ω›
  process : ℕ → Ω → E
  martingale : Martingale process filtration μ

/--
Candidate Banach-valued convergence shape that is not claimed by this Stage1
artifact.  A terminal theorem for this target would need exact geometric
hypotheses on `E` and a checked Lean theorem name before the public scope could
be broadened.
-/
def BanachValuedAlmostSureConvergenceTarget
    {Ω : Type u} [MeasurableSpace Ω] {E : Type*} [NormedAddCommGroup E]
    [NormedSpace ℝ E] [CompleteSpace E]
    (D : BanachValuedDiscreteMartingaleData Ω E) : Prop :=
  ∃ g : Ω → E,
    AEStronglyMeasurable g D.μ ∧
      ∀ᵐ ω ∂D.μ, Filter.Tendsto (fun n : ℕ => D.process n ω) Filter.atTop (𝓝 (g ω))

/-- Repo-local result of the vector-valued martingale convergence audit. -/
inductive VectorValuedAuditStatus where
  | outOfScopeForCheckedWrapper
  | integrationBlocker
  deriving DecidableEq, Repr

/--
Banach/vector-valued martingale convergence is outside the checked local scope.
The audited primary Lean 4 sources expose generic Banach-valued martingale
definitions, but not a terminal convergence theorem with the needed geometric
hypotheses.
-/
def vectorValuedAuditStatus : VectorValuedAuditStatus :=
  .integrationBlocker

/-- The exact repo-local vector-valued audit result. -/
theorem vectorValuedAuditStatus_eq_integrationBlocker :
    vectorValuedAuditStatus = .integrationBlocker :=
  rfl

/-- Primary local sources inspected for the vector-valued audit. -/
def vectorValuedAuditPrimarySources : List String := [
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.MeasureTheory.Function.ConditionalExpectation.Basic",
  "Mathlib.MeasureTheory.Function.ConditionalExpectation.Real",
  "Mathlib.MeasureTheory.Function.UniformIntegrable",
  "Mathlib.MeasureTheory.VectorMeasure.Decomposition.RadonNikodym",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.L1"
]

/-- Positive vector-valued API findings that typecheck at the pinned mathlib revision. -/
def vectorValuedPositiveApiFindings : List String := [
  "MeasureTheory.Martingale is generic for E with NormedAddCommGroup, NormedSpace Real E, and CompleteSpace E",
  "MeasureTheory.Filtration.limitProcess is generic in the process codomain",
  "MeasureTheory.memLp_limitProcess_of_eLpNorm_bdd is generic for MemLp of a chosen limitProcess",
  "Bochner integration and conditional expectation support complete real normed codomains"
]

/--
Concrete blocker for vector-valued completion: the pinned terminal martingale
convergence theorems are scalar real-valued, and no Lean class or theorem was
found encoding the Banach-space geometry usually needed for broad
Banach-valued martingale convergence.
-/
def vectorValuedIntegrationBlockers : List String := [
  "MeasureTheory.Submartingale.ae_tendsto_limitProcess is stated for processes X : Nat -> Ω -> Real",
  "MeasureTheory.Submartingale.tendsto_eLpNorm_one_limitProcess is stated for processes X : Nat -> Ω -> Real",
  "MeasureTheory.Martingale.ae_eq_condExp_limitProcess is stated for processes X : Nat -> Ω -> Real",
  "No terminal theorem named for Banach-valued, vector-valued, RNP, or Radon-Nikodym-property martingale convergence was found in the inspected primary Lean 4 sources",
  "Mathlib has Radon-Nikodym theorems for scalar/signed/complex measures, but no audited class giving the exact Banach-space geometric hypothesis for this martingale convergence branch"
]

/-! ## Audit probes retained in the checked file. -/

#check MeasureTheory.Filtration
#check MeasureTheory.Filtration.rightCont
#check MeasureTheory.Filtration.IsRightContinuous
#check MeasureTheory.Filtration.limitProcess
#check MeasureTheory.Martingale
#check MeasureTheory.Martingale.integrable
#check MeasureTheory.Martingale.submartingale
#check MeasureTheory.Martingale.ae_eq_condExp_limitProcess
#check MeasureTheory.Submartingale
#check MeasureTheory.Submartingale.integrable
#check MeasureTheory.Submartingale.ae_tendsto_limitProcess
#check MeasureTheory.Submartingale.memLp_limitProcess
#check MeasureTheory.Submartingale.ae_tendsto_limitProcess_of_uniformIntegrable
#check MeasureTheory.Submartingale.tendsto_eLpNorm_one_limitProcess
#check MeasureTheory.UniformIntegrable
#check MeasureTheory.UniformIntegrable.memLp

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Martingale.Upcrossing",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.MeasureTheory.Function.UniformIntegrable"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.Filtration.limitProcess",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.Martingale.submartingale",
  "MeasureTheory.Martingale.ae_eq_condExp_limitProcess",
  "MeasureTheory.Submartingale",
  "MeasureTheory.Submartingale.integrable",
  "MeasureTheory.Submartingale.ae_tendsto_limitProcess",
  "MeasureTheory.Submartingale.memLp_limitProcess",
  "MeasureTheory.Submartingale.ae_tendsto_limitProcess_of_uniformIntegrable",
  "MeasureTheory.Submartingale.tendsto_eLpNorm_one_limitProcess",
  "MeasureTheory.Integrable.tendsto_ae_condExp",
  "MeasureTheory.Integrable.tendsto_eLpNorm_condExp",
  "MeasureTheory.UniformIntegrable",
  "MeasureTheory.UniformIntegrable.memLp"
]

/-- Exact anchor/module pair requested by `S1-M-281.anchor-audit`. -/
def requestedAnchorAudit : List (String × String × String) := [
  ("terminal",
    "Mathlib.Probability.Martingale.Convergence",
    "MeasureTheory.Submartingale.ae_tendsto_limitProcess"),
  ("bridge",
    "Mathlib.Probability.Martingale.Basic",
    "MeasureTheory.Martingale.submartingale")
]

/--
Search terms audited for broader variants not closed by this local wrapper.
-/
def broaderVariantSearchTerms : List String := [
  "continuous-time martingale convergence",
  "LocalMartingale convergence",
  "vector-valued martingale convergence",
  "Doob martingale convergence",
  "martingale convergence theorem stopped process",
  "uniform integrability martingale convergence"
]

end S1_M_281
end Stage1
end AwesomeTheorems
