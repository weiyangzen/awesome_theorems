import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric
import Mathlib.MeasureTheory.Measure.Prokhorov
import Mathlib.MeasureTheory.Integral.BoundedContinuousFunction
import Mathlib.Topology.Semicontinuity.Basic

/-!
# S1-M-151 / THM-M-1186: McCann theorem, optimal transport existence

This Stage1 artifact records a conservative Lean 4 statement-shape boundary for
existence of an optimal transport plan.

The pinned mathlib snapshot has probability measures, product measures, marginal
maps, weak-convergence and Levy-Prokhorov infrastructure, lower semicontinuity,
and nonnegative extended integrals.  It does not expose a terminal McCann or
Kantorovich optimal-transport existence theorem.

The declarations below therefore normalize the coupling and cost-minimizer
objects without adding proof placeholders.  The compactness/tightness boundary is
now stated directly for probability measures on `X × Y`; the cost-functional
lower-semicontinuity boundary is stated as the concrete proposition
`LowerSemicontinuousCostFunctionalTarget c`, with a checked bounded-continuous
subcase and the full lower-semicontinuous `ENNReal` cost case left as an
explicit formalization leaf.

Public Stage1 backfill note: this repo-local artifact currently provides only
`StatementShape` plus checked probability and coupling wrappers.  It is not a
closed proof of McCann/Kantorovich optimal-transport existence.

Public scope decision for the Stage1 blueprint: use compact metric Borel spaces
as the terminal theorem target for this slot.  This is narrower than the usual
Polish/Radon formulation and broader than a finite-dimensional Euclidean-only
setting.  The compact metric target matches the repo-local mathlib anchors for
probability measures, Levy-Prokhorov topology, product couplings, and compactness
of probability-measure spaces, while avoiding an unproved general tightness
package.
-/

noncomputable section

open MeasureTheory Set Filter
open scoped ENNReal NNReal Topology

namespace AwesomeTheorems.Stage1.S1_M_151

universe u v

variable {X : Type u} {Y : Type v} [MeasurableSpace X] [MeasurableSpace Y]

/--
A transport plan between two probability measures.

