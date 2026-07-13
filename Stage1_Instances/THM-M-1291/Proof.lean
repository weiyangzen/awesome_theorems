import Statement
import Mathlib.Analysis.MeanInequalitiesPow
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.MeasureTheory.Integral.Lebesgue.Add

/-!
# THM-M-1291: Brezis-Lieb lemma

The proof separates the subunit and superunit exponent ranges.  For
`0 < p <= 1`, subadditivity supplies a fixed integrable dominator.  For
`1 < p`, a weighted convexity estimate feeds the classical positive-part
truncation argument.
-/

namespace Stage1Instances.THM_M_1291

open Filter MeasureTheory
open scoped ENNReal NNReal Topology

universe u

theorem rpow_add_le_weighted
    {p d x y : ℝ} (hp : 1 ≤ p) (hd : 0 < d) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    (x + y) ^ p ≤ (1 + d) ^ (p - 1) * x ^ p +
      (1 + 1 / d) ^ (p - 1) * y ^ p := by
  let w₁ : ℝ := 1 / (1 + d)
  let w₂ : ℝ := d / (1 + d)
  let z₁ : ℝ := (1 + d) * x
  let z₂ : ℝ := (1 + d) / d * y
  have hd0 : d ≠ 0 := hd.ne'
  have h1d : 0 < 1 + d := by linarith
  have hw₁ : 0 ≤ w₁ := by dsimp [w₁]; positivity
  have hw₂ : 0 ≤ w₂ := by dsimp [w₂]; positivity
  have hw : w₁ + w₂ = 1 := by
    dsimp [w₁, w₂]
    field_simp
  have hz₁ : 0 ≤ z₁ := by dsimp [z₁]; positivity
  have hz₂ : 0 ≤ z₂ := by dsimp [z₂]; positivity
  have hj := Real.rpow_arith_mean_le_arith_mean_rpow
    ({0, 1} : Finset ℕ) (fun i => if i = 0 then w₁ else w₂)
      (fun i => if i = 0 then z₁ else z₂)
      (by
        intro i hi
        simp only [Finset.mem_insert, Finset.mem_singleton] at hi
        rcases hi with rfl | rfl
        · simp [hw₁]
        · simp [hw₂])
      (by simp [hw])
      (by
        intro i hi
        simp only [Finset.mem_insert, Finset.mem_singleton] at hi
        rcases hi with rfl | rfl
        · simp [hz₁]
        · simp [hz₂]) hp
  have hcenter : w₁ * z₁ + w₂ * z₂ = x + y := by
    dsimp [w₁, w₂, z₁, z₂]
    field_simp
  have hcoef1 : w₁ * z₁ ^ p = (1 + d) ^ (p - 1) * x ^ p := by
    dsimp [w₁, z₁]
    rw [Real.mul_rpow h1d.le hx]
    rw [Real.rpow_sub h1d p 1, Real.rpow_one]
    field_simp
  have honeplus : 1 + 1 / d = (1 + d) / d := by
    field_simp
    ring
  have hcoef2 : w₂ * z₂ ^ p = (1 + 1 / d) ^ (p - 1) * y ^ p := by
    dsimp [w₂, z₂]
    rw [Real.mul_rpow (by positivity : 0 ≤ (1 + d) / d) hy]
    rw [honeplus]
    rw [Real.rpow_sub (by positivity : 0 < (1 + d) / d) p 1, Real.rpow_one]
    field_simp
  simpa [Finset.sum_insert, hcenter, hcoef1, hcoef2] using hj

