import Mathlib.Probability.Kernel.Invariance
import Mathlib.Probability.Kernel.Integral
import Mathlib.Probability.Kernel.Composition.IntegralCompProd
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.MeasureTheory.Integral.BoundedContinuousFunction
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric
import Mathlib.MeasureTheory.Measure.Prokhorov
import Mathlib.MeasureTheory.Measure.Tight
import Mathlib.Topology.Compactness.Compact
import Mathlib.Topology.ContinuousMap.Bounded.Basic

/-!
# S1-M-219 / THM-M-1052: Krylov-Bogolyubov theorem

This Stage1 artifact records a conservative Lean 4 statement-shape boundary for
the Krylov-Bogolyubov invariant-measure theorem.

The pinned mathlib snapshot has Markov kernels, kernel composition with
measures, probability measures, weak-convergence topology on probability
measures, Levy-Prokhorov infrastructure, tightness predicates, and the predicate
`ProbabilityTheory.Kernel.Invariant`.  This audit did not find a terminal
Krylov-Bogolyubov theorem proving existence of an invariant probability measure
for Feller Markov dynamics on compact spaces.

The declarations below therefore normalize the invariant-probability target and
the missing compactness/Feller/cluster-point proof packages without adding
proof placeholders.  The checked theorems are wrappers around available mathlib
facts or definitional statement-shape unfoldings.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped ENNReal ProbabilityTheory Topology BoundedContinuousFunction

namespace AwesomeTheorems.Stage1.S1_M_219

universe u

variable {Ω : Type u} [MeasurableSpace Ω]

/--
An invariant probability measure for a Markov kernel.

The invariant measure is stored as a `ProbabilityMeasure`; the invariant
property uses mathlib's kernel-invariance predicate
`ProbabilityTheory.Kernel.Invariant κ μ`, i.e. `μ.bind κ = μ`.
-/
structure InvariantProbability (κ : Kernel Ω Ω) : Type u where
  measure : ProbabilityMeasure Ω
  invariant : Kernel.Invariant κ (measure : Measure Ω)

/-- The invariant-probability field is available as a theorem wrapper. -/
theorem InvariantProbability.invariant_measure {κ : Kernel Ω Ω}
    (π : InvariantProbability κ) :
    Kernel.Invariant κ (π.measure : Measure Ω) :=
  π.invariant

/-- Invariance unfolds to equality after composing a measure with the kernel. -/
theorem invariant_comp_eq {κ : Kernel Ω Ω} {μ : Measure Ω}
    (h : Kernel.Invariant κ μ) :
    κ ∘ₘ μ = μ :=
  h.def

/-- Invariance gives equality on every measurable set. -/
theorem invariant_apply {κ : Kernel Ω Ω} {μ : Measure Ω}
    (h : Kernel.Invariant κ μ) {s : Set Ω} :
    (κ ∘ₘ μ) s = μ s := by
  rw [h.def]

/-- Mathlib proves that reversible Markov kernels have invariant measures. -/
theorem invariant_of_reversible {κ : Kernel Ω Ω} [IsMarkovKernel κ]
    {π : Measure Ω} (hπ : Kernel.IsReversible κ π) :
    Kernel.Invariant κ π :=
  hπ.invariant

/-- The identity kernel leaves every probability measure invariant. -/
theorem id_invariant (μ : ProbabilityMeasure Ω) :
    Kernel.Invariant (Kernel.id : Kernel Ω Ω) (μ : Measure Ω) := by
  rw [Kernel.Invariant]
  exact Measure.id_comp

/-- Any probability measure is an invariant probability for the identity kernel. -/
def invariantProbability_id (μ : ProbabilityMeasure Ω) :
    InvariantProbability (Kernel.id : Kernel Ω Ω) where
  measure := μ
  invariant := id_invariant μ

/-- Powers of a Markov kernel are Markov kernels. -/
theorem isMarkovKernel_pow (κ : Kernel Ω Ω) [IsMarkovKernel κ] (n : ℕ) :
    IsMarkovKernel (κ ^ n : Kernel Ω Ω) := by
  induction n with
  | zero =>
      change IsMarkovKernel (Kernel.id : Kernel Ω Ω)
      infer_instance
  | succ n hn =>
      rw [pow_succ]
      haveI : IsMarkovKernel (κ ^ n : Kernel Ω Ω) := hn
      exact Kernel.IsMarkovKernel.comp (η := (κ ^ n : Kernel Ω Ω)) (κ := κ)

/--
The `n`-step pushforward of a probability measure by a Markov kernel, as a raw
measure.
-/
def iteratedPushForwardMeasure (κ : Kernel Ω Ω) (μ : ProbabilityMeasure Ω) (n : ℕ) :
    Measure Ω :=
  (κ ^ n : Kernel Ω Ω) ∘ₘ (μ : Measure Ω)

/-- Every iterated Markov-kernel pushforward of a probability measure has mass one. -/
theorem iteratedPushForwardMeasure_univ (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) (n : ℕ) :
    iteratedPushForwardMeasure κ μ n Set.univ = 1 := by
  haveI : IsMarkovKernel (κ ^ n : Kernel Ω Ω) := isMarkovKernel_pow κ n
  simp [iteratedPushForwardMeasure]

/-- The `n`-step pushforward of a probability measure by a Markov kernel. -/
def iteratedPushForward (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) (n : ℕ) : ProbabilityMeasure Ω :=
  ⟨iteratedPushForwardMeasure κ μ n, ⟨iteratedPushForwardMeasure_univ κ μ n⟩⟩

