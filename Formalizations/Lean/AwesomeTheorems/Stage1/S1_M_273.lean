import Mathlib.Probability.Moments.MGFAnalytic
import Mathlib.Probability.Moments.SubGaussian

/-!
# S1-M-273 / THM-M-0993: Chernoff bounds

This Stage1 artifact records checkable Lean 4 wrappers for Chernoff bounds in
pinned mathlib.  The wrapped facts cover upper and lower tails of a real random
variable and the standard finite independent-sum form obtained by combining the
single-variable Chernoff bound with mathlib's `iIndepFun.mgf_sum` and
`iIndepFun.cgf_sum`.

The theorem is therefore machine-closed for the normalized finite-family
mgf/cgf statement shapes below.  Broader named variants, such as multiplicative
binomial Chernoff forms, remain integrator follow-up tasks rather than claims
made by this file.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped MeasureTheory ProbabilityTheory ENNReal NNReal BigOperators

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_273

universe u v

/-- Upper-tail Chernoff statement for one real random variable, in mgf form. -/
def UpperTailMGFStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : Ω → ℝ) (ε t : ℝ),
      0 ≤ t →
        Integrable (fun ω => Real.exp (t * X ω)) μ →
          μ.real {ω | ε ≤ X ω} ≤ Real.exp (-t * ε) * mgf X μ t

/-- Lower-tail Chernoff statement for one real random variable, in mgf form. -/
def LowerTailMGFStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : Ω → ℝ) (ε t : ℝ),
      t ≤ 0 →
        Integrable (fun ω => Real.exp (t * X ω)) μ →
          μ.real {ω | X ω ≤ ε} ≤ Real.exp (-t * ε) * mgf X μ t

/--
Upper-tail Chernoff statement for a finite sum of independent real random
variables, with the right side factored into the product of individual mgfs.
-/
def IndependentSumUpperTailMGFStatement : Prop :=
  ∀ (Ω : Type u) (ι : Type v) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε t : ℝ),
      iIndepFun X μ →
        (∀ i, Measurable (X i)) →
          (∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ) →
            0 ≤ t →
              μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
                Real.exp (-t * ε) * ∏ i ∈ s, mgf (X i) μ t

/--
Upper-tail Chernoff statement for a finite sum of independent real random
variables, in cumulant-generating-function form.
-/
def IndependentSumUpperTailCGFStatement : Prop :=
  ∀ (Ω : Type u) (ι : Type v) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε t : ℝ),
      iIndepFun X μ →
        (∀ i, Measurable (X i)) →
          (∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ) →
            0 ≤ t →
              μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
                Real.exp (-t * ε + ∑ i ∈ s, cgf (X i) μ t)

/--
Lower-tail Chernoff statement for a finite sum of independent real random
variables, with the right side factored into the product of individual mgfs.
-/
def IndependentSumLowerTailMGFStatement : Prop :=
  ∀ (Ω : Type u) (ι : Type v) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε t : ℝ),
      iIndepFun X μ →
        (∀ i, Measurable (X i)) →
          (∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ) →
            t ≤ 0 →
              μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε} ≤
                Real.exp (-t * ε) * ∏ i ∈ s, mgf (X i) μ t

/--
Lower-tail Chernoff statement for a finite sum of independent real random
variables, in cumulant-generating-function form.
-/
def IndependentSumLowerTailCGFStatement : Prop :=
  ∀ (Ω : Type u) (ι : Type v) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε t : ℝ),
      iIndepFun X μ →
        (∀ i, Measurable (X i)) →
          (∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ) →
            t ≤ 0 →
              μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε} ≤
                Real.exp (-t * ε + ∑ i ∈ s, cgf (X i) μ t)