theorem abs_rpow_norm_sub_rpow_norm_sub_le_weighted
    {E : Type*} [SeminormedAddCommGroup E]
    {p d : ℝ} (hp : 1 ≤ p) (hd : 0 < d) (a b : E) :
    |‖a‖ ^ p - ‖a - b‖ ^ p| ≤ ((1 + d) ^ (p - 1) - 1) * ‖a‖ ^ p +
      (1 + 1 / d) ^ (p - 1) * ‖b‖ ^ p := by
  rw [abs_sub_le_iff]
  constructor
  · have hnorm : ‖a‖ ≤ ‖a - b‖ + ‖b‖ := by
      calc
        ‖a‖ = ‖(a - b) + b‖ := by rw [sub_add_cancel]
        _ ≤ ‖a - b‖ + ‖b‖ := norm_add_le _ _
    have hrpow := Real.rpow_le_rpow (norm_nonneg a) hnorm (zero_le_one.trans hp)
    have hadd := rpow_add_le_weighted hp hd (norm_nonneg (a - b)) (norm_nonneg b)
    have hcoef : 1 ≤ (1 + d) ^ (p - 1) := by
      have hb : 1 ≤ 1 + d := by linarith
      simpa using Real.one_le_rpow hb (sub_nonneg.mpr hp)
    by_cases horder : ‖a - b‖ ^ p ≤ ‖a‖ ^ p
    · nlinarith [Real.rpow_nonneg (norm_nonneg a) p,
        Real.rpow_nonneg (norm_nonneg (a - b)) p,
        Real.rpow_nonneg (show 0 ≤ 1 + 1 / d by positivity) (p - 1),
        Real.rpow_nonneg (norm_nonneg b) p]
    · have hrev : ‖a‖ ^ p ≤ ‖a - b‖ ^ p := le_of_not_ge horder
      have hR : 0 ≤ ((1 + d) ^ (p - 1) - 1) * ‖a‖ ^ p +
          (1 + 1 / d) ^ (p - 1) * ‖b‖ ^ p := by
        exact add_nonneg
          (mul_nonneg (sub_nonneg.mpr hcoef) (Real.rpow_nonneg (norm_nonneg a) p))
          (mul_nonneg
            (Real.rpow_nonneg (show 0 ≤ 1 + 1 / d by positivity) (p - 1))
            (Real.rpow_nonneg (norm_nonneg b) p))
      linarith
  · have hnorm : ‖a - b‖ ≤ ‖a‖ + ‖b‖ := norm_sub_le _ _
    have hrpow := Real.rpow_le_rpow (norm_nonneg (a - b)) hnorm (zero_le_one.trans hp)
    have hadd := rpow_add_le_weighted hp hd (norm_nonneg a) (norm_nonneg b)
    linarith

theorem rpow_coeff_tendsto_zero {p : ℝ} :
    Tendsto (fun d : ℝ => (1 + d) ^ (p - 1) - 1)
      (nhdsWithin 0 (Set.Ioi 0)) (nhds 0) := by
  have hbase : Tendsto (fun d : ℝ => 1 + d)
      (nhdsWithin 0 (Set.Ioi 0)) (nhds 1) := by
    have hc : Tendsto (fun _d : ℝ => (1 : ℝ))
        (nhdsWithin 0 (Set.Ioi 0)) (nhds 1) := tendsto_const_nhds
    have hi : Tendsto (fun d : ℝ => d)
        (nhdsWithin 0 (Set.Ioi 0)) (nhds 0) := tendsto_id.mono_left inf_le_left
    simpa using hc.add hi
  have hpow : Tendsto (fun d : ℝ => (1 + d) ^ (p - 1))
      (nhdsWithin 0 (Set.Ioi 0)) (nhds (1 ^ (p - 1))) :=
    (Real.continuousAt_rpow_const (x := 1) (q := p - 1)
      (Or.inl one_ne_zero)).tendsto.comp hbase
  simpa using hpow.sub_const 1

noncomputable def truncatedError
    (p d : ℝ) {E : Type*} [SeminormedAddCommGroup E] (u v : E) : ℝ :=
  max
    (|‖u + v‖ ^ p - ‖u‖ ^ p - ‖v‖ ^ p| -
      ((1 + d) ^ (p - 1) - 1) * ‖u‖ ^ p)
    0

theorem truncatedError_nonneg
    {p d : ℝ} {E : Type*} [SeminormedAddCommGroup E] (u v : E) :
    0 ≤ truncatedError p d u v := le_max_right _ _