The plan is a probability measure on the product whose two coordinate
push-forwards are the prescribed marginals.
-/
structure TransportPlan (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Type (max u v) where
  plan : Measure (X × Y)
  isProbability : IsProbabilityMeasure plan
  fst_marginal : Measure.map Prod.fst plan = (μ : Measure X)
  snd_marginal : Measure.map Prod.snd plan = (ν : Measure Y)

instance (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (γ : TransportPlan μ ν) : IsProbabilityMeasure γ.plan :=
  γ.isProbability

/-- The cost of a transport plan, as a nonnegative extended integral. -/
def TransportCost {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (γ : TransportPlan μ ν) : ℝ≥0∞ :=
  ∫⁻ z, c z ∂γ.plan

/-- The same cost functional on the ambient probability-measure space. -/
def ProbabilityTransportCost (c : X × Y → ℝ≥0∞) (γ : ProbabilityMeasure (X × Y)) :
    ℝ≥0∞ :=
  ∫⁻ z, c z ∂(γ : Measure (X × Y))

/-- The cost wrapper unfolds to the underlying nonnegative extended integral. -/
theorem transportCost_eq_lintegral {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (γ : TransportPlan μ ν) :
    TransportCost c γ = ∫⁻ z, c z ∂γ.plan :=
  rfl

/--
Concrete target for the missing Portmanteau lower-semicontinuity leaf.

For a lower-semicontinuous cost `c`, the direct-method proof needs this
functional on `ProbabilityMeasure (X × Y)` to be lower semicontinuous for weak
convergence.
-/
def LowerSemicontinuousCostFunctionalTarget
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    (c : X × Y → ℝ≥0∞) : Prop :=
  LowerSemicontinuous (fun γ : ProbabilityMeasure (X × Y) => ProbabilityTransportCost c γ)

/--
Checked subcase of the cost-functional lower-semicontinuity leaf: bounded
continuous `ℝ≥0` costs give a continuous, hence lower-semicontinuous,
`lintegral` functional on probability measures.
-/
theorem probabilityTransportCost_continuous_boundedContinuous
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    (c : BoundedContinuousFunction (X × Y) ℝ≥0) :
    Continuous (fun γ : ProbabilityMeasure (X × Y) =>
      ProbabilityTransportCost (fun z => (c z : ℝ≥0∞)) γ) := by
  simpa [ProbabilityTransportCost] using
    (ProbabilityMeasure.continuous_lintegral_boundedContinuousFunction c)

/-- The checked bounded-continuous subcase in lower-semicontinuity form. -/
theorem probabilityTransportCost_lowerSemicontinuous_boundedContinuous
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    (c : BoundedContinuousFunction (X × Y) ℝ≥0) :
    LowerSemicontinuous (fun γ : ProbabilityMeasure (X × Y) =>
      ProbabilityTransportCost (fun z => (c z : ℝ≥0∞)) γ) :=
  (probabilityTransportCost_continuous_boundedContinuous c).lowerSemicontinuous

/-- The bounded-continuous subcase also satisfies the concrete C005 target. -/
theorem lowerSemicontinuousCostFunctionalTarget_boundedContinuous
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    (c : BoundedContinuousFunction (X × Y) ℝ≥0) :
    LowerSemicontinuousCostFunctionalTarget (fun z => (c z : ℝ≥0∞)) := by
  simpa [LowerSemicontinuousCostFunctionalTarget] using
    probabilityTransportCost_lowerSemicontinuous_boundedContinuous c

/-- A plan is optimal if no other plan has smaller cost. -/
def IsOptimalTransportPlan {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (γ : TransportPlan μ ν) : Prop :=
  ∀ η : TransportPlan μ ν, TransportCost c γ ≤ TransportCost c η

/--
The independent product coupling, checked against mathlib's product-measure
marginal theorems.
-/
def independentPlan (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    TransportPlan μ ν where
  plan := (μ : Measure X).prod (ν : Measure Y)
  isProbability := by infer_instance
  fst_marginal := by
    rw [Measure.map_fst_prod]
    simp
  snd_marginal := by
    rw [Measure.map_snd_prod]
    simp

/-- The product coupling carries the expected probability-measure instance. -/
theorem independentPlan_isProbability (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    IsProbabilityMeasure (independentPlan μ ν).plan :=
  (independentPlan μ ν).isProbability

/-- The checked product coupling makes the coupling type nonempty. -/
theorem nonempty_transportPlan (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Nonempty (TransportPlan μ ν) :=
  ⟨independentPlan μ ν⟩

/-- The first marginal field is definitionally available as a theorem wrapper. -/
theorem fst_marginal_eq {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) :
    Measure.map Prod.fst γ.plan = (μ : Measure X) :=
  γ.fst_marginal

/-- The second marginal field is definitionally available as a theorem wrapper. -/
theorem snd_marginal_eq {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) :
    Measure.map Prod.snd γ.plan = (ν : Measure Y) :=
  γ.snd_marginal

/-- The product coupling has the expected first marginal. -/
theorem independentPlan_fst (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Measure.map Prod.fst (independentPlan μ ν).plan = (μ : Measure X) :=
  (independentPlan μ ν).fst_marginal

/-- The product coupling has the expected second marginal. -/
theorem independentPlan_snd (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Measure.map Prod.snd (independentPlan μ ν).plan = (ν : Measure Y) :=
  (independentPlan μ ν).snd_marginal

/--
Probability-measure version of the coupling set.

This is the compactness/tightness surface used by the Stage1 McCann slot: weak
compactness and Prokhorov tightness live naturally on
`ProbabilityMeasure (X × Y)`, while `TransportPlan` remains the normalized
plan object used for costs and optimality.
-/
def ProbabilityCouplingSet (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Set (ProbabilityMeasure (X × Y)) :=
  {γ | Measure.map Prod.fst (γ : Measure (X × Y)) = (μ : Measure X) ∧
    Measure.map Prod.snd (γ : Measure (X × Y)) = (ν : Measure Y)}

/-- A normalized transport plan gives a probability-measure coupling. -/
def TransportPlan.toProbabilityMeasure {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) : ProbabilityMeasure (X × Y) :=
  ⟨γ.plan, γ.isProbability⟩

/-- The probability-measure cost wrapper agrees with the normalized transport-plan cost. -/
theorem probabilityTransportCost_eq_transportCost
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (γ : TransportPlan μ ν) :
    ProbabilityTransportCost c γ.toProbabilityMeasure = TransportCost c γ :=
  rfl

/-- The probability-measure coupling associated to a transport plan has the prescribed marginals. -/
theorem transportPlan_toProbabilityMeasure_mem
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y} (γ : TransportPlan μ ν) :
    γ.toProbabilityMeasure ∈ ProbabilityCouplingSet μ ν :=
  ⟨γ.fst_marginal, γ.snd_marginal⟩

/-- A probability-measure coupling can be re-bundled as a normalized transport plan. -/
def TransportPlan.ofProbabilityMeasure
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : ProbabilityMeasure (X × Y)) (hγ : γ ∈ ProbabilityCouplingSet μ ν) :
    TransportPlan μ ν where
  plan := (γ : Measure (X × Y))
  isProbability := by infer_instance
  fst_marginal := hγ.1
  snd_marginal := hγ.2

/-- Re-bundling a probability-measure coupling does not change its cost. -/
theorem transportPlan_ofProbabilityMeasure_cost_eq
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞)
    (γ : ProbabilityMeasure (X × Y)) (hγ : γ ∈ ProbabilityCouplingSet μ ν) :
    TransportCost c (TransportPlan.ofProbabilityMeasure γ hγ) =
      ProbabilityTransportCost c γ :=
  rfl

/-- Re-bundling a probability-measure coupling and forgetting it again is definitionally neutral. -/
theorem transportPlan_ofProbabilityMeasure_toProbabilityMeasure
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : ProbabilityMeasure (X × Y)) (hγ : γ ∈ ProbabilityCouplingSet μ ν) :
    (TransportPlan.ofProbabilityMeasure γ hγ).toProbabilityMeasure = γ :=
  rfl

/-- The independent product plan as a probability-measure coupling. -/
def independentProbabilityCoupling (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    ProbabilityMeasure (X × Y) :=
  (independentPlan μ ν).toProbabilityMeasure

/-- The independent probability coupling has the prescribed marginals. -/
theorem independentProbabilityCoupling_mem
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    independentProbabilityCoupling μ ν ∈ ProbabilityCouplingSet μ ν :=
  transportPlan_toProbabilityMeasure_mem (independentPlan μ ν)

/-- The probability-measure coupling set is nonempty. -/
theorem probabilityCouplingSet_nonempty
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    (ProbabilityCouplingSet μ ν).Nonempty :=
  ⟨independentProbabilityCoupling μ ν, independentProbabilityCoupling_mem μ ν⟩

/--
First marginal of a probability measure on a product, as a probability measure.

This wraps `ProbabilityMeasure.map` so the weak-continuity theorem for
push-forwards can be used directly on the coupling set.
-/
def firstMarginalProbability
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace X] (γ : ProbabilityMeasure (X × Y)) : ProbabilityMeasure X :=
  γ.map continuous_fst.measurable.aemeasurable

/--
Second marginal of a probability measure on a product, as a probability measure.

This wraps `ProbabilityMeasure.map` so the weak-continuity theorem for
push-forwards can be used directly on the coupling set.
-/
def secondMarginalProbability
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace Y] (γ : ProbabilityMeasure (X × Y)) : ProbabilityMeasure Y :=
  γ.map continuous_snd.measurable.aemeasurable

@[simp]
theorem firstMarginalProbability_toMeasure
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace X] (γ : ProbabilityMeasure (X × Y)) :
    ((firstMarginalProbability γ : ProbabilityMeasure X) : Measure X) =
      Measure.map Prod.fst (γ : Measure (X × Y)) :=
  rfl

@[simp]
theorem secondMarginalProbability_toMeasure
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace Y] (γ : ProbabilityMeasure (X × Y)) :
    ((secondMarginalProbability γ : ProbabilityMeasure Y) : Measure Y) =
      Measure.map Prod.snd (γ : Measure (X × Y)) :=
  rfl

/-- The first-marginal push-forward is continuous for weak convergence. -/
theorem firstMarginalProbability_continuous
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace X] :
    Continuous (firstMarginalProbability : ProbabilityMeasure (X × Y) → ProbabilityMeasure X) :=
  ProbabilityMeasure.continuous_map continuous_fst

/-- The second-marginal push-forward is continuous for weak convergence. -/
theorem secondMarginalProbability_continuous
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace Y] :
    Continuous (secondMarginalProbability : ProbabilityMeasure (X × Y) → ProbabilityMeasure Y) :=
  ProbabilityMeasure.continuous_map continuous_snd

/-- The coupling set is exactly the intersection of the two closed marginal fibers. -/
theorem probabilityCouplingSet_eq_marginal_fibers
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace X] [BorelSpace Y]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    ProbabilityCouplingSet μ ν =
      firstMarginalProbability ⁻¹' {μ} ∩ secondMarginalProbability ⁻¹' {ν} := by
  ext γ
  constructor
  · intro hγ
    constructor
    · apply ProbabilityMeasure.toMeasure_injective
      simpa using hγ.1
    · apply ProbabilityMeasure.toMeasure_injective
      simpa using hγ.2
  · rintro ⟨hfst, hsnd⟩
    constructor
    · have h := congr_arg (fun ρ : ProbabilityMeasure X => (ρ : Measure X)) hfst
      simpa using h
    · have h := congr_arg (fun ρ : ProbabilityMeasure Y => (ρ : Measure Y)) hsnd
      simpa using h

/--
The probability-measure coupling set is closed for weak convergence once the
marginal probability-measure spaces are Hausdorff.
-/
theorem probabilityCouplingSet_isClosed_of_marginal_t2
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace X] [BorelSpace Y]
    [T2Space (ProbabilityMeasure X)] [T2Space (ProbabilityMeasure Y)]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    IsClosed (ProbabilityCouplingSet μ ν) := by
  rw [probabilityCouplingSet_eq_marginal_fibers μ ν]
  exact (isClosed_singleton.preimage firstMarginalProbability_continuous).inter
    (isClosed_singleton.preimage secondMarginalProbability_continuous)

