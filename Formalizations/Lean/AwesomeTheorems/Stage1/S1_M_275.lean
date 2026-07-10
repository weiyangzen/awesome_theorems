import Mathlib.Probability.Moments.SubGaussian
import Mathlib.Probability.Moments.Variance

/-!
# S1-M-275 / THM-M-0995: Bernstein inequality

This Stage1 artifact records a conservative Lean 4 boundary for the Bernstein
tail inequality for sums of independent bounded real random variables.

The pinned mathlib snapshot has moment-generating functions, Chernoff bounds,
sub-Gaussian Hoeffding/Azuma-Hoeffding bounds, independence, variance, and
Chebyshev anchors.  It does not expose a terminal theorem named as Bernstein's
inequality for bounded independent summands.  The declarations below therefore
freeze a statement shape and add checked wrappers around the available mathlib
anchors.  No terminal Bernstein proof is claimed here.
-/

noncomputable section

open Finset MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_275

universe u

/-- Finite partial sum of a real stochastic process. -/
def partialSum {Ω : Type u} (n : ℕ) (X : ℕ → Ω → ℝ) (ω : Ω) : ℝ :=
  ∑ i ∈ Finset.range n, X i ω

/--
Data package for the classical bounded-summand Bernstein inequality.

`varianceBudget` represents an upper bound for the sum of variances, and
`bound` represents a common almost-sure bound on `|X_i|`.
-/
structure BernsteinBoundedProblem (Ω : Type u) [MeasurableSpace Ω] : Type u where
  μ : Measure Ω
  n : ℕ
  X : ℕ → Ω → ℝ
  varianceBudget : ℝ
  bound : ℝ
  isProbability : IsProbabilityMeasure μ
  varianceBudget_nonneg : 0 ≤ varianceBudget
  bound_nonneg : 0 ≤ bound
  aemeasurable : ∀ i, i < n → AEMeasurable (X i) μ
  memLp_two : ∀ i, i < n → MemLp (X i) 2 μ
  independent : iIndepFun X μ
  mean_zero : ∀ i, i < n → μ[X i] = 0
  abs_bound_ae : ∀ i, i < n → ∀ᵐ ω ∂μ, |X i ω| ≤ bound
  variance_sum_le : (∑ i ∈ Finset.range n, Var[X i; μ]) ≤ varianceBudget

/-- Upper-tail event for the finite sum. -/
def upperTail {Ω : Type u} [MeasurableSpace Ω]
    (P : BernsteinBoundedProblem Ω) (t : ℝ) : Set Ω :=
  {ω | t ≤ partialSum P.n P.X ω}

/--
Public Stage1 tail-form choices for the normalized Bernstein target.

The current checked statement shape selects `oneSidedUpper`.  Lower-tail and
two-sided absolute-tail forms should be added only as separate checked variants,
not silently folded into this statement boundary.
-/
inductive NormalizedTailTarget : Type
  | oneSidedUpper
  | oneSidedLower
  | twoSidedAbsolute
  deriving DecidableEq

/-- Public normalized Bernstein target selected for THM-M-0995. -/
def publicNormalizedTailTarget : NormalizedTailTarget :=
  NormalizedTailTarget.oneSidedUpper

/--
Human-readable public-doc text synchronized with the checked Stage1 statement.
-/
def publicNormalizedTailTargetProse : String :=
  "one-sided upper-tail Bernstein bound: P(S_n >= t) <= exp(-t^2 / (2 * (v + c*t/3))) for t >= 0"

/-- Classical one-sided Bernstein exponential bound. -/
def bernsteinUpperBound (varianceBudget bound t : ℝ) : ℝ :=
  Real.exp (-(t ^ 2) / (2 * (varianceBudget + bound * t / 3)))

/--
Bernstein upper-tail conclusion for centered independent bounded summands.

This is a statement boundary only.  The Bernstein-specific bridge from the
bounded-variance hypotheses to this exponential tail bound is not present as a
checked local proof in this Stage1 artifact.
-/
def BernsteinTailConclusion {Ω : Type u} [MeasurableSpace Ω]
    (P : BernsteinBoundedProblem Ω) : Prop :=
  ∀ t : ℝ, 0 ≤ t →
    P.μ.real (upperTail P t) ≤
      bernsteinUpperBound P.varianceBudget P.bound t