/-- The underlying measure of the `n`-step pushforward is kernel composition. -/
theorem iteratedPushForward_toMeasure (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) (n : ℕ) :
    (iteratedPushForward κ μ n : Measure Ω) = iteratedPushForwardMeasure κ μ n :=
  rfl

/--
Cesaro empirical average of the first `n + 1` Markov iterates, as a raw measure.

The normalization by `n + 1` avoids an empty average and matches the usual
Krylov-Bogolyubov empirical-measure sequence
`(1 / (n + 1)) • ∑_{i=0}^{n} κ^i_* μ`.
-/
def cesaroEmpiricalAverageMeasure (κ : Kernel Ω Ω) (μ : ProbabilityMeasure Ω) (n : ℕ) :
    Measure Ω :=
  ((n + 1 : ℕ) : ℝ≥0∞)⁻¹ •
    ∑ i ∈ Finset.range (n + 1), iteratedPushForwardMeasure κ μ i

/-- The raw Cesaro empirical average has total mass one. -/
theorem cesaroEmpiricalAverageMeasure_univ (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) (n : ℕ) :
    cesaroEmpiricalAverageMeasure κ μ n Set.univ = 1 := by
  simp [cesaroEmpiricalAverageMeasure, iteratedPushForwardMeasure_univ]
  exact ENNReal.inv_mul_cancel (by simp) (by simp)

/-- The raw Cesaro empirical average is a probability measure. -/
theorem cesaroEmpiricalAverageMeasure_isProbabilityMeasure
    (κ : Kernel Ω Ω) [IsMarkovKernel κ] (μ : ProbabilityMeasure Ω) (n : ℕ) :
    IsProbabilityMeasure (cesaroEmpiricalAverageMeasure κ μ n) :=
  ⟨cesaroEmpiricalAverageMeasure_univ κ μ n⟩

/-- Cesaro empirical average of the first `n + 1` Markov iterates. -/
def cesaroEmpiricalAverage (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) (n : ℕ) : ProbabilityMeasure Ω :=
  ⟨cesaroEmpiricalAverageMeasure κ μ n,
    cesaroEmpiricalAverageMeasure_isProbabilityMeasure κ μ n⟩

/-- The underlying measure of the Cesaro average is the normalized finite sum of iterates. -/
theorem cesaroEmpiricalAverage_toMeasure (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) (n : ℕ) :
    (cesaroEmpiricalAverage κ μ n : Measure Ω) =
      cesaroEmpiricalAverageMeasure κ μ n :=
  rfl