/-- Normalized Stage1 statement shape for the finite-sum Chernoff package. -/
def StatementShape : Prop :=
  UpperTailMGFStatement.{u} ∧
    LowerTailMGFStatement.{u} ∧
      IndependentSumUpperTailMGFStatement.{u, v} ∧
        IndependentSumUpperTailCGFStatement.{u, v} ∧
          IndependentSumLowerTailMGFStatement.{u, v} ∧
            IndependentSumLowerTailCGFStatement.{u, v}

/-!
## Variant-scope decision

The public Stage1 completion target selected here is the additive finite-family
mgf/cgf Chernoff package above.  The named textbook variants listed below are
kept as explicit non-selected scopes for later child tasks unless an integrator
widens the public theorem text and adds separate checked wrappers.
-/

/-- Variant families often grouped under the name "Chernoff bound". -/
inductive PublicVariantScope where
  | additiveMGFCGF
  | multiplicativeBernoulliBinomial
  | optimizedOverTilt
  | largeDeviationRateFunction
  deriving DecidableEq

/-- The current repo-local public completion target for THM-M-0993. -/
def selectedPublicVariantScope : PublicVariantScope :=
  .additiveMGFCGF

/-- The selected public statement is exactly the checked additive mgf/cgf package. -/
def SelectedPublicStatement : Prop :=
  StatementShape.{u, v}

/-- Scope gate: multiplicative Bernoulli/binomial Chernoff is not selected here. -/
theorem selectedPublicScope_excludes_multiplicativeBernoulliBinomial :
    selectedPublicVariantScope ≠ .multiplicativeBernoulliBinomial := by
  decide

/--
Child-task gate for `THM-M-0993.binomial-specialization`: the selected public
scope is the additive mgf/cgf package, so no multiplicative Bernoulli/binomial
specialization is required for the current repo-local completion target.
-/
theorem binomialSpecialization_notRequired_for_selectedPublicScope :
    selectedPublicVariantScope = .additiveMGFCGF ∧
      selectedPublicVariantScope ≠ .multiplicativeBernoulliBinomial := by
  exact ⟨rfl, selectedPublicScope_excludes_multiplicativeBernoulliBinomial⟩

/-- Scope gate: optimized-over-tilt Chernoff is not selected here. -/
theorem selectedPublicScope_excludes_optimizedOverTilt :
    selectedPublicVariantScope ≠ .optimizedOverTilt := by
  decide

/-- Scope gate: large-deviation rate-function Chernoff is not selected here. -/
theorem selectedPublicScope_excludes_largeDeviationRateFunction :
    selectedPublicVariantScope ≠ .largeDeviationRateFunction := by
  decide

/-!
## Optional optimized-over-tilt wrappers

The current public completion scope does not require optimized Chernoff forms.
The definitions and wrappers in this section are nevertheless checked locally so
an integrator can widen the public scope later without introducing an
anchor-only dependency.  The infimum is taken over the subtype of tilt
parameters for which the relevant exponential-integrability hypotheses hold.
-/

/-- Admissible nonnegative tilt parameter for an independent finite-sum upper tail. -/
def IndependentSumUpperTailAdmissibleTilt
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) (X : ι → Ω → ℝ) (s : Finset ι) (t : ℝ) : Prop :=
  0 ≤ t ∧ ∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ

/-- Admissible nonpositive tilt parameter for an independent finite-sum lower tail. -/
def IndependentSumLowerTailAdmissibleTilt
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) (X : ι → Ω → ℝ) (s : Finset ι) (t : ℝ) : Prop :=
  t ≤ 0 ∧ ∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ

