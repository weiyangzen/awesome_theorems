import Mathlib.Probability.StrongLaw
import Mathlib.Probability.Moments.Variance

/-!
# S1-M-266 / THM-M-0986: Khinchin's law of large numbers

This Stage1 artifact records a conservative Lean 4 boundary for the weak law
of large numbers formulation associated with Khinchin.  The local mathlib
snapshot contains a stronger strong-law theorem for independent identically
distributed integrable random variables.  We expose the weak-law statement in
terms of `MeasureTheory.TendstoInMeasure` and prove a wrapper from the pinned
mathlib strong law.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped Topology MeasureTheory ProbabilityTheory
open scoped Function

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_266

universe u v

/-- Data package for an iid integrable sequence of Banach-valued random variables. -/
structure KhinchinWeakLawProblem (Ω : Type u) (E : Type v) [MeasurableSpace Ω]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] : Type (max u v) where
  μ : Measure Ω
  is_probability : IsProbabilityMeasure μ
  X : ℕ → Ω → E
  integrable_zero : Integrable (X 0) μ
  pairwise_independent : Pairwise ((· ⟂ᵢ[μ] ·) on X)
  identically_distributed : ∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) μ μ

/-- The empirical average of the first `n` random variables. -/
def empiricalAverage {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (P : KhinchinWeakLawProblem Ω E) (n : ℕ) (ω : Ω) : E :=
  (n : ℝ)⁻¹ • (∑ i ∈ Finset.range n, P.X i ω)

/-- The expected value of the common distribution, represented by `X 0`. -/
def commonExpectation {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (P : KhinchinWeakLawProblem Ω E) : E :=
  P.μ[P.X 0]

/--
The weak-law conclusion: empirical averages converge in probability, formalized
as convergence in measure, to the common expectation.
-/
def KhinchinWeakLawConclusion {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (P : KhinchinWeakLawProblem Ω E) : Prop :=
  TendstoInMeasure P.μ (fun n ω => empiricalAverage P n ω) atTop
    (fun _ => commonExpectation P)

/--
Stage1 normalized statement-shape candidate for Khinchin's weak law of large
numbers.  The `CompleteSpace` and `BorelSpace` hypotheses match the available
mathlib strong-law theorem used by the checked wrapper below.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) (E : Type v) [MeasurableSpace Ω] [NormedAddCommGroup E]
    [NormedSpace ℝ E] [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
      ∀ P : KhinchinWeakLawProblem Ω E,
        KhinchinWeakLawConclusion P

/-- The statement-shape definition unfolds to the normalized weak-law form. -/
theorem statementShape_iff :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) (E : Type v) [MeasurableSpace Ω] [NormedAddCommGroup E]
        [NormedSpace ℝ E] [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
          ∀ P : KhinchinWeakLawProblem Ω E,
            KhinchinWeakLawConclusion P :=
  Iff.rfl

/-- The data package exposes the checked mathlib integrability hypothesis. -/
theorem integrable_zero {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (P : KhinchinWeakLawProblem Ω E) :
    Integrable (P.X 0) P.μ :=
  P.integrable_zero

/-- The data package exposes the checked mathlib pairwise-independence hypothesis. -/
theorem pairwise_independent {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (P : KhinchinWeakLawProblem Ω E) :
    Pairwise ((· ⟂ᵢ[P.μ] ·) on P.X) :=
  P.pairwise_independent

/-- The data package exposes the checked mathlib identical-distribution hypothesis. -/
theorem identically_distributed {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (P : KhinchinWeakLawProblem Ω E) :
    ∀ i, ProbabilityTheory.IdentDistrib (P.X i) (P.X 0) P.μ P.μ :=
  P.identically_distributed

/--
Checked repo-local wrapper: the pinned mathlib strong law implies Khinchin's
weak law, with convergence in probability expressed as `TendstoInMeasure`.
-/
theorem khinchinWeakLaw_inMeasure_from_strongLaw_wrapper
    {Ω : Type u} {E : Type v} [MeasurableSpace Ω] [NormedAddCommGroup E]
    [NormedSpace ℝ E] [CompleteSpace E] [MeasurableSpace E] [BorelSpace E]
    (P : KhinchinWeakLawProblem Ω E) :
    KhinchinWeakLawConclusion P := by
  haveI : IsProbabilityMeasure P.μ := P.is_probability
  have hmeas : ∀ i, AEStronglyMeasurable (P.X i) P.μ := fun i =>
    (P.identically_distributed i).aestronglyMeasurable_iff.2 P.integrable_zero.1
  have havg (n : ℕ) :
      AEStronglyMeasurable (fun ω => empiricalAverage P n ω) P.μ := by
    exact AEStronglyMeasurable.const_smul
      (aestronglyMeasurable_fun_sum _ fun i _ => hmeas i) _
  exact tendstoInMeasure_of_tendsto_ae havg
    (ProbabilityTheory.strong_law_ae P.X P.integrable_zero P.pairwise_independent
      P.identically_distributed)

/--
Checked mathlib anchor: the strong law itself, in the same hypothesis shape as
the weak-law wrapper.
-/
theorem strong_law_ae_mathlib_wrapper
    {Ω : Type u} {E : Type v} [MeasurableSpace Ω] {μ : Measure Ω}
    [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (X : ℕ → Ω → E) (hint : Integrable (X 0) μ)
    (hindep : Pairwise ((· ⟂ᵢ[μ] ·) on X))
    (hident : ∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) μ μ) :
    ∀ᵐ ω ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ • (∑ i ∈ Finset.range n, X i ω))
        atTop (𝓝 μ[X 0]) :=
  ProbabilityTheory.strong_law_ae X hint hindep hident

/-- Checked mathlib bridge: almost-sure convergence on a finite measure implies convergence in measure. -/
theorem tendstoInMeasure_of_tendsto_ae_wrapper
    {Ω : Type u} {E : Type v} [MeasurableSpace Ω] {μ : Measure Ω}
    [PseudoEMetricSpace E] [MeasurableSpace E] [IsFiniteMeasure μ]
    {f : ℕ → Ω → E} {g : Ω → E}
    (hf : ∀ n, AEStronglyMeasurable (f n) μ)
    (hfg : ∀ᵐ ω ∂μ, Tendsto (fun n => f n ω) atTop (𝓝 (g ω))) :
    TendstoInMeasure μ f atTop g :=
  tendstoInMeasure_of_tendsto_ae hf hfg

/-- Checked mathlib Chebyshev inequality anchor for variance-based weak-law routes. -/
theorem chebyshev_variance_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {X : Ω → ℝ} (hX : MemLp X 2 μ) {c : ℝ} (hc : 0 < c) :
    μ {ω | c ≤ ‖X ω - μ[X]‖} ≤ ENNReal.ofReal (Var[X; μ] / c ^ 2) :=
  ProbabilityTheory.meas_ge_le_variance_div_sq hX hc

/-- Checked mathlib variance-sum anchor for direct finite-variance weak-law routes. -/
theorem indepFun_variance_sum_mathlib_wrapper
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] {μ : Measure Ω}
    {X : ι → Ω → ℝ} {s : Finset ι}
    (hs : ∀ i ∈ s, MemLp (X i) 2 μ)
    (h : Set.Pairwise ↑s fun i j => X i ⟂ᵢ[μ] X j) :
    Var[∑ i ∈ s, X i; μ] = ∑ i ∈ s, Var[X i; μ] :=
  ProbabilityTheory.IndepFun.variance_sum hs h

/-- mathlib modules checked for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.StrongLaw",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Integrable",
  "Mathlib.Probability.Moments.Variance",
  "Mathlib.MeasureTheory.Function.LpSeminorm.ChebyshevMarkov"
]

/-- Pinned mathlib commit used for the source-anchor audit in this Stage1 slot. -/
def mathlibPinnedCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Suggested public status label for the implemented Lean statement.  This records
only the local wrapper over pinned mathlib, not completion of the broader
Stage1 public checklist.
-/
def implementedStatementPublicStatusLabel : String :=
  "local_wrapper_upstream_mathlib"

/-- Primary-source anchors audited in the pinned mathlib tree. -/
def mathlibPrimarySourceAnchors : List String := [
  "Mathlib/Probability/StrongLaw.lean:788 ProbabilityTheory.strong_law_ae",
  "Mathlib/Probability/StrongLaw.lean:832 ProbabilityTheory.strong_law_Lp",
  "Mathlib/MeasureTheory/Function/ConvergenceInMeasure.lean:57 MeasureTheory.TendstoInMeasure",
  "Mathlib/MeasureTheory/Function/ConvergenceInMeasure.lean:119 MeasureTheory.tendstoInMeasure_iff_norm",
  "Mathlib/MeasureTheory/Function/ConvergenceInMeasure.lean:223 MeasureTheory.tendstoInMeasure_of_tendsto_ae",
  "Mathlib/Probability/IdentDistrib.lean:71 ProbabilityTheory.IdentDistrib",
  "Mathlib/Probability/IdentDistrib.lean:169 ProbabilityTheory.IdentDistrib.aestronglyMeasurable_iff",
  "Mathlib/Probability/IdentDistrib.lean:233 ProbabilityTheory.IdentDistrib.integrable_iff",
  "Mathlib/Probability/Moments/Variance.lean:79 scoped notation Var",
  "Mathlib/Probability/Moments/Variance.lean:397 ProbabilityTheory.meas_ge_le_variance_div_sq",
  "Mathlib/Probability/Moments/Variance.lean:422 ProbabilityTheory.IndepFun.variance_sum"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.strong_law_ae",
  "ProbabilityTheory.strong_law_Lp",
  "MeasureTheory.TendstoInMeasure",
  "MeasureTheory.tendstoInMeasure_of_tendsto_ae",
  "MeasureTheory.tendstoInMeasure_iff_norm",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.meas_ge_le_variance_div_sq",
  "ProbabilityTheory.IndepFun.variance_sum"
]

/--
Optional public follow-up tasks that are intentionally not required for the
checked strong-law wrapper status.
-/
def optionalFollowUpTasks : List String := [
  "Build a direct real-valued finite-variance weak-law proof using " ++
    "ProbabilityTheory.meas_ge_le_variance_div_sq and " ++
    "ProbabilityTheory.IndepFun.variance_sum.",
  "Audit the exact historical Khinchin formulation against the implemented " ++
    "iid integrable Banach-valued statement."
]

/-- Search terms that did not locate a separately named weak-law theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "weak_law",
  "weak law of large numbers",
  "Khinchin law",
  "Khintchine law",
  "Khinchin weak law",
  "law of large numbers TendstoInMeasure",
  "TendstoInMeasure average expectation"
]

end S1_M_266
end Stage1
end AwesomeTheorems