/--
Stage1 normalized statement-shape candidate for Bernstein's inequality.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ P : BernsteinBoundedProblem Ω,
      BernsteinTailConclusion P

/-- The statement-shape definition unfolds to the normalized Bernstein form. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ P : BernsteinBoundedProblem Ω,
          BernsteinTailConclusion P :=
  Iff.rfl

/-- Checked synchronization between the public target decision and `StatementShape`. -/
theorem statementShape_is_public_oneSidedUpper :
    publicNormalizedTailTarget = NormalizedTailTarget.oneSidedUpper ∧
      (StatementShape.{u} ↔
        ∀ (Ω : Type u) [MeasurableSpace Ω],
          ∀ P : BernsteinBoundedProblem Ω,
            ∀ t : ℝ, 0 ≤ t →
              P.μ.real (upperTail P t) ≤
                bernsteinUpperBound P.varianceBudget P.bound t) :=
  ⟨rfl, Iff.rfl⟩

/-- The data package exposes the checked probability-measure hypothesis. -/
theorem isProbability {Ω : Type u} [MeasurableSpace Ω]
    (P : BernsteinBoundedProblem Ω) :
    IsProbabilityMeasure P.μ :=
  P.isProbability

/-- The data package exposes the checked independent-process hypothesis. -/
theorem independent {Ω : Type u} [MeasurableSpace Ω]
    (P : BernsteinBoundedProblem Ω) :
    iIndepFun P.X P.μ :=
  P.independent

/-- The data package exposes the checked variance-budget hypothesis. -/
theorem variance_sum_le {Ω : Type u} [MeasurableSpace Ω]
    (P : BernsteinBoundedProblem Ω) :
    (∑ i ∈ Finset.range P.n, Var[P.X i; P.μ]) ≤ P.varianceBudget :=
  P.variance_sum_le

/-- Checked mathlib Chernoff upper-tail anchor using the moment-generating function. -/
theorem chernoff_upper_tail_mgf_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {X : Ω → ℝ} (ε t : ℝ) (ht : 0 ≤ t)
    (h_int : Integrable (fun ω => Real.exp (t * X ω)) μ) :
    μ.real {ω | ε ≤ X ω} ≤
      Real.exp (-t * ε) * ProbabilityTheory.mgf X μ t :=
  ProbabilityTheory.measure_ge_le_exp_mul_mgf ε ht h_int

/-- Checked mathlib Chernoff upper-tail anchor using the cumulant-generating function. -/
theorem chernoff_upper_tail_cgf_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {X : Ω → ℝ} (ε t : ℝ) (ht : 0 ≤ t)
    (h_int : Integrable (fun ω => Real.exp (t * X ω)) μ) :
    μ.real {ω | ε ≤ X ω} ≤
      Real.exp (-t * ε + ProbabilityTheory.cgf X μ t) :=
  ProbabilityTheory.measure_ge_le_exp_cgf ε ht h_int

/-- Checked mathlib Hoeffding/sub-Gaussian sum-tail anchor. -/
theorem hoeffding_subgaussian_sum_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {X : ℕ → Ω → ℝ} (h_indep : iIndepFun X μ) {c : ℝ≥0} {n : ℕ}
    (h_subG : ∀ i < n, ProbabilityTheory.HasSubgaussianMGF (X i) c μ)
    {ε : ℝ} (hε : 0 ≤ ε) :
    μ.real {ω | ε ≤ ∑ i ∈ Finset.range n, X i ω}
      ≤ Real.exp (-ε ^ 2 / (2 * n * c)) :=
  ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun
    h_indep h_subG hε

/-- Checked mathlib Chebyshev inequality anchor for variance-based reductions. -/
theorem chebyshev_variance_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {X : Ω → ℝ} (hX : MemLp X 2 μ) {c : ℝ} (hc : 0 < c) :
    μ {ω | c ≤ |X ω - μ[X]|} ≤
      ENNReal.ofReal (Var[X; μ] / c ^ 2) :=
  ProbabilityTheory.meas_ge_le_variance_div_sq hX hc