/-- Optimized upper-tail finite-sum Chernoff statement, factored mgf form. -/
def IndependentSumUpperTailMGFOptimizedStatement : Prop :=
  ∀ (Ω : Type u) (ι : Type v) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε : ℝ),
      iIndepFun X μ →
        (∀ i, Measurable (X i)) →
          (∃ t, IndependentSumUpperTailAdmissibleTilt μ X s t) →
            μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
              ⨅ τ : {t : ℝ // IndependentSumUpperTailAdmissibleTilt μ X s t},
                Real.exp (-τ.1 * ε) * ∏ i ∈ s, mgf (X i) μ τ.1

/-- Optimized upper-tail finite-sum Chernoff statement, cgf form. -/
def IndependentSumUpperTailCGFOptimizedStatement : Prop :=
  ∀ (Ω : Type u) (ι : Type v) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε : ℝ),
      iIndepFun X μ →
        (∀ i, Measurable (X i)) →
          (∃ t, IndependentSumUpperTailAdmissibleTilt μ X s t) →
            μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
              ⨅ τ : {t : ℝ // IndependentSumUpperTailAdmissibleTilt μ X s t},
                Real.exp (-τ.1 * ε + ∑ i ∈ s, cgf (X i) μ τ.1)

/-- Optimized lower-tail finite-sum Chernoff statement, factored mgf form. -/
def IndependentSumLowerTailMGFOptimizedStatement : Prop :=
  ∀ (Ω : Type u) (ι : Type v) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε : ℝ),
      iIndepFun X μ →
        (∀ i, Measurable (X i)) →
          (∃ t, IndependentSumLowerTailAdmissibleTilt μ X s t) →
            μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε} ≤
              ⨅ τ : {t : ℝ // IndependentSumLowerTailAdmissibleTilt μ X s t},
                Real.exp (-τ.1 * ε) * ∏ i ∈ s, mgf (X i) μ τ.1

/-- Optimized lower-tail finite-sum Chernoff statement, cgf form. -/
def IndependentSumLowerTailCGFOptimizedStatement : Prop :=
  ∀ (Ω : Type u) (ι : Type v) [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε : ℝ),
      iIndepFun X μ →
        (∀ i, Measurable (X i)) →
          (∃ t, IndependentSumLowerTailAdmissibleTilt μ X s t) →
            μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε} ≤
              ⨅ τ : {t : ℝ // IndependentSumLowerTailAdmissibleTilt μ X s t},
                Real.exp (-τ.1 * ε + ∑ i ∈ s, cgf (X i) μ τ.1)

/-- Optional optimized-over-tilt statement package for finite-sum Chernoff bounds. -/
def OptimizedOverTiltStatement : Prop :=
  IndependentSumUpperTailMGFOptimizedStatement.{u, v} ∧
    IndependentSumUpperTailCGFOptimizedStatement.{u, v} ∧
      IndependentSumLowerTailMGFOptimizedStatement.{u, v} ∧
        IndependentSumLowerTailCGFOptimizedStatement.{u, v}

/-- Checked mathlib wrapper: Chernoff upper-tail bound in mgf form. -/
theorem upperTail_mgf_mathlib
    {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : Ω → ℝ) (ε t : ℝ)
    (ht : 0 ≤ t)
    (h_int : Integrable (fun ω => Real.exp (t * X ω)) μ) :
    μ.real {ω | ε ≤ X ω} ≤ Real.exp (-t * ε) * mgf X μ t :=
  measure_ge_le_exp_mul_mgf ε ht h_int

/-- Checked mathlib wrapper: Chernoff lower-tail bound in mgf form. -/
theorem lowerTail_mgf_mathlib
    {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : Ω → ℝ) (ε t : ℝ)
    (ht : t ≤ 0)
    (h_int : Integrable (fun ω => Real.exp (t * X ω)) μ) :
    μ.real {ω | X ω ≤ ε} ≤ Real.exp (-t * ε) * mgf X μ t :=
  measure_le_le_exp_mul_mgf ε ht h_int

/-- Checked mathlib wrapper: independent finite sums have factored mgf. -/
theorem independentSum_mgf_factorization
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    {μ : Measure Ω} {X : ι → Ω → ℝ} {t : ℝ}
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (s : Finset ι) :
    mgf (∑ i ∈ s, X i) μ t = ∏ i ∈ s, mgf (X i) μ t :=
  h_indep.mgf_sum h_meas s

/-- Checked mathlib wrapper: integrability of the exponential of an independent finite sum. -/
theorem independentSum_integrable_exp
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : ι → Ω → ℝ} {t : ℝ}
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    {s : Finset ι}
    (h_int : ∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ) :
    Integrable (fun ω => Real.exp (t * (∑ i ∈ s, X i) ω)) μ :=
  h_indep.integrable_exp_mul_sum h_meas h_int

