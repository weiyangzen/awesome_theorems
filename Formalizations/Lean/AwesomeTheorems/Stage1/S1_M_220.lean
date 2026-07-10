import Mathlib.Probability.HasLaw
import Mathlib.Probability.Independence.InfinitePi
import Mathlib.Probability.Martingale.OptionalStopping
import Mathlib.Probability.Process.HittingTime

/-!
# S1-M-220 / THM-M-1064: Skorokhod embedding

This Stage1 artifact records a conservative Lean 4 boundary for the
Skorokhod-embedding slot summarized as "embedding a random walk".

The pinned mathlib snapshot has probability laws, independence, filtrations,
adapted processes, stopping times, stopped values/processes, hitting times, and
martingale optional stopping.  It does not expose a terminal theorem named
Skorokhod embedding or a ready-made Brownian-motion embedding theorem.  The main
result is therefore represented as an explicit statement shape, while the
available stochastic-process substrate is checked by small wrappers below.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace AwesomeTheorems.Stage1.S1_M_220

universe uΩ uβ

/--
Candidate first targets for the Skorokhod-embedding Stage1 slot.

The options are recorded in Lean so the variant-selection child can be validated
repo-locally before a later serial integrator backfills public planning docs.
-/
inductive SkorokhodVariant where
  /-- Classical Brownian-motion embedding target. -/
  | brownianMotionEmbedding
  /-- Simple random-walk embedding target. -/
  | simpleRandomWalkEmbedding
  /-- Reduced finite-state discrete embedding target. -/
  | finiteStateDiscreteEmbedding
  /-- Martingale-difference embedding target. -/
  | martingaleDifferenceEmbedding
deriving DecidableEq

/--
Chosen first target for this Stage1 line: a finite-state discrete embedding.

This is the lowest-risk repo-local branch because the current artifact already
uses discrete time, stopping times, stopped values, laws, integrability, and
independence interfaces available in pinned mathlib, while the terminal
Brownian-motion Skorokhod theorem remains absent from the local dependency
closure.
-/
def selectedFirstVariant : SkorokhodVariant :=
  SkorokhodVariant.finiteStateDiscreteEmbedding

/-- Checked selector equation for the variant-selection child task. -/
theorem selectedFirstVariant_eq_finiteStateDiscrete :
    selectedFirstVariant = SkorokhodVariant.finiteStateDiscreteEmbedding :=
  rfl

/-- Brownian-motion embedding is deferred until a Brownian API or upstream proof is pinned. -/
theorem selectedFirstVariant_ne_brownian :
    selectedFirstVariant ≠ SkorokhodVariant.brownianMotionEmbedding := by
  decide

/-- Simple random-walk embedding is not the first target chosen by this child. -/
theorem selectedFirstVariant_ne_simpleRandomWalk :
    selectedFirstVariant ≠ SkorokhodVariant.simpleRandomWalkEmbedding := by
  decide

/-- Martingale-difference embedding is deferred until the discrete law package is concretized. -/
theorem selectedFirstVariant_ne_martingaleDifference :
    selectedFirstVariant ≠ SkorokhodVariant.martingaleDifferenceEmbedding := by
  decide

/-- Human-readable rationale strings retained in the checked artifact. -/
def selectedFirstVariantRationale : List String := [
  "first target: finite-state discrete embedding",
  "reason: matches the existing discrete-time SkorokhodEmbeddingData boundary",
  "reason: uses repo-local checked anchors for Filtration, IsStoppingTime, stoppedValue, HasLaw, Integrable, and independence interfaces",
  "non-claim: this does not prove the terminal Skorokhod embedding theorem",
  "deferred: Brownian-motion embedding, simple random-walk embedding, and martingale-difference embedding"
]

/-- Variants intentionally left for later child tasks. -/
def deferredVariants : List SkorokhodVariant := [
  SkorokhodVariant.brownianMotionEmbedding,
  SkorokhodVariant.simpleRandomWalkEmbedding,
  SkorokhodVariant.martingaleDifferenceEmbedding
]

/--
Boundary data for a future discrete-time Skorokhod embedding theorem.