/-- Checked mathlib variance-of-independent-sum anchor. -/
theorem independent_variance_sum_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {ι : Type u} {X : ι → Ω → ℝ} {s : Finset ι}
    (hs : ∀ i ∈ s, MemLp (X i) 2 μ)
    (h : (s : Set ι).Pairwise fun i j => X i ⟂ᵢ[μ] X j) :
    Var[∑ i ∈ s, X i; μ] = ∑ i ∈ s, Var[X i; μ] :=
  ProbabilityTheory.IndepFun.variance_sum hs h

/-- mathlib modules checked for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Moments.Basic",
  "Mathlib.Probability.Moments.SubGaussian",
  "Mathlib.Probability.Moments.Variance",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Integration",
  "Mathlib.Probability.Moments.MGFAnalytic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.ChebyshevMarkov"
]

/-- Pinned mathlib revision audited for this Stage1 Bernstein slot. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Checked equality for downstream public backfill of the audited mathlib revision. -/
theorem mathlibAnchorRevision_eq :
    mathlibAnchorRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Primary-source mathlib anchors audited in the pinned dependency tree. -/
def mathlibPrimarySourceAnchors : List String := [
  "Mathlib/Probability/Moments/Basic.lean:429 ProbabilityTheory.measure_ge_le_exp_mul_mgf",
  "Mathlib/Probability/Moments/Basic.lean:461 ProbabilityTheory.measure_ge_le_exp_cgf",
  "Mathlib/Probability/Moments/SubGaussian.lean:787 ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun",
  "Mathlib/Probability/Moments/Variance.lean:397 ProbabilityTheory.meas_ge_le_variance_div_sq",
  "Mathlib/Probability/Moments/Variance.lean:422 ProbabilityTheory.IndepFun.variance_sum"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.mgf",
  "ProbabilityTheory.cgf",
  "ProbabilityTheory.measure_ge_le_exp_mul_mgf",
  "ProbabilityTheory.measure_ge_le_exp_cgf",
  "ProbabilityTheory.HasSubgaussianMGF",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun",
  "ProbabilityTheory.meas_ge_le_variance_div_sq",
  "ProbabilityTheory.IndepFun.variance_sum",
  "ProbabilityTheory.iIndepFun"
]

/--
Exact child-task anchor list for `S1-M-275-C002`.

Each requested anchor has a checked local wrapper above.  These anchors support
the Stage1 audit but do not constitute a terminal Bernstein proof.
-/
def c002RequestedAnchorNames : List String := [
  "ProbabilityTheory.measure_ge_le_exp_mul_mgf",
  "ProbabilityTheory.measure_ge_le_exp_cgf",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun",
  "ProbabilityTheory.meas_ge_le_variance_div_sq",
  "ProbabilityTheory.IndepFun.variance_sum"
]

/-- Denominator appearing in the one-summand Bernstein MGF bound. -/
def bernsteinMGFDenominator (theta bound : ℝ) : ℝ :=
  1 - theta * bound / 3

/-- Candidate one-summand Bernstein MGF upper bound. -/
def bernsteinSingleSummandMGFUpperBound
    (varianceProxy bound theta : ℝ) : ℝ :=
  Real.exp (theta ^ 2 * varianceProxy /
    (2 * bernsteinMGFDenominator theta bound))

/--
The explicit Bernstein-MGF domain condition makes the denominator positive.

This is a checked side-condition lemma only; it does not prove the MGF bound.
-/
theorem bernsteinMGFDenominator_pos {theta bound : ℝ}
    (h_domain : theta * bound < 3) :
    0 < bernsteinMGFDenominator theta bound := by
  dsimp [bernsteinMGFDenominator]
  nlinarith

/--
The checked denominator positivity also gives the nonzero denominator needed by
division-based real optimization steps.
-/
theorem bernsteinMGFOptimizationDenominator_ne_zero {theta bound : ℝ}
    (h_domain : theta * bound < 3) :
    2 * bernsteinMGFDenominator theta bound ≠ 0 :=
  ne_of_gt (mul_pos zero_lt_two (bernsteinMGFDenominator_pos h_domain))

/--
Exact Stage1 target for the missing centered bounded-summand Bernstein MGF
lemma.

