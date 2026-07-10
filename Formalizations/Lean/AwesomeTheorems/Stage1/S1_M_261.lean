import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Probability.ConditionalExpectation
import Mathlib.Probability.IdentDistrib
import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Martingale.Convergence
import Mathlib.Probability.Martingale.OptionalStopping
import Mathlib.Probability.Kernel.IonescuTulcea.Traj
import Mathlib.Probability.Process.FiniteDimensionalLaws
import Mathlib.Probability.Process.Kolmogorov
import Mathlib.Probability.Process.Stopping
import Mathlib.MeasureTheory.Measure.Portmanteau
import Mathlib.MeasureTheory.Measure.Prokhorov
import Mathlib.Probability.ProductMeasure

/-!
# S1-M-261 / THM-M-0981: Kolmogorov axioms

This Stage1 artifact records a conservative repo-local wrapper for the
Kolmogorov axiomatization of probability.  In mathlib, a probability space is
represented by a measurable space together with a `Measure` whose total mass is
one, encoded by `IsProbabilityMeasure`.  Countable additivity and positivity are
inherited from the `Measure` object itself.

The declarations below expose the textbook axiom clauses as a checked
`KolmogorovAxioms` predicate and add small wrappers for adjacent Stage1
probability interfaces: laws of random variables, push-forward probability
measures, independence, martingale/process infrastructure, and the existing
Kolmogorov-process condition used in stochastic-process regularity.
-/

noncomputable section

open Filter Function MeasureTheory ProbabilityTheory Set
open scoped ENNReal NNReal ProbabilityTheory MeasureTheory Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_261

universe u v w uT uE

/--
Pinned mathlib revision used for this Stage1 audit.

The public integration note should record that this revision represents the
core Kolmogorov probability axioms through `Measure` plus
`IsProbabilityMeasure`.
-/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Machine-status label for the checked core axiom wrapper: the repo-local proof
body imports and wraps theorem bodies from the pinned mathlib dependency.
-/
def coreAxiomMachineStatus : String :=
  "local_wrapper_upstream_mathlib"

/--
Textbook Kolmogorov probability axioms, expressed for a mathlib measure:
the empty event has probability zero, the whole sample space has probability
one, and countable unions of pairwise disjoint measurable events are additive.

Nonnegativity is part of the codomain `ℝ≥0∞` of `Measure`, so it is not an
extra field in this predicate.
-/
def KolmogorovAxioms {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) : Prop :=
  P ∅ = 0 ∧
    P univ = 1 ∧
      ∀ A : ℕ → Set Ω,
        (∀ n, MeasurableSet (A n)) →
          Pairwise (Disjoint on A) →
            P (⋃ n, A n) = ∑' n, P (A n)

/--
Normalized Stage1 statement shape: every mathlib probability measure satisfies
the explicit Kolmogorov axiom predicate above.
-/
def StatementShape (Ω : Type u) [MeasurableSpace Ω] : Prop :=
  ∀ P : Measure Ω, IsProbabilityMeasure P → KolmogorovAxioms P

/-- mathlib's `Measure` and `IsProbabilityMeasure` classes supply the axiom clauses. -/
theorem kolmogorovAxioms_of_isProbabilityMeasure
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P] :
    KolmogorovAxioms P := by
  refine ⟨by simp, by simp, ?_⟩
  intro A hmeas hdisj
  exact measure_iUnion hdisj hmeas

/-- Repo-local wrapper for the normalized statement shape. -/
theorem statementShape_mathlib_wrapper
    (Ω : Type u) [MeasurableSpace Ω] :
    StatementShape Ω := by
  intro P hP
  letI := hP
  exact kolmogorovAxioms_of_isProbabilityMeasure P

/-- The empty event has probability zero. -/
theorem probability_empty
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P] :
    P ∅ = 0 := by
  simp

/-- The whole sample space has probability one. -/
theorem probability_univ
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P] :
    P univ = 1 := by
  simp

/-- Countable additivity on pairwise disjoint measurable events. -/
theorem probability_iUnion_disjoint
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (A : ℕ → Set Ω) (hmeas : ∀ n, MeasurableSet (A n))
    (hdisj : Pairwise (Disjoint on A)) :
    P (⋃ n, A n) = ∑' n, P (A n) :=
  measure_iUnion hdisj hmeas

/-- Complement probabilities add to one for measurable events. -/
theorem probability_add_compl
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    {s : Set Ω} (hs : MeasurableSet s) :
    P s + P sᶜ = 1 :=
  prob_add_prob_compl (μ := P) hs

/-- A `ProbabilityMeasure` subtype also satisfies the explicit axiom predicate. -/
theorem probabilityMeasure_toMeasure_axioms
    {Ω : Type u} [MeasurableSpace Ω] (P : ProbabilityMeasure Ω) :
    KolmogorovAxioms (P : Measure Ω) :=
  kolmogorovAxioms_of_isProbabilityMeasure (P : Measure Ω)

/-- The law of a random variable is its push-forward measure. -/
theorem hasLaw_map
    {Ω : Type u} [MeasurableSpace Ω] {E : Type v} [MeasurableSpace E]
    {P : Measure Ω} {X : Ω → E} (hX : AEMeasurable X P) :
    HasLaw X (P.map X) P where
  aemeasurable := hX
  map_eq := rfl