The process `randomWalk` is the source random walk to be represented by stopped
values of `drivingProcess`.  The selected first variant is finite-state and
discrete-time, so its source-law, centering, integrability, finite-range, and
probability-space assumptions are stated below as a concrete package rather
than as an opaque embedding proposition.
-/
structure SkorokhodEmbeddingData (Ω : Type uΩ) [MeasurableSpace Ω]
    (P : Measure Ω) : Type (max uΩ 1) where
  randomWalk : ℕ → Ω → ℝ
  drivingProcess : ℕ → Ω → ℝ
  filtration : Filtration ℕ (inferInstance : MeasurableSpace Ω)
  stoppingTimes : ℕ → Ω → WithTop ℕ
  targetLaw : ℕ → Measure ℝ
  finiteExpectationHypotheses : Prop
  independenceHypotheses : Prop
  convergenceBridgeHypotheses : Prop

/--
Concrete hypothesis package for the selected finite-state discrete variant.

This replaces the former opaque `SkorokhodEmbeddingData.embeddingHypotheses`
field with explicit repo-local assumptions: the source measure is a probability
measure, each declared target law is a probability measure, each random-walk
coordinate has the declared law, each coordinate is centered and integrable, and
the random-walk coordinate range is finite.
-/
structure FiniteStateDiscreteEmbeddingAssumptions {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SkorokhodEmbeddingData Ω P) : Prop where
  source_probability : IsProbabilityMeasure P
  target_law_probability : ∀ n, IsProbabilityMeasure (D.targetLaw n)
  random_walk_law : ∀ n, HasLaw (D.randomWalk n) (D.targetLaw n) P
  random_walk_centered : ∀ n, ∫ ω, D.randomWalk n ω ∂P = 0
  random_walk_integrable : ∀ n, Integrable (D.randomWalk n) P
  random_walk_finite_range : ∀ n, (Set.range (D.randomWalk n)).Finite

/--
Conclusion package expected from a completed Skorokhod embedding formalization.

This intentionally states only the theorem boundary.  A later proof must replace
the remaining abstract moment, independence, and convergence fields with
canonical assumptions, then prove the stopped-value law and related
integrability and independence interfaces.
-/
structure SkorokhodEmbeddingConclusion {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SkorokhodEmbeddingData Ω P) : Prop where
  stopping_time : ∀ n, IsStoppingTime D.filtration (D.stoppingTimes n)
  random_walk_law : ∀ n, HasLaw (D.randomWalk n) (D.targetLaw n) P
  stopped_value_law :
    ∀ n, HasLaw (stoppedValue D.drivingProcess (D.stoppingTimes n)) (D.targetLaw n) P
  stopped_value_integrability : ∀ n, Integrable (stoppedValue D.drivingProcess (D.stoppingTimes n)) P
  finite_moment_control : D.finiteExpectationHypotheses
  independence_interface : D.independenceHypotheses
  convergence_bridge : D.convergenceBridgeHypotheses

/--
Checked stopped-value integrability package for the selected finite-state
discrete branch.

The package isolates the exact assumptions under which mathlib's stopped-value
and stopped-process integrability lemmas apply: coordinatewise integrability of
the driving process, genuine stopping-time proofs, and deterministic upper
bounds for each candidate stop.  It is intentionally not a Skorokhod proof; it
is the repo-local API bridge needed before a later proof can populate the
`SkorokhodEmbeddingConclusion.stopped_value_integrability` field.
-/
structure StoppedValueIntegrabilityAssumptions {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SkorokhodEmbeddingData Ω P) : Prop where
  driving_integrable : ∀ n, Integrable (D.drivingProcess n) P
  stopping_time : ∀ n, IsStoppingTime D.filtration (D.stoppingTimes n)
  bounded_stopping_time : ∀ n, ∃ N : ℕ, ∀ ω, D.stoppingTimes n ω ≤ N

/--
Checked stopping-time construction package for the selected discrete branch.

The package records the exact mathlib route expected for the future
Skorokhod stopping times: an adapted driving process hits measurable target
sets after deterministic starting times, and `hittingAfter` supplies the
candidate stopping times.
-/
structure HittingAfterStoppingConstruction {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} (D : SkorokhodEmbeddingData Ω P) : Type (max uΩ 1) where
  hitSet : ℕ → Set ℝ
  startTime : ℕ → ℕ
  driving_adapted : Adapted D.filtration D.drivingProcess
  hitSet_measurable : ∀ n, MeasurableSet (hitSet n)
  stoppingTimes_eq_hittingAfter :
    ∀ n, D.stoppingTimes n = hittingAfter D.drivingProcess (hitSet n) (startTime n)