The intended proof obligation starts from centeredness, a common almost-sure
absolute bound, and a variance proxy, and should produce both integrability of
the exponential and the MGF estimate on the explicit domain `theta * bound < 3`.
This declaration is a checked statement boundary only.
-/
def CenteredBoundedSummandBernsteinMGFStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ {μ : Measure Ω} [IsProbabilityMeasure μ],
      ∀ {X : Ω → ℝ} {varianceProxy bound theta : ℝ},
        AEMeasurable X μ →
          MemLp X 2 μ →
            μ[X] = 0 →
              0 ≤ varianceProxy →
                Var[X; μ] ≤ varianceProxy →
                  0 ≤ bound →
                    (∀ᵐ ω ∂μ, |X ω| ≤ bound) →
                      0 ≤ theta →
                        theta * bound < 3 →
                          Integrable (fun ω => Real.exp (theta * X ω)) μ ∧
                            ProbabilityTheory.mgf X μ theta ≤
                              bernsteinSingleSummandMGFUpperBound
                                varianceProxy bound theta

/--
Checked unfolding of the C004 MGF target.  This theorem records the precise
missing lemma shape without claiming that the lemma has been proved.
-/
theorem centeredBoundedSummandBernsteinMGFStatement_iff :
    CenteredBoundedSummandBernsteinMGFStatement.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ {μ : Measure Ω} [IsProbabilityMeasure μ],
          ∀ {X : Ω → ℝ} {varianceProxy bound theta : ℝ},
            AEMeasurable X μ →
              MemLp X 2 μ →
                μ[X] = 0 →
                  0 ≤ varianceProxy →
                    Var[X; μ] ≤ varianceProxy →
                      0 ≤ bound →
                        (∀ᵐ ω ∂μ, |X ω| ≤ bound) →
                          0 ≤ theta →
                            theta * bound < 3 →
                              Integrable (fun ω =>
                                Real.exp (theta * X ω)) μ ∧
                                ProbabilityTheory.mgf X μ theta ≤
                                  bernsteinSingleSummandMGFUpperBound
                                    varianceProxy bound theta :=
  Iff.rfl

/-- C004 machine-state marker: the Bernstein-specific MGF proof is still open. -/
def c004MachineState : String :=
  "not_repo_local_closed"

/-- C004 proof-debt classification for the missing Bernstein-specific MGF lemma. -/
def c004DebtClass : String :=
  "formalization_debt"

/-- C004 local proof leaves still needed before the MGF lemma can be claimed. -/
def c004RemainingProofLeaves : List String := [
  "prove exponential integrability from the a.e. absolute bound and finite probability measure",
  "prove the scalar inequality exp(theta*x) <= 1 + theta*x + theta^2*x^2/(2*(1-theta*bound/3)) on |x| <= bound and theta*bound < 3",
  "integrate the scalar inequality and use E[X]=0",
  "replace E[X^2] by Var[X; μ] under centeredness",
  "monotonically replace Var[X; μ] by the variance proxy in the exponential bound"
]

/-! ## S1-M-275-C005 finite independent-sum MGF/CGF bridge -/

/--
Prefix-truncated process used to apply mathlib's whole-family independence APIs
with only `Finset.range n` measurability hypotheses.
-/
def prefixProcess {Ω : Type u} (n : ℕ) (X : ℕ → Ω → ℝ) : ℕ → Ω → ℝ :=
  fun i ω => if i < n then X i ω else 0

/-- The prefix process agrees with the original process on `Finset.range n`. -/
theorem prefixProcess_eq_of_lt {Ω : Type u} {n i : ℕ} (X : ℕ → Ω → ℝ)
    (hi : i < n) :
    prefixProcess n X i = X i := by
  funext ω
  simp [prefixProcess, hi]

/-- The finite partial sum is definitionally the `Finset.range n` sum. -/
theorem partialSum_apply {Ω : Type u} (n : ℕ) (X : ℕ → Ω → ℝ) (ω : Ω) :
    partialSum n X ω = ∑ i ∈ Finset.range n, X i ω :=
  rfl