/--
Membership in the coupling set is retained by weak limits.

This is the closed-marginal leaf needed by the direct-method compactness route:
if the weak limit lies in the closure of the coupling set, then its two
coordinate marginals are still the prescribed measures.
-/
theorem probabilityCouplingSet_mem_of_mem_closure
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace X] [BorelSpace Y]
    [T2Space (ProbabilityMeasure X)] [T2Space (ProbabilityMeasure Y)]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {γ : ProbabilityMeasure (X × Y)}
    (hγ : γ ∈ closure (ProbabilityCouplingSet μ ν)) :
    γ ∈ ProbabilityCouplingSet μ ν :=
  (probabilityCouplingSet_isClosed_of_marginal_t2 μ ν).closure_subset hγ

/--
Filter formulation of the weak-closedness leaf: an eventually-coupling net of
probability measures has a weak limit that is again a coupling.
-/
theorem probabilityCouplingSet_mem_of_tendsto
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace X] [BorelSpace Y]
    [T2Space (ProbabilityMeasure X)] [T2Space (ProbabilityMeasure Y)]
    {ι : Type*} {l : Filter ι} [l.NeBot]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {γs : ι → ProbabilityMeasure (X × Y)} {γ : ProbabilityMeasure (X × Y)}
    (hγs : ∀ᶠ i in l, γs i ∈ ProbabilityCouplingSet μ ν)
    (hlim : Tendsto γs l (𝓝 γ)) :
    γ ∈ ProbabilityCouplingSet μ ν :=
  (probabilityCouplingSet_isClosed_of_marginal_t2 μ ν).mem_of_tendsto hlim hγs