/--
Stage1 normalized statement shape for the Skorokhod embedding slot.

The statement is deliberately not proved here.  It freezes explicit universe,
probability-space, filtration, stopping-time, law, integrability, independence,
and convergence-boundary parameters for a later terminal formalization.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) [MeasurableSpace Ω] (P : Measure Ω),
    ∀ D : SkorokhodEmbeddingData Ω P,
      FiniteStateDiscreteEmbeddingAssumptions D →
        D.finiteExpectationHypotheses →
          D.independenceHypotheses →
            D.convergenceBridgeHypotheses →
              SkorokhodEmbeddingConclusion D

/-- Project the explicit probability-space assumption for the selected finite-state variant. -/
theorem finiteStateDiscrete_source_probability {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : FiniteStateDiscreteEmbeddingAssumptions D) :
    IsProbabilityMeasure P :=
  h.source_probability

/-- Project the explicit target-law probability assumption for the selected finite-state variant. -/
theorem finiteStateDiscrete_target_law_probability {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : FiniteStateDiscreteEmbeddingAssumptions D) :
    ∀ n, IsProbabilityMeasure (D.targetLaw n) :=
  h.target_law_probability

/-- Project the explicit random-walk law assumption for the selected finite-state variant. -/
theorem finiteStateDiscrete_random_walk_law {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : FiniteStateDiscreteEmbeddingAssumptions D) :
    ∀ n, HasLaw (D.randomWalk n) (D.targetLaw n) P :=
  h.random_walk_law

/--
Convert the selected finite-state source-law assumption into the underlying
push-forward identity used by downstream map/law lemmas.
-/
theorem finiteStateDiscrete_random_walk_map_eq {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : FiniteStateDiscreteEmbeddingAssumptions D) :
    ∀ n, P.map (D.randomWalk n) = D.targetLaw n :=
  fun n => (h.random_walk_law n).map_eq

/-- Project the explicit centering assumption for the selected finite-state variant. -/
theorem finiteStateDiscrete_random_walk_centered {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : FiniteStateDiscreteEmbeddingAssumptions D) :
    ∀ n, ∫ ω, D.randomWalk n ω ∂P = 0 :=
  h.random_walk_centered

/-- Project the explicit integrability assumption for the selected finite-state variant. -/
theorem finiteStateDiscrete_random_walk_integrable {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : FiniteStateDiscreteEmbeddingAssumptions D) :
    ∀ n, Integrable (D.randomWalk n) P :=
  h.random_walk_integrable

/-- Project the explicit finite-range assumption for the selected finite-state variant. -/
theorem finiteStateDiscrete_random_walk_finite_range {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : FiniteStateDiscreteEmbeddingAssumptions D) :
    ∀ n, (Set.range (D.randomWalk n)).Finite :=
  h.random_walk_finite_range

/-- Project coordinatewise integrability for the driving process. -/
theorem stoppedValueIntegrability_driving_integrable {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : StoppedValueIntegrabilityAssumptions D) :
    ∀ n, Integrable (D.drivingProcess n) P :=
  h.driving_integrable

/-- Project the stopping-time proofs needed for stopped-value integrability. -/
theorem stoppedValueIntegrability_stopping_time {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : StoppedValueIntegrabilityAssumptions D) :
    ∀ n, IsStoppingTime D.filtration (D.stoppingTimes n) :=
  h.stopping_time

/-- Project deterministic upper bounds for the candidate stopping times. -/
theorem stoppedValueIntegrability_bounded_stopping_time {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : StoppedValueIntegrabilityAssumptions D) :
    ∀ n, ∃ N : ℕ, ∀ ω, D.stoppingTimes n ω ≤ N :=
  h.bounded_stopping_time

/--
Use mathlib's stopped-value integrability theorem to populate the
stopped-value integrability obligation for every bounded candidate stop.
-/
theorem stoppedValueIntegrability_stopped_value_integrable {Ω : Type uΩ}
    [MeasurableSpace Ω] {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : StoppedValueIntegrabilityAssumptions D) :
    ∀ n, Integrable (stoppedValue D.drivingProcess (D.stoppingTimes n)) P := by
  intro n
  obtain ⟨N, hN⟩ := h.bounded_stopping_time n
  exact integrable_stoppedValue ℕ (h.stopping_time n) h.driving_integrable hN