/--
The prefix process preserves an independent family by composing each coordinate
with either the identity map or the constant-zero map.
-/
theorem prefixProcess_iIndepFun {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {n : ℕ} {X : ℕ → Ω → ℝ}
    (h_indep : iIndepFun X μ) :
    iIndepFun (prefixProcess n X) μ := by
  classical
  simpa [prefixProcess, Function.comp_def] using
    h_indep.comp (fun i x => if i < n then x else 0)
      (by
        intro i
        by_cases hi : i < n
        · simp [hi]
          exact measurable_id
        · simp [hi])

/-- Prefix measurability is enough for the truncated process to be a.e. measurable everywhere. -/
theorem prefixProcess_aemeasurable {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {n : ℕ} {X : ℕ → Ω → ℝ}
    (h_meas : ∀ i, i < n → AEMeasurable (X i) μ) :
    ∀ i, AEMeasurable (prefixProcess n X i) μ := by
  classical
  intro i
  by_cases hi : i < n
  · rw [prefixProcess_eq_of_lt X hi]
    exact h_meas i hi
  · have h_eq : prefixProcess n X i = fun _ => 0 := by
      funext ω
      simp [prefixProcess, hi]
    rw [h_eq]
    exact aemeasurable_const

/--
Checked C005 MGF bridge for the `Finset.range n` prefix.

This is a local wrapper around mathlib's `ProbabilityTheory.iIndepFun.mgf_sum₀`,
with the parent artifact's prefix-only measurability shape.
-/
theorem independent_prefix_mgf_sum_range_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {X : ℕ → Ω → ℝ} {n : ℕ} (theta : ℝ)
    (h_indep : iIndepFun X μ)
    (h_meas : ∀ i, i < n → AEMeasurable (X i) μ) :
    ProbabilityTheory.mgf (partialSum n X) μ theta =
      ∏ i ∈ Finset.range n, ProbabilityTheory.mgf (X i) μ theta := by
  classical
  have h_bridge :=
    (prefixProcess_iIndepFun (n := n) (X := X) h_indep).mgf_sum₀
      (t := theta) (prefixProcess_aemeasurable (n := n) (X := X) h_meas)
      (Finset.range n)
  have hsum :
      (∑ i ∈ Finset.range n, prefixProcess n X i) = partialSum n X := by
    funext ω
    simp only [Finset.sum_apply, partialSum]
    refine Finset.sum_congr rfl ?_
    intro i hi
    simp [prefixProcess, Finset.mem_range.mp hi]
  have hprod :
      (∏ i ∈ Finset.range n,
        ProbabilityTheory.mgf (prefixProcess n X i) μ theta) =
        ∏ i ∈ Finset.range n, ProbabilityTheory.mgf (X i) μ theta := by
    refine Finset.prod_congr rfl ?_
    intro i hi
    rw [prefixProcess_eq_of_lt X (Finset.mem_range.mp hi)]
  rw [hsum, hprod] at h_bridge
  exact h_bridge

/--
Checked C005 CGF bridge for the `Finset.range n` prefix.

This is a local wrapper around mathlib's `ProbabilityTheory.iIndepFun.cgf_sum₀`;
the exponential-integrability hypotheses are required only for indices in the
finite prefix.
-/
theorem independent_prefix_cgf_sum_range_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω] {μ : Measure Ω}
    {X : ℕ → Ω → ℝ} {n : ℕ} (theta : ℝ)
    (h_indep : iIndepFun X μ)
    (h_meas : ∀ i, i < n → AEMeasurable (X i) μ)
    (h_int : ∀ i, i < n →
      Integrable (fun ω => Real.exp (theta * X i ω)) μ) :
    ProbabilityTheory.cgf (partialSum n X) μ theta =
      ∑ i ∈ Finset.range n, ProbabilityTheory.cgf (X i) μ theta := by
  classical
  have h_int_prefix :
      ∀ i ∈ Finset.range n,
        Integrable (fun ω => Real.exp (theta * prefixProcess n X i ω)) μ := by
    intro i hi
    exact (h_int i (Finset.mem_range.mp hi)).congr
      (by
        filter_upwards with ω
        simp [prefixProcess, Finset.mem_range.mp hi])
  have h_bridge :=
    (prefixProcess_iIndepFun (n := n) (X := X) h_indep).cgf_sum₀
      (t := theta) (prefixProcess_aemeasurable (n := n) (X := X) h_meas)
      (s := Finset.range n) h_int_prefix
  have hsum :
      (∑ i ∈ Finset.range n, prefixProcess n X i) = partialSum n X := by
    funext ω
    simp only [Finset.sum_apply, partialSum]
    refine Finset.sum_congr rfl ?_
    intro i hi
    simp [prefixProcess, Finset.mem_range.mp hi]
  have hcgf :
      (∑ i ∈ Finset.range n,
        ProbabilityTheory.cgf (prefixProcess n X i) μ theta) =
        ∑ i ∈ Finset.range n, ProbabilityTheory.cgf (X i) μ theta := by
    refine Finset.sum_congr rfl ?_
    intro i hi
    rw [prefixProcess_eq_of_lt X (Finset.mem_range.mp hi)]
  rw [hsum, hcgf] at h_bridge
  exact h_bridge

/-- C005 machine-state marker: the finite independent prefix bridge is locally checked. -/
def c005MachineState : String :=
  "local_wrapper_upstream_mathlib"

/--
C005 proof-debt classification: this child closes the finite independence
bridge, while the parent Bernstein theorem still has separate open leaves.
-/
def c005DebtClass : String :=
  "closed_child_leaf_parent_formalization_debt_remains"

/-- C005 checked theorem names for public backfill. -/
def c005CheckedBridgeNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_275.prefixProcess",
  "AwesomeTheorems.Stage1.S1_M_275.prefixProcess_iIndepFun",
  "AwesomeTheorems.Stage1.S1_M_275.prefixProcess_aemeasurable",
  "AwesomeTheorems.Stage1.S1_M_275.independent_prefix_mgf_sum_range_mathlib_wrapper",
  "AwesomeTheorems.Stage1.S1_M_275.independent_prefix_cgf_sum_range_mathlib_wrapper"
]