/--
Levy-Prokhorov formulation of the same closedness leaf.  The local mathlib
theorem `LevyProkhorov.continuous_toMeasure_probabilityMeasure` transfers
Levy-Prokhorov convergence to weak convergence, and the weakly closed coupling
set then retains the prescribed marginals.
-/
theorem probabilityCouplingSet_mem_of_tendsto_levyProkhorov
    [PseudoMetricSpace X] [PseudoMetricSpace Y] [OpensMeasurableSpace (X × Y)]
    [BorelSpace X] [BorelSpace Y]
    [T2Space (ProbabilityMeasure X)] [T2Space (ProbabilityMeasure Y)]
    {ι : Type*} {l : Filter ι} [l.NeBot]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {γs : ι → LevyProkhorov (ProbabilityMeasure (X × Y))}
    {γ : LevyProkhorov (ProbabilityMeasure (X × Y))}
    (hγs : ∀ᶠ i in l, LevyProkhorov.toMeasure (γs i) ∈ ProbabilityCouplingSet μ ν)
    (hlim : Tendsto γs l (𝓝 γ)) :
    LevyProkhorov.toMeasure γ ∈ ProbabilityCouplingSet μ ν := by
  exact probabilityCouplingSet_mem_of_tendsto hγs
    ((LevyProkhorov.continuous_toMeasure_probabilityMeasure.tendsto γ).comp hlim)

/--
Concrete tightness theorem for the probability-measure coupling set in compact
source and target spaces.
-/
theorem probabilityCouplingSet_isTight_of_compactSpace
    [TopologicalSpace X] [TopologicalSpace Y] [CompactSpace X] [CompactSpace Y]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    IsTightMeasureSet {((γ : ProbabilityMeasure (X × Y)) : Measure (X × Y)) |
        γ ∈ ProbabilityCouplingSet μ ν} := by
  exact IsTightMeasureSet.of_compactSpace