theorem truncatedError_le
    {p d : ℝ} {E : Type*} [SeminormedAddCommGroup E]
    (hp : 1 ≤ p) (hd : 0 < d) (u v : E) :
    truncatedError p d u v ≤
      ((1 + 1 / d) ^ (p - 1) + 1) * ‖v‖ ^ p := by
  have habs := abs_rpow_norm_sub_rpow_norm_sub_le_weighted hp hd u (-v)
  simp only [sub_neg_eq_add, norm_neg] at habs
  have htri :
      |‖u + v‖ ^ p - ‖u‖ ^ p - ‖v‖ ^ p| ≤
        |‖u + v‖ ^ p - ‖u‖ ^ p| + ‖v‖ ^ p := by
    calc
      |‖u + v‖ ^ p - ‖u‖ ^ p - ‖v‖ ^ p| ≤
          |‖u + v‖ ^ p - ‖u‖ ^ p| + |‖v‖ ^ p| := abs_sub _ _
      _ = |‖u + v‖ ^ p - ‖u‖ ^ p| + ‖v‖ ^ p := by
        rw [abs_of_nonneg (Real.rpow_nonneg (norm_nonneg v) p)]
  have hinside :
      |‖u + v‖ ^ p - ‖u‖ ^ p - ‖v‖ ^ p| -
          ((1 + d) ^ (p - 1) - 1) * ‖u‖ ^ p ≤
        ((1 + 1 / d) ^ (p - 1) + 1) * ‖v‖ ^ p := by
    rw [abs_sub_comm] at habs
    nlinarith
  have hright : 0 ≤ ((1 + 1 / d) ^ (p - 1) + 1) * ‖v‖ ^ p := by
    exact mul_nonneg
      (add_nonneg (Real.rpow_nonneg (show 0 ≤ 1 + 1 / d by positivity) _) zero_le_one)
      (Real.rpow_nonneg (norm_nonneg v) _)
  exact max_le hinside hright

theorem integrable_of_ae_tendsto_of_uniform_integral_bound
    {alpha : Type*} [MeasurableSpace alpha] {mu : Measure alpha}
    {g : alpha → ℝ} {gseq : ℕ → alpha → ℝ}
    (hseq : ∀ n, Integrable (gseq n) mu)
    (hseq0 : ∀ n x, 0 ≤ gseq n x)
    (hg0 : ∀ x, 0 ≤ g x)
    (ht : ∀ᵐ x ∂mu, Tendsto (fun n => gseq n x) atTop (nhds (g x)))
    {C : ℝ} (hC : ∀ n, ∫ x, gseq n x ∂mu ≤ C) : Integrable g mu := by
  have hgmeas : AEStronglyMeasurable g mu :=
    aestronglyMeasurable_of_tendsto_ae atTop
      (fun n => (hseq n).aestronglyMeasurable) ht
  have hlin : ∫⁻ x, ENNReal.ofReal (g x) ∂mu ≤ ENNReal.ofReal C := by
    have hfatou := MeasureTheory.lintegral_liminf_le'
      (μ := mu) (f := fun n x => ENNReal.ofReal (gseq n x))
      (fun n => ENNReal.measurable_ofReal.comp_aemeasurable (hseq n).aemeasurable)
    rw [lintegral_congr_ae] at hfatou
    · exact hfatou.trans (Filter.liminf_le_of_frequently_le'
        (Frequently.of_forall fun n => by
          rw [← ofReal_integral_eq_lintegral_ofReal (hseq n)
            (Eventually.of_forall (hseq0 n))]
          exact ENNReal.ofReal_le_ofReal (hC n)))
    · filter_upwards [ht] with x hx
      exact (ENNReal.continuous_ofReal.tendsto (g x) |>.comp hx).liminf_eq
  exact (lintegral_ofReal_ne_top_iff_integrable hgmeas
    (Eventually.of_forall hg0)).mp (hlin.trans_lt ENNReal.ofReal_lt_top).ne