/-- Checked wrapper: finite independent-sum Chernoff upper tail, factored mgf form. -/
theorem independentSum_upperTail_mgf_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε t : ℝ)
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (h_int : ∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ)
    (ht : 0 ≤ t) :
    μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
      Real.exp (-t * ε) * ∏ i ∈ s, mgf (X i) μ t := by
  classical
  have hsum_int :
      Integrable (fun ω => Real.exp (t * (∑ i ∈ s, X i) ω)) μ :=
    independentSum_integrable_exp h_indep h_meas h_int
  calc
    μ.real {ω | ε ≤ ∑ i ∈ s, X i ω}
        ≤ Real.exp (-t * ε) * mgf (∑ i ∈ s, X i) μ t := by
          simpa only [Finset.sum_apply] using
            measure_ge_le_exp_mul_mgf (X := (∑ i ∈ s, X i)) ε ht hsum_int
    _ = Real.exp (-t * ε) * ∏ i ∈ s, mgf (X i) μ t := by
        rw [independentSum_mgf_factorization h_indep h_meas s]

/-- Checked wrapper: finite independent-sum Chernoff upper tail, cgf form. -/
theorem independentSum_upperTail_cgf_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε t : ℝ)
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (h_int : ∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ)
    (ht : 0 ≤ t) :
    μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
      Real.exp (-t * ε + ∑ i ∈ s, cgf (X i) μ t) := by
  classical
  have hsum_int :
      Integrable (fun ω => Real.exp (t * (∑ i ∈ s, X i) ω)) μ :=
    independentSum_integrable_exp h_indep h_meas h_int
  calc
    μ.real {ω | ε ≤ ∑ i ∈ s, X i ω}
        ≤ Real.exp (-t * ε + cgf (∑ i ∈ s, X i) μ t) := by
          simpa only [Finset.sum_apply] using
            measure_ge_le_exp_cgf (X := (∑ i ∈ s, X i)) ε ht hsum_int
    _ = Real.exp (-t * ε + ∑ i ∈ s, cgf (X i) μ t) := by
        rw [h_indep.cgf_sum h_meas h_int]

/-- Checked wrapper: finite independent-sum Chernoff lower tail, factored mgf form. -/
theorem independentSum_lowerTail_mgf_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε t : ℝ)
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (h_int : ∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ)
    (ht : t ≤ 0) :
    μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε} ≤
      Real.exp (-t * ε) * ∏ i ∈ s, mgf (X i) μ t := by
  classical
  have hsum_int :
      Integrable (fun ω => Real.exp (t * (∑ i ∈ s, X i) ω)) μ :=
    independentSum_integrable_exp h_indep h_meas h_int
  calc
    μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε}
        ≤ Real.exp (-t * ε) * mgf (∑ i ∈ s, X i) μ t := by
          simpa only [Finset.sum_apply] using
            measure_le_le_exp_mul_mgf (X := (∑ i ∈ s, X i)) ε ht hsum_int
    _ = Real.exp (-t * ε) * ∏ i ∈ s, mgf (X i) μ t := by
        rw [independentSum_mgf_factorization h_indep h_meas s]