/--
Use mathlib's stopped-process integrability theorem for the whole process
stopped at each bounded Skorokhod candidate time.
-/
theorem stoppedValueIntegrability_stopped_process_integrable {Ω : Type uΩ}
    [MeasurableSpace Ω] {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : StoppedValueIntegrabilityAssumptions D) :
    ∀ k n, Integrable (stoppedProcess D.drivingProcess (D.stoppingTimes k) n) P := by
  intro k n
  exact integrable_stoppedProcess (h.stopping_time k) h.driving_integrable n

/-- Project the stopping-time obligation from the future conclusion package. -/
theorem conclusion_stopping_time {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SkorokhodEmbeddingData Ω P} (h : SkorokhodEmbeddingConclusion D) :
    ∀ n, IsStoppingTime D.filtration (D.stoppingTimes n) :=
  h.stopping_time

/-- Project the stopped-value law obligation from the future conclusion package. -/
theorem conclusion_stopped_value_law {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SkorokhodEmbeddingData Ω P} (h : SkorokhodEmbeddingConclusion D) :
    ∀ n, HasLaw (stoppedValue D.drivingProcess (D.stoppingTimes n)) (D.targetLaw n) P :=
  h.stopped_value_law

/-- Project the stopped-value integrability obligation from the future conclusion package. -/
theorem conclusion_stopped_value_integrability {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : SkorokhodEmbeddingConclusion D) :
    ∀ n, Integrable (stoppedValue D.drivingProcess (D.stoppingTimes n)) P :=
  h.stopped_value_integrability

/--
Convert the stopped-value law conclusion into the push-forward identity that
will be used to compare embedded terminal laws.
-/
theorem conclusion_stopped_value_map_eq {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    {D : SkorokhodEmbeddingData Ω P} (h : SkorokhodEmbeddingConclusion D) :
    ∀ n, P.map (stoppedValue D.drivingProcess (D.stoppingTimes n)) = D.targetLaw n :=
  fun n => (h.stopped_value_law n).map_eq

/--
The checked construction package yields the stopping-time obligation expected
by the future Skorokhod conclusion.
-/
theorem hittingAfterConstruction_stopping_time {Ω : Type uΩ} [MeasurableSpace Ω]
    {P : Measure Ω} {D : SkorokhodEmbeddingData Ω P}
    (h : HittingAfterStoppingConstruction D) :
    ∀ n, IsStoppingTime D.filtration (D.stoppingTimes n) := by
  intro n
  rw [h.stoppingTimes_eq_hittingAfter n]
  exact h.driving_adapted.isStoppingTime_hittingAfter (h.hitSet_measurable n)

section MathlibAnchors

variable {Ω : Type uΩ} [MeasurableSpace Ω]

/-- Checked mathlib wrapper: deterministic times are stopping times. -/
theorem const_stopping_time_wrapper
    (ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)) (n : ℕ) :
    IsStoppingTime ℱ (fun _ : Ω => (n : WithTop ℕ)) :=
  isStoppingTime_const ℱ n

omit [MeasurableSpace Ω] in
/-- Checked mathlib wrapper: stopping at a deterministic time returns that process value. -/
theorem stoppedValue_const_wrapper {β : Type uβ} (u : ℕ → Ω → β) (n : ℕ) :
    stoppedValue u (fun _ : Ω => (n : WithTop ℕ)) = u n :=
  stoppedValue_const u n

omit [MeasurableSpace Ω] in
/-- Checked mathlib wrapper: hitting the empty set after time `n` is the infinite time. -/
theorem hittingAfter_empty_wrapper {β : Type uβ} (u : ℕ → Ω → β) (n : ℕ) :
    hittingAfter u (∅ : Set β) n = fun _ : Ω => (⊤ : WithTop ℕ) :=
  hittingAfter_empty (u := u) n

omit [MeasurableSpace Ω] in
/-- Checked mathlib wrapper: hitting the whole state space after `n` returns `n`. -/
theorem hittingAfter_univ_wrapper {β : Type uβ} (u : ℕ → Ω → β) (n : ℕ) :
    hittingAfter u (Set.univ : Set β) n = fun _ : Ω => (n : WithTop ℕ) :=
  hittingAfter_univ (u := u) n