/-- Pushing an iterated law forward once shifts the Markov-iterate index. -/
theorem kernel_comp_iteratedPushForwardMeasure (κ : Kernel Ω Ω)
    (μ : ProbabilityMeasure Ω) (n : ℕ) :
    κ ∘ₘ iteratedPushForwardMeasure κ μ n =
      iteratedPushForwardMeasure κ μ (n + 1) := by
  rw [iteratedPushForwardMeasure, iteratedPushForwardMeasure, Measure.comp_assoc]
  change (κ * (κ ^ n : Kernel Ω Ω)) ∘ₘ (μ : Measure Ω) =
    (κ ^ (n + 1) : Kernel Ω Ω) ∘ₘ (μ : Measure Ω)
  rw [pow_succ']

/-- Pushing forward a finite sum of iterated laws shifts every summand. -/
theorem kernel_comp_finset_sum_iteratedPushForwardMeasure (κ : Kernel Ω Ω)
    (μ : ProbabilityMeasure Ω) (s : Finset ℕ) :
    κ ∘ₘ (∑ i ∈ s, iteratedPushForwardMeasure κ μ i) =
      ∑ i ∈ s, iteratedPushForwardMeasure κ μ (i + 1) := by
  ext t ht
  rw [Measure.bind_apply ht κ.aemeasurable]
  rw [Measure.finset_sum_apply]
  rw [lintegral_finset_sum_measure]
  simp_rw [← Measure.bind_apply ht κ.aemeasurable]
  simp_rw [kernel_comp_iteratedPushForwardMeasure]

/--
The kernel pushforward of a Cesaro average is the normalized shifted finite sum
of Markov iterates.

This is the algebraic core of the Cesaro-shift argument.  The remaining
vanishing step is analytic: compare this shifted finite sum with the original
Cesaro sum against bounded continuous tests and show that the two boundary
terms disappear as `n → ∞`.
-/
theorem kernel_comp_cesaroEmpiricalAverageMeasure_shiftedSum
    (κ : Kernel Ω Ω) (μ : ProbabilityMeasure Ω) (n : ℕ) :
    κ ∘ₘ cesaroEmpiricalAverageMeasure κ μ n =
      ((n + 1 : ℕ) : ℝ≥0∞)⁻¹ •
        ∑ i ∈ Finset.range (n + 1), iteratedPushForwardMeasure κ μ (i + 1) := by
  rw [cesaroEmpiricalAverageMeasure]
  change ((((n + 1 : ℕ) : ℝ≥0∞)⁻¹ •
      ∑ i ∈ Finset.range (n + 1), iteratedPushForwardMeasure κ μ i) : Measure Ω).bind κ =
      ((n + 1 : ℕ) : ℝ≥0∞)⁻¹ •
        ∑ i ∈ Finset.range (n + 1), iteratedPushForwardMeasure κ μ (i + 1)
  rw [Measure.bind_smul]
  rw [← show κ ∘ₘ (∑ i ∈ Finset.range (n + 1), iteratedPushForwardMeasure κ μ i) =
    (∑ i ∈ Finset.range (n + 1), iteratedPushForwardMeasure κ μ i).bind κ from rfl]
  rw [kernel_comp_finset_sum_iteratedPushForwardMeasure]

/-- The pushforward of a probability measure by a Markov kernel as a probability measure. -/
def kernelPushForwardProbability (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) : ProbabilityMeasure Ω :=
  ⟨κ ∘ₘ (μ : Measure Ω), by
    constructor
    simp⟩

/-- The underlying measure of a Markov-kernel pushforward probability. -/
theorem kernelPushForwardProbability_toMeasure (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) :
    (kernelPushForwardProbability κ μ : Measure Ω) = κ ∘ₘ (μ : Measure Ω) :=
  rfl

/-- The Markov operator associated to a kernel on bounded continuous real tests. -/
def markovOperator [TopologicalSpace Ω] (κ : Kernel Ω Ω) (f : Ω →ᵇ ℝ) (x : Ω) :
    ℝ :=
  ∫ y, f y ∂(κ x)

/--
Concrete bounded-continuous-test formulation of the Feller condition.

For every bounded continuous real-valued test function `f`, the Markov
operator `x ↦ ∫ f y ∂κ x` is represented by another bounded continuous test
function.
-/
def MarkovOperatorMapsBoundedContinuous [TopologicalSpace Ω] (κ : Kernel Ω Ω) :
    Prop :=
  ∀ f : Ω →ᵇ ℝ, ∃ g : Ω →ᵇ ℝ, ⇑g = markovOperator κ f

/--
Selected textbook Feller condition for this Stage1 slot.

This records the standard bounded-continuous-test version: a Markov kernel is
Feller when its Markov operator preserves bounded continuous test functions.
-/
def TextbookFellerCondition [TopologicalSpace Ω] (κ : Kernel Ω Ω) : Prop :=
  MarkovOperatorMapsBoundedContinuous κ

/-- The selected textbook Feller condition is exactly the Markov-operator one. -/
theorem markovOperatorMaps_iff_textbookFeller [TopologicalSpace Ω] (κ : Kernel Ω Ω) :
    MarkovOperatorMapsBoundedContinuous κ ↔ TextbookFellerCondition κ :=
  Iff.rfl

/--
Statement-shape predicate for the Feller property.

The former abstract `Prop` placeholder is now pinned to the concrete
bounded-continuous-test Markov-operator condition.  What remains open is the
larger Krylov-Bogolyubov proof using this condition, not this statement-shape
equivalence.
-/
structure FellerKernelShape [TopologicalSpace Ω] (κ : Kernel Ω Ω) : Type u where
  textbook_condition : TextbookFellerCondition κ

/-- A Feller shape exposes the selected textbook bounded-continuous-test condition. -/
theorem FellerKernelShape.textbookCondition [TopologicalSpace Ω] {κ : Kernel Ω Ω}
    (hκ : FellerKernelShape κ) :
    TextbookFellerCondition κ :=
  hκ.textbook_condition

/-- Bundling the selected textbook condition is equivalent to inhabiting `FellerKernelShape`. -/
theorem fellerKernelShape_nonempty_iff_textbookFeller [TopologicalSpace Ω]
    (κ : Kernel Ω Ω) :
    Nonempty (FellerKernelShape κ) ↔ TextbookFellerCondition κ := by
  constructor
  · rintro ⟨hκ⟩
    exact hκ.textbookCondition
  · intro hκ
    exact ⟨⟨hκ⟩⟩

/-- The identity kernel evaluates the Markov operator by substitution. -/
theorem markovOperator_id_apply [TopologicalSpace Ω] [MeasurableSingletonClass Ω]
    (f : Ω →ᵇ ℝ) (x : Ω) :
    markovOperator (Kernel.id : Kernel Ω Ω) f x = f x := by
  simp [markovOperator, Kernel.id]

/-- The identity kernel satisfies the selected textbook Feller condition. -/
theorem textbookFellerCondition_id [TopologicalSpace Ω] [MeasurableSingletonClass Ω] :
    TextbookFellerCondition (Kernel.id : Kernel Ω Ω) := by
  intro f
  refine ⟨f, ?_⟩
  funext x
  exact (markovOperator_id_apply f x).symm

/--
Coerce a set of probability measures to the corresponding set of ordinary
measures.

This is the shape expected by `MeasureTheory.IsTightMeasureSet`, while the
relative-compactness statement lives on `ProbabilityMeasure Ω`.
-/
def probabilityMeasureUnderlyingMeasureSet (S : Set (ProbabilityMeasure Ω)) :
    Set (Measure Ω) :=
  {m : Measure Ω | ∃ μ ∈ S, (μ : Measure Ω) = m}

/-- Membership in the underlying-measure set is exactly membership after coercion. -/
theorem mem_probabilityMeasureUnderlyingMeasureSet
    {S : Set (ProbabilityMeasure Ω)} {m : Measure Ω} :
    m ∈ probabilityMeasureUnderlyingMeasureSet S ↔
      ∃ μ ∈ S, (μ : Measure Ω) = m :=
  Iff.rfl

/--
Every family of probability measures is tight when the state space is compact.

This is the direct repo-local wrapper around
`MeasureTheory.IsTightMeasureSet.of_compactSpace` from the pinned
`Mathlib.MeasureTheory.Measure.Tight` API.
-/
theorem probabilityMeasureUnderlyingMeasureSet_tight_of_compactSpace
    [TopologicalSpace Ω] [CompactSpace Ω] (S : Set (ProbabilityMeasure Ω)) :
    IsTightMeasureSet (probabilityMeasureUnderlyingMeasureSet S) :=
  IsTightMeasureSet.of_compactSpace

/--
On a compact Borel Hausdorff state space, the probability-measure space is
compact.

This wraps the pinned Prokhorov/Levy-Prokhorov compactness instance for
`ProbabilityMeasure Ω`.
-/
theorem compactSpace_probabilityMeasure_of_compactSpace
    [TopologicalSpace Ω] [T2Space Ω] [BorelSpace Ω] [CompactSpace Ω] :
    CompactSpace (ProbabilityMeasure Ω) :=
  inferInstance

/--
Tightness gives relative compactness of a set of probability measures.

The conclusion is phrased as compactness of `closure S`, the repo-local
relative-compactness shape used later to extract weak cluster points.
-/
theorem probabilityMeasureSet_closure_isCompact_of_tight
    [TopologicalSpace Ω] [T2Space Ω] [BorelSpace Ω]
    {S : Set (ProbabilityMeasure Ω)}
    (hS : IsTightMeasureSet (probabilityMeasureUnderlyingMeasureSet S)) :
    IsCompact (closure S) := by
  exact isCompact_closure_of_isTightMeasureSet (by simpa [probabilityMeasureUnderlyingMeasureSet] using hS)

/--
Compactness of the state space makes every set of probability measures
relatively compact.

This is the compactness-to-tightness-to-Prokhorov bridge needed by the
Krylov-Bogolyubov averaging argument.
-/
theorem probabilityMeasureSet_closure_isCompact_of_compactSpace
    [TopologicalSpace Ω] [T2Space Ω] [BorelSpace Ω] [CompactSpace Ω]
    (S : Set (ProbabilityMeasure Ω)) :
    IsCompact (closure S) :=
  probabilityMeasureSet_closure_isCompact_of_tight
    (probabilityMeasureUnderlyingMeasureSet_tight_of_compactSpace S)

/-- The Cesaro empirical averages generated from a Markov kernel and an initial law. -/
def cesaroEmpiricalAveragesSet (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (μ : ProbabilityMeasure Ω) : Set (ProbabilityMeasure Ω) :=
  Set.range (cesaroEmpiricalAverage κ μ)

/-- Each Cesaro empirical average belongs to the empirical-average set. -/
theorem cesaroEmpiricalAverage_mem_averagesSet
    (κ : Kernel Ω Ω) [IsMarkovKernel κ] (μ : ProbabilityMeasure Ω) (n : ℕ) :
    cesaroEmpiricalAverage κ μ n ∈ cesaroEmpiricalAveragesSet κ μ :=
  ⟨n, rfl⟩

/-- On compact state spaces, the Cesaro empirical averages are tight. -/
theorem cesaroEmpiricalAveragesSet_tight_of_compactSpace
    [TopologicalSpace Ω] [CompactSpace Ω]
    (κ : Kernel Ω Ω) [IsMarkovKernel κ] (μ : ProbabilityMeasure Ω) :
    IsTightMeasureSet
      (probabilityMeasureUnderlyingMeasureSet (cesaroEmpiricalAveragesSet κ μ)) :=
  probabilityMeasureUnderlyingMeasureSet_tight_of_compactSpace
    (cesaroEmpiricalAveragesSet κ μ)

/--
On compact Borel Hausdorff state spaces, the Cesaro empirical averages have
compact closure in `ProbabilityMeasure Ω`.
-/
theorem cesaroEmpiricalAveragesSet_closure_isCompact_of_compactSpace
    [TopologicalSpace Ω] [T2Space Ω] [BorelSpace Ω] [CompactSpace Ω]
    (κ : Kernel Ω Ω) [IsMarkovKernel κ] (μ : ProbabilityMeasure Ω) :
    IsCompact (closure (cesaroEmpiricalAveragesSet κ μ)) :=
  probabilityMeasureSet_closure_isCompact_of_compactSpace
    (cesaroEmpiricalAveragesSet κ μ)

/--
A weak cluster point of the Cesaro empirical averages.

The cluster-point condition is phrased using the topology on
`ProbabilityMeasure Ω`; in the pinned Levy-Prokhorov/Prokhorov API this is the
weak-convergence topology on probability measures.
-/
def WeakClusterPointOfEmpiricalAverages [TopologicalSpace Ω]
    [T2Space Ω] [BorelSpace Ω]
    (κ : Kernel Ω Ω) [IsMarkovKernel κ] (μ ν : ProbabilityMeasure Ω) : Prop :=
  ν ∈ closure (cesaroEmpiricalAveragesSet κ μ) ∧
    MapClusterPt ν Filter.atTop (cesaroEmpiricalAverage κ μ)

/--
Any sequence whose range has compact closure has a cluster point along `atTop`.

This is the topological extraction wrapper used for the empirical-average
sequence.  It deliberately stops at `MapClusterPt`; extracting an explicit
convergent subsequence is a first-countability/metric follow-up leaf, while the
Krylov-Bogolyubov invariance proof only needs a weak cluster point here.
-/
theorem exists_clusterPoint_of_compact_closure_range
    {X : Type u} [TopologicalSpace X] (u : ℕ → X)
    (hcompact : IsCompact (closure (Set.range u))) :
    ∃ x : X, x ∈ closure (Set.range u) ∧ MapClusterPt x Filter.atTop u := by
  have hmap :
      Filter.map u Filter.atTop ≤ Filter.principal (closure (Set.range u)) := by
    rw [Filter.le_principal_iff, Filter.mem_map]
    exact Filter.Eventually.of_forall fun n => subset_closure ⟨n, rfl⟩
  haveI : (Filter.map u Filter.atTop).NeBot :=
    Filter.NeBot.map (show (Filter.atTop : Filter ℕ).NeBot by infer_instance) u
  rcases hcompact.exists_clusterPt hmap with ⟨x, hx, hcluster⟩
  exact ⟨x, hx, mapClusterPt_def.mpr hcluster⟩

/--
On compact Borel Hausdorff state spaces, the Cesaro empirical averages have a
weak cluster point.
-/
theorem exists_weakClusterPointOfEmpiricalAverages_of_compactSpace
    [TopologicalSpace Ω] [T2Space Ω] [BorelSpace Ω] [CompactSpace Ω]
    (κ : Kernel Ω Ω) [IsMarkovKernel κ] (μ : ProbabilityMeasure Ω) :
    ∃ ν : ProbabilityMeasure Ω, WeakClusterPointOfEmpiricalAverages κ μ ν := by
  simpa [WeakClusterPointOfEmpiricalAverages, cesaroEmpiricalAveragesSet] using
    exists_clusterPoint_of_compact_closure_range
      (u := cesaroEmpiricalAverage κ μ)
      (cesaroEmpiricalAveragesSet_closure_isCompact_of_compactSpace κ μ)

/--
Weak convergence of probability measures, stated in the bounded-continuous-test
form used by the Feller bridge.
-/
def WeakConvergenceAgainstBoundedContinuous [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    {ι : Type*} (μs : ι → ProbabilityMeasure Ω) (l : Filter ι)
    (μ : ProbabilityMeasure Ω) : Prop :=
  ∀ f : Ω →ᵇ ℝ,
    Filter.Tendsto (fun i => ∫ x, f x ∂(μs i : Measure Ω)) l
      (𝓝 (∫ x, f x ∂(μ : Measure Ω)))

/--
The repo-local bounded-continuous-test statement is exactly the pinned mathlib
weak-convergence topology on `ProbabilityMeasure Ω`.
-/
theorem weakConvergenceAgainstBoundedContinuous_iff_tendsto
    [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    {ι : Type*} {μs : ι → ProbabilityMeasure Ω} {l : Filter ι}
    {μ : ProbabilityMeasure Ω} :
    WeakConvergenceAgainstBoundedContinuous μs l μ ↔ Filter.Tendsto μs l (𝓝 μ) := by
  rw [WeakConvergenceAgainstBoundedContinuous]
  exact (ProbabilityMeasure.tendsto_iff_forall_integral_tendsto).symm

/--
Feller weak-convergence bridge for the Markov operator.

For every weakly convergent net or sequence of probability measures, integrals
of the Markov-operator image of a bounded continuous test function pass to the
same weak limit.  This is the analytic bridge needed before the later
Cesaro-shift leaf identifies the cluster-point limit as invariant.
-/
def MarkovOperatorWeakConvergenceBridge [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    (κ : Kernel Ω Ω) : Prop :=
  ∀ {ι : Type*} (l : Filter ι) (μs : ι → ProbabilityMeasure Ω)
    (μ : ProbabilityMeasure Ω),
    Filter.Tendsto μs l (𝓝 μ) →
      ∀ f : Ω →ᵇ ℝ,
        Filter.Tendsto (fun i => ∫ x, markovOperator κ f x ∂(μs i : Measure Ω)) l
          (𝓝 (∫ x, markovOperator κ f x ∂(μ : Measure Ω)))

/--
The selected bounded-continuous-test Feller condition supplies the
weak-convergence bridge for the Markov operator.
-/
theorem markovOperatorWeakConvergenceBridge_of_mapsBoundedContinuous
    [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    {κ : Kernel Ω Ω} (hκ : MarkovOperatorMapsBoundedContinuous κ) :
    MarkovOperatorWeakConvergenceBridge κ := by
  intro ι l μs μ hμ f
  rcases hκ f with ⟨g, hg⟩
  simpa [← hg] using
    (ProbabilityMeasure.tendsto_iff_forall_integral_tendsto.mp hμ g)

/-- A bundled Feller kernel supplies the weak-convergence bridge for its Markov operator. -/
theorem FellerKernelShape.markovOperatorWeakConvergenceBridge
    [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    {κ : Kernel Ω Ω} (hκ : FellerKernelShape κ) :
    MarkovOperatorWeakConvergenceBridge κ :=
  markovOperatorWeakConvergenceBridge_of_mapsBoundedContinuous hκ.textbookCondition

/--
Cesaro-shift vanishing against bounded continuous tests.

This is the exact test-function leaf needed after the finite shifted-sum
identity: the Markov-operator integral over the `n`th Cesaro average and the
ordinary integral over that same average have asymptotically zero difference.
-/
def CesaroShiftVanishingAgainstBoundedContinuous
    [TopologicalSpace Ω] (κ : Kernel Ω Ω) [IsMarkovKernel κ]
    (avg : ℕ → ProbabilityMeasure Ω) : Prop :=
  ∀ f : Ω →ᵇ ℝ,
    Filter.Tendsto
      (fun n => ∫ x, markovOperator κ f x ∂(avg n : Measure Ω) -
        ∫ x, f x ∂(avg n : Measure Ω))
      Filter.atTop (𝓝 0)

/--
Cesaro-shift vanishing plus convergence of both test-function sequences
identifies the Markov-operator integral at the weak limit with the original
test integral at the same limit.
-/
theorem markovOperator_integral_eq_of_cesaroShiftVanishing
    [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    {κ : Kernel Ω Ω} [IsMarkovKernel κ]
    {avg : ℕ → ProbabilityMeasure Ω} {μ : ProbabilityMeasure Ω}
    (hshift : CesaroShiftVanishingAgainstBoundedContinuous κ avg)
    (hmarkov : ∀ f : Ω →ᵇ ℝ,
      Filter.Tendsto (fun n => ∫ x, markovOperator κ f x ∂(avg n : Measure Ω))
        Filter.atTop (𝓝 (∫ x, markovOperator κ f x ∂(μ : Measure Ω))))
    (hweak : WeakConvergenceAgainstBoundedContinuous avg Filter.atTop μ) :
    ∀ f : Ω →ᵇ ℝ,
      ∫ x, markovOperator κ f x ∂(μ : Measure Ω) =
        ∫ x, f x ∂(μ : Measure Ω) := by
  intro f
  have hSub := (hmarkov f).sub (hweak f)
  have hZero := hshift f
  have hlim := tendsto_nhds_unique hSub hZero
  exact sub_eq_zero.mp hlim

/-- The reverse direction of the kernel-invariance definition. -/
theorem invariant_of_comp_eq {κ : Kernel Ω Ω} {μ : Measure Ω}
    (h : κ ∘ₘ μ = μ) :
    Kernel.Invariant κ μ :=
  h

/--
Bounded continuous real tests determine the measure.

This is kept as an explicit obligation because the full Riesz/Portmanteau
separation leaf is not proved in this child.
-/
def BoundedContinuousIntegralDeterminesMeasure [TopologicalSpace Ω] : Prop :=
  ∀ {ν ρ : Measure Ω},
    (∀ f : Ω →ᵇ ℝ, ∫ x, f x ∂ν = ∫ x, f x ∂ρ) → ν = ρ

/--
The Markov-operator integral represents integration against the kernel-composed
measure.

This records the Fubini/kernel-integral representation still needed to turn
test-function Markov-operator equalities into equality of raw measures.
-/
def MarkovOperatorIntegralRepresentsKernelComp [TopologicalSpace Ω]
    (κ : Kernel Ω Ω) : Prop :=
  ∀ (μ : ProbabilityMeasure Ω) (f : Ω →ᵇ ℝ),
    ∫ x, f x ∂(κ ∘ₘ (μ : Measure Ω)) =
      ∫ x, markovOperator κ f x ∂(μ : Measure Ω)

/--
If bounded continuous tests separate measures and the Markov-operator integral
represents kernel composition, equality of all Markov-operator test integrals
at `μ` gives `Kernel.Invariant κ μ`.
-/
theorem kernelInvariant_of_markovOperator_integral_eq
    [TopologicalSpace Ω]
    {κ : Kernel Ω Ω} {μ : ProbabilityMeasure Ω}
    (hcomp : MarkovOperatorIntegralRepresentsKernelComp κ)
    (hext : BoundedContinuousIntegralDeterminesMeasure (Ω := Ω))
    (heq : ∀ f : Ω →ᵇ ℝ,
      ∫ x, markovOperator κ f x ∂(μ : Measure Ω) =
        ∫ x, f x ∂(μ : Measure Ω)) :
    Kernel.Invariant κ (μ : Measure Ω) := by
  apply invariant_of_comp_eq
  apply hext
  intro f
  rw [hcomp μ f, heq f]

/--
Conditional invariant-limit bridge for the Cesaro argument.

This theorem does not prove the full Krylov-Bogolyubov terminal step by itself:
it isolates the remaining analytic obligations as explicit hypotheses and then
derives `Kernel.Invariant κ μ` for the weak limit.
-/
theorem kernelInvariant_of_cesaroShiftVanishing
    [TopologicalSpace Ω] [OpensMeasurableSpace Ω]
    {κ : Kernel Ω Ω} [IsMarkovKernel κ]
    {avg : ℕ → ProbabilityMeasure Ω} {μ : ProbabilityMeasure Ω}
    (hshift : CesaroShiftVanishingAgainstBoundedContinuous κ avg)
    (hmarkov : ∀ f : Ω →ᵇ ℝ,
      Filter.Tendsto (fun n => ∫ x, markovOperator κ f x ∂(avg n : Measure Ω))
        Filter.atTop (𝓝 (∫ x, markovOperator κ f x ∂(μ : Measure Ω))))
    (hweak : WeakConvergenceAgainstBoundedContinuous avg Filter.atTop μ)
    (hcomp : MarkovOperatorIntegralRepresentsKernelComp κ)
    (hext : BoundedContinuousIntegralDeterminesMeasure (Ω := Ω)) :
    Kernel.Invariant κ (μ : Measure Ω) :=
  kernelInvariant_of_markovOperator_integral_eq hcomp hext
    (markovOperator_integral_eq_of_cesaroShiftVanishing hshift hmarkov hweak)

/--
Checked Levy-Prokhorov edistance formula on probability measures.

The formula records the metric anchor used by the weak-convergence topology on
`ProbabilityMeasure Ω`.
-/
theorem levyProkhorov_edist_probabilityMeasure_def
    [PseudoEMetricSpace Ω] [OpensMeasurableSpace Ω]
    (μ ν : LevyProkhorov (ProbabilityMeasure Ω)) :
    edist μ ν =
      levyProkhorovEDist μ.toMeasure.toMeasure ν.toMeasure.toMeasure :=
  LevyProkhorov.edist_probabilityMeasure_def μ ν

/--
Compactness/tightness package used in the Krylov-Bogolyubov proof.

On compact Borel Hausdorff spaces, the tightness and relative-compactness
fields below are now supplied repo-locally for the Cesaro empirical averages by
`cesaroEmpiricalAveragesSet_tight_of_compactSpace` and
`cesaroEmpiricalAveragesSet_closure_isCompact_of_compactSpace`.  The terminal
cluster-point extraction and invariance bridge remain separate proof leaves.
-/
structure CompactAveragingPackage [TopologicalSpace Ω] (κ : Kernel Ω Ω) : Type u where
  empirical_averages_tight : Prop
  empirical_averages_tight_holds : empirical_averages_tight
  weak_cluster_point_exists : Prop
  weak_cluster_point_exists_holds : weak_cluster_point_exists
  cluster_point_invariance_bridge : Prop
  cluster_point_invariance_bridge_holds : cluster_point_invariance_bridge

/--
Data package for a Krylov-Bogolyubov invariant-measure theorem.

The package separates the kernel object model, compactness/tightness branch,
weak-cluster branch, and final invariant probability.  A terminal proof should
construct `invariant_probability` from concrete Feller and compactness
hypotheses rather than supply the abstract package fields.
-/
structure KrylovBogolyubovData [TopologicalSpace Ω] (κ : Kernel Ω Ω) :
    Type u where
  isMarkov : IsMarkovKernel κ
  feller : FellerKernelShape κ
  compact_averaging : CompactAveragingPackage κ
  invariant_probability : InvariantProbability κ

/--
Normalized Stage1 statement shape for the Krylov-Bogolyubov theorem.

For every compact Borel state space and every Feller Markov kernel on that
space, there exists an invariant probability measure.  The current repo-local
artifact records this as an existence-data target, not as a completed proof.
-/
def StatementShape
    (Ω : Type u) [TopologicalSpace Ω] [MeasurableSpace Ω] [BorelSpace Ω]
    [CompactSpace Ω] : Prop :=
  ∀ κ : Kernel Ω Ω,
    IsMarkovKernel κ →
      FellerKernelShape κ →
        CompactAveragingPackage κ →
          Nonempty (KrylovBogolyubovData κ)

/-- The statement shape unfolds to the normalized existence-data package. -/
theorem statementShape_iff
    (Ω : Type u) [TopologicalSpace Ω] [MeasurableSpace Ω] [BorelSpace Ω]
    [CompactSpace Ω] :
    StatementShape Ω ↔
      ∀ κ : Kernel Ω Ω,
        IsMarkovKernel κ →
          FellerKernelShape κ →
            CompactAveragingPackage κ →
              Nonempty (KrylovBogolyubovData κ) :=
  Iff.rfl

/-- A terminal data package exposes the invariant probability measure. -/
theorem exists_invariant_probability_of_data
    [TopologicalSpace Ω] {κ : Kernel Ω Ω}
    (d : KrylovBogolyubovData κ) :
    ∃ μ : ProbabilityMeasure Ω, Kernel.Invariant κ (μ : Measure Ω) :=
  ⟨d.invariant_probability.measure, d.invariant_probability.invariant⟩

/-- The probability field of a terminal data package is invariant. -/
theorem data_invariant_probability
    [TopologicalSpace Ω] {κ : Kernel Ω Ω}
    (d : KrylovBogolyubovData κ) :
    Kernel.Invariant κ (d.invariant_probability.measure : Measure Ω) :=
  d.invariant_probability.invariant

/--
Deterministic-map specialization statement shape.

This records the classical compact-dynamical-system version: a measurable
self-map, viewed as a deterministic Markov kernel, should have an invariant
probability measure after the compactness and averaging bridge is supplied.
-/
def DeterministicStatementShape
    (Ω : Type u) [TopologicalSpace Ω] [MeasurableSpace Ω] [BorelSpace Ω]
    [CompactSpace Ω] : Prop :=
  ∀ (T : Ω → Ω) (hT : Measurable T),
    ∃ μ : ProbabilityMeasure Ω,
      Kernel.Invariant (Kernel.deterministic T hT) (μ : Measure Ω)

/-- The identity-map deterministic kernel has any supplied probability measure as invariant. -/
theorem deterministic_id_invariant (μ : ProbabilityMeasure Ω) :
    Kernel.Invariant (Kernel.deterministic (fun x : Ω => x) measurable_id)
      (μ : Measure Ω) := by
  simpa [Kernel.id] using id_invariant μ

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Kernel.Invariance",
  "Mathlib.Probability.Kernel.Integral",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Composition.MeasureComp",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Integral.BoundedContinuousFunction",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Measure.Prokhorov",
  "Mathlib.MeasureTheory.Measure.Tight",
  "Mathlib.Topology.Compactness.Compact",
  "Mathlib.Topology.ContinuousMap.Bounded.Basic",
  "Mathlib.MeasureTheory.Measure.Regular",
  "Mathlib.Probability.Process.FiniteDimensionalLaws",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Martingale.Convergence"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.Kernel.Invariant",
  "ProbabilityTheory.Kernel.Invariant.def",
  "ProbabilityTheory.Kernel.IsReversible",
  "ProbabilityTheory.Kernel.IsReversible.invariant",
  "ProbabilityTheory.Kernel.deterministic",
  "ProbabilityTheory.Kernel.id",
  "ProbabilityTheory.Kernel.integral_deterministic",
  "MeasureTheory.Measure.id_comp",
  "MeasureTheory.Measure.bind_smul",
  "MeasureTheory.lintegral_finset_sum_measure",
  "MeasureTheory.ProbabilityMeasure",
  "BoundedContinuousFunction",
  "MeasureTheory.IsTightMeasureSet",
  "MeasureTheory.IsTightMeasureSet.of_compactSpace",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto",
  "MeasureTheory.ProbabilityMeasure.continuous_integral_boundedContinuousFunction",
  "MeasureTheory.levyProkhorovEDist",
  "MeasureTheory.LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure",
  "MeasureTheory.LevyProkhorov.edist_probabilityMeasure_def",
  "MeasureTheory.LevyProkhorov.eq_convergenceInDistribution",
  "MeasureTheory.isCompact_closure_of_isTightMeasureSet",
  "IsCompact.exists_clusterPt",
  "tendsto_nhds_unique",
  "MapClusterPt",
  "MeasureTheory.isTightMeasureSet_singleton_of_innerRegular"
]

/--
Search terms that did not locate a terminal Krylov-Bogolyubov theorem in pinned
mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Krylov",
  "Bogolyubov",
  "Bogoliubov",
  "Krylov-Bogolyubov",
  "invariant probability",
  "InvariantMeasure",
  "Feller",
  "stationary measure",
  "Markov kernel invariant measure",
  "Prokhorov invariant"
]

/-! ## Audit probes -/

#check InvariantProbability
#check InvariantProbability.invariant_measure
#check invariant_comp_eq
#check invariant_apply
#check invariant_of_reversible
#check id_invariant
#check invariantProbability_id
#check isMarkovKernel_pow
#check iteratedPushForwardMeasure
#check iteratedPushForwardMeasure_univ
#check iteratedPushForward
#check iteratedPushForward_toMeasure
#check cesaroEmpiricalAverageMeasure
#check cesaroEmpiricalAverageMeasure_univ
#check cesaroEmpiricalAverageMeasure_isProbabilityMeasure
#check cesaroEmpiricalAverage
#check cesaroEmpiricalAverage_toMeasure
#check kernel_comp_iteratedPushForwardMeasure
#check kernel_comp_finset_sum_iteratedPushForwardMeasure
#check kernel_comp_cesaroEmpiricalAverageMeasure_shiftedSum
#check kernelPushForwardProbability
#check kernelPushForwardProbability_toMeasure
#check markovOperator
#check MarkovOperatorMapsBoundedContinuous
#check TextbookFellerCondition
#check markovOperatorMaps_iff_textbookFeller
#check FellerKernelShape
#check FellerKernelShape.textbookCondition
#check fellerKernelShape_nonempty_iff_textbookFeller
#check markovOperator_id_apply
#check textbookFellerCondition_id
#check probabilityMeasureUnderlyingMeasureSet
#check mem_probabilityMeasureUnderlyingMeasureSet
#check probabilityMeasureUnderlyingMeasureSet_tight_of_compactSpace
#check compactSpace_probabilityMeasure_of_compactSpace
#check probabilityMeasureSet_closure_isCompact_of_tight
#check probabilityMeasureSet_closure_isCompact_of_compactSpace
#check cesaroEmpiricalAveragesSet
#check cesaroEmpiricalAverage_mem_averagesSet
#check cesaroEmpiricalAveragesSet_tight_of_compactSpace
#check cesaroEmpiricalAveragesSet_closure_isCompact_of_compactSpace
#check WeakClusterPointOfEmpiricalAverages
#check exists_clusterPoint_of_compact_closure_range
#check exists_weakClusterPointOfEmpiricalAverages_of_compactSpace
#check WeakConvergenceAgainstBoundedContinuous
#check weakConvergenceAgainstBoundedContinuous_iff_tendsto
#check MarkovOperatorWeakConvergenceBridge
#check markovOperatorWeakConvergenceBridge_of_mapsBoundedContinuous
#check FellerKernelShape.markovOperatorWeakConvergenceBridge
#check CesaroShiftVanishingAgainstBoundedContinuous
#check markovOperator_integral_eq_of_cesaroShiftVanishing
#check invariant_of_comp_eq
#check BoundedContinuousIntegralDeterminesMeasure
#check MarkovOperatorIntegralRepresentsKernelComp
#check kernelInvariant_of_markovOperator_integral_eq
#check kernelInvariant_of_cesaroShiftVanishing
#check levyProkhorov_edist_probabilityMeasure_def
#check CompactAveragingPackage
#check KrylovBogolyubovData
#check StatementShape
#check statementShape_iff
#check exists_invariant_probability_of_data
#check deterministic_id_invariant
#check Kernel.Invariant
#check Kernel.IsReversible.invariant
#check Kernel.deterministic
#check Kernel.id
#check Measure.id_comp
#check Measure.bind_smul
#check lintegral_finset_sum_measure
#check ProbabilityMeasure
#check IsTightMeasureSet
#check IsTightMeasureSet.of_compactSpace
#check isCompact_closure_of_isTightMeasureSet
#check MeasureTheory.levyProkhorovEDist
#check LevyProkhorov.edist_probabilityMeasure_def
#check LevyProkhorov.eq_convergenceInDistribution
#check IsCompact.exists_clusterPt
#check MapClusterPt
#check tendsto_nhds_unique
#check ProbabilityMeasure.tendsto_iff_forall_integral_tendsto
#check ProbabilityMeasure.continuous_integral_boundedContinuousFunction

end AwesomeTheorems.Stage1.S1_M_219