/-- C005 local leaf-budget ledger for the checked finite prefix bridge. -/
def c005LocalLeafBudgetLedger : List String := [
  "C005-L01 local_proof_body: prefixProcess_eq_of_lt and partialSum_apply align the local prefix notation with Finset.range n.",
  "C005-L02 local_proof_body: prefixProcess_iIndepFun preserves independence by iIndepFun.comp through identity/constant-zero coordinate maps.",
  "C005-L03 local_proof_body: prefixProcess_aemeasurable turns prefix-only a.e. measurability into whole-family measurability for the truncated process.",
  "C005-L04 local_wrapper_upstream_mathlib: independent_prefix_mgf_sum_range_mathlib_wrapper applies ProbabilityTheory.iIndepFun.mgf_sum₀ to the prefix process.",
  "C005-L05 local_wrapper_upstream_mathlib: independent_prefix_cgf_sum_range_mathlib_wrapper applies ProbabilityTheory.iIndepFun.cgf_sum₀ with prefix-only exponential-integrability hypotheses."
]

/-- C005 gate: no completed state in this child retains repo-local integration debt. -/
def c005NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- Checked C005 machine-state equality for downstream public backfill. -/
theorem c005MachineState_eq :
    c005MachineState = "local_wrapper_upstream_mathlib" :=
  rfl

/-- Checked C005 integration-debt gate. -/
theorem c005NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c005NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-275-C006 real Chernoff/Bernstein optimization -/

/-- Optimizing value of the Chernoff parameter for the Bernstein exponent. -/
def bernsteinChernoffOptimizingTheta
    (varianceBudget bound t : ℝ) : ℝ :=
  t / (varianceBudget + bound * t / 3)

/-- Chernoff exponent after inserting the Bernstein MGF upper bound. -/
def bernsteinChernoffExponent
    (varianceBudget bound t theta : ℝ) : ℝ :=
  -theta * t + theta ^ 2 * varianceBudget /
    (2 * bernsteinMGFDenominator theta bound)

/--
For positive variance budget, the Bernstein optimizer has a positive
denominator.  The `0 < varianceBudget` assumption is the concrete side
condition that keeps the MGF domain `theta * bound < 3` open.
-/
theorem bernsteinChernoffOptimizerDenominator_pos {v c t : ℝ}
    (hv : 0 < v) (hc : 0 ≤ c) (ht : 0 ≤ t) :
    0 < v + c * t / 3 := by
  nlinarith [mul_nonneg hc ht]