omit [MeasurableSpace Ω] in
/-- Checked mathlib wrapper: `hittingAfter` is always after its declared start time. -/
theorem le_hittingAfter_wrapper {β : Type uβ} {u : ℕ → Ω → β} {s : Set β}
    {n : ℕ} (ω : Ω) :
    (n : WithTop ℕ) ≤ hittingAfter u s n ω :=
  le_hittingAfter (u := u) (s := s) (n := n) ω

omit [MeasurableSpace Ω] in
/-- Checked mathlib wrapper: a witnessed hit gives an upper bound on `hittingAfter`. -/
theorem hittingAfter_le_of_mem_wrapper {β : Type uβ} {u : ℕ → Ω → β} {s : Set β}
    {n i : ℕ} {ω : Ω} (hin : n ≤ i) (his : u i ω ∈ s) :
    hittingAfter u s n ω ≤ i :=
  hittingAfter_le_of_mem (u := u) (s := s) hin his

/--
Checked mathlib wrapper: hitting a measurable set after a deterministic time is
a stopping time for an adapted discrete process.
-/
theorem adapted_hittingAfter_isStoppingTime_wrapper {β : Type uβ} [MeasurableSpace β]
    (ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)) {u : ℕ → Ω → β}
    {s : Set β} {n : ℕ} (hu : Adapted ℱ u) (hs : MeasurableSet s) :
    IsStoppingTime ℱ (hittingAfter u s n) :=
  hu.isStoppingTime_hittingAfter hs

/--
Checked mathlib wrapper: the event that an adapted process has hit by level
`i` is measurable in the `i`th σ-algebra of the filtration.
-/
theorem adapted_hittingAfter_measurableSet_le_wrapper {β : Type uβ} [MeasurableSpace β]
    (ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)) {u : ℕ → Ω → β}
    {s : Set β} {n i : ℕ} (hu : Adapted ℱ u) (hs : MeasurableSet s) :
    MeasurableSet[ℱ i] {ω | hittingAfter u s n ω ≤ i} :=
  (adapted_hittingAfter_isStoppingTime_wrapper ℱ hu hs).measurableSet_le i

omit [MeasurableSpace Ω] in
/-- Checked mathlib wrapper: stopped processes agree with the original process before stopping. -/
theorem stoppedProcess_eq_of_le_wrapper {β : Type uβ} {u : ℕ → Ω → β}
    {τ : Ω → WithTop ℕ} {n : ℕ} {ω : Ω} (h : (n : WithTop ℕ) ≤ τ ω) :
    stoppedProcess u τ n ω = u n ω :=
  stoppedProcess_eq_of_le (u := u) (τ := τ) h

/-- Checked mathlib wrapper: the identity random variable has its source measure as its law. -/
theorem hasLaw_id_wrapper {X : Type uβ} [MeasurableSpace X] (μ : Measure X) :
    HasLaw (id : X → X) μ μ :=
  HasLaw.id

/-- Checked mathlib wrapper: a law records the associated push-forward equality. -/
theorem hasLaw_map_eq_wrapper {X : Type uβ} [MeasurableSpace X]
    {μ : Measure X} {P : Measure Ω} {f : Ω → X} (h : HasLaw f μ P) :
    P.map f = μ :=
  h.map_eq

/-- Checked mathlib wrapper: a law records ae-measurability of the random variable. -/
theorem hasLaw_aemeasurable_wrapper {X : Type uβ} [MeasurableSpace X]
    {μ : Measure X} {P : Measure Ω} {f : Ω → X} (h : HasLaw f μ P) :
    AEMeasurable f P :=
  h.aemeasurable

/-- Checked mathlib wrapper: an ae-measurable map has its own push-forward as its law. -/
theorem hasLaw_map_self_wrapper {X : Type uβ} [MeasurableSpace X]
    {P : Measure Ω} {f : Ω → X} (hf : AEMeasurable f P) :
    HasLaw f (P.map f) P where
  aemeasurable := hf
  map_eq := rfl

