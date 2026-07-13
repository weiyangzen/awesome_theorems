import ObligationTree
import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0995 proof execution

This module closes the exact Bernstein target.  In addition to the individual
and finite-sum MGF estimates, it records why the registry-v1 optimizer was
false and implements the corrected positive-variance/zero-variance split.
-/

noncomputable section

open Finset MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0995.Proof

open Stage1Instances.THM_M_0995
open Stage1Instances.THM_M_0995.ObligationTree

universe u

/-! ## The bounded centered summand estimate -/

/-- The scalar exponential remainder used in Bernstein's MGF estimate. -/
theorem exp_sub_one_sub_le_quadratic
    {x c : Real} (hx : |x| <= c) (hc : c < 3) :
    Real.exp x - 1 - x <= x ^ 2 / (2 * (1 - c / 3)) := by
  have hc0 : 0 <= c := (abs_nonneg x).trans hx
  have hc3 : 0 <= c / 3 := div_nonneg hc0 (by norm_num)
  have hc3lt : c / 3 < 1 := (div_lt_one (by norm_num)).2 hc
  by_cases hx0 : x = 0
  · simp [hx0]
  have hxabs : 0 < |x| := abs_pos.mpr hx0
  have hxabs3 : |x| / 3 < 1 := (div_lt_one (by norm_num)).2 (hx.trans_lt hc)
  rw [Real.exp_eq_exp_ℝ, NormedSpace.exp_eq_tsum Real]
  let f : Nat -> Real := fun n => ((n.factorial : Real)⁻¹) * x ^ n
  have hExp : Summable f := by
    simpa [smul_eq_mul] using
      (NormedSpace.expSeries_summable' (𝕂 := Real) (𝔸 := Real) x)
  have hGeom : Summable (fun n : Nat => x ^ 2 / 2 * (|x| / 3) ^ n) :=
    (summable_geometric_of_lt_one (div_nonneg (abs_nonneg x) (by norm_num)) hxabs3).mul_left _
  have hTerm (n : Nat) : f (n + 2) <= x ^ 2 / 2 * (|x| / 3) ^ n := by
    have hfacNat : 2 * 3 ^ n <= (n + 2).factorial := by
      cases n with
      | zero => norm_num [Nat.factorial]
      | succ n =>
          have h := Nat.factorial_mul_pow_sub_le_factorial
            (n := 3) (m := n + 3) (by omega)
          simp only [Nat.factorial, Nat.add_sub_cancel_right] at h
          calc
            2 * 3 ^ (n + 1) = 3 ^ n * 6 := by rw [pow_succ]; omega
            _ <= (n + 3).factorial := by
              simpa [Nat.factorial, Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using h
            _ = (n + 1 + 2).factorial := by congr 2
    have hfac : (2 : Real) * 3 ^ n <= ((n + 2).factorial : Real) := by
      exact_mod_cast hfacNat
    calc
      f (n + 2) <= (((n + 2).factorial : Real)⁻¹) * |x| ^ (n + 2) := by
        dsimp [f]
        exact mul_le_mul_of_nonneg_left
          (le_abs_self (x ^ (n + 2)) |>.trans_eq (abs_pow x (n + 2))) (by positivity)
      _ <= ((2 : Real) * 3 ^ n)⁻¹ * |x| ^ (n + 2) := by
        gcongr
      _ = x ^ 2 / 2 * (|x| / 3) ^ n := by
        rw [show n + 2 = 2 + n by omega, pow_add]
        simp only [div_pow]
        rw [sq_abs]
        field_simp
  have hTail : (∑' n : Nat, f (n + 2)) <=
      ∑' n : Nat, x ^ 2 / 2 * (|x| / 3) ^ n :=
    (hExp.comp_injective (fun _ _ h => Nat.add_right_cancel h :
      Function.Injective (fun n : Nat => n + 2))).tsum_le_tsum
      hTerm hGeom
  change (∑' n : Nat, f n) - 1 - x <= _
  rw [← hExp.sum_add_tsum_nat_add 2]
  simp only [f, sum_range_succ, range_one, sum_singleton, Nat.factorial_zero,
    Nat.cast_one, inv_one, pow_zero, mul_one, Nat.factorial_one, pow_one]
  simp only [one_mul]
  have hcancel : 1 + x + (∑' n : Nat, f (n + 2)) - 1 - x =
      ∑' n : Nat, f (n + 2) := by ring
  rw [hcancel]
  calc
    (∑' n : Nat, f (n + 2)) <= ∑' n : Nat, x ^ 2 / 2 * (|x| / 3) ^ n := hTail
    _ = x ^ 2 / 2 * (1 - |x| / 3)⁻¹ := by
      rw [tsum_mul_left, tsum_geometric_of_lt_one
        (div_nonneg (abs_nonneg x) (by norm_num)) hxabs3]
    _ <= x ^ 2 / 2 * (1 - c / 3)⁻¹ := by
      have hinv : (1 - |x| / 3)⁻¹ <= (1 - c / 3)⁻¹ :=
        (inv_le_inv₀ (sub_pos.mpr hxabs3) (sub_pos.mpr hc3lt)).2
          (sub_le_sub_left (div_le_div_of_nonneg_right hx (by norm_num)) 1)
      apply mul_le_mul_of_nonneg_left
        hinv
        (div_nonneg (sq_nonneg x) (by norm_num))
    _ = x ^ 2 / (2 * (1 - c / 3)) := by
      simp only [div_eq_mul_inv, mul_inv]
      ring

/-- The scalar estimate packaged at the exact registry-v2 interface. -/
theorem expRemainderPackage : ExpRemainderPackage := by
  intro x c hx hc
  exact exp_sub_one_sub_le_quadratic hx hc

/-- Checked scalar-to-individual-MGF composition certificate. -/
theorem individualMGFAssemblyPackage : IndividualMGFAssemblyPackage.{u} := by
  intro hExp
  intro Omega _ P i s hi hs hsb
  letI : IsProbabilityMeasure P.mu := P.isProbability
  let C := s ^ 2 / (2 * (1 - s * P.bound / 3))
  have hden : 0 < 2 * (1 - s * P.bound / 3) := by nlinarith
  have hC : 0 <= C := div_nonneg (sq_nonneg s) hden.le
  have hXle : ∀ᵐ omega ∂P.mu, P.X i omega <= P.bound := by
    filter_upwards [P.abs_bound_ae i hi] with omega homega
    exact (le_abs_self _).trans homega
  have hInt : Integrable (fun omega => Real.exp (s * P.X i omega)) P.mu :=
    ProbabilityTheory.integrable_exp_mul_of_le s P.bound hs (P.aemeasurable i hi) hXle
  have hXInt : Integrable (P.X i) P.mu := (P.memLp_two i hi).integrable one_le_two
  have hSqInt : Integrable (fun omega => (P.X i omega) ^ 2) P.mu :=
    (P.memLp_two i hi).integrable_sq
  have hRhsInt : Integrable (fun omega => 1 + s * P.X i omega + C * (P.X i omega) ^ 2) P.mu :=
    ((integrable_const 1).add (hXInt.const_mul s)).add (hSqInt.const_mul C)
  have hpoint : ∀ᵐ omega ∂P.mu,
      Real.exp (s * P.X i omega) <= 1 + s * P.X i omega + C * (P.X i omega) ^ 2 := by
    filter_upwards [P.abs_bound_ae i hi] with omega homega
    have hx : |s * P.X i omega| <= s * P.bound := by
      rw [abs_mul, abs_of_nonneg hs]
      exact mul_le_mul_of_nonneg_left homega hs
    have hscalar := hExp (s * P.X i omega) (s * P.bound) hx hsb
    dsimp [C]
    rw [show (s * P.X i omega) ^ 2 = s ^ 2 * (P.X i omega) ^ 2 by ring] at hscalar
    have hrewrite :
        s ^ 2 * (P.X i omega) ^ 2 / (2 * (1 - s * P.bound / 3)) =
          s ^ 2 / (2 * (1 - s * P.bound / 3)) * (P.X i omega) ^ 2 := by
      field_simp [ne_of_gt hden]
    rw [hrewrite] at hscalar
    linarith
  have hmgf : mgf (P.X i) P.mu s <= 1 + C * Var[P.X i; P.mu] := by
    change (∫ omega, Real.exp (s * P.X i omega) ∂P.mu) <= _
    calc
      (∫ omega, Real.exp (s * P.X i omega) ∂P.mu) <=
          ∫ omega, (1 + s * P.X i omega + C * (P.X i omega) ^ 2) ∂P.mu :=
        integral_mono_ae hInt hRhsInt hpoint
      _ = 1 + C * Var[P.X i; P.mu] := by
        have hOuter := integral_add ((integrable_const 1).add (hXInt.const_mul s))
          (hSqInt.const_mul C)
        have hInner := integral_add
          (integrable_const (1 : Real) : Integrable (fun _ : Omega => (1 : Real)) P.mu)
          (hXInt.const_mul s)
        simp only [Pi.add_apply] at hOuter hInner
        rw [show (∫ omega, 1 + s * P.X i omega + C * (P.X i omega) ^ 2 ∂P.mu) =
              (∫ omega, 1 + s * P.X i omega ∂P.mu) +
                ∫ omega, C * (P.X i omega) ^ 2 ∂P.mu from hOuter,
          show (∫ omega, 1 + s * P.X i omega ∂P.mu) =
              (∫ _omega, 1 ∂P.mu) + ∫ omega, s * P.X i omega ∂P.mu from hInner,
          integral_const,
          integral_const_mul, integral_const_mul, probReal_univ, P.mean_zero i hi,
          mul_zero, add_zero,
          ← ProbabilityTheory.variance_of_integral_eq_zero (P.aemeasurable i hi)
            (P.mean_zero i hi)]
        simp
  calc
    mgf (P.X i) P.mu s <= 1 + C * Var[P.X i; P.mu] := hmgf
    _ <= Real.exp (C * Var[P.X i; P.mu]) := by
      simpa [add_comm] using Real.add_one_le_exp (C * Var[P.X i; P.mu])
    _ = Real.exp (s ^ 2 * Var[P.X i; P.mu] /
        (2 * (1 - s * P.bound / 3))) := by
      congr 1
      dsimp [C]
      ring

/-- The exact individual MGF package from the frozen obligation registry. -/
theorem individualMGFPackage : IndividualMGFPackage.{u} :=
  individualMGF_compose expRemainderPackage individualMGFAssemblyPackage

/-! ## Independent finite-sum bridge -/

/-- Truncate outside the finite prefix so mathlib's whole-family MGF identity applies. -/
def prefixProcess {Omega : Type u} (n : Nat) (X : Nat -> Omega -> Real) :
    Nat -> Omega -> Real :=
  fun i omega => if i < n then X i omega else 0

theorem prefixProcess_iIndepFun
    {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    {n : Nat} {X : Nat -> Omega -> Real} (h : iIndepFun X mu) :
    iIndepFun (prefixProcess n X) mu := by
  classical
  simpa [prefixProcess, Function.comp_def] using
    h.comp (fun i x => if i < n then x else 0) (by
      intro i
      by_cases hi : i < n
      · simpa [hi] using (measurable_id : Measurable (fun x : Real => x))
      · simp [hi])

theorem prefixProcess_aemeasurable
    {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    {n : Nat} {X : Nat -> Omega -> Real}
    (h : forall i, i < n -> AEMeasurable (X i) mu) :
    forall i, AEMeasurable (prefixProcess n X i) mu := by
  classical
  intro i
  by_cases hi : i < n
  · rw [show prefixProcess n X i = X i by funext omega; simp [prefixProcess, hi]]
    exact h i hi
  · rw [show prefixProcess n X i = fun _ => 0 by funext omega; simp [prefixProcess, hi]]
    exact aemeasurable_const

theorem partialSum_mgf_eq_prod
    {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    {n : Nat} {X : Nat -> Omega -> Real} (s : Real)
    (hIndep : iIndepFun X mu)
    (hMeas : forall i, i < n -> AEMeasurable (X i) mu) :
    mgf (partialSum n X) mu s =
      ∏ i ∈ range n, mgf (X i) mu s := by
  classical
  have h := (prefixProcess_iIndepFun (n := n) hIndep).mgf_sum₀
    (t := s) (prefixProcess_aemeasurable (n := n) hMeas) (range n)
  have hsum : (∑ i ∈ range n, prefixProcess n X i) = partialSum n X := by
    funext omega
    simp only [Finset.sum_apply, partialSum]
    exact Finset.sum_congr rfl fun i hi => by simp [prefixProcess, mem_range.mp hi]
  have hprod : (∏ i ∈ range n, mgf (prefixProcess n X i) mu s) =
      ∏ i ∈ range n, mgf (X i) mu s := by
    exact Finset.prod_congr rfl fun i hi => by
      rw [show prefixProcess n X i = X i by
        funext omega
        simp [prefixProcess, mem_range.mp hi]]
  rwa [hsum, hprod] at h

/-- The finite-prefix product identity at the exact registry-v2 interface. -/
theorem prefixMGFPackage : PrefixMGFPackage.{u} := by
  intro Omega _ mu n X s hIndep hMeas
  exact partialSum_mgf_eq_prod s hIndep hMeas

/-- Checked individual/prefix-to-sum-MGF composition certificate. -/
theorem sumMGFAssemblyPackage : SumMGFAssemblyPackage.{u} := by
  intro hIndividual hPrefix
  intro Omega _ P s hs hsb
  letI : IsProbabilityMeasure P.mu := P.isProbability
  have hprefix := hPrefix Omega P.mu P.n P.X s P.independent P.aemeasurable
  rw [hprefix]
  calc
    (∏ i ∈ range P.n, mgf (P.X i) P.mu s) <=
        ∏ i ∈ range P.n,
          Real.exp (s ^ 2 * Var[P.X i; P.mu] /
            (2 * (1 - s * P.bound / 3))) := by
      apply Finset.prod_le_prod
      · intro i hi
        exact integral_nonneg (fun _ => Real.exp_nonneg _)
      · intro i hi
        exact hIndividual Omega P i s (mem_range.mp hi) hs hsb
    _ = Real.exp (∑ i ∈ range P.n,
          s ^ 2 * Var[P.X i; P.mu] /
            (2 * (1 - s * P.bound / 3))) := by
      rw [Real.exp_sum]
    _ <= Real.exp (s ^ 2 * P.varianceBudget /
          (2 * (1 - s * P.bound / 3))) := by
      apply Real.exp_le_exp.mpr
      have hden : 0 < 2 * (1 - s * P.bound / 3) := by nlinarith
      rw [← Finset.sum_div]
      simp only [← Finset.mul_sum]
      exact div_le_div_of_nonneg_right
        (mul_le_mul_of_nonneg_left P.variance_sum_le (sq_nonneg s)) hden.le

/-- The exact independent finite-sum MGF package. -/
theorem sumMGFPackage : SumMGFPackage.{u} :=
  sumMGF_compose individualMGFPackage prefixMGFPackage sumMGFAssemblyPackage

/-! ## Optimization and variance-zero boundary -/

/-- Chernoff's inequality specialized to the exact finite sum interface. -/
theorem chernoffPackage : ChernoffPackage.{u} := by
  intro Omega _ P s t hs
  letI : IsProbabilityMeasure P.mu := P.isProbability
  have hsum_meas : AEMeasurable (partialSum P.n P.X) P.mu := by
    unfold partialSum
    exact Finset.aemeasurable_fun_sum (range P.n) fun i hi =>
      P.aemeasurable i (Finset.mem_range.mp hi)
  have hsum_bound : ∀ᵐ omega ∂P.mu,
      |partialSum P.n P.X omega| <= P.n * P.bound := by
    have hall : ∀ᵐ omega ∂P.mu, ∀ i ∈ range P.n, |P.X i omega| <= P.bound := by
      rw [Finset.eventually_all]
      intro i hi
      exact P.abs_bound_ae i (Finset.mem_range.mp hi)
    filter_upwards [hall] with omega homega
    calc
      |partialSum P.n P.X omega| <= ∑ i ∈ range P.n, |P.X i omega| := by
        simpa [partialSum] using
          (Finset.abs_sum_le_sum_abs (s := range P.n) (f := fun i => P.X i omega))
      _ <= ∑ _i ∈ range P.n, P.bound := by
        exact Finset.sum_le_sum fun i hi => homega i hi
      _ = P.n * P.bound := by simp
  have hInt : Integrable
      (fun omega => Real.exp (s * partialSum P.n P.X omega)) P.mu := by
    apply (integrable_const (Real.exp (|s| * (P.n * P.bound)))).mono
    · exact hsum_meas.const_mul s |>.exp.aestronglyMeasurable
    filter_upwards [hsum_bound] with omega homega
    simp only [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    exact Real.exp_le_exp.mpr <| calc
      s * partialSum P.n P.X omega
          <= |s * partialSum P.n P.X omega| := le_abs_self _
      _ = |s| * |partialSum P.n P.X omega| := abs_mul _ _
      _ <= |s| * (P.n * P.bound) :=
        mul_le_mul_of_nonneg_left homega (abs_nonneg s)
  simpa [ProbabilityTheory.mgf] using
    (ProbabilityTheory.measure_ge_le_exp_mul_mgf
      (μ := P.mu) (X := partialSum P.n P.X) t hs hInt)

/-- The optimizer is admissible once the variance budget is positive. -/
theorem optimizeExponentPackage_of_pos
    {v b t : Real} (hv : 0 < v) (hb : 0 <= b) (ht : 0 <= t) :
    let s := t / (v + b * t / 3)
    0 <= s ∧ s * b < 3 ∧
      Real.exp (-s * t) * Real.exp (s ^ 2 * v / (2 * (1 - s * b / 3))) <=
        Real.exp (-(t ^ 2) / (2 * (v + b * t / 3))) := by
  let d := v + b * t / 3
  have hd : 0 < d := by dsimp [d]; nlinarith [mul_nonneg hb ht]
  have hs : 0 <= t / d := div_nonneg ht hd.le
  have hsb : t / d * b < 3 := by
    rw [div_mul_eq_mul_div, div_lt_iff₀ hd]
    dsimp [d]
    nlinarith [mul_nonneg hb ht]
  refine ⟨hs, hsb, ?_⟩
  rw [← Real.exp_add]
  apply Real.exp_le_exp.mpr
  have hdne : d ≠ 0 := ne_of_gt hd
  have hmgfden : 1 - (t / d) * b / 3 ≠ 0 :=
    ne_of_gt (by nlinarith : 0 < 1 - (t / d) * b / 3)
  dsimp [d] at *
  field_simp [hdne, hmgfden]
  nlinarith [sq_nonneg t]

/-- The corrected positive-variance optimizer package. -/
theorem positiveVarianceOptimizePackage : PositiveVarianceOptimizePackage := by
  intro v b t hv hb ht
  exact optimizeExponentPackage_of_pos hv hb ht

/-- Zero total variance forces every summand in the prefix to vanish almost everywhere. -/
theorem partialSum_ae_zero_of_varianceBudget_eq_zero
    {Omega : Type u} [MeasurableSpace Omega] (P : BoundedSummandProblem Omega)
    (hv : P.varianceBudget = 0) :
    ∀ᵐ omega ∂P.mu, partialSum P.n P.X omega = 0 := by
  letI : IsProbabilityMeasure P.mu := P.isProbability
  have hsum : (∑ i ∈ range P.n, Var[P.X i; P.mu]) = 0 := by
    apply le_antisymm
    · simpa [hv] using P.variance_sum_le
    · exact Finset.sum_nonneg fun _ _ => variance_nonneg _ _
  have hvar (i : Nat) (hi : i < P.n) : Var[P.X i; P.mu] = 0 := by
    exact (Finset.sum_eq_zero_iff_of_nonneg fun j _ => variance_nonneg (P.X j) P.mu).mp hsum
      i (mem_range.mpr hi)
  have hzero : ∀ i, i ∈ range P.n -> ∀ᵐ omega ∂P.mu, P.X i omega = 0 := by
    intro i hi
    have hconst := ProbabilityTheory.ae_eq_integral_of_variance_eq_zero
      (P.memLp_two i (mem_range.mp hi)) (hvar i (mem_range.mp hi))
    simpa [P.mean_zero i (mem_range.mp hi)] using hconst
  have hall : ∀ᵐ omega ∂P.mu, ∀ i ∈ range P.n, P.X i omega = 0 := by
    rw [Finset.eventually_all]
    exact hzero
  filter_upwards [hall] with omega homega
  exact Finset.sum_eq_zero fun i hi => homega i hi

/-- The almost-everywhere zero conclusion at the registry-v2 interface. -/
theorem varianceZeroAEPackage : VarianceZeroAEPackage.{u} := by
  intro Omega _ P hv
  exact partialSum_ae_zero_of_varianceBudget_eq_zero P hv

/-- Direct terminal proof of the exact frozen root, with a separate zero-variance branch. -/
theorem bernsteinInequality : StatementShape.{u} := by
  intro Omega _ P t ht
  letI : IsProbabilityMeasure P.mu := P.isProbability
  by_cases hv : P.varianceBudget = 0
  · by_cases ht0 : t = 0
    · subst t
      simp only [zero_pow (by norm_num : (2 : Nat) ≠ 0), neg_zero, zero_div, Real.exp_zero]
      exact measureReal_le_one
    · have htpos : 0 < t := lt_of_le_of_ne ht (Ne.symm ht0)
      have hae := partialSum_ae_zero_of_varianceBudget_eq_zero P hv
      have hnull : P.mu {omega | t <= partialSum P.n P.X omega} = 0 := by
        rw [measure_eq_zero_iff_ae_notMem]
        filter_upwards [hae] with omega homega
        simp [homega, not_le.mpr htpos]
      rw [measureReal_def, hnull, ENNReal.toReal_zero]
      exact Real.exp_nonneg _
  · have hvpos : 0 < P.varianceBudget :=
      lt_of_le_of_ne P.varianceBudget_nonneg (Ne.symm hv)
    let d := P.varianceBudget + P.bound * t / 3
    let s := t / d
    have hopt := optimizeExponentPackage_of_pos hvpos P.bound_nonneg ht
    change 0 <= s ∧ s * P.bound < 3 ∧ _ at hopt
    obtain ⟨hs, hsb, hexp⟩ := hopt
    calc
      P.mu.real {omega | t <= partialSum P.n P.X omega} <=
          Real.exp (-s * t) *
            (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu) :=
        chernoffPackage Omega P s t hs
      _ <= Real.exp (-s * t) * Real.exp
          (s ^ 2 * P.varianceBudget / (2 * (1 - s * P.bound / 3))) := by
        gcongr
        exact sumMGFPackage Omega P s hs hsb
      _ <= Real.exp (-(t ^ 2) /
          (2 * (P.varianceBudget + P.bound * t / 3))) := hexp

/-- The zero-denominator branch follows from the probability-measure bound. -/
theorem zeroDenominatorPackage : ZeroDenominatorPackage.{u} := by
  intro Omega _ P t ht hden
  letI : IsProbabilityMeasure P.mu := P.isProbability
  rw [hden]
  simp only [mul_zero, div_zero, Real.exp_zero]
  exact measureReal_le_one

/-- Checked zero-denominator/variance-zero branch composition certificate. -/
theorem zeroVarianceAssemblyPackage : ZeroVarianceAssemblyPackage.{u} := by
  intro hZeroDenominator hVarianceZero
  intro Omega _ P t ht hv
  letI : IsProbabilityMeasure P.mu := P.isProbability
  by_cases ht0 : t = 0
  · subst t
    have hden : P.varianceBudget + P.bound * 0 / 3 = 0 := by simp [hv]
    exact hZeroDenominator Omega P 0 (by norm_num) hden
  · have htpos : 0 < t := lt_of_le_of_ne ht (Ne.symm ht0)
    have hae := hVarianceZero Omega P hv
    have hnull : P.mu {omega | t <= partialSum P.n P.X omega} = 0 := by
      rw [measure_eq_zero_iff_ae_notMem]
      filter_upwards [hae] with omega homega
      simp [homega, not_le.mpr htpos]
    rw [measureReal_def, hnull, ENNReal.toReal_zero]
    exact Real.exp_nonneg _

/-- Complete exact-root estimate on the zero-variance branch. -/
theorem zeroVariancePackage : ZeroVariancePackage.{u} :=
  zeroVariance_compose zeroDenominatorPackage varianceZeroAEPackage
    zeroVarianceAssemblyPackage

/-- The frozen optimizer interface is inconsistent at `v = 0, b = 1, t = 1`. -/
theorem not_optimizeExponentPackage : Not OptimizeExponentPackage := by
  intro h
  have hcase := h 0 1 1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  norm_num at hcase

/-- Compose the tail, sum-MGF, optimization, and zero-denominator branches. -/
theorem assemblyPackage : AssemblyPackage.{u} := by
  intro _hIndividual hSum hChernoff hOptimize hZero
  intro Omega _ P t ht
  let d := P.varianceBudget + P.bound * t / 3
  by_cases hd : d = 0
  · exact hZero Omega P t ht hd
  have hdpos : 0 < d := lt_of_le_of_ne
    (add_nonneg P.varianceBudget_nonneg
      (div_nonneg (mul_nonneg P.bound_nonneg ht) (by norm_num)))
    (Ne.symm hd)
  let s := t / d
  obtain ⟨hs0, hsb, hopt⟩ :=
    hOptimize P.varianceBudget P.bound t P.varianceBudget_nonneg P.bound_nonneg ht hdpos
  calc
    P.mu.real {omega | t <= partialSum P.n P.X omega}
        <= Real.exp (-s * t) *
          (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu) :=
      hChernoff Omega P s t hs0
    _ <= Real.exp (-s * t) *
          Real.exp (s ^ 2 * P.varianceBudget /
            (2 * (1 - s * P.bound / 3))) := by
      gcongr
      exact hSum Omega P s hs0 hsb
    _ <= Real.exp (-(t ^ 2) /
        (2 * (P.varianceBudget + P.bound * t / 3))) := hopt

/-- Corrected exhaustive assembly of the registry-v2 proof children. -/
theorem assemblyPackageV2 : AssemblyPackageV2.{u} := by
  intro hSum hChernoff hOptimize hZeroVariance
  intro Omega _ P t ht
  by_cases hv : P.varianceBudget = 0
  · exact hZeroVariance Omega P t ht hv
  · have hvpos : 0 < P.varianceBudget :=
      lt_of_le_of_ne P.varianceBudget_nonneg (Ne.symm hv)
    let d := P.varianceBudget + P.bound * t / 3
    let s := t / d
    obtain ⟨hs, hsb, hexp⟩ := hOptimize P.varianceBudget P.bound t
      hvpos P.bound_nonneg ht
    calc
      P.mu.real {omega | t <= partialSum P.n P.X omega} <=
          Real.exp (-s * t) *
            (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu) :=
        hChernoff Omega P s t hs
      _ <= Real.exp (-s * t) * Real.exp
          (s ^ 2 * P.varianceBudget / (2 * (1 - s * P.bound / 3))) := by
        gcongr
        exact hSum Omega P s hs hsb
      _ <= Real.exp (-(t ^ 2) /
          (2 * (P.varianceBudget + P.bound * t / 3))) := hexp

/-- Registry-v2 root composition, consuming every corrected required child. -/
theorem bernsteinInequality_via_registry_v2 : StatementShape.{u} :=
  root_compose_v2 sumMGFPackage chernoffPackage positiveVarianceOptimizePackage
    zeroVariancePackage assemblyPackageV2

end Stage1Instances.THM_M_0995.Proof

#check Stage1Instances.THM_M_0995.Proof.zeroDenominatorPackage
#check Stage1Instances.THM_M_0995.Proof.exp_sub_one_sub_le_quadratic
#check Stage1Instances.THM_M_0995.Proof.expRemainderPackage
#check Stage1Instances.THM_M_0995.Proof.individualMGFPackage
#check Stage1Instances.THM_M_0995.Proof.individualMGFAssemblyPackage
#check Stage1Instances.THM_M_0995.Proof.prefixProcess_iIndepFun
#check Stage1Instances.THM_M_0995.Proof.prefixProcess_aemeasurable
#check Stage1Instances.THM_M_0995.Proof.partialSum_mgf_eq_prod
#check Stage1Instances.THM_M_0995.Proof.prefixMGFPackage
#check Stage1Instances.THM_M_0995.Proof.sumMGFPackage
#check Stage1Instances.THM_M_0995.Proof.sumMGFAssemblyPackage
#check Stage1Instances.THM_M_0995.Proof.chernoffPackage
#check Stage1Instances.THM_M_0995.Proof.optimizeExponentPackage_of_pos
#check Stage1Instances.THM_M_0995.Proof.positiveVarianceOptimizePackage
#check Stage1Instances.THM_M_0995.Proof.partialSum_ae_zero_of_varianceBudget_eq_zero
#check Stage1Instances.THM_M_0995.Proof.varianceZeroAEPackage
#check Stage1Instances.THM_M_0995.Proof.zeroVariancePackage
#check Stage1Instances.THM_M_0995.Proof.zeroVarianceAssemblyPackage
#check Stage1Instances.THM_M_0995.Proof.bernsteinInequality
#check Stage1Instances.THM_M_0995.Proof.not_optimizeExponentPackage
#check Stage1Instances.THM_M_0995.Proof.assemblyPackage
#check Stage1Instances.THM_M_0995.Proof.assemblyPackageV2
#check Stage1Instances.THM_M_0995.Proof.bernsteinInequality_via_registry_v2
#print axioms Stage1Instances.THM_M_0995.Proof.zeroDenominatorPackage
#print axioms Stage1Instances.THM_M_0995.Proof.exp_sub_one_sub_le_quadratic
#print axioms Stage1Instances.THM_M_0995.Proof.expRemainderPackage
#print axioms Stage1Instances.THM_M_0995.Proof.individualMGFPackage
#print axioms Stage1Instances.THM_M_0995.Proof.individualMGFAssemblyPackage
#print axioms Stage1Instances.THM_M_0995.Proof.prefixProcess_iIndepFun
#print axioms Stage1Instances.THM_M_0995.Proof.prefixProcess_aemeasurable
#print axioms Stage1Instances.THM_M_0995.Proof.partialSum_mgf_eq_prod
#print axioms Stage1Instances.THM_M_0995.Proof.prefixMGFPackage
#print axioms Stage1Instances.THM_M_0995.Proof.sumMGFPackage
#print axioms Stage1Instances.THM_M_0995.Proof.sumMGFAssemblyPackage
#print axioms Stage1Instances.THM_M_0995.Proof.chernoffPackage
#print axioms Stage1Instances.THM_M_0995.Proof.optimizeExponentPackage_of_pos
#print axioms Stage1Instances.THM_M_0995.Proof.positiveVarianceOptimizePackage
#print axioms Stage1Instances.THM_M_0995.Proof.partialSum_ae_zero_of_varianceBudget_eq_zero
#print axioms Stage1Instances.THM_M_0995.Proof.varianceZeroAEPackage
#print axioms Stage1Instances.THM_M_0995.Proof.zeroVariancePackage
#print axioms Stage1Instances.THM_M_0995.Proof.zeroVarianceAssemblyPackage
#print axioms Stage1Instances.THM_M_0995.Proof.bernsteinInequality
#print axioms Stage1Instances.THM_M_0995.Proof.not_optimizeExponentPackage
#print axioms Stage1Instances.THM_M_0995.Proof.assemblyPackage
#print axioms Stage1Instances.THM_M_0995.Proof.assemblyPackageV2
#print axioms Stage1Instances.THM_M_0995.Proof.bernsteinInequality_via_registry_v2