/--
Concrete compactness theorem for the ambient probability-measure space in the
selected compact metric Borel scope.
-/
theorem compactSpace_probabilityMeasure_prod_of_compactMetric
    [MetricSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [BorelSpace Y] [CompactSpace Y] :
    CompactSpace (ProbabilityMeasure (X × Y)) := by
  infer_instance

/--
In the selected compact metric Borel scope, the weak closure of the
probability-measure coupling set is compact.

The later closed-marginal leaf should strengthen this from compact closure to
compactness of the coupling set itself.
-/
theorem probabilityCouplingSet_closure_isCompact_of_compactMetric
    [MetricSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [BorelSpace Y] [CompactSpace Y]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    IsCompact (closure (ProbabilityCouplingSet μ ν)) := by
  exact isClosed_closure.isCompact

/--
In the selected compact metric Borel scope, the probability-measure coupling set
itself is compact once the marginal fibers are known to be closed.
-/
theorem probabilityCouplingSet_isCompact_of_compactMetric
    [MetricSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [BorelSpace Y] [CompactSpace Y]
    [OpensMeasurableSpace (X × Y)]
    [T2Space (ProbabilityMeasure X)] [T2Space (ProbabilityMeasure Y)]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    IsCompact (ProbabilityCouplingSet μ ν) :=
  (probabilityCouplingSet_isClosed_of_marginal_t2 μ ν).isCompact

/--
An attained minimum on the ambient probability-measure coupling set gives an
optimal normalized `TransportPlan`.

This is the final normalization step in the direct-method route: the compactness
and lower-semicontinuity argument may run on `ProbabilityMeasure (X × Y)`, but
the public theorem target is the bundled `TransportPlan`.
-/
theorem exists_optimal_transportPlan_of_probabilityCoupling_minimizer
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {c : X × Y → ℝ≥0∞} {γ : ProbabilityMeasure (X × Y)}
    (hγ : γ ∈ ProbabilityCouplingSet μ ν)
    (hmin : IsMinOn (fun ρ : ProbabilityMeasure (X × Y) =>
      ProbabilityTransportCost c ρ) (ProbabilityCouplingSet μ ν) γ) :
    ∃ γ₀ : TransportPlan μ ν, IsOptimalTransportPlan c γ₀ := by
  refine ⟨TransportPlan.ofProbabilityMeasure γ hγ, ?_⟩
  intro η
  simpa [transportPlan_ofProbabilityMeasure_cost_eq,
    probabilityTransportCost_eq_transportCost] using
    (isMinOn_iff.mp hmin) η.toProbabilityMeasure (transportPlan_toProbabilityMeasure_mem η)

/--
Direct-method minimizer theorem for the normalized `TransportPlan` object,
assuming the compact coupling-set leaf and the cost-functional
lower-semicontinuity leaf have already been supplied.
-/
theorem exists_optimal_transportPlan_of_isCompact_lsc
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {c : X × Y → ℝ≥0∞}
    (hne : (ProbabilityCouplingSet μ ν).Nonempty)
    (hcompact : IsCompact (ProbabilityCouplingSet μ ν))
    (hlsc : LowerSemicontinuousCostFunctionalTarget c) :
    ∃ γ : TransportPlan μ ν, IsOptimalTransportPlan c γ := by
  have hlsc_global :
      LowerSemicontinuous (fun γ : ProbabilityMeasure (X × Y) =>
        ProbabilityTransportCost c γ) := by
    simpa [LowerSemicontinuousCostFunctionalTarget] using hlsc
  obtain ⟨γ, hγ, hmin⟩ :=
    LowerSemicontinuousOn.exists_isMinOn hne hcompact
      (hlsc_global.lowerSemicontinuousOn (ProbabilityCouplingSet μ ν))
  exact exists_optimal_transportPlan_of_probabilityCoupling_minimizer hγ hmin

/--
Compact metric Borel specialization of the direct-method minimizer theorem.

This closes the minimizer-extraction step for the selected public scope, still
conditional on the general `ENNReal` lower-semicontinuity target from C005.
-/
theorem exists_optimal_transportPlan_of_compactMetric_lscTarget
    [MetricSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [BorelSpace Y] [CompactSpace Y]
    [OpensMeasurableSpace (X × Y)]
    [T2Space (ProbabilityMeasure X)] [T2Space (ProbabilityMeasure Y)]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    {c : X × Y → ℝ≥0∞}
    (hlsc : LowerSemicontinuousCostFunctionalTarget c) :
    ∃ γ : TransportPlan μ ν, IsOptimalTransportPlan c γ :=
  exists_optimal_transportPlan_of_isCompact_lsc
    (probabilityCouplingSet_nonempty μ ν)
    (probabilityCouplingSet_isCompact_of_compactMetric μ ν) hlsc

/--
Data package for a McCann/Kantorovich existence theorem.

The fields split the part already expressible in mathlib from the missing
existence proof.  The compactness/tightness package is no longer an abstract
`Prop`: it is the concrete tightness assertion for the coupling family as a set
of measures coming from `ProbabilityMeasure (X × Y)`.  Likewise, the
cost-functional lower-semicontinuity field is now the concrete C005 target
`LowerSemicontinuousCostFunctionalTarget c`, not an arbitrary placeholder
proposition.
-/
structure OptimalTransportExistenceData
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞) : Type (max u v) where
  cost_lowerSemicontinuous : LowerSemicontinuous c
  admissible_plan : TransportPlan μ ν
  probability_couplings_tight :
    IsTightMeasureSet {((γ : ProbabilityMeasure (X × Y)) : Measure (X × Y)) |
        γ ∈ ProbabilityCouplingSet μ ν}
  cost_functional_lowerSemicontinuous : LowerSemicontinuousCostFunctionalTarget c
  minimizer : TransportPlan μ ν
  optimality : IsOptimalTransportPlan c minimizer

/--
Normalized Stage1 statement shape for optimal-transport existence.

For every pair of probability measures on Borel topological spaces and every
lower-semicontinuous nonnegative extended cost, the theorem asserts the
existence of an optimal coupling after the terminal compactness and
lower-semicontinuity packages have been supplied.
-/
def StatementShape
    (X : Type u) (Y : Type v)
    [TopologicalSpace X] [MeasurableSpace X] [BorelSpace X]
    [TopologicalSpace Y] [MeasurableSpace Y] [BorelSpace Y]
    [OpensMeasurableSpace (X × Y)] : Prop :=
  ∀ (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞),
    LowerSemicontinuous c →
      Nonempty (OptimalTransportExistenceData μ ν c)

/-- The statement shape unfolds to the normalized existence-data package. -/
theorem statementShape_iff
    (X : Type u) (Y : Type v)
    [TopologicalSpace X] [MeasurableSpace X] [BorelSpace X]
    [TopologicalSpace Y] [MeasurableSpace Y] [BorelSpace Y]
    [OpensMeasurableSpace (X × Y)] :
    StatementShape X Y ↔
      ∀ (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
        (c : X × Y → ℝ≥0∞),
        LowerSemicontinuous c →
          Nonempty (OptimalTransportExistenceData μ ν c) :=
  Iff.rfl

/--
Checked public theorem-scope decision for S1-M-151.

The selected public target is the compact metric Borel setting:
`MetricSpace`, `BorelSpace`, and `CompactSpace` on both source and target.
The broader Polish/Radon theorem is deferred until the tightness and regularity
leaves are formalized; the finite-dimensional Euclidean setting is unnecessarily
narrow for the current mathlib compactness anchors.
-/
def CompactMetricBorelScope
    (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y] : Prop :=
  True

/-- The public scope decision is a checked class-boundary marker, not a proof of McCann. -/
theorem compactMetricBorelScope_holds
    (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y] :
    CompactMetricBorelScope X Y :=
  trivial

/--
Narrowed statement shape for the selected public target.

This aliases the existing `StatementShape` under compact metric Borel hypotheses
so later proof children can replace the abstract existence data with concrete
compactness and lower-semicontinuity theorems without changing the public scope.
-/
def StatementShapeCompactMetric
    (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    [OpensMeasurableSpace (X × Y)] : Prop :=
  StatementShape X Y

/-- The compact metric statement is definitionally the general shape under stronger hypotheses. -/
theorem statementShapeCompactMetric_iff
    (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    [OpensMeasurableSpace (X × Y)] :
    StatementShapeCompactMetric X Y ↔ StatementShape X Y :=
  Iff.rfl

/-- Machine-readable record of the chosen public scope for child task S1-M-151-C002. -/
def chosenPublicScope : String :=
  "compact metric Borel spaces"

/-- Scope alternatives intentionally not selected for the current public Stage1 target. -/
def deferredPublicScopeAlternatives : List String := [
  "full Polish/Radon spaces: deferred until tightness and regular-measure leaves are formalized",
  "finite-dimensional Euclidean Borel spaces: safe but too narrow for the compactness anchors already available"
]

/-- A terminal data package exposes the optimal transport plan. -/
theorem exists_optimal_plan_of_data
    [TopologicalSpace X] [TopologicalSpace Y] [OpensMeasurableSpace (X × Y)]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {c : X × Y → ℝ≥0∞}
    (d : OptimalTransportExistenceData μ ν c) :
    ∃ γ : TransportPlan μ ν, IsOptimalTransportPlan c γ :=
  ⟨d.minimizer, d.optimality⟩

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.Prod",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Measure.Prokhorov",
  "Mathlib.MeasureTheory.Measure.Tight",
  "Mathlib.MeasureTheory.Measure.Regular",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Integral.BoundedContinuousFunction",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.Topology.Semicontinuity.Basic"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.ProbabilityMeasure",
  "MeasureTheory.ProbabilityMeasure.toMeasure",
  "MeasureTheory.IsProbabilityMeasure",
  "MeasureTheory.Measure.prod",
  "MeasureTheory.Measure.map_fst_prod",
  "MeasureTheory.Measure.map_snd_prod",
  "MeasureTheory.levyProkhorovEDist",
  "MeasureTheory.levyProkhorovDist",
  "MeasureTheory.LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure",
  "MeasureTheory.IsTightMeasureSet",
  "MeasureTheory.IsTightMeasureSet.of_compactSpace",
  "MeasureTheory.isCompact_setOf_finiteMeasure_eq_of_compactSpace",
  "MeasureTheory.Measure.InnerRegular",
  "MeasureTheory.isTightMeasureSet_singleton_of_innerRegular",
  "MeasureTheory.ProbabilityMeasure.continuous_lintegral_boundedContinuousFunction",
  "MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto",
  "MeasureTheory.lintegral_le_liminf_lintegral_of_forall_isOpen_measure_le_liminf_measure",
  "LowerSemicontinuous",
  "lintegral"
]

/-- M0387-level local leaf ledger for child task S1-M-151-C005. -/
def costLowerSemicontinuityLeafLedger : List String := [
  "C005-L01 local_proof_body: ProbabilityTransportCost normalizes the ambient functional gamma |-> lintegral c dgamma on ProbabilityMeasure (X x Y).",
  "C005-L02 local_proof_body: probabilityTransportCost_eq_transportCost bridges ProbabilityTransportCost to the normalized TransportPlan cost.",
  "C005-L03 local_wrapper_upstream_mathlib: probabilityTransportCost_continuous_boundedContinuous uses ProbabilityMeasure.continuous_lintegral_boundedContinuousFunction for bounded continuous NNReal costs.",
  "C005-L04 local_wrapper_upstream_mathlib: probabilityTransportCost_lowerSemicontinuous_boundedContinuous closes the bounded-continuous subcase as a LowerSemicontinuous functional.",
  "C005-L05 unchecked formalization_debt: prove the Portmanteau/Vitali approximation theorem upgrading LowerSemicontinuous c : X x Y -> ENNReal to LowerSemicontinuousCostFunctionalTarget c.",
  "C005-L06 unchecked formalization_debt: feed the proved general lower-semicontinuity target into the direct-method minimizer theorem over the closed coupling set."
]

/-- M0387-level local leaf ledger for child task S1-M-151-C006. -/
def directMethodMinimizerLeafLedger : List String := [
  "C006-L01 local_proof_body: TransportPlan.ofProbabilityMeasure re-bundles any ProbabilityCouplingSet member as a normalized TransportPlan.",
  "C006-L02 local_proof_body: transportPlan_ofProbabilityMeasure_cost_eq proves the re-bundling preserves the ENNReal lintegral cost.",
  "C006-L03 local_proof_body: exists_optimal_transportPlan_of_probabilityCoupling_minimizer converts any ambient ProbabilityMeasure minimizer into an optimal normalized TransportPlan.",
  "C006-L04 local_wrapper_upstream_mathlib: exists_optimal_transportPlan_of_isCompact_lsc uses LowerSemicontinuousOn.exists_isMinOn on the compact coupling set.",
  "C006-L05 local_wrapper_upstream_mathlib: exists_optimal_transportPlan_of_compactMetric_lscTarget closes the compact-metric direct-method extraction once LowerSemicontinuousCostFunctionalTarget c is supplied.",
  "C006-L06 unchecked formalization_debt: the terminal McCann/Kantorovich theorem still depends on C005-L05, the general Portmanteau lower-semicontinuity theorem for lsc ENNReal costs."
]

/--
Search terms that did not locate a terminal McCann/Kantorovich existence theorem
in pinned mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "McCann",
  "OptimalTransport",
  "optimal transport",
  "Kantorovich",
  "Monge",
  "Wasserstein",
  "transport plan",
  "coupling",
  "cost minimizer",
  "exists optimal coupling"
]

/--
Machine-readable C007 external-anchor audit status.

This records the 2026-05-01 child pass outcome without claiming a theorem:
no completed external Lean 4 McCann/Kantorovich/Wasserstein/OptimalTransport
probability-transport existence proof was found or integrated, and authenticated
GitHub code search was blocked by the absence of a local `gh` login/token.
-/
def externalAnchorAuditC007 : List String := [
  "C007 external-anchor audit, 2026-05-01",
  "gh auth status: not logged in; no GH_TOKEN/GITHUB_TOKEN/GITHUB_PAT was present in the process environment",
  "GitHub REST repository search found no Lean repositories for OptimalTransport or Wasserstein and only an unrelated Newton-Kantorovich repository for Kantorovich",
  "GitHub REST code search was rate-limited without authentication, so absence from global GitHub code search is not proved",
  "local pinned mathlib search at 8a178386ffc0f5fef0b77738bb5449d50efeea95 found no terminal optimal-transport existence theorem",
  "no external Lean 4 proof body was pinned, imported, or checked in this child pass",
  "repo_local_integration_debt gate: no completed external proof was found; THM-M-1186 remains formalization_debt, not completed"
]

/--
Machine-readable C008 completion-gate status.

This child task is a guardrail: the terminal McCann/Kantorovich theorem must
remain unchecked until all local validation, anchor-audit, leaf-ledger,
public-merge, and metadata-consistency gates are closed.
-/
def completionGateLedgerC008 : List String := [
  "C008-G01 local Lean validation: checked for this file, but terminal StatementShape is not proved",
  "C008-G02 machine anchor audit: C007 found no completed external Lean 4 proof to pin/import/check; authenticated global code search remains an open public-doc task",
  "C008-G03 leaf ledger: C005-L05 remains unchecked formalization_debt for lsc ENNReal Portmanteau lower semicontinuity",
  "C008-G04 leaf ledger: C006-L06 remains unchecked formalization_debt because terminal McCann/Kantorovich existence depends on C005-L05",
  "C008-G05 public merge-back: not closed in this Lean artifact; serial integrator must update Stage1 blueprint/todo/README/meta surfaces",
  "C008-G06 README/meta/blueprint consistency: not closed by this child because shared public docs are outside the write scope",
  "C008-G07 repo_local_integration_debt: no completed anchor-only external proof is being claimed; any later external proof must be pinned/imported/checked or recorded as a blocker before completion"
]

/-- C008 does not claim terminal completion of THM-M-1186. -/
def terminalCompletionClaimC008 : Bool :=
  false

/-- The C008 terminal-completion marker is intentionally false. -/
theorem terminalCompletionClaimC008_eq_false :
    terminalCompletionClaimC008 = false :=
  rfl

/-! ## Audit probes -/

#check TransportPlan
#check TransportCost
#check ProbabilityTransportCost
#check transportCost_eq_lintegral
#check probabilityTransportCost_eq_transportCost
#check LowerSemicontinuousCostFunctionalTarget
#check probabilityTransportCost_continuous_boundedContinuous
#check probabilityTransportCost_lowerSemicontinuous_boundedContinuous
#check lowerSemicontinuousCostFunctionalTarget_boundedContinuous
#check IsOptimalTransportPlan
#check independentPlan
#check independentPlan_isProbability
#check nonempty_transportPlan
#check ProbabilityCouplingSet
#check TransportPlan.toProbabilityMeasure
#check transportPlan_toProbabilityMeasure_mem
#check TransportPlan.ofProbabilityMeasure
#check transportPlan_ofProbabilityMeasure_cost_eq
#check transportPlan_ofProbabilityMeasure_toProbabilityMeasure
#check independentProbabilityCoupling
#check independentProbabilityCoupling_mem
#check probabilityCouplingSet_nonempty
#check firstMarginalProbability
#check secondMarginalProbability
#check firstMarginalProbability_continuous
#check secondMarginalProbability_continuous
#check probabilityCouplingSet_eq_marginal_fibers
#check probabilityCouplingSet_isClosed_of_marginal_t2
#check probabilityCouplingSet_mem_of_mem_closure
#check probabilityCouplingSet_mem_of_tendsto
#check probabilityCouplingSet_mem_of_tendsto_levyProkhorov
#check probabilityCouplingSet_isTight_of_compactSpace
#check compactSpace_probabilityMeasure_prod_of_compactMetric
#check probabilityCouplingSet_closure_isCompact_of_compactMetric
#check probabilityCouplingSet_isCompact_of_compactMetric
#check exists_optimal_transportPlan_of_probabilityCoupling_minimizer
#check exists_optimal_transportPlan_of_isCompact_lsc
#check exists_optimal_transportPlan_of_compactMetric_lscTarget
#check OptimalTransportExistenceData
#check StatementShape
#check CompactMetricBorelScope
#check StatementShapeCompactMetric
#check exists_optimal_plan_of_data
#check costLowerSemicontinuityLeafLedger
#check directMethodMinimizerLeafLedger
#check externalAnchorAuditC007
#check completionGateLedgerC008
#check terminalCompletionClaimC008_eq_false
#check MeasureTheory.ProbabilityMeasure
#check MeasureTheory.levyProkhorovEDist
#check MeasureTheory.ProbabilityMeasure.continuous_lintegral_boundedContinuousFunction
#check LowerSemicontinuous

end AwesomeTheorems.Stage1.S1_M_151