/-- Checked mathlib wrapper: measure-preserving maps induce `HasLaw`. -/
theorem measurePreserving_hasLaw_wrapper {X Y : Type uβ} [MeasurableSpace X]
    [MeasurableSpace Y] {μ : Measure X} {ν : Measure Y} {f : X → Y}
    (h : MeasurePreserving f μ ν) :
    HasLaw f ν μ :=
  h.hasLaw

/-- Checked mathlib wrapper: a measurable `HasLaw` map is measure-preserving. -/
theorem hasLaw_measurePreserving_wrapper {X : Type uβ} [MeasurableSpace X]
    {μ : Measure X} {P : Measure Ω} {f : Ω → X} (h : HasLaw f μ P)
    (hf : Measurable f) :
    MeasurePreserving f P μ :=
  h.measurePreserving hf

/-- Checked mathlib wrapper: compose a law with another law on the intermediate law space. -/
theorem hasLaw_comp_wrapper {X Y : Type uβ} [MeasurableSpace X] [MeasurableSpace Y]
    {μ : Measure X} {ν : Measure Y} {P : Measure Ω} {f : Ω → X} {g : X → Y}
    (hg : HasLaw g ν μ) (hf : HasLaw f μ P) :
    HasLaw (g ∘ f) ν P :=
  hg.comp hf

/--
Checked map/push-forward wrapper: composing a random variable with an
ae-measurable map gives the mapped law.
-/
theorem hasLaw_comp_map_wrapper {X Y : Type uβ} [MeasurableSpace X] [MeasurableSpace Y]
    {μ : Measure X} {P : Measure Ω} {f : Ω → X} {g : X → Y}
    (hf : HasLaw f μ P) (hg : AEMeasurable g μ) :
    HasLaw (g ∘ f) (μ.map g) P :=
  (hasLaw_map_self_wrapper (Ω := X) (P := μ) (f := g) hg).comp hf

/--
Checked map/push-forward wrapper: a measure-preserving map out of the
intermediate law transports the law of a random variable.
-/
theorem hasLaw_comp_of_measurePreserving_wrapper {X Y : Type uβ}
    [MeasurableSpace X] [MeasurableSpace Y] {μ : Measure X} {ν : Measure Y}
    {P : Measure Ω} {f : Ω → X} {g : X → Y} (hf : HasLaw f μ P)
    (hg : MeasurePreserving g μ ν) :
    HasLaw (g ∘ f) ν P :=
  hg.hasLaw.comp hf

/-- Checked mathlib wrapper: measurable push-forwards compose by function composition. -/
theorem measure_map_map_wrapper {X Y : Type uβ} [MeasurableSpace X] [MeasurableSpace Y]
    {μ : Measure Ω} {f : Ω → X} {g : X → Y} (hf : Measurable f) (hg : Measurable g) :
    (μ.map f).map g = μ.map (g ∘ f) :=
  Measure.map_map hg hf

/--
Checked mathlib wrapper: finite-dimensional deterministic stopped values inherit the law supplied
by a measure-preserving map.
-/
theorem deterministic_stoppedValue_hasLaw_of_measurePreserving {X : Type uβ}
    [MeasurableSpace X] {μ : Measure Ω} {ν : Measure X} {u : ℕ → Ω → X} {n : ℕ}
    (h : MeasurePreserving (u n) μ ν) :
    HasLaw (stoppedValue u (fun _ : Ω => (n : WithTop ℕ))) ν μ := by
  rw [stoppedValue_const_wrapper u n]
  exact h.hasLaw

/--
Checked law wrapper: deterministic stopped values inherit an already established
law for the deterministic process coordinate.
-/
theorem deterministic_stoppedValue_hasLaw_of_hasLaw {X : Type uβ}
    [MeasurableSpace X] {μ : Measure Ω} {ν : Measure X} {u : ℕ → Ω → X} {n : ℕ}
    (h : HasLaw (u n) ν μ) :
    HasLaw (stoppedValue u (fun _ : Ω => (n : WithTop ℕ))) ν μ := by
  rw [stoppedValue_const_wrapper u n]
  exact h

/--
Checked mathlib wrapper: a stopped value at a bounded stopping time is
integrable when all deterministic process coordinates are integrable.
-/
theorem integrable_stoppedValue_wrapper {μ : Measure Ω}
    {ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)}
    {u : ℕ → Ω → ℝ} {τ : Ω → WithTop ℕ}
    (hτ : IsStoppingTime ℱ τ) (hu : ∀ n, Integrable (u n) μ)
    {N : ℕ} (hbdd : ∀ ω, τ ω ≤ N) :
    Integrable (stoppedValue u τ) μ :=
  integrable_stoppedValue ℕ hτ hu hbdd