/-- Push-forward along an almost-everywhere measurable random variable preserves probability. -/
theorem map_isProbabilityMeasure
    {Ω : Type u} [MeasurableSpace Ω] {E : Type v} [MeasurableSpace E]
    {P : Measure Ω} [IsProbabilityMeasure P] {X : Ω → E}
    (hX : AEMeasurable X P) :
    IsProbabilityMeasure (P.map X) :=
  Measure.isProbabilityMeasure_map hX

/-- Identically distributed random variables have equal Bochner expectations. -/
theorem identDistrib_integral_eq
    {Ω₁ : Type u} {Ω₂ : Type v} [MeasurableSpace Ω₁] [MeasurableSpace Ω₂]
    {E : Type w} [MeasurableSpace E] [NormedAddCommGroup E] [NormedSpace ℝ E] [BorelSpace E]
    {P₁ : Measure Ω₁} {P₂ : Measure Ω₂} {X : Ω₁ → E} {Y : Ω₂ → E}
    (hXY : IdentDistrib X Y P₁ P₂) :
    ∫ ω, X ω ∂P₁ = ∫ ω, Y ω ∂P₂ :=
  hXY.integral_eq

/-- Independence of two random variables is symmetric in mathlib. -/
theorem indepFun_symm
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} {F : Type w} [MeasurableSpace E] [MeasurableSpace F]
    {P : Measure Ω} {X : Ω → E} {Y : Ω → F} :
    IndepFun X Y P → IndepFun Y X P :=
  IndepFun.symm

/-- A martingale is strongly adapted to its filtration. -/
theorem martingale_stronglyAdapted
    {Ω : Type u} {E : Type v} {ι : Type w} [Preorder ι]
    {mΩ : MeasurableSpace Ω} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    {P : Measure Ω} {X : ι → Ω → E} {𝓕 : Filtration ι mΩ}
    (hX : Martingale X 𝓕 P) :
    StronglyAdapted 𝓕 X :=
  hX.stronglyAdapted

/-- A stochastic process satisfying mathlib's Kolmogorov condition is an AE Kolmogorov process. -/
theorem kolmogorovProcess_to_ae
    {T : Type uT} {Ω : Type u} {E : Type uE} [PseudoEMetricSpace T]
    [MeasurableSpace Ω] [PseudoEMetricSpace E]
    {P : Measure Ω} {X : T → Ω → E} {p q : ℝ} {M : ℝ≥0}
    (hX : IsKolmogorovProcess X P p q M) :
    IsAEKolmogorovProcess X P p q M :=
  hX.IsAEKolmogorovProcess

/-- The Kolmogorov-process condition includes measurability of each time slice. -/
theorem kolmogorovProcess_measurable
    {T : Type uT} {Ω : Type u} {E : Type uE} [PseudoEMetricSpace T]
    [MeasurableSpace Ω] [PseudoEMetricSpace E] [MeasurableSpace E] [BorelSpace E]
    {P : Measure Ω} {X : T → Ω → E} {p q : ℝ} {M : ℝ≥0}
    (hX : IsKolmogorovProcess X P p q M) (t : T) :
    Measurable (X t) :=
  hX.measurable t

/-! ## Stochastic-process audit wrappers -/

/--
Conditional expectation against an independent sigma algebra is almost surely constant.