/-- Checked wrapper: finite independent-sum Chernoff lower tail, cgf form. -/
theorem independentSum_lowerTail_cgf_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε t : ℝ)
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (h_int : ∀ i ∈ s, Integrable (fun ω => Real.exp (t * X i ω)) μ)
    (ht : t ≤ 0) :
    μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε} ≤
      Real.exp (-t * ε + ∑ i ∈ s, cgf (X i) μ t) := by
  classical
  have hsum_int :
      Integrable (fun ω => Real.exp (t * (∑ i ∈ s, X i) ω)) μ :=
    independentSum_integrable_exp h_indep h_meas h_int
  calc
    μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε}
        ≤ Real.exp (-t * ε + cgf (∑ i ∈ s, X i) μ t) := by
          simpa only [Finset.sum_apply] using
            measure_le_le_exp_cgf (X := (∑ i ∈ s, X i)) ε ht hsum_int
    _ = Real.exp (-t * ε + ∑ i ∈ s, cgf (X i) μ t) := by
        rw [h_indep.cgf_sum h_meas h_int]

/-- Checked wrapper: optimized finite independent-sum upper tail, factored mgf form. -/
theorem independentSum_upperTail_mgf_iInf_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε : ℝ)
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (h_nonempty : ∃ t, IndependentSumUpperTailAdmissibleTilt μ X s t) :
    μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
      ⨅ τ : {t : ℝ // IndependentSumUpperTailAdmissibleTilt μ X s t},
        Real.exp (-τ.1 * ε) * ∏ i ∈ s, mgf (X i) μ τ.1 := by
  classical
  letI : Nonempty {t : ℝ // IndependentSumUpperTailAdmissibleTilt μ X s t} :=
    ⟨⟨h_nonempty.choose, h_nonempty.choose_spec⟩⟩
  exact le_ciInf fun τ =>
    independentSum_upperTail_mgf_mathlib μ X s ε τ.1 h_indep h_meas τ.2.2 τ.2.1

/-- Checked wrapper: optimized finite independent-sum upper tail, cgf form. -/
theorem independentSum_upperTail_cgf_iInf_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε : ℝ)
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (h_nonempty : ∃ t, IndependentSumUpperTailAdmissibleTilt μ X s t) :
    μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
      ⨅ τ : {t : ℝ // IndependentSumUpperTailAdmissibleTilt μ X s t},
        Real.exp (-τ.1 * ε + ∑ i ∈ s, cgf (X i) μ τ.1) := by
  classical
  letI : Nonempty {t : ℝ // IndependentSumUpperTailAdmissibleTilt μ X s t} :=
    ⟨⟨h_nonempty.choose, h_nonempty.choose_spec⟩⟩
  exact le_ciInf fun τ =>
    independentSum_upperTail_cgf_mathlib μ X s ε τ.1 h_indep h_meas τ.2.2 τ.2.1

/-- Checked wrapper: optimized finite independent-sum lower tail, factored mgf form. -/
theorem independentSum_lowerTail_mgf_iInf_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε : ℝ)
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (h_nonempty : ∃ t, IndependentSumLowerTailAdmissibleTilt μ X s t) :
    μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε} ≤
      ⨅ τ : {t : ℝ // IndependentSumLowerTailAdmissibleTilt μ X s t},
        Real.exp (-τ.1 * ε) * ∏ i ∈ s, mgf (X i) μ τ.1 := by
  classical
  letI : Nonempty {t : ℝ // IndependentSumLowerTailAdmissibleTilt μ X s t} :=
    ⟨⟨h_nonempty.choose, h_nonempty.choose_spec⟩⟩
  exact le_ciInf fun τ =>
    independentSum_lowerTail_mgf_mathlib μ X s ε τ.1 h_indep h_meas τ.2.2 τ.2.1

/-- Checked wrapper: optimized finite independent-sum lower tail, cgf form. -/
theorem independentSum_lowerTail_cgf_iInf_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : ι → Ω → ℝ)
    (s : Finset ι) (ε : ℝ)
    (h_indep : iIndepFun X μ) (h_meas : ∀ i, Measurable (X i))
    (h_nonempty : ∃ t, IndependentSumLowerTailAdmissibleTilt μ X s t) :
    μ.real {ω | (∑ i ∈ s, X i ω) ≤ ε} ≤
      ⨅ τ : {t : ℝ // IndependentSumLowerTailAdmissibleTilt μ X s t},
        Real.exp (-τ.1 * ε + ∑ i ∈ s, cgf (X i) μ τ.1) := by
  classical
  letI : Nonempty {t : ℝ // IndependentSumLowerTailAdmissibleTilt μ X s t} :=
    ⟨⟨h_nonempty.choose, h_nonempty.choose_spec⟩⟩
  exact le_ciInf fun τ =>
    independentSum_lowerTail_cgf_mathlib μ X s ε τ.1 h_indep h_meas τ.2.2 τ.2.1

/-- Checked wrapper: mathlib's sub-Gaussian independent-sum tail bound. -/
theorem independentSubGaussianSum_upperTail_mathlib
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω]
    {μ : Measure Ω} {X : ι → Ω → ℝ} {c : ι → ℝ≥0}
    (h_indep : iIndepFun X μ) {s : Finset ι}
    (h_subG : ∀ i ∈ s, HasSubgaussianMGF (X i) (c i) μ)
    {ε : ℝ} (hε : 0 ≤ ε) :
    μ.real {ω | ε ≤ ∑ i ∈ s, X i ω} ≤
      Real.exp (-ε ^ 2 / (2 * ∑ i ∈ s, c i)) :=
  HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun h_indep h_subG hε

/-- Local wrapper closing the normalized Stage1 statement shape from pinned mathlib. -/
theorem statementShape_mathlib : StatementShape.{u, v} := by
  constructor
  · intro Ω _ μ _ X ε t ht h_int
    exact upperTail_mgf_mathlib μ X ε t ht h_int
  constructor
  · intro Ω _ μ _ X ε t ht h_int
    exact lowerTail_mgf_mathlib μ X ε t ht h_int
  constructor
  · intro Ω ι _ μ _ X s ε t h_indep h_meas h_int ht
    exact independentSum_upperTail_mgf_mathlib μ X s ε t h_indep h_meas h_int ht
  constructor
  · intro Ω ι _ μ _ X s ε t h_indep h_meas h_int ht
    exact independentSum_upperTail_cgf_mathlib μ X s ε t h_indep h_meas h_int ht
  constructor
  · intro Ω ι _ μ _ X s ε t h_indep h_meas h_int ht
    exact independentSum_lowerTail_mgf_mathlib μ X s ε t h_indep h_meas h_int ht
  · intro Ω ι _ μ _ X s ε t h_indep h_meas h_int ht
    exact independentSum_lowerTail_cgf_mathlib μ X s ε t h_indep h_meas h_int ht

/-- Checked wrapper for the selected public variant scope. -/
theorem selectedPublicStatement_mathlib : SelectedPublicStatement.{u, v} :=
  statementShape_mathlib

/-- Local wrapper closing the optional optimized-over-tilt statement package. -/
theorem optimizedOverTiltStatement_mathlib : OptimizedOverTiltStatement.{u, v} := by
  constructor
  · intro Ω ι _ μ _ X s ε h_indep h_meas h_nonempty
    exact independentSum_upperTail_mgf_iInf_mathlib μ X s ε h_indep h_meas h_nonempty
  constructor
  · intro Ω ι _ μ _ X s ε h_indep h_meas h_nonempty
    exact independentSum_upperTail_cgf_iInf_mathlib μ X s ε h_indep h_meas h_nonempty
  constructor
  · intro Ω ι _ μ _ X s ε h_indep h_meas h_nonempty
    exact independentSum_lowerTail_mgf_iInf_mathlib μ X s ε h_indep h_meas h_nonempty
  · intro Ω ι _ μ _ X s ε h_indep h_meas h_nonempty
    exact independentSum_lowerTail_cgf_iInf_mathlib μ X s ε h_indep h_meas h_nonempty

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check statementShape_mathlib
#check PublicVariantScope
#check selectedPublicVariantScope
#check SelectedPublicStatement
#check selectedPublicStatement_mathlib
#check selectedPublicScope_excludes_multiplicativeBernoulliBinomial
#check binomialSpecialization_notRequired_for_selectedPublicScope
#check selectedPublicScope_excludes_optimizedOverTilt
#check selectedPublicScope_excludes_largeDeviationRateFunction
#check IndependentSumUpperTailAdmissibleTilt
#check IndependentSumLowerTailAdmissibleTilt
#check OptimizedOverTiltStatement
#check independentSum_upperTail_mgf_iInf_mathlib
#check independentSum_upperTail_cgf_iInf_mathlib
#check independentSum_lowerTail_mgf_iInf_mathlib
#check independentSum_lowerTail_cgf_iInf_mathlib
#check optimizedOverTiltStatement_mathlib
#check le_ciInf
#check measure_ge_le_exp_mul_mgf
#check measure_le_le_exp_mul_mgf
#check measure_ge_le_exp_cgf
#check measure_le_le_exp_cgf
#check iIndepFun.mgf_sum
#check iIndepFun.cgf_sum
#check iIndepFun.integrable_exp_mul_sum
#check HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#check MeasureTheory.meas_ge_le_lintegral_div

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Moments.Basic",
  "Mathlib.Probability.Moments.MGFAnalytic",
  "Mathlib.Probability.Moments.ComplexMGF",
  "Mathlib.Probability.Moments.IntegrableExpMul",
  "Mathlib.Probability.Moments.SubGaussian",
  "Mathlib.Probability.Independence.Integration",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.MeasureTheory.Integral.Lebesgue.Markov",
  "Mathlib.MeasureTheory.Function.LpSeminorm.ChebyshevMarkov"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.measure_ge_le_exp_mul_mgf",
  "ProbabilityTheory.measure_le_le_exp_mul_mgf",
  "ProbabilityTheory.measure_ge_le_exp_cgf",
  "ProbabilityTheory.measure_le_le_exp_cgf",
  "ProbabilityTheory.iIndepFun.mgf_sum",
  "ProbabilityTheory.iIndepFun.cgf_sum",
  "ProbabilityTheory.iIndepFun.integrable_exp_mul_sum",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun",
  "ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun",
  "MeasureTheory.meas_ge_le_lintegral_div",
  "MeasureTheory.mul_meas_ge_le_lintegral₀",
  "le_ciInf"
]

/--
Pinned binomial/Bernoulli APIs inspected for the binomial-specialization child.
No named multiplicative binomial Chernoff theorem was identified in the checked
mathlib search surface, and this Stage1 slot does not select that variant.
-/
def binomialSpecializationAuditNames : List String := [
  "ProbabilityTheory.binomial",
  "ProbabilityTheory.ae_le_of_hasLaw_binomial",
  "PMF.binomial",
  "PMF.binomial_apply",
  "PMF.binomial_one_eq_bernoulli",
  "PMF.binomial_apply_of_le"
]

/-- Search terms used in the pinned local mathlib tree for the anchor audit. -/
def mathlibAuditSearchTerms : List String := [
  "Chernoff",
  "measure_ge_le_exp_mul_mgf",
  "measure_ge_le_exp_cgf",
  "mgf_sum",
  "cgf_sum",
  "integrable_exp_mul_sum",
  "HasSubgaussianMGF",
  "measure_sum_ge_le_of_iIndepFun",
  "Bernoulli",
  "binomial",
  "iInf",
  "le_ciInf",
  "Hoeffding",
  "Markov inequality"
]

/-- Primary-source pin for the mathlib proof body used by this local wrapper. -/
def mathlibPrimarySource : String :=
  "https://github.com/leanprover-community/mathlib4, revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"

end S1_M_273
end Stage1
end AwesomeTheorems