theorem abs_rpow_norm_add_sub_rpow_norm_le
    {E : Type*} [SeminormedAddCommGroup E]
    {p : ℝ} (hp : 0 < p) (hp1 : p ≤ 1) (a b : E) :
    |‖a + b‖ ^ p - ‖a‖ ^ p| ≤ ‖b‖ ^ p := by
  rw [abs_le]
  constructor
  · have hnorm : ‖a‖ ≤ ‖a + b‖ + ‖b‖ := by
      calc
        ‖a‖ = ‖(a + b) + (-b)‖ := by simp
        _ ≤ ‖a + b‖ + ‖-b‖ := norm_add_le _ _
        _ = ‖a + b‖ + ‖b‖ := by simp
    have hrpow := Real.rpow_le_rpow (norm_nonneg _) hnorm hp.le
    have hadd := Real.rpow_add_le_add_rpow
      (norm_nonneg (a + b)) (norm_nonneg b) hp.le hp1
    linarith
  · have hnorm : ‖a + b‖ ≤ ‖a‖ + ‖b‖ := norm_add_le _ _
    have hrpow := Real.rpow_le_rpow (norm_nonneg _) hnorm hp.le
    have hadd := Real.rpow_add_le_add_rpow
      (norm_nonneg a) (norm_nonneg b) hp.le hp1
    linarith