/--
Checked mathlib wrapper: every coordinate of the process stopped at a stopping
time is integrable when the original process is coordinatewise integrable.
-/
theorem integrable_stoppedProcess_wrapper {μ : Measure Ω}
    {ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)}
    {u : ℕ → Ω → ℝ} {τ : Ω → WithTop ℕ}
    (hτ : IsStoppingTime ℱ τ) (hu : ∀ n, Integrable (u n) μ) (n : ℕ) :
    Integrable (stoppedProcess u τ n) μ :=
  integrable_stoppedProcess hτ hu n

/--
Checked martingale API wrapper: a submartingale supplies integrability of its
bounded stopped value through the optional-stopping substrate.
-/
theorem submartingale_integrable_stoppedValue_wrapper {μ : Measure Ω}
    {ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)}
    {f : ℕ → Ω → ℝ} (hf : Submartingale f ℱ μ) {τ : Ω → WithTop ℕ}
    (hτ : IsStoppingTime ℱ τ) {N : ℕ} (hbdd : ∀ ω, τ ω ≤ N) :
    Integrable (stoppedValue f τ) μ :=
  hf.integrable_stoppedValue hτ hbdd

/--
Checked optional-stopping wrapper: submartingale stopped values are monotone in
expectation for bounded ordered stopping times.
-/
theorem submartingale_expected_stoppedValue_mono_wrapper {μ : Measure Ω}
    {ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)}
    [SigmaFiniteFiltration μ ℱ] {f : ℕ → Ω → ℝ} (hf : Submartingale f ℱ μ)
    {τ π : Ω → WithTop ℕ} (hτ : IsStoppingTime ℱ τ) (hπ : IsStoppingTime ℱ π)
    (hle : τ ≤ π) {N : ℕ} (hbdd : ∀ ω, π ω ≤ N) :
    μ[stoppedValue f τ] ≤ μ[stoppedValue f π] :=
  hf.expected_stoppedValue_mono hτ hπ hle hbdd

/--
Checked optional-stopping wrapper: stopping a submartingale at a stopping time
again gives a submartingale.
-/
theorem submartingale_stoppedProcess_wrapper {μ : Measure Ω}
    {ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)}
    [SigmaFiniteFiltration μ ℱ] {f : ℕ → Ω → ℝ} (hf : Submartingale f ℱ μ)
    {τ : Ω → WithTop ℕ} (hτ : IsStoppingTime ℱ τ) :
    Submartingale (stoppedProcess f τ) ℱ μ :=
  hf.stoppedProcess hτ

/-- Mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.InfinitePi",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.HittingTime",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Kernel.IonescuTulcea.Traj",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.SigmaFiniteFiltration",
  "MeasureTheory.Adapted",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.ProgMeasurable",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.isStoppingTime_const",
  "MeasureTheory.stoppedValue",
  "MeasureTheory.stoppedValue_const",
  "MeasureTheory.stoppedProcess",
  "MeasureTheory.stoppedProcess_eq_of_le",
  "MeasureTheory.integrable_stoppedValue",
  "MeasureTheory.integrable_stoppedProcess",
  "MeasureTheory.hittingAfter",
  "MeasureTheory.hittingAfter_empty",
  "MeasureTheory.Adapted.isStoppingTime_hittingAfter",
  "MeasureTheory.Submartingale.integrable_stoppedValue",
  "MeasureTheory.Submartingale.stoppedProcess",
  "MeasureTheory.Submartingale.expected_stoppedValue_mono",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.HasLaw.id",
  "ProbabilityTheory.HasLaw.map_eq",
  "ProbabilityTheory.HasLaw.aemeasurable",
  "ProbabilityTheory.HasLaw.comp",
  "MeasureTheory.MeasurePreserving.hasLaw",
  "ProbabilityTheory.HasLaw.measurePreserving",
  "MeasureTheory.Measure.map_map",
  "MeasureTheory.AEMeasurable.map_map_of_aemeasurable",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.iIndepFun_iff_map_fun_eq_infinitePi_map"
]

