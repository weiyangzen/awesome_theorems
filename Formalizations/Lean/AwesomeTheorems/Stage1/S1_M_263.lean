import Mathlib.Probability.StrongLaw
import Mathlib.MeasureTheory.Function.ConvergenceInMeasure

/-!
# S1-M-263 / THM-M-0983: Law of large numbers

This Stage1 artifact records a checked Lean 4 wrapper for the frequency form
of the law of large numbers: empirical frequencies converge almost surely to
the underlying probability.

The pinned mathlib snapshot already contains the strong law of large numbers
in `ProbabilityTheory.strong_law_ae_real` from `Mathlib.Probability.StrongLaw`
at mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`.  The local
wrapper below specializes that theorem to real-valued `0/1` success indicators,
with the limiting probability supplied by the expectation of the reference
indicator.  The proof body remains upstream in pinned mathlib; this file
provides the repo-local statement-shape and wrapper closure for this Stage1
slot.
-/

noncomputable section

open MeasureTheory Filter Finset
open scoped MeasureTheory ProbabilityTheory Topology ENNReal NNReal
open scoped Function

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_263

universe u

/--
Empirical frequency of successes among the first `n` observations.

For the intended frequency interpretation, `X i ω` is a real-valued indicator
with values `0` and `1`; this is recorded in `FrequencyLawData.indicator_values`.
-/
def empiricalFrequency {Ω : Type u} (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  (∑ i ∈ Finset.range n, X i ω) / (n : ℝ)

/--
Normalized data for the frequency/probability law of large numbers.

`X n` represents the `n`-th success indicator.  The field
`expectation_eq_probability` is the formal bridge from expectation of the
reference indicator to the source phrase "probability"; for concrete events,
a later integrator can discharge it from a measurable-set indicator integral.
-/
structure FrequencyLawData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  X : ℕ → Ω → ℝ
  probability : ℝ
  integrable_zero : Integrable (X 0) μ
  pairwise_independent : Pairwise ((· ⟂ᵢ[μ] ·) on X)
  identically_distributed : ∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) μ μ
  indicator_values : ∀ n, ∀ᵐ ω ∂μ, X n ω = 0 ∨ X n ω = 1
  expectation_eq_probability : μ[X 0] = probability

/-- Almost-sure convergence of empirical frequencies to the event probability. -/
def FrequencyLawConclusion {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) : Prop :=
  ∀ᵐ ω ∂D.μ,
    Tendsto (fun n : ℕ => empiricalFrequency D.X n ω) atTop (𝓝 D.probability)

/--
Convergence in probability, formalized by mathlib as convergence in measure,
for empirical frequencies.  For probability measures this is exactly the weak
convergence-in-probability reading of the phrase "frequency converges to
probability".
-/
def FrequencyLawInProbabilityConclusion {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) : Prop :=
  TendstoInMeasure D.μ (fun n ω => empiricalFrequency D.X n ω) atTop
    (fun _ => D.probability)

/--
Stage1 normalized statement shape for THM-M-0983.

For pairwise independent, identically distributed real-valued success
indicators, empirical frequencies converge almost surely to the probability of
success, represented by the expectation of the reference indicator.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : FrequencyLawData Ω,
      FrequencyLawConclusion D

/-- The statement-shape definition unfolds to the explicit data-parametrized form. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : FrequencyLawData Ω,
          FrequencyLawConclusion D :=
  Iff.rfl

/-- Project the integrability hypothesis from the normalized data package. -/
theorem integrable_zero {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) :
    Integrable (D.X 0) D.μ :=
  D.integrable_zero

/-- Project the pairwise-independence hypothesis from the normalized data package. -/
theorem pairwise_independent {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) :
    Pairwise ((· ⟂ᵢ[D.μ] ·) on D.X) :=
  D.pairwise_independent

/--
Family-level independence implies the pairwise `IndepFun` hypothesis consumed
by `ProbabilityTheory.strong_law_ae_real`.
-/
theorem iIndepFun_pairwise_independent {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X : ℕ → Ω → ℝ}
    (h : ProbabilityTheory.iIndepFun X μ) :
    Pairwise ((· ⟂ᵢ[μ] ·) on X) := by
  intro i j hij
  exact h.indepFun hij

/-- Project identical distribution of each coordinate with the reference indicator. -/
theorem identically_distributed {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) (i : ℕ) :
    ProbabilityTheory.IdentDistrib (D.X i) (D.X 0) D.μ D.μ :=
  D.identically_distributed i

/-- Project the `0/1` indicator-value hypothesis. -/
theorem indicator_values {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) (n : ℕ) :
    ∀ᵐ ω ∂D.μ, D.X n ω = 0 ∨ D.X n ω = 1 :=
  D.indicator_values n

/-- Project the expectation/probability bridge for the reference indicator. -/
theorem expectation_eq_probability {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) :
    D.μ[D.X 0] = D.probability :=
  D.expectation_eq_probability

/-! ## Family-level independent data. -/

/--
Normalized frequency-law data using the standard family-level independence
interface `iIndepFun`.

The existing `FrequencyLawData` package keeps the pairwise interface because
that is what `ProbabilityTheory.strong_law_ae_real` expects.  The conversion
below is the checked bridge from the usual IID-family formulation to that
pairwise hypothesis.
-/
structure IIndepFrequencyLawData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  X : ℕ → Ω → ℝ
  probability : ℝ
  integrable_zero : Integrable (X 0) μ
  independent : ProbabilityTheory.iIndepFun X μ
  identically_distributed : ∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) μ μ
  indicator_values : ∀ n, ∀ᵐ ω ∂μ, X n ω = 0 ∨ X n ω = 1
  expectation_eq_probability : μ[X 0] = probability

namespace IIndepFrequencyLawData

/-- The packaged family-level independence gives the pairwise SLLN hypothesis. -/
theorem pairwise_independent {Ω : Type u} [MeasurableSpace Ω]
    (D : IIndepFrequencyLawData Ω) :
    Pairwise ((· ⟂ᵢ[D.μ] ·) on D.X) :=
  iIndepFun_pairwise_independent D.independent

/--
Convert family-independent frequency-law data into the pairwise data package
used by the checked mathlib strong-law wrapper.
-/
def toFrequencyLawData {Ω : Type u} [MeasurableSpace Ω]
    (D : IIndepFrequencyLawData Ω) : FrequencyLawData Ω where
  μ := D.μ
  X := D.X
  probability := D.probability
  integrable_zero := D.integrable_zero
  pairwise_independent := D.pairwise_independent
  identically_distributed := D.identically_distributed
  indicator_values := D.indicator_values
  expectation_eq_probability := D.expectation_eq_probability

end IIndepFrequencyLawData

/-! ## Concrete measurable-event indicators. -/

/--
The real-valued indicator of an event, normalized to the `0/1` convention used
by the frequency wrapper.
-/
def eventIndicator {Ω : Type u} (E : Set Ω) : Ω → ℝ :=
  E.indicator fun _ => (1 : ℝ)

/-- The real-valued probability attached to an event by a measure. -/
def eventProbability {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (E : Set Ω) : ℝ :=
  μ.real E

/--
Concrete package for one measurable event and its `0/1` real-valued indicator.

The theorem `EventIndicatorData.expectation_eq_probability` below is the
repo-local bridge from mathlib's indicator integral API to the probability term
used in `FrequencyLawData`.
-/
structure EventIndicatorData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  event : Set Ω
  measurable_event : MeasurableSet event

namespace EventIndicatorData

/-- The packaged real-valued `0/1` indicator. -/
def indicator {Ω : Type u} [MeasurableSpace Ω]
    (D : EventIndicatorData Ω) : Ω → ℝ :=
  eventIndicator D.event

/-- The packaged real-valued event probability. -/
def probability {Ω : Type u} [MeasurableSpace Ω]
    (D : EventIndicatorData Ω) : ℝ :=
  eventProbability D.μ D.event

/-- The packaged indicator is measurable. -/
theorem measurable_indicator {Ω : Type u} [MeasurableSpace Ω]
    (D : EventIndicatorData Ω) :
    Measurable D.indicator := by
  simpa [indicator, eventIndicator] using
    (measurable_const.indicator D.measurable_event :
      Measurable (D.event.indicator fun _ : Ω => (1 : ℝ)))

/-- The packaged indicator is integrable under a finite measure. -/
theorem integrable_indicator {Ω : Type u} [MeasurableSpace Ω]
    (D : EventIndicatorData Ω) [IsFiniteMeasure D.μ] :
    Integrable D.indicator D.μ := by
  simpa [indicator, eventIndicator] using
    ((integrable_const (1 : ℝ) :
      Integrable (fun _ : Ω => (1 : ℝ)) D.μ).indicator D.measurable_event)

/-- Pointwise `0/1` values for the packaged event indicator. -/
theorem indicator_values {Ω : Type u} [MeasurableSpace Ω]
    (D : EventIndicatorData Ω) :
    ∀ ω, D.indicator ω = 0 ∨ D.indicator ω = 1 := by
  intro ω
  by_cases hω : ω ∈ D.event
  · right
    simp [indicator, eventIndicator, hω]
  · left
    simp [indicator, eventIndicator, hω]

/-- Almost-everywhere `0/1` values for the packaged event indicator. -/
theorem ae_indicator_values {Ω : Type u} [MeasurableSpace Ω]
    (D : EventIndicatorData Ω) :
    ∀ᵐ ω ∂D.μ, D.indicator ω = 0 ∨ D.indicator ω = 1 :=
  Filter.Eventually.of_forall D.indicator_values

/--
Expectation/probability bridge for a concrete measurable event.

This is the child-task closure: it instantiates mathlib's
`MeasureTheory.integral_indicator_one` as the real expectation of the event
indicator and identifies the result with `μ.real event`.
-/
theorem expectation_eq_probability {Ω : Type u} [MeasurableSpace Ω]
    (D : EventIndicatorData Ω) :
    D.μ[D.indicator] = D.probability := by
  simpa [indicator, eventIndicator, probability, eventProbability] using
    (MeasureTheory.integral_indicator_one (μ := D.μ) D.measurable_event)

end EventIndicatorData

/-- Indicators for a sequence of measurable events. -/
def eventIndicators {Ω : Type u} (E : ℕ → Set Ω) : ℕ → Ω → ℝ :=
  fun n => eventIndicator (E n)

/--
Concrete event-family package whose indicators can be fed into the normalized
law-of-large-numbers wrapper once pairwise independence and identical
distribution are supplied.
-/
structure EventFrequencyLawData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  event : ℕ → Set Ω
  measurable_event : ∀ n, MeasurableSet (event n)
  pairwise_independent : Pairwise ((· ⟂ᵢ[μ] ·) on eventIndicators event)
  identically_distributed :
    ∀ i, ProbabilityTheory.IdentDistrib
      (eventIndicators event i) (eventIndicators event 0) μ μ

namespace EventFrequencyLawData

/-- The reference event package at index `0`. -/
def reference {Ω : Type u} [MeasurableSpace Ω]
    (D : EventFrequencyLawData Ω) : EventIndicatorData Ω where
  μ := D.μ
  event := D.event 0
  measurable_event := D.measurable_event 0

/-- The reference indicator is integrable under a finite measure. -/
theorem reference_integrable {Ω : Type u} [MeasurableSpace Ω]
    (D : EventFrequencyLawData Ω) [IsFiniteMeasure D.μ] :
    Integrable D.reference.indicator D.μ := by
  simpa [reference] using
    ((integrable_const (1 : ℝ) :
      Integrable (fun _ : Ω => (1 : ℝ)) D.μ).indicator (D.measurable_event 0))

/--
Convert a concrete measurable-event family into the normalized frequency-law
data package.  The probability field is closed by
`EventIndicatorData.expectation_eq_probability`.
-/
def toFrequencyLawData {Ω : Type u} [MeasurableSpace Ω]
    (D : EventFrequencyLawData Ω) [IsFiniteMeasure D.μ] :
    FrequencyLawData Ω where
  μ := D.μ
  X := eventIndicators D.event
  probability := D.reference.probability
  integrable_zero := by
    simpa [reference, eventIndicators, EventIndicatorData.indicator] using
      D.reference_integrable
  pairwise_independent := D.pairwise_independent
  identically_distributed := D.identically_distributed
  indicator_values := by
    intro n
    exact Filter.Eventually.of_forall (by
      intro ω
      by_cases hω : ω ∈ D.event n
      · right
        simp [eventIndicators, eventIndicator, hω]
      · left
        simp [eventIndicators, eventIndicator, hω])
  expectation_eq_probability := by
    simpa [reference, eventIndicators] using
      D.reference.expectation_eq_probability

end EventFrequencyLawData

/-- The empirical-frequency notation unfolds to the mathlib strong-law average. -/
theorem empiricalFrequency_apply {Ω : Type u}
    (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) :
    empiricalFrequency X n ω = (∑ i ∈ Finset.range n, X i ω) / (n : ℝ) :=
  rfl

/--
Checked repo-local wrapper around mathlib's real-valued almost-sure strong law
of large numbers.
-/
theorem frequencyLaw_ae_mathlib_wrapper {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) :
    FrequencyLawConclusion D := by
  have h :=
    ProbabilityTheory.strong_law_ae_real D.X D.integrable_zero
      D.pairwise_independent D.identically_distributed
  filter_upwards [h] with ω hω
  simpa [FrequencyLawConclusion, empiricalFrequency, D.expectation_eq_probability] using hω

/--
Checked almost-sure frequency wrapper from family-level `iIndepFun`
independence.  This is the child-task bridge into the pairwise hypothesis used
by `ProbabilityTheory.strong_law_ae_real`.
-/
theorem frequencyLaw_ae_from_iIndepFun_wrapper {Ω : Type u} [MeasurableSpace Ω]
    (D : IIndepFrequencyLawData Ω) :
    FrequencyLawConclusion D.toFrequencyLawData :=
  frequencyLaw_ae_mathlib_wrapper D.toFrequencyLawData

/--
Concrete event-family version of the checked almost-sure frequency wrapper.
-/
theorem eventFrequencyLaw_ae_mathlib_wrapper {Ω : Type u} [MeasurableSpace Ω]
    (D : EventFrequencyLawData Ω) [IsFiniteMeasure D.μ] :
    FrequencyLawConclusion D.toFrequencyLawData :=
  frequencyLaw_ae_mathlib_wrapper D.toFrequencyLawData

/--
Checked convergence-in-probability wrapper derived from the almost-sure
frequency wrapper.

This closes the child-task phrase decision without adding a separate weak-law
proof: the public phrase `频率收敛于概率` should record the almost-sure statement
as the primary strong-law theorem and may also record convergence in probability
as this finite-measure consequence.
-/
theorem frequencyLaw_inProbability_from_ae_wrapper {Ω : Type u} [MeasurableSpace Ω]
    (D : FrequencyLawData Ω) [IsFiniteMeasure D.μ] :
    FrequencyLawInProbabilityConclusion D := by
  have hX : ∀ i, AEStronglyMeasurable (D.X i) D.μ := fun i =>
    (D.identically_distributed i).aestronglyMeasurable_iff.2 D.integrable_zero.1
  have hfreq :
      ∀ n, AEStronglyMeasurable (fun ω => empiricalFrequency D.X n ω) D.μ := by
    intro n
    have hsum : AEStronglyMeasurable (fun ω => ∑ i ∈ Finset.range n, D.X i ω) D.μ :=
      aestronglyMeasurable_fun_sum _ fun i _ => hX i
    simpa [empiricalFrequency, div_eq_mul_inv] using hsum.mul_const ((n : ℝ)⁻¹)
  exact tendstoInMeasure_of_tendsto_ae hfreq
    (by simpa using frequencyLaw_ae_mathlib_wrapper D)

/-- Family-level independent convergence-in-probability wrapper. -/
theorem frequencyLaw_inProbability_from_iIndepFun_wrapper
    {Ω : Type u} [MeasurableSpace Ω]
    (D : IIndepFrequencyLawData Ω) [IsFiniteMeasure D.μ] :
    FrequencyLawInProbabilityConclusion D.toFrequencyLawData :=
  by
    haveI : IsFiniteMeasure D.toFrequencyLawData.μ := by
      simpa [IIndepFrequencyLawData.toFrequencyLawData] using
        (inferInstance : IsFiniteMeasure D.μ)
    exact frequencyLaw_inProbability_from_ae_wrapper D.toFrequencyLawData

/-- Concrete event-family convergence-in-probability wrapper. -/
theorem eventFrequencyLaw_inProbability_from_ae_wrapper {Ω : Type u} [MeasurableSpace Ω]
    (D : EventFrequencyLawData Ω) [IsFiniteMeasure D.μ] :
    FrequencyLawInProbabilityConclusion D.toFrequencyLawData :=
  by
    haveI : IsFiniteMeasure D.toFrequencyLawData.μ := by
      simpa [EventFrequencyLawData.toFrequencyLawData] using
        (inferInstance : IsFiniteMeasure D.μ)
    exact frequencyLaw_inProbability_from_ae_wrapper D.toFrequencyLawData

/-- The normalized Stage1 statement is closed by the pinned mathlib theorem. -/
theorem statementShape_mathlib_wrapper :
    StatementShape.{u} := by
  intro Ω _mΩ D
  exact frequencyLaw_ae_mathlib_wrapper D

/-- Pinned mathlib revision supplying `ProbabilityTheory.strong_law_ae_real`. -/
def mathlibPinnedCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Machine-state classification for the local law-of-large-numbers wrapper. -/
def localWrapperMachineState : String :=
  "local_wrapper_upstream_mathlib"

/-- mathlib modules checked while locating repo-local law-of-large-numbers anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.StrongLaw",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Integrable",
  "Mathlib.MeasureTheory.Integral.Bochner.Set",
  "Mathlib.MeasureTheory.Integral.DominatedConvergence",
  "Mathlib.Analysis.PSeries",
  "Mathlib.Analysis.Asymptotics.SpecificAsymptotics"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.strong_law_ae_real",
  "ProbabilityTheory.strong_law_ae",
  "ProbabilityTheory.strong_law_Lp",
  "MeasureTheory.TendstoInMeasure",
  "MeasureTheory.tendstoInMeasure_of_tendsto_ae",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.IdentDistrib.integral_eq",
  "ProbabilityTheory.IdentDistrib.integrable_iff",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.iIndepFun.indepFun",
  "MeasureTheory.Integrable.isProbabilityMeasure_of_indepFun",
  "MeasureTheory.integral_indicator_one",
  "MeasureTheory.integral_indicator_const",
  "MeasureTheory.Measure.real"
]

/--
Audit note for the public Stage1 backfill: `ProbabilityTheory.strong_law_ae_real`
from `Mathlib.Probability.StrongLaw`, pinned through the Lake dependency at
`mathlibPinnedCommit`, closes the normalized almost-sure IID frequency wrapper
`frequencyLaw_ae_mathlib_wrapper`.
-/
def publicBackfillAuditNote : String :=
  "ProbabilityTheory.strong_law_ae_real from Mathlib.Probability.StrongLaw at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95 closes the normalized almost-sure IID frequency wrapper frequencyLaw_ae_mathlib_wrapper."

/-- Public phrase decision for `频率收敛于概率`. -/
def publicPhraseConvergenceDecision : String :=
  "Record `频率收敛于概率` as both: the primary Stage1 theorem is almost-sure convergence via frequencyLaw_ae_mathlib_wrapper, and convergence in probability follows under the finite-measure/probability-measure side condition via frequencyLaw_inProbability_from_ae_wrapper. No separate weak-law proof is required unless the public scope asks for weaker hypotheses than the strong-law wrapper."

/-- Public independence-interface decision for the strong-law wrapper. -/
def publicIndependenceBridgeDecision : String :=
  "The standard family-level IID independence hypothesis is represented by IIndepFrequencyLawData.independent : ProbabilityTheory.iIndepFun X μ. The checked theorem iIndepFun_pairwise_independent applies ProbabilityTheory.iIndepFun.indepFun pointwise to produce Pairwise ((· ⟂ᵢ[μ] ·) on X), exactly the pairwise IndepFun hypothesis consumed by ProbabilityTheory.strong_law_ae_real. The wrappers frequencyLaw_ae_from_iIndepFun_wrapper and frequencyLaw_inProbability_from_iIndepFun_wrapper validate the converted package repo-locally."

/--
Search terms checked while auditing this slot.  The pinned mathlib theorem
already closes the normalized frequency wrapper, so these are retained as audit
metadata rather than blockers.
-/
def auditSearchTerms : List String := [
  "law of large numbers",
  "strong law of large numbers",
  "frequency converges to probability",
  "strong_law_ae_real",
  "strong_law_ae",
  "TendstoInMeasure",
  "tendstoInMeasure_of_tendsto_ae",
  "IdentDistrib",
  "Pairwise ((. IndepFun[mu] .) on X)",
  "iIndepFun.indepFun",
  "indicator",
  "integral_indicator_one",
  "0/1 random variables"
]

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check statementShape_mathlib_wrapper
#check frequencyLaw_ae_mathlib_wrapper
#check empiricalFrequency
#check FrequencyLawConclusion
#check FrequencyLawInProbabilityConclusion
#check iIndepFun_pairwise_independent
#check IIndepFrequencyLawData
#check IIndepFrequencyLawData.pairwise_independent
#check IIndepFrequencyLawData.toFrequencyLawData
#check eventIndicator
#check eventProbability
#check EventIndicatorData
#check EventIndicatorData.measurable_indicator
#check EventIndicatorData.integrable_indicator
#check EventIndicatorData.indicator_values
#check EventIndicatorData.expectation_eq_probability
#check eventIndicators
#check EventFrequencyLawData
#check EventFrequencyLawData.toFrequencyLawData
#check frequencyLaw_ae_from_iIndepFun_wrapper
#check eventFrequencyLaw_ae_mathlib_wrapper
#check frequencyLaw_inProbability_from_ae_wrapper
#check frequencyLaw_inProbability_from_iIndepFun_wrapper
#check eventFrequencyLaw_inProbability_from_ae_wrapper
#check ProbabilityTheory.strong_law_ae_real
#check ProbabilityTheory.strong_law_ae
#check ProbabilityTheory.strong_law_Lp
#check MeasureTheory.TendstoInMeasure
#check MeasureTheory.tendstoInMeasure_of_tendsto_ae
#check ProbabilityTheory.IdentDistrib
#check ProbabilityTheory.IdentDistrib.integral_eq
#check ProbabilityTheory.IdentDistrib.integrable_iff
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.indepFun
#check MeasureTheory.integral_indicator_one
#check mathlibPinnedCommit
#check localWrapperMachineState
#check publicBackfillAuditNote
#check publicPhraseConvergenceDecision
#check publicIndependenceBridgeDecision

end S1_M_263
end Stage1
end AwesomeTheorems