theorem splittingLimit_subunit
    {alpha : Type*} [MeasurableSpace alpha] (mu : Measure alpha)
    {p : ℝ} (hp : 0 < p) (hp1 : p ≤ 1)
    (f : alpha → ℂ) (fseq : ℕ → alpha → ℂ)
    (hfseq_meas : ∀ n, AEStronglyMeasurable (fseq n) mu)
    (hconv : ∀ᵐ x ∂mu, Tendsto (fun n => fseq n x) atTop (nhds (f x)))
    (hf_int : Integrable (pPower p f) mu)
    (hfseq_int : ∀ n, Integrable (pPower p (fseq n)) mu) :
    SplittingLimit mu p f fseq := by
  have hf_meas : AEStronglyMeasurable f mu :=
    aestronglyMeasurable_of_tendsto_ae atTop hfseq_meas hconv
  have hsub_meas (n : ℕ) : AEStronglyMeasurable (fun x => fseq n x - f x) mu :=
    (hfseq_meas n).sub hf_meas
  have hpmeas {g : alpha → ℂ} (hg : AEStronglyMeasurable g mu) :
      AEStronglyMeasurable (pPower p g) mu :=
    (Real.continuous_rpow_const hp.le).comp_aestronglyMeasurable hg.norm
  have hsub_int (n : ℕ) :
      Integrable (pPower p (fun x => fseq n x - f x)) mu := by
    apply Integrable.mono' ((hfseq_int n).add hf_int) (hpmeas (hsub_meas n))
    filter_upwards with x
    simp only [pPower, Pi.add_apply]
    rw [Real.norm_eq_abs]
    have hn : ‖fseq n x - f x‖ ≤ ‖fseq n x‖ + ‖f x‖ := norm_sub_le _ _
    calc
      |‖fseq n x - f x‖ ^ p| = ‖fseq n x - f x‖ ^ p :=
        abs_of_nonneg (Real.rpow_nonneg (norm_nonneg _) _)
      _ ≤ (‖fseq n x‖ + ‖f x‖) ^ p :=
        Real.rpow_le_rpow (norm_nonneg _) hn hp.le
      _ ≤ ‖fseq n x‖ ^ p + ‖f x‖ ^ p :=
        Real.rpow_add_le_add_rpow (norm_nonneg _) (norm_nonneg _) hp.le hp1
  have hcorrected_meas (n : ℕ) : AEStronglyMeasurable
      (fun x => pPower p (fseq n) x -
        pPower p (fun y => fseq n y - f y) x) mu :=
    (hpmeas (hfseq_meas n)).sub (hpmeas (hsub_meas n))
  have hbound (n : ℕ) : ∀ᵐ x ∂mu,
      ‖pPower p (fseq n) x - pPower p (fun y => fseq n y - f y) x‖ ≤
        pPower p f x := by
    filter_upwards with x
    rw [Real.norm_eq_abs]
    simpa [pPower] using
      (abs_rpow_norm_add_sub_rpow_norm_le hp hp1 (fseq n x - f x) (f x))
  have hlim : ∀ᵐ x ∂mu, Tendsto
      (fun n => pPower p (fseq n) x -
        pPower p (fun y => fseq n y - f y) x)
      atTop (nhds (pPower p f x)) := by
    filter_upwards [hconv] with x hx
    have hsub : Tendsto (fun n => fseq n x - f x) atTop (nhds 0) := by
      simpa using hx.sub (tendsto_const_nhds :
        Tendsto (fun _ : ℕ => f x) atTop (nhds (f x)))
    have hpow := ((Real.continuous_rpow_const hp.le).tendsto _).comp
      ((continuous_norm.tendsto _).comp hx)
    have hpowSub := ((Real.continuous_rpow_const hp.le).tendsto _).comp
      ((continuous_norm.tendsto _).comp hsub)
    simpa [pPower, Real.zero_rpow hp.ne'] using hpow.sub hpowSub
  have hdc := tendsto_integral_of_dominated_convergence
    (pPower p f) hcorrected_meas hf_int hbound hlim
  unfold SplittingLimit
  convert hdc using 1
  ext n
  exact (integral_sub (hfseq_int n) (hsub_int n)).symm

theorem splittingLimit_superunit
    {alpha : Type*} [MeasurableSpace alpha] (mu : Measure alpha) (p : ℝ)
    (hp : 1 < p)
    (f : alpha → ℂ) (fseq : ℕ → alpha → ℂ)
    (hfm : ∀ n, AEStronglyMeasurable (fseq n) mu)
    (hae : ∀ᵐ x ∂mu, Tendsto (fun n => fseq n x) atTop (nhds (f x)))
    {C : ℝ}
    (hint : ∀ n, Integrable (fun x => ‖fseq n x‖ ^ p) mu)
    (hbound : ∀ n, ∫ x, ‖fseq n x‖ ^ p ∂mu ≤ C) :
    SplittingLimit mu p f fseq := by
  have hp0 : 0 < p := lt_trans zero_lt_one hp
  have hfpow : Integrable (fun x => ‖f x‖ ^ p) mu := by
    apply integrable_of_ae_tendsto_of_uniform_integral_bound hint
      (fun n x => Real.rpow_nonneg (norm_nonneg _) _)
      (fun x => Real.rpow_nonneg (norm_nonneg _) _) _ hbound
    filter_upwards [hae] with x hx
    exact ((Real.continuous_rpow_const hp0.le).tendsto _).comp
      ((continuous_norm.tendsto _).comp hx)
  have hfmeas : AEStronglyMeasurable f mu :=
    aestronglyMeasurable_of_tendsto_ae atTop hfm hae
  have hsubmeas (n : ℕ) :
      AEStronglyMeasurable (fun x => fseq n x - f x) mu := (hfm n).sub hfmeas
  have hpowmeas (g : alpha → ℂ) (hg : AEStronglyMeasurable g mu) :
      AEStronglyMeasurable (fun x => ‖g x‖ ^ p) mu :=
    ((Real.continuous_rpow_const hp0.le).comp continuous_norm).aestronglyMeasurable
      |>.comp_aemeasurable hg.aemeasurable
  have hsubint (n : ℕ) : Integrable (fun x => ‖fseq n x - f x‖ ^ p) mu := by
    let A : ℝ := 2 ^ (p - 1)
    apply Integrable.mono' ((hint n).const_mul A |>.add (hfpow.const_mul A))
      (hpowmeas _ (hsubmeas n))
    filter_upwards with x
    rw [Real.norm_eq_abs, abs_of_nonneg (Real.rpow_nonneg (norm_nonneg _) _)]
    have hn := norm_sub_le (fseq n x) (f x)
    have hm := Real.rpow_le_rpow (norm_nonneg _) hn hp0.le
    have hw := rpow_add_le_weighted hp.le (by norm_num : (0 : ℝ) < 1)
      (norm_nonneg (fseq n x)) (norm_nonneg (f x))
    dsimp [A]
    norm_num at hw
    simpa using hm.trans hw
  let err : ℕ → alpha → ℝ := fun n x =>
    |‖fseq n x‖ ^ p - ‖fseq n x - f x‖ ^ p - ‖f x‖ ^ p|
  have herrmeas (n : ℕ) : AEStronglyMeasurable (err n) mu :=
    (((hpowmeas _ (hfm n)).sub (hpowmeas _ (hsubmeas n))).sub
      (hpowmeas _ hfmeas)).norm
  have herrint (n : ℕ) : Integrable (err n) mu :=
    (((hint n).sub (hsubint n)).sub hfpow).abs
  have herrlim : ∀ᵐ x ∂mu, Tendsto (fun n => err n x) atTop (nhds 0) := by
    filter_upwards [hae] with x hx
    have hsub : Tendsto (fun n => fseq n x - f x) atTop (nhds 0) := by
      simpa using hx.sub (tendsto_const_nhds :
        Tendsto (fun _ : ℕ => f x) atTop (nhds (f x)))
    have hpow := ((Real.continuous_rpow_const hp0.le).tendsto _).comp
      ((continuous_norm.tendsto _).comp hx)
    have hpowSub := ((Real.continuous_rpow_const hp0.le).tendsto _).comp
      ((continuous_norm.tendsto _).comp hsub)
    have hc := (hpow.sub hpowSub).sub_const (‖f x‖ ^ p)
    simpa [err, Real.zero_rpow hp0.ne'] using hc.abs
  have hremBound : ∃ M : ℝ, 0 ≤ M ∧
      ∀ n, ∫ x, ‖fseq n x - f x‖ ^ p ∂mu ≤ M := by
    let A : ℝ := 2 ^ (p - 1)
    refine ⟨max (A * C + A * ∫ x, ‖f x‖ ^ p ∂mu) 0, le_max_right _ _, ?_⟩
    intro n
    have hi : ∫ x, ‖fseq n x - f x‖ ^ p ∂mu ≤
        A * C + A * ∫ x, ‖f x‖ ^ p ∂mu := by
      apply le_trans (integral_mono_ae (hsubint n)
        ((hint n).const_mul A |>.add (hfpow.const_mul A)) ?_) ?_
      · filter_upwards with x
        have hn := norm_sub_le (fseq n x) (f x)
        have hm := Real.rpow_le_rpow (norm_nonneg _) hn hp0.le
        have hw := rpow_add_le_weighted hp.le (by norm_num : (0 : ℝ) < 1)
          (norm_nonneg (fseq n x)) (norm_nonneg (f x))
        dsimp [A]
        norm_num at hw
        simpa using hm.trans hw
      · change ∫ x, A * ‖fseq n x‖ ^ p + A * ‖f x‖ ^ p ∂mu ≤ _
        rw [integral_add (hint n |>.const_mul A) (hfpow.const_mul A),
            integral_const_mul, integral_const_mul]
        have hA : 0 ≤ A := Real.rpow_nonneg (by norm_num) _
        nlinarith [hbound n]
    exact hi.trans (le_max_left _ _)
  obtain ⟨M, hM0, hM⟩ := hremBound
  have herrIntegral : Tendsto (fun n => ∫ x, err n x ∂mu) atTop (nhds 0) := by
    rw [Metric.tendsto_atTop]
    intro eta heta
    have hcoeff := rpow_coeff_tendsto_zero (p := p)
    have hevent : ∀ᶠ d in nhdsWithin (0 : ℝ) (Set.Ioi 0),
        |((1 + d) ^ (p - 1) - 1) * M| < eta / 2 := by
      have ht : Tendsto (fun d : ℝ => ((1 + d) ^ (p - 1) - 1) * M)
          (nhdsWithin 0 (Set.Ioi 0)) (nhds (0 * M)) := hcoeff.mul_const M
      simpa [Real.dist_eq] using
        (Metric.tendsto_nhds.mp ht (eta / 2) (by positivity))
    have hIoi : ∀ᶠ d in nhdsWithin (0 : ℝ) (Set.Ioi 0), d ∈ Set.Ioi 0 :=
      self_mem_nhdsWithin
    obtain ⟨d, hd, hdsmall⟩ := (hevent.and hIoi).exists
    have hdpos : 0 < d := hdsmall
    let eps : ℝ := (1 + d) ^ (p - 1) - 1
    let K : ℝ := (1 + 1 / d) ^ (p - 1) + 1
    let trunc : ℕ → alpha → ℝ := fun n x =>
      truncatedError p d (fseq n x - f x) (f x)
    have heps0 : 0 ≤ eps := by
      dsimp [eps]
      exact sub_nonneg.mpr (Real.one_le_rpow (by linarith) (sub_nonneg.mpr hp.le))
    have hK0 : 0 ≤ K := by
      dsimp [K]
      exact add_nonneg (Real.rpow_nonneg (by positivity) _) zero_le_one
    have htrunc_meas (n : ℕ) : AEStronglyMeasurable (trunc n) mu := by
      have hinside : AEStronglyMeasurable
          (fun x => err n x - eps * ‖fseq n x - f x‖ ^ p) mu :=
        (herrmeas n).sub ((hpowmeas _ (hsubmeas n)).const_mul eps)
      simpa [trunc, truncatedError, err, eps, sub_add_cancel] using
        (continuous_max.comp_aestronglyMeasurable
          (hinside.prodMk (aestronglyMeasurable_const :
            AEStronglyMeasurable (fun _ : alpha => (0 : ℝ)) mu)))
    have hdomint : Integrable (fun x => K * ‖f x‖ ^ p) mu := hfpow.const_mul K
    have htrunc_bound (n : ℕ) : ∀ᵐ x ∂mu,
        ‖trunc n x‖ ≤ K * ‖f x‖ ^ p := by
      filter_upwards with x
      rw [Real.norm_eq_abs, abs_of_nonneg (truncatedError_nonneg _ _)]
      exact truncatedError_le hp.le hdpos _ _
    have htrunc_lim : ∀ᵐ x ∂mu,
        Tendsto (fun n => trunc n x) atTop (nhds 0) := by
      filter_upwards [herrlim, hae] with x hxerr hx
      have hsub : Tendsto (fun n => fseq n x - f x) atTop (nhds 0) := by
        simpa using hx.sub (tendsto_const_nhds :
          Tendsto (fun _ : ℕ => f x) atTop (nhds (f x)))
      have hsubpow := ((Real.continuous_rpow_const hp0.le).tendsto _).comp
        ((continuous_norm.tendsto _).comp hsub)
      have hinside := hxerr.sub (hsubpow.const_mul eps)
      have hzeroT : Tendsto (fun _n : ℕ => (0 : ℝ)) atTop (nhds 0) :=
        tendsto_const_nhds
      have hmax := hinside.max hzeroT
      simpa [trunc, truncatedError, err, eps, sub_add_cancel,
        Real.zero_rpow hp0.ne'] using hmax
    have htruncInt := tendsto_integral_of_dominated_convergence
      (fun x => K * ‖f x‖ ^ p) htrunc_meas hdomint htrunc_bound htrunc_lim
    obtain ⟨N, hN⟩ := Metric.tendsto_atTop.mp htruncInt (eta / 2) (by positivity)
    refine ⟨N, fun n hn => ?_⟩
    have htnorm : |∫ x, trunc n x ∂mu| < eta / 2 := by
      simpa [Real.dist_eq] using hN n hn
    have ht_nonneg : 0 ≤ ∫ x, trunc n x ∂mu :=
      integral_nonneg (fun x => truncatedError_nonneg _ _)
    have hepsM : eps * M < eta / 2 := by
      have : |eps * M| < eta / 2 := by simpa [eps] using hd
      exact lt_of_le_of_lt (le_abs_self _) this
    have hpoint : ∀ x, err n x ≤ trunc n x + eps * ‖fseq n x - f x‖ ^ p := by
      intro x
      dsimp [trunc, truncatedError, err]
      dsimp [eps]
      rw [sub_add_cancel]
      linarith [le_max_left (err n x - eps * ‖fseq n x - f x‖ ^ p) 0]
    have hintle : ∫ x, err n x ∂mu ≤
        ∫ x, trunc n x ∂mu + eps * ∫ x, ‖fseq n x - f x‖ ^ p ∂mu := by
      have htruncint : Integrable (trunc n) mu :=
        Integrable.mono' hdomint (htrunc_meas n) (htrunc_bound n)
      have hsumint := htruncint.add ((hsubint n).const_mul eps)
      calc
        ∫ x, err n x ∂mu ≤ ∫ x, trunc n x + eps * ‖fseq n x - f x‖ ^ p ∂mu :=
          integral_mono_ae (herrint n) hsumint (Eventually.of_forall hpoint)
        _ = _ := by
          rw [integral_add htruncint ((hsubint n).const_mul eps), integral_const_mul]
    have hepsrem : eps * ∫ x, ‖fseq n x - f x‖ ^ p ∂mu ≤ eps * M :=
      mul_le_mul_of_nonneg_left (hM n) heps0
    have herrNonneg : 0 ≤ ∫ x, err n x ∂mu :=
      integral_nonneg (fun x => abs_nonneg _)
    rw [Real.dist_eq, sub_zero, abs_of_nonneg herrNonneg]
    have ht_lt : ∫ x, trunc n x ∂mu < eta / 2 := by
      simpa [abs_of_nonneg ht_nonneg] using htnorm
    linarith
  have hcorrInt (n : ℕ) :
      ∫ x, ‖fseq n x‖ ^ p - ‖fseq n x - f x‖ ^ p ∂mu =
        (∫ x, ‖fseq n x‖ ^ p ∂mu) - ∫ x, ‖fseq n x - f x‖ ^ p ∂mu :=
    integral_sub (hint n) (hsubint n)
  unfold SplittingLimit
  simp only [pPower]
  rw [Metric.tendsto_atTop]
  intro eta heta
  obtain ⟨N, hN⟩ := Metric.tendsto_atTop.mp herrIntegral eta heta
  refine ⟨N, fun n hn => ?_⟩
  have habsint := abs_integral_le_integral_abs
    (μ := mu) (f := fun x => ‖fseq n x‖ ^ p - ‖fseq n x - f x‖ ^ p - ‖f x‖ ^ p)
  have herrlt : ∫ x, err n x ∂mu < eta := by
    have hnon : 0 ≤ ∫ x, err n x ∂mu := integral_nonneg (fun x => abs_nonneg _)
    simpa [Real.dist_eq, abs_of_nonneg hnon] using hN n hn
  rw [Real.dist_eq]
  calc
    |(∫ x, ‖fseq n x‖ ^ p ∂mu) - (∫ x, ‖fseq n x - f x‖ ^ p ∂mu) -
        ∫ x, ‖f x‖ ^ p ∂mu| =
        |∫ x, ‖fseq n x‖ ^ p - ‖fseq n x - f x‖ ^ p - ‖f x‖ ^ p ∂mu| := by
      have hi := integral_sub (μ := mu)
        (hf := ((hint n).sub (hsubint n))) (hg := hfpow)
      have hi' :
          ∫ x, ‖fseq n x‖ ^ p - ‖fseq n x - f x‖ ^ p - ‖f x‖ ^ p ∂mu =
            (∫ x, ‖fseq n x‖ ^ p - ‖fseq n x - f x‖ ^ p ∂mu) -
              ∫ x, ‖f x‖ ^ p ∂mu := by
        simpa only [Pi.sub_apply] using hi
      rw [hi', hcorrInt n]
    _ ≤ ∫ x, err n x ∂mu := by simpa [err] using habsint
    _ < eta := herrlt

theorem brezisLiebTarget_proof : BrezisLiebTarget.{u} := by
  intro alpha _ mu p hp f fseq hfm hae hub
  obtain ⟨C, hC⟩ := hub
  have hint : ∀ n, Integrable (fun x => ‖fseq n x‖ ^ p) mu := fun n => (hC n).1
  have hbound : ∀ n, ∫ x, ‖fseq n x‖ ^ p ∂mu ≤ C := fun n => (hC n).2
  by_cases hp1 : p ≤ 1
  · have hfpow : Integrable (fun x => ‖f x‖ ^ p) mu := by
      apply integrable_of_ae_tendsto_of_uniform_integral_bound hint
        (fun n x => Real.rpow_nonneg (norm_nonneg _) _)
        (fun x => Real.rpow_nonneg (norm_nonneg _) _) _ hbound
      filter_upwards [hae] with x hx
      exact ((Real.continuous_rpow_const hp.le).tendsto _).comp
        ((continuous_norm.tendsto _).comp hx)
    exact splittingLimit_subunit mu hp hp1 f fseq hfm hae
      (by simpa [pPower] using hfpow)
      (fun n => by simpa [pPower] using hint n)
  · exact splittingLimit_superunit mu p (lt_of_not_ge hp1) f fseq hfm hae hint hbound

#print axioms brezisLiebTarget_proof

end Stage1Instances.THM_M_1291
