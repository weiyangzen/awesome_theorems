import Mathlib.Probability.StrongLaw

/-!
# S1-M-264 / THM-M-0984: Strong law of large numbers

This Stage1 artifact records a checked Lean 4 wrapper for the strong law of
large numbers as available in the pinned mathlib snapshot.

The source item says "almost sure convergence".  mathlib's theorem
`ProbabilityTheory.strong_law_ae` proves the Banach-valued iid integrable
version, with Etemadi's pairwise-independence hypothesis: for independent
identically distributed integrable random variables `X n`, the empirical
averages `n⁻¹ • ∑ i ∈ range n, X i` converge almost surely to `μ[X 0]`.

This file does not introduce new axioms or placeholders.  The terminal proof
body is upstream in pinned mathlib; this file supplies the repo-local wrapper
and statement-shape surface.
-/

noncomputable section

open MeasureTheory Filter Finset Function
open scoped MeasureTheory ProbabilityTheory Topology ENNReal NNReal

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_264

universe u v

/-- Stage1 machine-state classification for this repo-local artifact. -/
def machineState : String :=
  "local_wrapper_upstream_mathlib"

/-- mathlib commit used for the upstream strong-law anchor in the Stage1 audit. -/
def pinnedMathlibCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Upstream mathlib module containing the terminal proof body. -/
def upstreamStrongLawModule : String :=
  "Mathlib.Probability.StrongLaw"

/-- Upstream theorem used by the checked local wrapper. -/
def upstreamStrongLawTheorem : String :=
  "ProbabilityTheory.strong_law_ae"

/-- The closed Stage1 boundary for this artifact. -/
def closedStatementBoundary : List String := [
  "iid integrable Banach-valued strong law",
  "Integrable (X 0) μ",
  "Pairwise ((· ⟂ᵢ[μ] ·) on X)",
  "∀ i, IdentDistrib (X i) (X 0) μ μ",
  "almost-sure convergence of empirical averages to μ[X 0]"
]

/--
Nearby strong-law variants that this Stage1 wrapper intentionally does not
claim to close.
-/
def unclaimedStrongLawVariants : List String := [
  "Kolmogorov non-iid strong law",
  "martingale strong law",
  "triangular-array strong law",
  "ergodic-theorem-derived almost-sure averages"
]

/--
The repo-local completion claim is deliberately restricted to mathlib's
iid/pairwise-independent integrable statement, not to the broader SLLN family.
-/
def completionClaimBoundary : List String :=
  closedStatementBoundary ++
    ["not Kolmogorov non-iid, martingale, triangular-array, or ergodic SLLN"]

/-- Empirical average of the first `n` terms in a Banach-valued random sequence. -/
def empiricalAverage
    {Ω : Type u} {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (X : ℕ → Ω → E) (n : ℕ) (ω : Ω) : E :=
  (n : ℝ)⁻¹ • (∑ i ∈ Finset.range n, X i ω)

/--
Normalized data for the strong law of large numbers in the form proved by
mathlib.

The probability-measure hypothesis is intentionally not a field: the pinned
mathlib theorem derives it from the nontrivial independence/integrability
hypotheses when needed, and also handles the degenerate zero-a.e. case.
-/
structure StrongLawData (Ω : Type u) [MeasurableSpace Ω]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E] where
  μ : Measure Ω
  X : ℕ → Ω → E
  integrable_zero : Integrable (X 0) μ
  pairwise_independent : Pairwise (Function.onFun (fun Y Z => Y ⟂ᵢ[μ] Z) X)
  identically_distributed : ∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) μ μ

/-- Almost-sure convergence conclusion of the strong law. -/
def StrongLawConclusion
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : StrongLawData Ω E) : Prop :=
  ∀ᵐ ω ∂D.μ,
    Tendsto (fun n : ℕ => empiricalAverage D.X n ω) atTop (𝓝 D.μ[D.X 0])

/--
Stage1 normalized statement shape for the strong law of large numbers.

This is a repo-local theorem target, not merely a proposition stub: the wrapper
below closes it by calling the pinned mathlib theorem.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ (E : Type v) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
      [MeasurableSpace E] [BorelSpace E],
      ∀ D : StrongLawData Ω E,
        StrongLawConclusion D

/--
The same Stage1 statement boundary with the three core hypotheses exposed
directly rather than bundled in `StrongLawData`.
-/
def StatementShapeExplicitHypotheses : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ (E : Type v) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
      [MeasurableSpace E] [BorelSpace E],
      ∀ (μ : Measure Ω) (X : ℕ → Ω → E),
        Integrable (X 0) μ →
        Pairwise ((· ⟂ᵢ[μ] ·) on X) →
        (∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) μ μ) →
        ∀ᵐ ω ∂μ,
          Tendsto (fun n : ℕ => empiricalAverage X n ω) atTop (𝓝 μ[X 0])

/-- The statement-shape definition unfolds to the explicit normalized form. -/
theorem statementShape_iff :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ (E : Type v) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
          [MeasurableSpace E] [BorelSpace E],
          ∀ D : StrongLawData Ω E,
            StrongLawConclusion D :=
  Iff.rfl