This is a repo-local wrapper around `MeasureTheory.condExp_indep_eq` from
`Mathlib.Probability.ConditionalExpectation`.
-/
theorem conditionalExpectation_indep_eq
    {Ω : Type u} {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    {m₁ m₂ m : MeasurableSpace Ω} {P : Measure Ω} {f : Ω → E}
    (hle₁ : m₁ ≤ m) (hle₂ : m₂ ≤ m) [SigmaFinite (P.trim hle₂)]
    (hf : StronglyMeasurable[m₁] f) (hindp : Indep m₁ m₂ P) :
    P[f | m₂] =ᵐ[P] fun _ => P[f] :=
  condExp_indep_eq hle₁ hle₂ hf hindp

/-- Constant times are stopping times. -/
theorem stoppingTime_const
    {Ω : Type u} {ι : Type v} {m : MeasurableSpace Ω} [Preorder ι]
    (𝓕 : Filtration ι m) (i : ι) :
    IsStoppingTime 𝓕 fun _ => (i : WithTop ι) :=
  isStoppingTime_const 𝓕 i

/-- A stopping time has measurable level sets at each time. -/
theorem stoppingTime_measurableSet_eq
    {Ω : Type u} {ι : Type v} {m : MeasurableSpace Ω} [LinearOrder ι]
    [TopologicalSpace ι] [OrderTopology ι] [FirstCountableTopology ι]
    {𝓕 : Filtration ι m} {τ : Ω → WithTop ι}
    (hτ : IsStoppingTime 𝓕 τ) (i : ι) :
    MeasurableSet[𝓕 i] {ω | τ ω = i} :=
  hτ.measurableSet_eq i

/-- Forward direction of the finite discrete-time optional stopping theorem. -/
theorem submartingale_expected_stoppedValue_mono
    {Ω : Type u} {E : Type v} {m : MeasurableSpace Ω} {P : Measure Ω}
    {𝓕 : Filtration ℕ m} {τ π : Ω → ℕ∞}
    [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E] [PartialOrder E]
    [IsOrderedAddMonoid E] [IsOrderedModule ℝ E] [ClosedIciTopology E]
    [SigmaFiniteFiltration P 𝓕] {X : ℕ → Ω → E}
    (hX : Submartingale X 𝓕 P) (hτ : IsStoppingTime 𝓕 τ)
    (hπ : IsStoppingTime 𝓕 π) (hle : τ ≤ π)
    {N : ℕ} (hbdd : ∀ ω, π ω ≤ N) :
    P[stoppedValue X τ] ≤ P[stoppedValue X π] :=
  hX.expected_stoppedValue_mono hτ hπ hle hbdd

/-- The finite discrete-time optional stopping theorem as a characterization of submartingales. -/
theorem submartingale_iff_expected_stoppedValue_mono_wrapper
    {Ω : Type u} {m : MeasurableSpace Ω} {P : Measure Ω}
    {𝓕 : Filtration ℕ m} {X : ℕ → Ω → ℝ} [SigmaFiniteFiltration P 𝓕]
    (hadp : StronglyAdapted 𝓕 X) (hint : ∀ i, Integrable (X i) P) :
    Submartingale X 𝓕 P ↔
      ∀ τ π : Ω → ℕ∞,
        IsStoppingTime 𝓕 τ →
          IsStoppingTime 𝓕 π →
            τ ≤ π →
              (∃ N : ℕ, ∀ ω, π ω ≤ N) →
                P[stoppedValue X τ] ≤ P[stoppedValue X π] :=
  submartingale_iff_expected_stoppedValue_mono hadp hint

/-- Stopping a submartingale at a stopping time yields another submartingale. -/
theorem submartingale_stoppedProcess
    {Ω : Type u} {m : MeasurableSpace Ω} {P : Measure Ω}
    {𝓕 : Filtration ℕ m} {X : ℕ → Ω → ℝ} {τ : Ω → ℕ∞}
    [SigmaFiniteFiltration P 𝓕]
    (hX : Submartingale X 𝓕 P) (hτ : IsStoppingTime 𝓕 τ) :
    Submartingale (stoppedProcess X τ) 𝓕 P :=
  hX.stoppedProcess hτ

/-- Almost-everywhere convergence theorem for L¹-bounded submartingales. -/
theorem submartingale_ae_tendsto_limitProcess
    {Ω : Type u} {m : MeasurableSpace Ω} {P : Measure Ω}
    {𝓕 : Filtration ℕ m} {X : ℕ → Ω → ℝ} {R : ℝ≥0}
    [IsFiniteMeasure P]
    (hX : Submartingale X 𝓕 P) (hbdd : ∀ n, eLpNorm (X n) 1 P ≤ R) :
    ∀ᵐ ω ∂P, Tendsto (fun n => X n ω) atTop (𝓝 (𝓕.limitProcess X P ω)) :=
  hX.ae_tendsto_limitProcess hbdd

/-- L¹ martingale convergence theorem, conditional-expectation form. -/
theorem martingale_ae_eq_condExp_limitProcess
    {Ω : Type u} {m : MeasurableSpace Ω} {P : Measure Ω}
    {𝓕 : Filtration ℕ m} {X : ℕ → Ω → ℝ}
    [IsFiniteMeasure P]
    (hX : Martingale X 𝓕 P) (hbdd : UniformIntegrable X 1 P) (n : ℕ) :
    X n =ᵐ[P] P[𝓕.limitProcess X P | 𝓕 n] :=
  hX.ae_eq_condExp_limitProcess hbdd n

/-- Portmanteau implication: weak convergence gives the closed-set limsup bound. -/
theorem portmanteau_limsup_measure_closed_le_of_tendsto
    {Ω : Type u} {ι : Type v} {L : Filter ι}
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω] [HasOuterApproxClosed Ω]
    {P : ProbabilityMeasure Ω} {Ps : ι → ProbabilityMeasure Ω}
    (hPs : Tendsto Ps L (𝓝 P)) {F : Set Ω} (hF : IsClosed F) :
    L.limsup (fun i => (Ps i : Measure Ω) F) ≤ (P : Measure Ω) F :=
  ProbabilityMeasure.limsup_measure_closed_le_of_tendsto hPs hF

/-- Portmanteau implication: weak convergence gives the open-set liminf bound. -/
theorem portmanteau_le_liminf_measure_open_of_tendsto
    {Ω : Type u} {ι : Type v} {L : Filter ι}
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω] [HasOuterApproxClosed Ω]
    {P : ProbabilityMeasure Ω} {Ps : ι → ProbabilityMeasure Ω}
    (hPs : Tendsto Ps L (𝓝 P)) {G : Set Ω} (hG : IsOpen G) :
    (P : Measure Ω) G ≤ L.liminf (fun i => (Ps i : Measure Ω) G) :=
  ProbabilityMeasure.le_liminf_measure_open_of_tendsto hPs hG

/-- Portmanteau implication for Borel sets whose frontier has zero limiting mass. -/
theorem portmanteau_tendsto_measure_of_null_frontier
    {Ω : Type u} {ι : Type v} {L : Filter ι}
    [MeasurableSpace Ω] [TopologicalSpace Ω] [OpensMeasurableSpace Ω] [HasOuterApproxClosed Ω]
    {P : ProbabilityMeasure Ω} {Ps : ι → ProbabilityMeasure Ω}
    (hPs : Tendsto Ps L (𝓝 P)) {E : Set Ω} (hE : P (frontier E) = 0) :
    Tendsto (fun i => Ps i E) L (𝓝 (P E)) :=
  ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto hPs hE