/-- The Bernstein optimizer is nonnegative under the standard tail-side hypotheses. -/
theorem bernsteinChernoffOptimizingTheta_nonneg {v c t : ℝ}
    (hv : 0 < v) (hc : 0 ≤ c) (ht : 0 ≤ t) :
    0 ≤ bernsteinChernoffOptimizingTheta v c t := by
  dsimp [bernsteinChernoffOptimizingTheta]
  exact div_nonneg ht
    (le_of_lt (bernsteinChernoffOptimizerDenominator_pos hv hc ht))

/-- The Bernstein optimizer lies in the open MGF domain `theta * bound < 3`. -/
theorem bernsteinChernoffOptimizingTheta_mul_bound_lt_three {v c t : ℝ}
    (hv : 0 < v) (hc : 0 ≤ c) (ht : 0 ≤ t) :
    bernsteinChernoffOptimizingTheta v c t * c < 3 := by
  dsimp [bernsteinChernoffOptimizingTheta]
  have hden_pos : 0 < v + c * t / 3 :=
    bernsteinChernoffOptimizerDenominator_pos hv hc ht
  rw [div_mul_eq_mul_div]
  rw [div_lt_iff₀ hden_pos]
  nlinarith

/--
The exact algebraic optimization step in the Bernstein proof.

Substituting `theta = t / (v + c*t/3)` into the Chernoff exponent
`-theta*t + theta^2*v/(2*(1-theta*c/3))` gives the normalized Bernstein
exponent `-t^2/(2*(v+c*t/3))`.
-/
theorem bernsteinChernoffExponent_at_optimizer {v c t : ℝ}
    (hv : 0 < v) (hc : 0 ≤ c) (ht : 0 ≤ t) :
    bernsteinChernoffExponent v c t
      (bernsteinChernoffOptimizingTheta v c t) =
        -(t ^ 2) / (2 * (v + c * t / 3)) := by
  dsimp [bernsteinChernoffExponent, bernsteinChernoffOptimizingTheta,
    bernsteinMGFDenominator]
  have hden_pos : 0 < v + c * t / 3 :=
    bernsteinChernoffOptimizerDenominator_pos hv hc ht
  have hden_ne : v + c * t / 3 ≠ 0 := ne_of_gt hden_pos
  field_simp [hden_ne]
  ring

/--
Checked conversion from a Chernoff bound at the optimizer to the public
Bernstein exponential bound.
-/
theorem bernsteinUpperBound_of_chernoff_at_optimizer {p v c t : ℝ}
    (hv : 0 < v) (hc : 0 ≤ c) (ht : 0 ≤ t)
    (h_chernoff :
      p ≤ Real.exp (bernsteinChernoffExponent v c t
        (bernsteinChernoffOptimizingTheta v c t))) :
    p ≤ bernsteinUpperBound v c t := by
  simpa [bernsteinUpperBound, bernsteinChernoffExponent_at_optimizer hv hc ht]
    using h_chernoff

/-- C006 machine-state marker: the positive-variance real optimization case is locally checked. -/
def c006MachineState : String :=
  "local_proof_body_positive_variance_case"

/--
C006 proof-debt classification: the positive-variance optimizer is checked,
while the nonnegative-variance boundary case and the parent MGF leaf remain.
-/
def c006DebtClass : String :=
  "partial_child_leaf_formalization_debt_zero_variance_boundary_remains"

/-- C006 checked theorem names for public backfill. -/
def c006CheckedOptimizationNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_275.bernsteinChernoffOptimizingTheta",
  "AwesomeTheorems.Stage1.S1_M_275.bernsteinChernoffExponent",
  "AwesomeTheorems.Stage1.S1_M_275.bernsteinChernoffOptimizerDenominator_pos",
  "AwesomeTheorems.Stage1.S1_M_275.bernsteinChernoffOptimizingTheta_nonneg",
  "AwesomeTheorems.Stage1.S1_M_275.bernsteinChernoffOptimizingTheta_mul_bound_lt_three",
  "AwesomeTheorems.Stage1.S1_M_275.bernsteinChernoffExponent_at_optimizer",
  "AwesomeTheorems.Stage1.S1_M_275.bernsteinUpperBound_of_chernoff_at_optimizer"
]