/-- Project the integrability hypothesis from the normalized data package. -/
theorem integrable_zero
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : StrongLawData Ω E) :
    Integrable (D.X 0) D.μ :=
  D.integrable_zero

/-- Project the pairwise-independence hypothesis from the normalized data package. -/
theorem pairwise_independent
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : StrongLawData Ω E) :
    Pairwise (Function.onFun (fun Y Z => Y ⟂ᵢ[D.μ] Z) D.X) :=
  D.pairwise_independent

/-- Project identical distribution of each coordinate with the reference variable. -/
theorem identically_distributed
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : StrongLawData Ω E) (i : ℕ) :
    ProbabilityTheory.IdentDistrib (D.X i) (D.X 0) D.μ D.μ :=
  D.identically_distributed i

/-- The empirical-average notation unfolds to mathlib's strong-law average. -/
theorem empiricalAverage_apply
    {Ω : Type u} {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (X : ℕ → Ω → E) (n : ℕ) (ω : Ω) :
    empiricalAverage X n ω = (n : ℝ)⁻¹ • (∑ i ∈ Finset.range n, X i ω) :=
  rfl

/--
Checked repo-local wrapper around mathlib's almost-sure strong law of large
numbers.
-/
theorem strongLaw_ae_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : StrongLawData Ω E) :
    StrongLawConclusion D :=
  ProbabilityTheory.strong_law_ae D.X D.integrable_zero
    D.pairwise_independent D.identically_distributed

/-- The normalized Stage1 statement is closed by the pinned mathlib theorem. -/
theorem statementShape_mathlib_wrapper :
    StatementShape.{u, v} := by
  intro Ω _mΩ E _add _space _complete _meas _borel D
  exact strongLaw_ae_mathlib_wrapper D

/--
Checked explicit-hypothesis surface for the public Stage1 statement summary.
-/
theorem statementShapeExplicitHypotheses_mathlib_wrapper :
    StatementShapeExplicitHypotheses.{u, v} := by
  intro Ω _mΩ E _add _space _complete _meas _borel μ X h_integrable h_indep h_ident
  exact ProbabilityTheory.strong_law_ae X h_integrable h_indep h_ident

/-- mathlib modules checked while locating repo-local strong-law anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.StrongLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Integrable",
  "Mathlib.MeasureTheory.Integral.DominatedConvergence",
  "Mathlib.Analysis.PSeries",
  "Mathlib.Analysis.Asymptotics.SpecificAsymptotics"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.strong_law_ae",
  "ProbabilityTheory.strong_law_ae_real",
  "ProbabilityTheory.strong_law_Lp",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.IdentDistrib.integral_eq",
  "ProbabilityTheory.IdentDistrib.integrable_iff",
  "ProbabilityTheory.truncation",
  "ProbabilityTheory.IdentDistrib.truncation",
  "MeasureTheory.Integrable.isProbabilityMeasure_of_indepFun",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.IndepFun"
]

/--
Search terms checked for alternative terminal strong-law anchors.  The pinned
mathlib theorem already closes the main Stage1 target, so these are retained as
audit metadata rather than blockers.
-/
def auditSearchTerms : List String := [
  "strong_law_ae",
  "strong_law_ae_real",
  "strong_law_Lp",
  "strong law of large numbers",
  "almost surely",
  "Pairwise ((. IndepFun[mu] .) on X)",
  "IdentDistrib",
  "iid integrable random variables"
]

/-- Public documents that must be synchronized by a serial integrator. -/
def publicBackfillTargets : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md or the authoritative README/status surface, if it mentions this slot"
]

/--
Checklist text for the public-status synchronization gate.  This is deliberately
metadata: the public planning documents are not edited by this Lean artifact.
-/
def publicStatusSyncGate : List String := [
  "replace any stale public open state for S1-M-264 if the local wrapper is accepted as the Stage1 closure target",
  "state machine status local_wrapper_upstream_mathlib",
  "cite Mathlib.Probability.StrongLaw / ProbabilityTheory.strong_law_ae",
  "cite mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "record local validation command cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_264.lean",
  "preserve the boundary: iid integrable Banach-valued pairwise-independent SLLN only",
  "state no residual repo_local_integration_debt for the normalized wrapper"
]

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check StatementShapeExplicitHypotheses
#check statementShape_mathlib_wrapper
#check statementShapeExplicitHypotheses_mathlib_wrapper
#check strongLaw_ae_mathlib_wrapper
#check machineState
#check pinnedMathlibCommit
#check upstreamStrongLawModule
#check upstreamStrongLawTheorem
#check closedStatementBoundary
#check unclaimedStrongLawVariants
#check completionClaimBoundary
#check publicBackfillTargets
#check publicStatusSyncGate
#check empiricalAverage
#check StrongLawConclusion
#check ProbabilityTheory.strong_law_ae
#check ProbabilityTheory.strong_law_ae_real
#check ProbabilityTheory.strong_law_Lp
#check ProbabilityTheory.IdentDistrib
#check ProbabilityTheory.IdentDistrib.integral_eq
#check ProbabilityTheory.IdentDistrib.integrable_iff
#check ProbabilityTheory.truncation

end S1_M_264
end Stage1
end AwesomeTheorems