/-- Prokhorov theorem wrapper: the closure of a tight set of probability measures is compact. -/
theorem prokhorov_isCompact_closure_of_isTightMeasureSet
    {E : Type u} [MeasurableSpace E] [TopologicalSpace E] [T2Space E] [BorelSpace E]
    {S : Set (ProbabilityMeasure E)}
    (hS : IsTightMeasureSet {((P : ProbabilityMeasure E) : Measure E) | P ∈ S}) :
    IsCompact (closure S) :=
  isCompact_closure_of_isTightMeasureSet hS

/-! ## Stochastic-process audit metadata -/

/-- Audit rows for next-round stochastic-process wrapper backfill. -/
structure StochasticProcessAuditFinding where
  id : String
  moduleName : String
  anchorNames : List String
  repoLocalResult : String
  conclusion : String

/-- Checked audit findings for conditional expectation, stopping, martingales, Portmanteau, and Prokhorov. -/
def stochasticProcessAuditFindings : List StochasticProcessAuditFinding := [
  {
    id := "M0981-L015-conditional-expectation",
    moduleName := "Mathlib.Probability.ConditionalExpectation",
    anchorNames := [
      "MeasureTheory.condExp_indep_eq"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Conditional expectation has a checked independent-sigma-algebra wrapper; tower-property wrappers remain a next-round candidate."
  },
  {
    id := "M0981-L016-stopping",
    moduleName := "Mathlib.Probability.Process.Stopping",
    anchorNames := [
      "MeasureTheory.isStoppingTime_const",
      "MeasureTheory.IsStoppingTime.measurableSet_eq"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Stopping-time definition and basic measurable-level-set wrappers are repo-locally checked."
  },
  {
    id := "M0981-L016-optional-stopping",
    moduleName := "Mathlib.Probability.Martingale.OptionalStopping",
    anchorNames := [
      "MeasureTheory.Submartingale.expected_stoppedValue_mono",
      "MeasureTheory.submartingale_iff_expected_stoppedValue_mono",
      "MeasureTheory.Submartingale.stoppedProcess"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Finite discrete-time optional-stopping and stopped-process wrappers are repo-locally checked."
  },
  {
    id := "M0981-L017-martingale-convergence",
    moduleName := "Mathlib.Probability.Martingale.Convergence",
    anchorNames := [
      "MeasureTheory.Submartingale.ae_tendsto_limitProcess",
      "MeasureTheory.Martingale.ae_eq_condExp_limitProcess"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Almost-everywhere submartingale convergence and L1 martingale conditional-expectation convergence wrappers are repo-locally checked."
  },
  {
    id := "M0981-L020-portmanteau",
    moduleName := "Mathlib.MeasureTheory.Measure.Portmanteau",
    anchorNames := [
      "MeasureTheory.ProbabilityMeasure.limsup_measure_closed_le_of_tendsto",
      "MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto",
      "MeasureTheory.ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Portmanteau closed-set, open-set, and null-frontier implications for probability measures are repo-locally checked."
  },
  {
    id := "M0981-L020-prokhorov",
    moduleName := "Mathlib.MeasureTheory.Measure.Prokhorov",
    anchorNames := [
      "MeasureTheory.isCompact_closure_of_isTightMeasureSet"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Prokhorov compactness of the closure of a tight set of probability measures is repo-locally checked."
  }
]

/-- Stochastic-process audit rows cover the six scoped findings above. -/
theorem stochasticProcessAuditFindings_length :
    stochasticProcessAuditFindings.length = 6 :=
  rfl

/-- Additional wrapper theorem names checked by the stochastic-process audit child. -/
def stochasticProcessCheckedWrapperTheoremNames : List String := [
  "conditionalExpectation_indep_eq",
  "stoppingTime_const",
  "stoppingTime_measurableSet_eq",
  "submartingale_expected_stoppedValue_mono",
  "submartingale_iff_expected_stoppedValue_mono_wrapper",
  "submartingale_stoppedProcess",
  "submartingale_ae_tendsto_limitProcess",
  "martingale_ae_eq_condExp_limitProcess",
  "portmanteau_limsup_measure_closed_le_of_tendsto",
  "portmanteau_le_liminf_measure_open_of_tendsto",
  "portmanteau_tendsto_measure_of_null_frontier",
  "prokhorov_isCompact_closure_of_isTightMeasureSet"
]

/-! ## Product-process existence audit anchors -/

/-! ## Product-process existence audit anchors -/

/--
The arbitrary product of a family of probability measures is itself a probability measure.

This is a repo-local wrapper around `Measure.infinitePi` from `Probability.ProductMeasure`.
-/
theorem productMeasure_infinitePi_isProbabilityMeasure
    {ι : Type u} {X : ι → Type v} [∀ i, MeasurableSpace (X i)]
    (μ : (i : ι) → Measure (X i)) [∀ i, IsProbabilityMeasure (μ i)] :
    IsProbabilityMeasure (Measure.infinitePi μ) := by
  infer_instance

/--
`Measure.infinitePi` is the projective limit of its finite-dimensional product marginals.
-/
theorem productMeasure_infinitePi_projectiveLimit
    {ι : Type u} {X : ι → Type v} [∀ i, MeasurableSpace (X i)]
    (μ : (i : ι) → Measure (X i)) [∀ i, IsProbabilityMeasure (μ i)] :
    IsProjectiveLimit (Measure.infinitePi μ)
      (fun I : Finset ι => Measure.pi (fun i : I => μ i)) :=
  Measure.isProjectiveLimit_infinitePi μ

/-- Finite-coordinate restrictions of `Measure.infinitePi` are ordinary finite product measures. -/
theorem productMeasure_infinitePi_map_restrict
    {ι : Type u} {X : ι → Type v} [∀ i, MeasurableSpace (X i)]
    (μ : (i : ι) → Measure (X i)) [∀ i, IsProbabilityMeasure (μ i)]
    {I : Finset ι} :
    (Measure.infinitePi μ).map I.restrict = Measure.pi (fun i : I => μ i) :=
  Measure.infinitePi_map_restrict μ

/-- The `Measure.infinitePi` value on a finite measurable box is the product of coordinates. -/
theorem productMeasure_infinitePi_pi
    {ι : Type u} {X : ι → Type v} [∀ i, MeasurableSpace (X i)]
    (μ : (i : ι) → Measure (X i)) [∀ i, IsProbabilityMeasure (μ i)]
    {s : Finset ι} {t : (i : ι) → Set (X i)}
    (ht : ∀ i ∈ s, MeasurableSet (t i)) :
    Measure.infinitePi μ (Set.pi s t) = ∏ i ∈ s, μ i (t i) :=
  Measure.infinitePi_pi μ ht

/-- Coordinate evaluation under `Measure.infinitePi` has the corresponding coordinate law. -/
theorem productMeasure_infinitePi_map_eval
    {ι : Type u} {X : ι → Type v} [∀ i, MeasurableSpace (X i)]
    (μ : (i : ι) → Measure (X i)) [∀ i, IsProbabilityMeasure (μ i)]
    (i : ι) :
    (Measure.infinitePi μ).map (fun x => x i) = μ i :=
  Measure.infinitePi_map_eval μ i

/-- The Ionescu-Tulcea trajectory construction returns a Markov kernel. -/
theorem ionescuTulcea_traj_isMarkovKernel
    {X : ℕ → Type u} [∀ n, MeasurableSpace (X n)]
    (κ : (n : ℕ) → Kernel (Π i : Finset.Iic n, X i) (X (n + 1)))
    [∀ n, IsMarkovKernel (κ n)] (a : ℕ) :
    IsMarkovKernel (Kernel.traj κ a) := by
  infer_instance

/-- The next-coordinate marginal of `Kernel.traj` is the one-step transition kernel. -/
theorem ionescuTulcea_traj_map_succ_self
    {X : ℕ → Type u} [∀ n, MeasurableSpace (X n)]
    {κ : (n : ℕ) → Kernel (Π i : Finset.Iic n, X i) (X (n + 1))}
    [∀ n, IsMarkovKernel (κ n)] {a : ℕ} :
    (Kernel.traj κ a).map (fun x => x (a + 1)) = κ a :=
  Kernel.map_traj_succ_self

/-- Finite restrictions of an Ionescu-Tulcea trajectory kernel recover `partialTraj`. -/
theorem ionescuTulcea_traj_map_frestrictLe
    {X : ℕ → Type u} [∀ n, MeasurableSpace (X n)]
    {κ : (n : ℕ) → Kernel (Π i : Finset.Iic n, X i) (X (n + 1))}
    [∀ n, IsMarkovKernel (κ n)] (a b : ℕ) :
    (Kernel.traj κ a).map (Preorder.frestrictLe b) = Kernel.partialTraj κ a b :=
  Kernel.traj_map_frestrictLe a b

/-- The trajectory measure generated from an initial law and Markov kernels is probabilistic. -/
theorem ionescuTulcea_trajMeasure_isProbabilityMeasure
    {X : ℕ → Type u} [∀ n, MeasurableSpace (X n)]
    (μ₀ : Measure (X 0)) [IsProbabilityMeasure μ₀]
    (κ : (n : ℕ) → Kernel (Π i : Finset.Iic n, X i) (X (n + 1)))
    [∀ n, IsMarkovKernel (κ n)] :
    IsProbabilityMeasure (Kernel.trajMeasure μ₀ κ) := by
  infer_instance

/--
Finite-dimensional distributions of an existing stochastic process form a projective family.

This supports the candidate Kolmogorov-extension audit boundary: it is a checked direction
from process to consistent finite-dimensional laws, not a construction of a process from laws.
-/
theorem finiteDimensionalLaws_isProjectiveMeasureFamily
    {T : Type uT} {Ω : Type u} {𝓧 : T → Type uE}
    [MeasurableSpace Ω] [∀ t, MeasurableSpace (𝓧 t)]
    {X : (t : T) → Ω → 𝓧 t} {P : Measure Ω}
    (hX : ∀ t, AEMeasurable (X t) P) :
    IsProjectiveMeasureFamily (fun I : Finset T => P.map (fun ω => I.restrict (X · ω))) :=
  isProjectiveMeasureFamily_map_restrict hX

/-- The law of an existing process is the projective limit of its finite-dimensional laws. -/
theorem finiteDimensionalLaws_isProjectiveLimit
    {T : Type uT} {Ω : Type u} {𝓧 : T → Type uE}
    [MeasurableSpace Ω] [∀ t, MeasurableSpace (𝓧 t)]
    {X : (t : T) → Ω → 𝓧 t} {P : Measure Ω}
    (hX : AEMeasurable (fun ω => (X · ω)) P) :
    IsProjectiveLimit (P.map (fun ω => (X · ω)))
      (fun I : Finset T => P.map (fun ω => I.restrict (X · ω))) :=
  isProjectiveLimit_map hX

/--
Uniqueness of finite-measure projective limits is available in pinned mathlib.

This is not an existence theorem; it is recorded to keep the public closure gate precise.
-/
theorem projectiveLimit_unique
    {ι : Type u} {X : ι → Type v} [∀ i, MeasurableSpace (X i)]
    {P : (J : Finset ι) → Measure (Π j : J, X j)}
    {μ ν : Measure (Π i, X i)} [∀ J, IsFiniteMeasure (P J)]
    (hμ : IsProjectiveLimit μ P) (hν : IsProjectiveLimit ν P) :
    μ = ν :=
  hμ.unique hν

/-- Product-process audit rows for the serialized public backfill. -/
structure ProductProcessAuditFinding where
  id : String
  moduleName : String
  anchorNames : List String
  repoLocalResult : String
  conclusion : String

/--
Audit conclusion for the product-process existence branch.

The checked rows cover arbitrary independent product measures, Ionescu-Tulcea sequence kernels,
finite-dimensional laws of an already existing process, and projective-limit uniqueness. They do
not expose a repo-local wrapper for a full Kolmogorov extension theorem constructing a process from
an arbitrary consistent family of finite-dimensional distributions.
-/
def productProcessAuditFindings : List ProductProcessAuditFinding := [
  {
    id := "M0981-L018-product-measure",
    moduleName := "Mathlib.Probability.ProductMeasure",
    anchorNames := [
      "Measure.infinitePi",
      "Measure.isProjectiveLimit_infinitePi",
      "Measure.infinitePi_map_restrict",
      "Measure.infinitePi_pi",
      "Measure.infinitePi_map_eval"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Arbitrary independent products of probability measures are repo-locally wrapped and checked."
  },
  {
    id := "M0981-L018-ionescu-tulcea",
    moduleName := "Mathlib.Probability.Kernel.IonescuTulcea.Traj",
    anchorNames := [
      "Kernel.traj",
      "Kernel.map_traj_succ_self",
      "Kernel.traj_map_frestrictLe",
      "Kernel.trajMeasure"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Sequence-indexed Markov-kernel trajectory construction is repo-locally wrapped and checked."
  },
  {
    id := "M0981-L019-finite-dimensional-laws",
    moduleName := "Mathlib.Probability.Process.FiniteDimensionalLaws",
    anchorNames := [
      "isProjectiveMeasureFamily_map_restrict",
      "isProjectiveLimit_map"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Existing-process finite-dimensional laws are projective and have the process law as projective limit."
  },
  {
    id := "M0981-L019-projective-uniqueness",
    moduleName := "Mathlib.MeasureTheory.Constructions.Projective",
    anchorNames := [
      "IsProjectiveMeasureFamily",
      "IsProjectiveLimit",
      "IsProjectiveLimit.unique"
    ],
    repoLocalResult := "local_wrapper_upstream_mathlib",
    conclusion :=
      "Projective-limit definitions and finite-measure uniqueness are checked; no general existence wrapper is claimed."
  },
  {
    id := "M0981-L019-kolmogorov-extension",
    moduleName := "pinned mathlib audit boundary",
    anchorNames := [
      "ProjectiveFamilyContent documentation reference",
      "ClosedCompactCylinders documentation reference"
    ],
    repoLocalResult := "not_repo_local_closed",
    conclusion :=
      "No repo-local checked theorem in this artifact constructs a process from an arbitrary consistent family of finite-dimensional distributions."
  }
]

/-- Product-process audit rows cover the five scoped findings above. -/
theorem productProcessAuditFindings_length :
    productProcessAuditFindings.length = 5 :=
  rfl

/-- Additional wrapper theorem names checked by the product-process child audit. -/
def productProcessCheckedWrapperTheoremNames : List String := [
  "productMeasure_infinitePi_isProbabilityMeasure",
  "productMeasure_infinitePi_projectiveLimit",
  "productMeasure_infinitePi_map_restrict",
  "productMeasure_infinitePi_pi",
  "productMeasure_infinitePi_map_eval",
  "ionescuTulcea_traj_isMarkovKernel",
  "ionescuTulcea_traj_map_succ_self",
  "ionescuTulcea_traj_map_frestrictLe",
  "ionescuTulcea_trajMeasure_isProbabilityMeasure",
  "finiteDimensionalLaws_isProjectiveMeasureFamily",
  "finiteDimensionalLaws_isProjectiveLimit",
  "projectiveLimit_unique"
]

/--
Closure decision for product-process existence.

The available product-measure, Ionescu-Tulcea, finite-dimensional-law, and uniqueness anchors are
checked in this repo. Full Kolmogorov extension from arbitrary consistent finite-dimensional laws
remains open for public status purposes until a construction theorem is located and wrapped, or a
concrete upstream integration blocker is recorded by the serialized integrator.
-/
def productProcessExistenceClosureDecision : String :=
  "open_not_completed_no_general_kolmogorov_extension_wrapper"

/-- Wrapper theorem names checked by this Stage1 artifact. -/
def checkedWrapperTheoremNames : List String := [
  "kolmogorovAxioms_of_isProbabilityMeasure",
  "statementShape_mathlib_wrapper",
  "probability_iUnion_disjoint",
  "probability_add_compl",
  "probabilityMeasure_toMeasure_axioms",
  "hasLaw_map",
  "map_isProbabilityMeasure",
  "identDistrib_integral_eq",
  "indepFun_symm",
  "martingale_stronglyAdapted",
  "kolmogorovProcess_to_ae",
  "kolmogorovProcess_measurable",
  "conditionalExpectation_indep_eq",
  "stoppingTime_const",
  "stoppingTime_measurableSet_eq",
  "submartingale_expected_stoppedValue_mono",
  "submartingale_iff_expected_stoppedValue_mono_wrapper",
  "submartingale_stoppedProcess",
  "submartingale_ae_tendsto_limitProcess",
  "martingale_ae_eq_condExp_limitProcess",
  "portmanteau_limsup_measure_closed_le_of_tendsto",
  "portmanteau_le_liminf_measure_open_of_tendsto",
  "portmanteau_tendsto_measure_of_null_frontier",
  "prokhorov_isCompact_closure_of_isTightMeasureSet"
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Measure.Typeclasses.Probability",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.MeasureSpace",
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.ConditionalExpectation",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Kernel.IonescuTulcea.Traj",
  "Mathlib.Probability.Process.FiniteDimensionalLaws",
  "Mathlib.Probability.ProductMeasure",
  "Mathlib.MeasureTheory.Constructions.Projective",
  "Mathlib.MeasureTheory.Constructions.ProjectiveFamilyContent",
  "Mathlib.MeasureTheory.Constructions.ClosedCompactCylinders",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Measure.Prokhorov"
]

/-- Search terms used for the terminal-audit boundary. -/
def anchorSearchTerms : List String := [
  "IsProbabilityMeasure",
  "ProbabilityMeasure",
  "measure_iUnion",
  "Kolmogorov axioms",
  "Kolmogorov extension",
  "IsKolmogorovProcess",
  "HasLaw",
  "IdentDistrib",
  "IndepFun",
  "Filtration",
  "IsStoppingTime",
  "Martingale",
  "Submartingale.expected_stoppedValue_mono",
  "Submartingale.ae_tendsto_limitProcess",
  "Martingale.ae_eq_condExp_limitProcess",
  "Portmanteau",
  "Prokhorov",
  "Measure.infinitePi",
  "Kernel.traj",
  "Ionescu-Tulcea",
  "finite-dimensional distributions",
  "IsProjectiveLimit",
  "Kolmogorov extension"
]

/--
Public theorem-tree package inventory proposed for `S1-M-261-C005`.

The entries are metadata for the serialized public-doc backfill.  They are
kept in the checked Lean artifact so the package ids can be audited without
editing shared public planning docs from a parallel child worker.
-/
structure PublicBackfillPackage where
  id : String
  label : String
  summary : String

/-- Unchecked public leaf inventory proposed for `S1-M-261-C005`. -/
structure PublicBackfillLeaf where
  id : String
  packageId : String
  target : String
  budget : Nat

/-- Theorem-tree packages `M0981.P0` through `M0981.P7`. -/
def m0981PublicBackfillPackages : List PublicBackfillPackage := [
  {
    id := "M0981.P0",
    label := "statement_normalization",
    summary :=
      "Freeze the sample space, measurable space, probability measure, event type, and explicit axiom predicate."
  },
  {
    id := "M0981.P1",
    label := "measure_probability_core",
    summary :=
      "Verify empty event, total mass one, countable additivity, complement identity, and the ProbabilityMeasure subtype bridge."
  },
  {
    id := "M0981.P2",
    label := "random_variable_law_expectation",
    summary :=
      "Bridge random variables to push-forward laws, probability preservation, identical distribution, and expectation equality."
  },
  {
    id := "M0981.P3",
    label := "independence_interfaces",
    summary :=
      "Audit IndepFun, iIndepFun, independent sigma-algebras, finite-family product identities, and process independence."
  },
  {
    id := "M0981.P4",
    label := "filtration_stopping_martingale",
    summary :=
      "Audit filtrations, adaptedness, stopping times, conditional expectation, martingale definitions, and optional-stopping/convergence theorem anchors."
  },
  {
    id := "M0981.P5",
    label := "product_process_existence",
    summary :=
      "Audit finite/infinite product measures, kernels, Ionescu-Tulcea, and possible Kolmogorov extension branches."
  },
  {
    id := "M0981.P6",
    label := "convergence_tightness",
    summary :=
      "Audit convergence in distribution, Portmanteau, Levy/Prokhorov, tightness, and finite/discrete special cases."
  },
  {
    id := "M0981.P7",
    label := "repo_local_gate",
    summary :=
      "Require any stronger upstream Lean proof to be pinned/imported/checked or blocked explicitly before public status closure."
  }
]

/-- Unchecked leaves `M0981-L014` through `M0981-L023` for public backfill. -/
def m0981UncheckedPublicBackfillLeaves : List PublicBackfillLeaf := [
  {
    id := "M0981-L014",
    packageId := "M0981.P3",
    target :=
      "Audit finite-family iIndepFun product/intersection identities and decide which public child wrapper should be added next.",
    budget := 80
  },
  {
    id := "M0981-L015",
    packageId := "M0981.P4",
    target :=
      "Audit ConditionalExpectation theorem names for law-of-total-expectation and tower-property wrappers.",
    budget := 100
  },
  {
    id := "M0981-L016",
    packageId := "M0981.P4",
    target := "Audit IsStoppingTime and optional-stopping wrappers for finite discrete-time special cases.",
    budget := 100
  },
  {
    id := "M0981-L017",
    packageId := "M0981.P4",
    target := "Audit martingale convergence anchors and choose minimal validated wrappers.",
    budget := 100
  },
  {
    id := "M0981-L018",
    packageId := "M0981.P5",
    target :=
      "Audit Measure.infinitePi, Measure.infinitePiNat, kernels, and Ionescu-Tulcea theorem names for product/process existence.",
    budget := 100
  },
  {
    id := "M0981-L019",
    packageId := "M0981.P5",
    target :=
      "Determine whether a genuine Kolmogorov extension theorem is present in pinned mathlib or remains a formalization task.",
    budget := 100
  },
  {
    id := "M0981-L020",
    packageId := "M0981.P6",
    target :=
      "Audit Portmanteau, Levy convergence, and Prokhorov tightness wrappers relevant to Stage1 convergence scope.",
    budget := 100
  },
  {
    id := "M0981-L021",
    packageId := "M0981.P6",
    target := "Add finite/discrete-state special-case wrappers if required by the public Stage1 item.",
    budget := 90
  },
  {
    id := "M0981-L022",
    packageId := "M0981.P7",
    target :=
      "If a stronger external Lean 4 proof is found, pin/import/check it or record concrete integration blocker.",
    budget := 80
  },
  {
    id := "M0981-L023",
    packageId := "M0981.P7",
    target := "Merge public theorem tree, status, and validation record only after integrator-owned public-surface patch.",
    budget := 60
  }
]

/-- The public package backfill has exactly the requested `P0` through `P7` entries. -/
theorem m0981PublicBackfillPackages_length :
    m0981PublicBackfillPackages.length = 8 :=
  rfl

/-- The unchecked public leaf backfill has exactly `L014` through `L023`. -/
theorem m0981UncheckedPublicBackfillLeaves_length :
    m0981UncheckedPublicBackfillLeaves.length = 10 :=
  rfl

/-- Every unchecked public-backfill leaf remains within the M0387 `<=100` budget. -/
theorem m0981UncheckedPublicBackfillLeaves_all_le_100 :
    m0981UncheckedPublicBackfillLeaves.all (fun leaf => leaf.budget <= 100) = true :=
  rfl

/-! ## C008 shared-import aggregation decision -/

/--
Serialized import-aggregator decision for `S1-M-261-C008`.

Parallel child workers must not edit shared Lean aggregators.  This record keeps the
decision in the owned Stage1 artifact so an integrator can apply it later with a
single shared-surface patch.
-/
structure SharedImportAggregatorDecision where
  targetImport : String
  currentSharedAggregator : String
  directValidationCommand : String
  childEditedSharedAggregator : Bool
  addInChildPatch : Bool
  integratorRecommendation : String
  requiredIfAdded : String

/--
C008 decision: do not add this Stage1 file to the shared aggregator from the child patch.

The file is already directly validated by the Stage1 per-file command.  A later serialized
integrator may add the import, but that patch must also validate the shared aggregator/build
surface because `AwesomeTheorems.lean` is public shared infrastructure.
-/
def c008SharedImportAggregatorDecision : SharedImportAggregatorDecision where
  targetImport := "import AwesomeTheorems.Stage1.S1_M_261"
  currentSharedAggregator := "Formalizations/Lean/AwesomeTheorems.lean"
  directValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_261.lean"
  childEditedSharedAggregator := false
  addInChildPatch := false
  integratorRecommendation :=
    "Keep S1_M_261 as a directly validated Stage1 artifact in this child pass; add the import only in a serialized integrator patch after reviewing shared build scope."
  requiredIfAdded :=
    "If the serialized integrator adds `import AwesomeTheorems.Stage1.S1_M_261`, rerun both `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_261.lean` and `cd Formalizations/Lean && lake build`."

/-- C008 did not edit the shared Lean import aggregator. -/
theorem c008SharedImportAggregatorDecision_no_child_aggregator_edit :
    c008SharedImportAggregatorDecision.childEditedSharedAggregator = false :=
  rfl

/-- C008 records that any aggregator import must be a later serialized patch. -/
theorem c008SharedImportAggregatorDecision_no_child_import :
    c008SharedImportAggregatorDecision.addInChildPatch = false :=
  rfl

/-! ## Audit probes -/

#check KolmogorovAxioms
#check StatementShape
#check IsProbabilityMeasure
#check ProbabilityMeasure
#check measure_iUnion
#check prob_add_prob_compl
#check HasLaw
#check IdentDistrib
#check IndepFun
#check Filtration
#check IsStoppingTime
#check Martingale
#check IsKolmogorovProcess
#check Measure.infinitePi
#check Measure.isProjectiveLimit_infinitePi
#check Measure.infinitePi_map_restrict
#check ProbabilityTheory.Kernel.traj
#check ProbabilityTheory.Kernel.trajMeasure
#check ProbabilityTheory.isProjectiveMeasureFamily_map_restrict
#check ProbabilityTheory.isProjectiveLimit_map
#check IsProjectiveLimit.unique
#check SharedImportAggregatorDecision
#check c008SharedImportAggregatorDecision

end S1_M_261
end Stage1
end AwesomeTheorems