/--
Search terms that did not locate a terminal Skorokhod embedding theorem in the
local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Skorokhod",
  "Skorokhod embedding",
  "SkorokhodEmbedding",
  "random walk embedding",
  "Brownian embedding",
  "BrownianMotion",
  "Root embedding",
  "Azema Yor embedding",
  "Monroe embedding"
]

/-! ## External Lean 4 audit -/

/--
Primary-source external Lean 4 audit row for Skorokhod/Brownian embedding
projects.

This is metadata only. A row is not completion evidence unless the cited
theorem is pinned/imported/checked inside this repository's Lake closure.
-/
structure ExternalLeanAuditRow where
  repositoryUrl : String
  commit : String
  auditedTerms : List String
  relevantModules : List String
  relevantTheoremNames : List String
  terminalSkorokhodEmbeddingFound : Bool
  repoLocalImportChecked : Bool
  integrationBlocker : String

/--
Primary-source audit of `RemyDegenne/brownian-motion` for the Skorokhod
embedding child task.

The repository contains substantial Brownian-motion infrastructure, including a
canonical `ProbabilityTheory.IsBrownian` predicate and the concrete Brownian
construction theorem `ProbabilityTheory.IsBrownian_brownian`.  The audited
source tree did not contain a terminal Skorokhod embedding theorem or a
`SkorokhodEmbedding` declaration, so this is relevant Brownian infrastructure
only, not a proof of this Stage1 theorem.
-/
def remyDegenneBrownianMotionSkorokhodAudit : ExternalLeanAuditRow where
  repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
  commit := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
  auditedTerms := [
    "Skorokhod",
    "SkorokhodEmbedding",
    "Skorokhod embedding",
    "BrownianMotion",
    "IsBrownian",
    "Root embedding",
    "Azema Yor embedding",
    "Monroe embedding"
  ]
  relevantModules := [
    "BrownianMotion.Gaussian.BrownianMotion",
    "BrownianMotion.Continuity.KolmogorovChentsov",
    "BrownianMotion.StochasticIntegral.OptionalSampling",
    "BrownianMotion.StochasticIntegral.QuadraticVariation"
  ]
  relevantTheoremNames := [
    "ProbabilityTheory.IsBrownian",
    "ProbabilityTheory.IsBrownian_brownian",
    "ProbabilityTheory.isGaussianProcess_brownian",
    "ProbabilityTheory.hasLaw_brownian_eval",
    "ProbabilityTheory.hasLaw_brownian_sub",
    "ProbabilityTheory.hasIndepIncrements_brownian",
    "ProbabilityTheory.IsPreBrownian.isMartingale"
  ]
  terminalSkorokhodEmbeddingFound := false
  repoLocalImportChecked := false
  integrationBlocker :=
    "No terminal Skorokhod embedding theorem was found in the audited Brownian source tree. The Brownian project is also not importable in this repository's current Lake closure: it uses leanprover/lean4:v4.30.0-rc1 with mathlib f23306121184717ace04f3ac514be974e3224c8b, while this repository uses leanprover/lean4:v4.29.0. A repo-local probe of `import BrownianMotion.Gaussian.BrownianMotion` failed with unknown module prefix `BrownianMotion`."

/-- External Lean 4 audit rows found for this Stage1 slot. -/
def externalLeanAuditRows : List ExternalLeanAuditRow := [
  remyDegenneBrownianMotionSkorokhodAudit
]

/-- The external audit did not find a terminal Lean 4 Skorokhod embedding theorem. -/
def externalAuditFoundTerminalSkorokhodEmbedding : Bool :=
  false

/-- Anchor-only Brownian infrastructure is not repo-local completion evidence. -/
def externalAuditAnchorOnlyEvidenceIsCompletion : Bool :=
  false

/-- Sanity check for the external-audit completion gate. -/
theorem externalAuditFoundTerminalSkorokhodEmbedding_eq_false :
    externalAuditFoundTerminalSkorokhodEmbedding = false :=
  rfl

/-- Sanity check that anchor-only external evidence is not treated as completion. -/
theorem externalAuditAnchorOnlyEvidenceIsCompletion_eq_false :
    externalAuditAnchorOnlyEvidenceIsCompletion = false :=
  rfl

end MathlibAnchors

end AwesomeTheorems.Stage1.S1_M_220