/-- C006 local leaf-budget ledger for the checked real optimization step. -/
def c006LocalLeafBudgetLedger : List String := [
  "C006-L01 local_proof_body: define theta = t/(v+c*t/3) and prove v+c*t/3 > 0 from 0 < v, 0 <= c, and 0 <= t.",
  "C006-L02 local_proof_body: prove theta >= 0 and theta*c < 3, giving the open MGF-domain side condition needed by C004.",
  "C006-L03 local_proof_body: field-simplify the Chernoff exponent at theta and close the normalized identity by ring.",
  "C006-L04 local_proof_body: rewrite a Chernoff bound at theta into the public bernsteinUpperBound expression."
]

/-- C006 local proof leaves still needed before the nonnegative-variance case is fully closed. -/
def c006RemainingProofLeaves : List String := [
  "handle the varianceBudget = 0 boundary for the public nonnegative-variance statement, either by a limiting Chernoff argument, a separate zero-variance probability argument, or a stronger MGF domain theorem"
]

/-- C006 gate: no completed state in this child retains repo-local integration debt. -/
def c006NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- Checked C006 machine-state equality for downstream public backfill. -/
theorem c006MachineState_eq :
    c006MachineState = "local_proof_body_positive_variance_case" :=
  rfl

/-- Checked C006 integration-debt gate. -/
theorem c006NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c006NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-275-C008 terminal completion gate -/

/--
C008 machine-state marker for the parent Bernstein theorem.

The parent is intentionally not marked complete: the terminal Bernstein proof is
not yet present as either a local proof body or a pinned upstream wrapper.
-/
def c008ParentMachineState : String :=
  "not_repo_local_closed"

/--
C008 proof-debt classification for the parent theorem after the checked C005
finite-sum bridge and C006 positive-variance optimization progress.
-/
def c008ParentDebtClass : String :=
  "formalization_debt"

/-- C008 terminal proof gate: no terminal local or pinned-upstream proof validates yet. -/
def c008TerminalLocalOrPinnedProofValidated : Bool :=
  false

/--
C008 leaf-budget gate for the current open parent leaves.

The remaining open proof work is split into concrete child leaves, but that is
not sufficient for theorem completion without the terminal proof gate above.
-/
def c008UncheckedLeavesClosedOrSplitIntoBudgetedSubleaves : Bool :=
  true

/-- C008 gate: no completed state in this parent slot retains repo-local integration debt. -/
def c008NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- C008 current parent status must remain non-completed. -/
def c008ParentCompletionAllowed : Bool :=
  c008TerminalLocalOrPinnedProofValidated &&
    c008UncheckedLeavesClosedOrSplitIntoBudgetedSubleaves

/-- C008 remaining parent blockers before THM-M-0995 may be marked complete. -/
def c008RemainingCompletionBlockers : List String := [
  "prove or pin/import/check the centered bounded-summand Bernstein MGF lemma",
  "close the public nonnegative-variance boundary case for the real optimization step",
  "assemble the terminal one-sided upper-tail Bernstein theorem from the checked MGF, finite-sum, Chernoff, and optimization leaves",
  "rerun local Lean validation after the terminal proof-body or pinned-upstream wrapper is added",
  "merge public blueprint/todo status serially without leaving unchecked leaves or anchor-only completion evidence"
]

/-- Checked C008 machine-state equality for downstream public backfill. -/
theorem c008ParentMachineState_eq :
    c008ParentMachineState = "not_repo_local_closed" :=
  rfl

/-- Checked C008 debt-class equality for downstream public backfill. -/
theorem c008ParentDebtClass_eq :
    c008ParentDebtClass = "formalization_debt" :=
  rfl

/-- Checked C008 terminal-proof gate: completion is not allowed yet. -/
theorem c008ParentCompletionAllowed_eq_false :
    c008ParentCompletionAllowed = false :=
  rfl

/-- Checked C008 integration-debt gate. -/
theorem c008NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c008NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/--
Search terms that did not locate a separately named Bernstein tail theorem in
the local pinned mathlib snapshot.
-/
def absentTerminalSearchTerms : List String := [
  "Bernstein probability inequality",
  "Bernstein tail inequality",
  "Bennett inequality",
  "bounded independent variance tail",
  "measure_sum_ge_le Bernstein",
  "subexponential",
  "subExponential",
  "Freedman inequality"
]

end S1_M_275
end Stage1
end AwesomeTheorems
