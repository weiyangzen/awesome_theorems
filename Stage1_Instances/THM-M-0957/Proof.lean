import ObligationTree
import Statement
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics

/-!
# THM-M-0957 exact proof execution

This module installs the pinned Behrend construction and inclusive-index
transport, proves every sharp-parameter leaf, and replays the frozen
composition chain to the exact historical root.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0957_ObligationTree

open Filter
open scoped Topology

/-- The rounded source dimension is eventually admissible and differs from
its real proxy by at most one. -/
theorem dimensionControl_proof : DimensionControlPackage := by
  refine ⟨4, ?_⟩
  intro N hN
  let x : Real := Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2)
  have hlog2 : 0 < Real.log (2 : Real) := Real.log_pos one_lt_two
  have hNp1 : (4 : Nat) + 1 <= N + 1 := Nat.add_le_add_right hN 1
  have hlogN : Real.log (5 : Real) <= Real.log ((N + 1 : Nat) : Real) := by
    apply Real.log_le_log (by norm_num)
    exact_mod_cast hNp1
  have hx2 : (2 : Real) <= x := by
    apply Real.le_sqrt_of_sq_le
    dsimp only [x]
    rw [sq, mul_div_assoc]
    gcongr
    rw [le_div_iff₀ hlog2]
    have hlog5 : 2 * Real.log 2 <= Real.log (5 : Real) := by
      calc
        2 * Real.log 2 = Real.log ((2 : Real) ^ 2) := by
          rw [Real.log_pow]
          norm_num
        _ <= Real.log (5 : Real) := Real.log_le_log (by norm_num) (by norm_num)
    linarith
  have hx0 : 0 <= x := Real.sqrt_nonneg _
  have hceilLow : x <= (sharpDimension N : Real) := by
    simpa only [sharpDimension, x, Nat.cast_add, Nat.cast_one] using Nat.le_ceil x
  have hceilHigh : (sharpDimension N : Real) < x + 1 := by
    simpa only [sharpDimension, x, Nat.cast_add, Nat.cast_one] using
      Nat.ceil_lt_add_one hx0
  constructor
  · exact_mod_cast hx2.trans hceilLow
  · rw [abs_le]
    constructor <;> dsimp only [x] at * <;> linarith

/-- For positive indices, the historical real power is exactly its
exponential logarithmic form. -/
theorem rpowNormalization_proof : RpowNormalizationPackage := by
  intro epsilon _hepsilon
  refine ⟨2, ?_⟩
  intro N hN
  have hNreal : (0 : Real) < (N : Real) := by
    exact_mod_cast (show 0 < N from (by omega))
  have hlog : 0 < Real.log (N : Real) := by
    exact Real.log_pos (by exact_mod_cast (show 1 < N from (by omega)))
  have hsqrt : 0 < Real.sqrt (Real.log (N : Real)) := Real.sqrt_pos.2 hlog
  rw [historicalLower, Real.rpow_def_of_pos hNreal]
  apply Real.exp_le_exp.mpr
  have hsquare : Real.sqrt (Real.log (N : Real)) *
      Real.sqrt (Real.log (N : Real)) = Real.log (N : Real) := by
    nlinarith [Real.sq_sqrt hlog.le]
  apply le_of_eq
  field_simp
  ring_nf
  rw [sq, hsquare]

/-- The proxy above `radixProxy` has the exact exponential form consumed by
the subtraction-by-one comparison. -/
theorem proxyRpowIdentity_proof : ProxyRpowIdentityPackage := by
  refine ⟨4, ?_⟩
  intro N _hN hdimension
  have hnpos : 0 < (sharpDimension N : Real) := by
    exact_mod_cast (show 0 < sharpDimension N from
      lt_of_lt_of_le (by decide) hdimension.1)
  have hbase : (0 : Real) < ((N + 1 : Nat) : Real) := by positivity
  rw [radixProxy, sub_add_cancel]
  rw [Real.rpow_def_of_pos hbase]
  rw [Real.exp_sub, Real.exp_log (by norm_num : (0 : Real) < 2)]
  congr 1

/-- The exponential slack eventually absorbs the subtraction by one in the
real radix proxy. -/
theorem proxySlackAbsorption_proof : ProxySlackAbsorptionPackage := by
  intro delta hdelta
  let f : Nat -> Real := fun N =>
    Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2)
  let S : Nat -> Real := fun N => Real.sqrt (Real.log (N : Real))
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hcoef : Real.sqrt (2 / Real.log 2) < (7 / 4 : Real) := by
    rw [Real.sqrt_lt' (by norm_num : (0 : Real) < 7 / 4)]
    rw [div_lt_iff₀ hlog2]
    nlinarith [Real.log_two_gt_d9]
  let c : Real := Real.exp (delta / 4) - 1
  have hc : 0 < c := by
    dsimp [c]
    rw [sub_pos, Real.one_lt_exp_iff]
    positivity
  have hTlog : Tendsto (fun N : Nat => Real.log (N : Real)) atTop atTop :=
    Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop
  have hTS : Tendsto S atTop atTop :=
    Real.tendsto_sqrt_atTop.comp hTlog
  have hlarge : ∀ᶠ N : Nat in atTop, 5 <= S N :=
    hTS.eventually_ge_atTop 5
  have hthreshold : ∀ᶠ N : Nat in atTop,
      2 * (Real.log 2 + delta / 4 - Real.log c) <= S N :=
    hTS.eventually_ge_atTop _
  have hinc0 : Tendsto (fun N : Nat =>
      Real.log (((N + 1 : Nat) : Real)) - Real.log (N : Real)) atTop (nhds 0) :=
    Real.tendsto_log_nat_add_one_sub_log.congr' <| by
      filter_upwards with N
      simp only [Nat.cast_add, Nat.cast_one]
  have hinc : ∀ᶠ N : Nat in atTop,
      Real.log (((N + 1 : Nat) : Real)) - Real.log (N : Real) < 1 :=
    hinc0.eventually_lt_const (by norm_num)
  have hpos : ∀ᶠ N : Nat in atTop, 0 < Real.log (N : Real) :=
    hTlog.eventually_gt_atTop 0
  have hbound : ∀ᶠ N : Nat in atTop, f N + 1 <= 2 * S N := by
    filter_upwards [hlarge, hinc, hpos] with N hL hI hP
    let L : Real := Real.log (N : Real)
    let s : Real := Real.sqrt L
    have hlogInc : Real.log (((N + 1 : Nat) : Real)) <= L + 1 := by
      dsimp [L]
      linarith
    have hs_sq : s ^ 2 = L := by
      dsimp [s]
      exact Real.sq_sqrt hP.le
    have hfactor :
        Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2) =
          Real.sqrt (2 / Real.log 2) *
            Real.sqrt (Real.log (((N + 1 : Nat) : Real))) := by
      rw [← Real.sqrt_mul (by positivity)]
      congr 1
      field_simp [hlog2.ne']
    have hsqrtInc :
        Real.sqrt (Real.log (((N + 1 : Nat) : Real))) <= s + 1 / 8 := by
      rw [Real.sqrt_le_iff]
      constructor
      · positivity
      · rw [add_pow_two, hs_sq]
        have hsnonneg : 0 <= s := by positivity
        nlinarith
    have hfbound : f N <= (7 / 4 : Real) * (s + 1 / 8) := by
      dsimp [f]
      rw [hfactor]
      exact mul_le_mul hcoef.le hsqrtInc
        (Real.sqrt_nonneg _) (by positivity)
    have hslarge : 5 <= s := by
      simpa only [S, s, L] using hL
    have hroom :
        (7 / 4 : Real) * (s + 1 / 8) + 1 <= 2 * s := by
      nlinarith
    dsimp [S]
    calc
      f N + 1 <= (7 / 4 : Real) * (s + 1 / 8) + 1 := by linarith
      _ <= 2 * s := hroom
      _ = 2 * Real.sqrt (Real.log (N : Real)) := by rfl
  have hall : ∀ᶠ N : Nat in atTop,
      f N + 1 <= 2 * S N /\
      2 * (Real.log 2 + delta / 4 - Real.log c) <= S N /\
      0 < Real.log (N : Real) := hbound.and (hthreshold.and hpos)
  obtain ⟨N0, hN0⟩ := eventually_atTop.1 hall
  refine ⟨N0, ?_⟩
  intro N hN hctrl
  obtain ⟨hboundN, hthresholdN, hlogN⟩ := hN0 N hN
  let n : Real := (sharpDimension N : Real)
  let L : Real := Real.log (N : Real)
  let s : Real := Real.sqrt L
  let a : Real := L / n - Real.log 2 - delta / 4
  let b : Real := Real.log (((N + 1 : Nat) : Real)) / n - Real.log 2
  have hnpos : 0 < n := by
    dsimp [n]
    exact_mod_cast (show 0 < sharpDimension N from
      lt_of_lt_of_le (by decide) hctrl.1)
  have hspos : 0 < s := by
    dsimp [s]
    exact Real.sqrt_pos.2 hlogN
  have hs_sq : s ^ 2 = L := by
    dsimp [s]
    exact Real.sq_sqrt hlogN.le
  have hnupper : n <= 2 * s := by
    have hdim : (sharpDimension N : Real) <= f N + 1 := by
      have habs := (abs_le.mp hctrl.2).2
      dsimp [f]
      linarith
    exact hdim.trans (by simpa only [S, n, s, L] using hboundN)
  have hratio : s / 2 <= L / n := by
    rw [le_div_iff₀ hnpos]
    have hm := mul_le_mul_of_nonneg_left hnupper
      (div_nonneg hspos.le (by norm_num : (0 : Real) <= 2))
    calc
      s / 2 * n <= s / 2 * (2 * s) := hm
      _ = s ^ 2 := by ring
      _ = L := hs_sq
  have ha_logc : 0 <= a + Real.log c := by
    dsimp [a]
    have := hthresholdN
    dsimp [S, s, L] at this
    linarith
  have hone : 1 <= Real.exp a * c := by
    calc
      1 = Real.exp 0 := by rw [Real.exp_zero]
      _ <= Real.exp (a + Real.log c) := Real.exp_le_exp.mpr ha_logc
      _ = Real.exp a * Real.exp (Real.log c) := Real.exp_add _ _
      _ = Real.exp a * c := by rw [Real.exp_log hc]
  have ha_delta : Real.exp a + 1 <= Real.exp (a + delta / 4) := by
    calc
      Real.exp a + 1 <= Real.exp a + Real.exp a * c := by linarith
      _ = Real.exp a * (1 + c) := by ring
      _ = Real.exp a * Real.exp (delta / 4) := by dsimp [c]; ring
      _ = Real.exp (a + delta / 4) := (Real.exp_add _ _).symm
  have hlogmono : L <= Real.log (((N + 1 : Nat) : Real)) := by
    dsimp [L]
    apply Real.log_le_log (by
      have : (1 : Real) < (N : Real) :=
        (Real.log_pos_iff (by positivity)).mp hlogN
      linarith)
    exact_mod_cast (show N <= N + 1 by omega)
  have hab : a + delta / 4 <= b := by
    dsimp [a, b]
    have hdiv := div_le_div_of_nonneg_right hlogmono hnpos.le
    linarith
  change Real.exp a + 1 <= Real.exp b
  exact ha_delta.trans (Real.exp_le_exp.mpr hab)

/-- Once the selected dimension is positive, flooring the real radix keeps
the full digit image inside the inclusive ambient interval. -/
theorem ambientFit_proof : AmbientFitPackage := by
  obtain ⟨Ndim, hdim⟩ := dimensionControl_proof
  refine ⟨Ndim, ?_⟩
  intro N hN
  have hdim := hdim N hN
  have hnpos : 0 < (sharpDimension N : Real) := by
    exact_mod_cast (show 0 < sharpDimension N from
      lt_of_lt_of_le (by decide) hdim.1)
  have hbase : (0 : Real) <= ((N + 1 : Nat) : Real) := by positivity
  have hrpow : (0 : Real) <=
      ((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹ :=
    Real.rpow_nonneg hbase _
  have hfloor : (sharpRadix N : Real) <=
      ((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹ / 2 := by
    simpa only [sharpRadix] using Nat.floor_le (div_nonneg hrpow (by norm_num))
  have htwo : ((2 * sharpRadix N : Nat) : Real) <=
      ((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹ := by
    norm_num at hfloor ⊢
    linarith
  have hsub : ((2 * sharpRadix N - 1 : Nat) : Real) <=
      ((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹ := by
    exact (Nat.cast_le.mpr (Nat.sub_le _ _)).trans htwo
  have hpow : (((2 * sharpRadix N - 1 : Nat) : Real) ^ sharpDimension N) <=
      (((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹) ^
        sharpDimension N := by
    exact pow_le_pow_left₀ (Nat.cast_nonneg _) hsub _
  have hnorm :
      (((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹) ^
          sharpDimension N = ((N + 1 : Nat) : Real) :=
    Real.rpow_inv_natCast_pow hbase (by exact_mod_cast hnpos.ne')
  exact_mod_cast hpow.trans_eq hnorm

/-- Ceiling rounding contributes at most one extra `log 2` to the linear
dimension loss. -/
theorem linearCeiling_proof : LinearCeilingPackage := by
  refine ⟨0, ?_⟩
  intro N _hN hcontrol
  let x : Real := 2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2
  let y : Real := 2 * Real.log (((N + 1 : Nat) : Real)) * Real.log 2
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hx : 0 <= x := by dsimp only [x]; positivity
  have hy : 0 <= y := by dsimp only [y]; positivity
  have hnupper : (sharpDimension N : Real) <= Real.sqrt x + 1 := by
    have habs := (abs_le.mp hcontrol.2).2
    change (sharpDimension N : Real) - Real.sqrt x <= 1 at habs
    linarith
  have hmul : (sharpDimension N : Real) * Real.log 2 <=
      (Real.sqrt x + 1) * Real.log 2 :=
    mul_le_mul_of_nonneg_right hnupper hlog2.le
  have hsqrt_mul : Real.sqrt x * Real.log 2 = Real.sqrt y := by
    have hsqrtx : 0 <= Real.sqrt x := Real.sqrt_nonneg _
    have hsqrty : 0 <= Real.sqrt y := Real.sqrt_nonneg _
    apply (sq_eq_sq₀ (mul_nonneg hsqrtx hlog2.le) hsqrty).mp
    rw [mul_pow, Real.sq_sqrt hx, Real.sq_sqrt hy]
    dsimp only [x, y]
    field_simp [hlog2.ne']
  rw [add_mul, one_mul, hsqrt_mul] at hmul
  simpa only [y] using hmul

/-- The increment from `N` to `N + 1` and the fixed ceiling loss are
eventually absorbed by the allocated linear slack. -/
theorem linearIncrementAbsorption_proof : LinearIncrementAbsorptionPackage := by
  intro delta hdelta
  let A : Real := Real.sqrt (2 * Real.log 2)
  let S : Nat -> Real := fun N => Real.sqrt (Real.log (N : Real))
  let T : Nat -> Real := fun N =>
    Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) * Real.log 2)
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hA : 0 < A := by dsimp [A]; positivity
  have hTlog : Tendsto (fun N : Nat => Real.log (N : Real)) atTop atTop :=
    Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop
  have hTS : Tendsto S atTop atTop :=
    Real.tendsto_sqrt_atTop.comp hTlog
  have hlarge : ∀ᶠ N : Nat in atTop,
      max 1 (max (16 * Real.log 2 / delta) (16 * A / delta)) <= S N :=
    hTS.eventually_ge_atTop _
  have hinc0 : Tendsto (fun N : Nat =>
      Real.log (((N + 1 : Nat) : Real)) - Real.log (N : Real)) atTop (nhds 0) :=
    Real.tendsto_log_nat_add_one_sub_log.congr' <| by
      filter_upwards with N
      simp only [Nat.cast_add, Nat.cast_one]
  have hinc : ∀ᶠ N : Nat in atTop,
      Real.log (((N + 1 : Nat) : Real)) - Real.log (N : Real) <= 1 :=
    (hinc0.eventually_lt_const (by norm_num)).mono fun _ h => h.le
  have hpos : ∀ᶠ N : Nat in atTop, 0 < Real.log (N : Real) :=
    hTlog.eventually_gt_atTop 0
  have hall := hlarge.and (hinc.and hpos)
  obtain ⟨N0, hN0⟩ := eventually_atTop.1 hall
  refine ⟨N0, ?_⟩
  intro N hN
  obtain ⟨hlargeN, hincN, hlogN⟩ := hN0 N hN
  let L : Real := Real.log (N : Real)
  let s : Real := Real.sqrt L
  let t : Real := T N
  have hspos : 0 < s := by dsimp [s]; exact Real.sqrt_pos.2 hlogN
  have hs_sq : s ^ 2 = L := by dsimp [s]; exact Real.sq_sqrt hlogN.le
  have ht0 : 0 <= t := by dsimp [t, T]; positivity
  have ht_sq : t ^ 2 =
      2 * Real.log (((N + 1 : Nat) : Real)) * Real.log 2 := by
    dsimp [t, T]
    rw [Real.sq_sqrt]
    positivity
  have hA_sq : A ^ 2 = 2 * Real.log 2 := by
    dsimp [A]
    rw [Real.sq_sqrt]
    positivity
  have hlogInc : Real.log (((N + 1 : Nat) : Real)) <= L + 1 := by
    dsimp [L]
    linarith
  have hlogmono : L <= Real.log (((N + 1 : Nat) : Real)) := by
    dsimp [L]
    have hNpos : 0 < (N : Real) := by
      have : (1 : Real) < (N : Real) :=
        (Real.log_pos_iff (by positivity)).mp hlogN
      linarith
    apply Real.log_le_log hNpos
    exact_mod_cast (show N <= N + 1 by omega)
  let B : Real := Real.log (((N + 1 : Nat) : Real))
  have hBpos : 0 < B := hlogN.trans_le hlogmono
  have hsqrtB : Real.sqrt B <= s + 1 / s := by
    rw [Real.sqrt_le_iff]
    constructor
    · positivity
    · calc
        B <= L + 1 := by simpa only [B] using hlogInc
        _ <= (s + 1 / s) ^ 2 := by
          rw [add_pow_two, hs_sq]
          have hs_ne := hspos.ne'
          field_simp [hs_ne]
          nlinarith [sq_nonneg (s - 1)]
  have ht_factor : t = A * Real.sqrt B := by
    dsimp [t, T, A, B]
    rw [← Real.sqrt_mul (by positivity)]
    congr 1
    ring
  have ht_upper : t <= A * s + A / s := by
    rw [ht_factor]
    have := mul_le_mul_of_nonneg_left hsqrtB hA.le
    convert this using 1 <;> ring
  have hbudget : Real.log 2 + A / s <= delta / 8 * s := by
    have hlargeN' :
        max 1 (max (16 * Real.log 2 / delta) (16 * A / delta)) <= s := by
      simpa only [S, s, L] using hlargeN
    have hs_one : 1 <= s := (le_max_left _ _).trans hlargeN'
    have hs_log : 16 * Real.log 2 / delta <= s :=
      (le_max_left _ _).trans ((le_max_right _ _).trans hlargeN')
    have hs_A : 16 * A / delta <= s :=
      (le_max_right _ _).trans ((le_max_right _ _).trans hlargeN')
    have hfixed : Real.log 2 <= delta / 16 * s := by
      rw [div_le_iff₀ hdelta] at hs_log
      nlinarith
    have hAfixed : A <= delta / 16 * s := by
      rw [div_le_iff₀ hdelta] at hs_A
      nlinarith
    have hinv : A / s <= delta / 16 * s := by
      exact (div_le_self (by positivity) hs_one).trans hAfixed
    linarith
  change t + Real.log 2 <= (A + delta / 8) * s
  calc
    t + Real.log 2 <= A * s + A / s + Real.log 2 := by linarith
    _ <= A * s + delta / 8 * s := by linarith
    _ = (A + delta / 8) * s := by ring

/-- The rounded dimension is eventually at most twice the square-root
logarithmic scale, which absorbs its allocated slack. -/
theorem dimensionSlack_proof : DimensionSlackPackage := by
  intro delta hdelta
  refine ⟨2, ?_⟩
  intro N hN hcontrol
  let A : Real := Real.log (N : Real)
  let B : Real := Real.log (((N + 1 : Nat) : Real))
  let l : Real := Real.log 2
  let x : Real := Real.sqrt (2 * B / l)
  let S : Real := Real.sqrt A
  have hNpos : (0 : Real) < (N : Real) := by positivity
  have hN1 : (1 : Real) < (N : Real) := by
    exact_mod_cast (show 1 < N from lt_of_lt_of_le (by decide) hN)
  have hApos : 0 < A := by dsimp only [A]; exact Real.log_pos hN1
  have hlpos : 0 < l := by dsimp only [l]; exact Real.log_pos one_lt_two
  have hNp1_le : N + 1 <= 2 * N := by omega
  have hB_le : B <= A + l := by
    dsimp only [A, B, l]
    calc
      Real.log (((N + 1 : Nat) : Real)) <= Real.log (((2 * N : Nat) : Real)) := by
        apply Real.log_le_log (by positivity)
        exact_mod_cast hNp1_le
      _ = Real.log (N : Real) + Real.log 2 := by
        rw [Nat.cast_mul, Real.log_mul (by norm_num) (by positivity)]
        ring
  have h2le3l : (2 : Real) <= 3 * l := by
    dsimp only [l]
    linarith [Real.log_two_gt_d9]
  have hxarg : 2 * B / l <= 3 * A + 2 := by
    have hscaled := div_le_div_of_nonneg_right
      (mul_le_mul_of_nonneg_left hB_le (by norm_num : (0 : Real) <= 2)) hlpos.le
    have hcoef : 2 * A / l <= 3 * A := by
      rw [div_le_iff₀ hlpos]
      nlinarith
    calc
      2 * B / l <= 2 * (A + l) / l := hscaled
      _ = 2 * A / l + 2 := by field_simp [hlpos.ne']
      _ <= 3 * A + 2 := by linarith
  have hSsq : S ^ 2 = A := by
    dsimp only [S]
    exact Real.sq_sqrt hApos.le
  have hAlog2 : l <= A := by
    dsimp only [A, l]
    exact Real.log_le_log (by norm_num) (by exact_mod_cast hN)
  have hS_tenth : (1 / 10 : Real) <= S := by
    apply Real.le_sqrt_of_sq_le
    dsimp only [S]
    norm_num
    linarith [Real.log_two_gt_d9]
  have harg : 3 * A + 2 <= (2 * S + 1) ^ 2 := by
    rw [add_pow_two, mul_pow, hSsq]
    nlinarith
  have hx_le : x <= 2 * S + 1 := by
    dsimp only [x]
    rw [Real.sqrt_le_iff]
    constructor
    · positivity
    · exact hxarg.trans harg
  have hn_lt : (sharpDimension N : Real) < x + 1 := by
    simpa only [sharpDimension, x, A, B, l, Nat.cast_add, Nat.cast_one] using
      Nat.ceil_lt_add_one (Real.sqrt_nonneg (2 * B / l))
  have hnsub : ((sharpDimension N - 2 : Nat) : Real) <= 2 * S := by
    rw [Nat.cast_sub hcontrol.1]
    norm_num
    exact le_of_lt (by linarith [hn_lt, hx_le])
  have hdelta4 : 0 <= delta / 4 := by positivity
  have hmul := mul_le_mul_of_nonneg_left hnsub hdelta4
  dsimp only [S] at hmul ⊢
  nlinarith

/-- The logarithm of the rounded dimension is lower order than the
square-root logarithmic scale. -/
theorem logDimensionLoss_proof : LogDimensionLossPackage := by
  intro delta hdelta
  let S : Nat -> Real := fun N => Real.sqrt (Real.log (N : Real))
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hTlog : Tendsto (fun N : Nat => Real.log (N : Real)) atTop atTop :=
    Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop
  have hTS : Tendsto S atTop atTop :=
    Real.tendsto_sqrt_atTop.comp hTlog
  have hlarge : ∀ᶠ N : Nat in atTop, 5 <= S N := hTS.eventually_ge_atTop 5
  have hinc0 : Tendsto (fun N : Nat =>
      Real.log (((N + 1 : Nat) : Real)) - Real.log (N : Real)) atTop (nhds 0) :=
    Real.tendsto_log_nat_add_one_sub_log.congr' <| by
      filter_upwards with N
      simp only [Nat.cast_add, Nat.cast_one]
  have hinc : ∀ᶠ N : Nat in atTop,
      Real.log (((N + 1 : Nat) : Real)) - Real.log (N : Real) <= 1 :=
    (hinc0.eventually_lt_const (by norm_num)).mono fun _ h => h.le
  have hpos : ∀ᶠ N : Nat in atTop, 0 < Real.log (N : Real) :=
    hTlog.eventually_gt_atTop 0
  have hdim_bound : ∀ᶠ N : Nat in atTop,
      Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2) + 1 <=
        2 * S N := by
    filter_upwards [hlarge, hinc, hpos] with N hL hI hP
    let L : Real := Real.log (N : Real)
    let s : Real := Real.sqrt L
    have hlogInc : Real.log (((N + 1 : Nat) : Real)) <= L + 1 := by
      dsimp [L]
      linarith
    have hs_sq : s ^ 2 = L := by
      dsimp [s]
      exact Real.sq_sqrt hP.le
    have hcoef : Real.sqrt (2 / Real.log 2) < (7 / 4 : Real) := by
      rw [Real.sqrt_lt' (by norm_num : (0 : Real) < 7 / 4)]
      rw [div_lt_iff₀ hlog2]
      nlinarith [Real.log_two_gt_d9]
    have hfactor :
        Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2) =
          Real.sqrt (2 / Real.log 2) *
            Real.sqrt (Real.log (((N + 1 : Nat) : Real))) := by
      rw [← Real.sqrt_mul (by positivity)]
      congr 1
      field_simp [hlog2.ne']
    have hsqrtInc :
        Real.sqrt (Real.log (((N + 1 : Nat) : Real))) <= s + 1 / 8 := by
      rw [Real.sqrt_le_iff]
      constructor
      · positivity
      · rw [add_pow_two, hs_sq]
        have hs0 : 0 <= s := by positivity
        have hs5 : 5 <= s := by simpa only [S, s, L] using hL
        nlinarith
    have hmain :
        Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2) <=
          (7 / 4 : Real) * (s + 1 / 8) := by
      rw [hfactor]
      exact mul_le_mul hcoef.le hsqrtInc (Real.sqrt_nonneg _) (by positivity)
    have hs5 : 5 <= s := by simpa only [S, s, L] using hL
    have hroom : (7 / 4 : Real) * (s + 1 / 8) + 1 <= 2 * s := by
      nlinarith
    simpa only [S, s, L] using (by linarith :
      Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2) + 1 <= 2 * s)
  have hsLittle : (fun N : Nat => Real.log (S N)) =o[atTop] S := by
    exact Real.isLittleO_log_id_atTop.comp_tendsto hTS
  have hsmall0 := (Asymptotics.isLittleO_iff.1 hsLittle)
    (show 0 < delta / 8 by positivity)
  have hsmall : ∀ᶠ N : Nat in atTop,
      Real.log (S N) <= delta / 8 * S N := by
    filter_upwards [hsmall0] with N hN
    rw [Real.norm_eq_abs, Real.norm_eq_abs] at hN
    have hlogle : Real.log (S N) <= |Real.log (S N)| := le_abs_self _
    have hsabs : |S N| = S N := abs_of_nonneg (by dsimp [S]; positivity)
    rw [hsabs] at hN
    exact hlogle.trans hN
  have hconstant : ∀ᶠ N : Nat in atTop,
      Real.log 2 - 2 * Real.log 2 < delta / 8 * S N := by
    have ht : Tendsto (fun N : Nat => delta / 8 * S N) atTop atTop :=
      hTS.const_mul_atTop (by positivity)
    exact ht.eventually_gt_atTop _
  have hall := hdim_bound.and (hlarge.and (hsmall.and hconstant))
  obtain ⟨N0, hN0⟩ := eventually_atTop.1 hall
  refine ⟨N0, ?_⟩
  intro N hN hctrl
  obtain ⟨hdimN, hlargeN, hsmallN, hconstantN⟩ := hN0 N hN
  have hnupper : (sharpDimension N : Real) <= 2 * S N := by
    have habs := (abs_le.mp hctrl.2).2
    exact (by linarith : (sharpDimension N : Real) <=
      Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2) + 1).trans hdimN
  have hnpos : 0 < (sharpDimension N : Real) := by
    exact_mod_cast (show 0 < sharpDimension N from
      lt_of_lt_of_le (by decide) hctrl.1)
  have hspos : 0 < S N := by
    exact (by linarith : 0 < S N)
  have hlogmono : Real.log (sharpDimension N : Real) <= Real.log (2 * S N) :=
    Real.log_le_log hnpos hnupper
  have hlogmul : Real.log (2 * S N) = Real.log 2 + Real.log (S N) := by
    rw [Real.log_mul (by norm_num) hspos.ne']
  rw [hlogmul] at hlogmono
  linarith

/-- The dimension ceiling is large enough for the reciprocal half of the
balanced exponent, without spending any epsilon slack. -/
theorem reciprocalBalancedCore_proof : ReciprocalBalancedCorePackage := by
  refine ⟨2, ?_⟩
  intro N hN hcontrol
  let A : Real := Real.log (N : Real)
  let B : Real := Real.log (((N + 1 : Nat) : Real))
  let l : Real := Real.log 2
  let s : Real := Real.sqrt (2 * B / l)
  let t : Real := Real.sqrt (2 * l) * Real.sqrt A
  have hN1 : (1 : Real) < (N : Real) := by
    exact_mod_cast (show 1 < N from lt_of_lt_of_le (by decide) hN)
  have hA : 0 < A := by dsimp only [A]; exact Real.log_pos hN1
  have hl : 0 < l := by dsimp only [l]; exact Real.log_pos (by norm_num)
  have hB : 0 < B := by
    dsimp only [B]
    exact Real.log_pos (by exact_mod_cast (show 1 < N + 1 by omega))
  have hAB : A <= B := by
    dsimp only [A, B]
    apply Real.log_le_log (by positivity)
    exact_mod_cast (show N <= N + 1 by omega)
  have hs0 : 0 <= s := by dsimp only [s]; exact Real.sqrt_nonneg _
  have ht0 : 0 <= t := by dsimp only [t]; positivity
  have hnpos : 0 < (sharpDimension N : Real) := by
    exact_mod_cast (show 0 < sharpDimension N from
      lt_of_lt_of_le (by decide) hcontrol.1)
  have hsn : s <= (sharpDimension N : Real) := by
    change Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2) <=
      (sharpDimension N : Real)
    simpa only [sharpDimension, Nat.cast_add, Nat.cast_one] using
      (Nat.le_ceil
        (Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2)))
  have hcore : 2 * A <= t * s := by
    apply (sq_le_sq₀ (mul_nonneg (by norm_num) hA.le) (mul_nonneg ht0 hs0)).mp
    have hs_sq : s ^ 2 = 2 * B / l := by
      dsimp only [s]
      rw [Real.sq_sqrt]
      positivity
    have htl_sq : Real.sqrt (2 * l) ^ 2 = 2 * l :=
      Real.sq_sqrt (by positivity)
    have hA_sq : Real.sqrt A ^ 2 = A := Real.sq_sqrt hA.le
    dsimp only [t]
    rw [show (Real.sqrt (2 * l) * Real.sqrt A * s) ^ 2 =
      Real.sqrt (2 * l) ^ 2 * Real.sqrt A ^ 2 * s ^ 2 by ring,
      htl_sq, hA_sq, hs_sq]
    rw [div_eq_mul_inv]
    calc
      (2 * A) ^ 2 = 4 * A ^ 2 := by ring
      _ <= 4 * (A * B) := by
        gcongr
        simpa only [pow_two] using mul_le_mul_of_nonneg_left hAB hA.le
      _ = (2 * l * A) * (2 * B * l⁻¹) := by
        field_simp [hl.ne']
        ring
  have htn := mul_le_mul_of_nonneg_left hsn ht0
  rw [div_le_iff₀ hnpos]
  change 2 * A <= t * (sharpDimension N : Real)
  exact hcore.trans htn

/-- Install the existing checked slack adapter on the proved reciprocal core. -/
theorem reciprocalDimensionLoss_proof : ReciprocalDimensionLossPackage :=
  reciprocalLoss_of_balanced_core reciprocalBalancedCore_proof

/-- The real radix before flooring is eventually at least one. -/
theorem radixBase_eventually_one :
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      1 <= ((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹ / 2 := by
  refine ⟨255, ?_⟩
  intro N hN
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hNplus : (256 : Nat) <= N + 1 := by omega
  have hNpluspos : 0 < (((N + 1 : Nat) : Real)) := by positivity
  have hNplusone : (1 : Real) < (((N + 1 : Nat) : Real)) := by
    exact_mod_cast (show 1 < N + 1 by omega)
  have hlogNplus : 0 < Real.log (((N + 1 : Nat) : Real)) := Real.log_pos hNplusone
  have hlogNplus' : 0 < Real.log ((N : Real) + 1) := by
    simpa only [Nat.cast_add, Nat.cast_one] using hlogNplus
  have hpow : (2 : Real) ^ ((8 : Nat) : Real) <= (((N + 1 : Nat) : Real)) := by
    rw [Real.rpow_natCast]
    norm_num
    exact_mod_cast hNplus
  have hL8 : 8 * Real.log 2 <= Real.log (((N + 1 : Nat) : Real)) := by
    rw [← Real.log_rpow (by norm_num : (0 : Real) < 2)]
    exact Real.log_le_log (by positivity) hpow
  let r : Real := Real.log (((N + 1 : Nat) : Real)) / Real.log 2
  have hr8 : 8 <= r := by
    dsimp only [r]
    exact (le_div_iff₀ hlog2).2 hL8
  have hr0 : 0 <= r := le_trans (by norm_num) hr8
  let x : Real := Real.sqrt (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2)
  have hrad : 2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2 = 2 * r := by
    dsimp only [r]
    ring
  have hxr : x <= r / 2 := by
    rw [← Real.sqrt_sq (by positivity : 0 <= r / 2)]
    apply Real.sqrt_le_sqrt
    rw [hrad]
    have hmul : 16 * r <= 2 * r ^ 2 := by
      calc
        16 * r = 8 * (2 * r) := by ring
        _ <= r * (2 * r) :=
          mul_le_mul_of_nonneg_right hr8 (mul_nonneg (by norm_num) hr0)
        _ = 2 * r ^ 2 := by ring
    calc
      2 * r <= r ^ 2 / 4 := by linarith
      _ = (r / 2) ^ 2 := by ring
  have hn_lt : (sharpDimension N : Real) < x + 1 := by
    simpa only [sharpDimension, x, Nat.cast_add, Nat.cast_one] using
      (Nat.ceil_lt_add_one
        (Real.sqrt_nonneg (2 * Real.log (((N + 1 : Nat) : Real)) / Real.log 2)))
  have hn_le_r : (sharpDimension N : Real) <= r := by linarith
  have hnpos_nat : 0 < sharpDimension N := by
    simp only [sharpDimension]
    rw [Nat.ceil_pos]
    apply Real.sqrt_pos.2
    exact div_pos (mul_pos (by norm_num) hlogNplus') hlog2
  have hnpos : 0 < (sharpDimension N : Real) := by exact_mod_cast hnpos_nat
  have hlogdiv : Real.log 2 <=
      Real.log (((N + 1 : Nat) : Real)) / (sharpDimension N : Real) := by
    rw [le_div_iff₀ hnpos]
    have hmul := mul_le_mul_of_nonneg_right hn_le_r hlog2.le
    have hmul' : (sharpDimension N : Real) * Real.log 2 <=
        Real.log (((N + 1 : Nat) : Real)) := by
      calc
        (sharpDimension N : Real) * Real.log 2 <= r * Real.log 2 := hmul
        _ = Real.log (((N + 1 : Nat) : Real)) := by
          dsimp only [r]
          exact div_mul_cancel₀ _ hlog2.ne'
    simpa only [mul_comm] using hmul'
  have hexp : (2 : Real) <=
      Real.exp (Real.log (((N + 1 : Nat) : Real)) /
        (sharpDimension N : Real)) := by
    rw [← Real.exp_log (by norm_num : (0 : Real) < 2), Real.exp_le_exp]
    exact hlogdiv
  rw [Real.rpow_def_of_pos hNpluspos]
  rw [le_div_iff₀ (by norm_num : (0 : Real) < 2)]
  simpa only [one_mul, div_eq_mul_inv] using hexp

/-- The selected natural radix is eventually nonzero. -/
theorem radixNonzero_proof : RadixNonzeroPackage := by
  obtain ⟨N0, hbase⟩ := radixBase_eventually_one
  refine ⟨N0, ?_⟩
  intro N hN
  have hb := hbase N hN
  rw [sharpRadix, ne_eq, Nat.floor_eq_zero]
  simp only [not_lt]
  exact hb

/-- Subtracting one absorbs the complete loss from the natural floor. -/
theorem radixFloor_proof : RadixFloorPackage := by
  obtain ⟨N0, hbase⟩ := radixBase_eventually_one
  refine ⟨N0, ?_⟩
  intro N hN
  have hb := hbase N hN
  refine ⟨by simpa only [radixProxy, sub_nonneg] using hb, ?_⟩
  exact (Nat.sub_one_lt_floor
    (((N + 1 : Nat) : Real) ^ (sharpDimension N : Real)⁻¹ / 2)).le

/-- Proof-phase installation of the pinned quantitative construction body. -/
theorem quantitativeConstruction_installed : QuantitativeConstructionPackage :=
  pinnedQuantitativeConstruction

/-- Proof-phase installation of the checked inclusive-index transport. -/
theorem indexMonotonicity_installed : IndexMonotonicityPackage :=
  pinnedIndexMonotonicity

/-! The remaining declarations replay the frozen child-to-root composition
after all analytic leaves have acquired proof bodies. -/

theorem parameterAdmissibility_proof : ParameterAdmissibilityPackage :=
  parameterAdmissibility_of_dimension_and_radix
    dimensionControl_proof radixNonzero_proof

theorem proxyLogLower_proof : ProxyLogLowerPackage :=
  proxyLogLower_of_identity_and_slack
    proxyRpowIdentity_proof proxySlackAbsorption_proof

theorem linearDimensionLoss_proof : LinearDimensionLossPackage :=
  linearLoss_of_ceiling_and_increment
    linearCeiling_proof linearIncrementAbsorption_proof

theorem subleadingLoss_proof : SubleadingLossPackage :=
  subleadingLoss_of_dimension_and_log
    dimensionSlack_proof logDimensionLoss_proof

theorem optimalExponentBridge_proof : OptimalExponentBridgePackage :=
  optimalExponent_of_components
    proxyLogLower_proof reciprocalDimensionLoss_proof
      linearDimensionLoss_proof subleadingLoss_proof

theorem proxyAsymptotic_proof : ProxyAsymptoticPackage :=
  proxyAsymptotic_of_dimension_and_bridge
    dimensionControl_proof optimalExponentBridge_proof

theorem ratioAsymptotic_proof : RatioAsymptoticPackage :=
  ratioAsymptotic_of_proxy_floor_and_dimension
    proxyAsymptotic_proof radixFloor_proof dimensionControl_proof

theorem sharpEstimate_proof : SharpEstimatePackage :=
  sharpEstimate_of_normalization_and_ratio
    rpowNormalization_proof ratioAsymptotic_proof

theorem sharpParameter_proof : SharpParameterPackage :=
  sharpParameters_of_components parameterAdmissibility_proof
    ambientFit_proof sharpEstimate_proof

theorem exactAssembly_proof : ExactAssembly :=
  exactAssembly_of_children quantitativeConstruction_installed
    sharpParameter_proof indexMonotonicity_installed

/-- Exact premise-free closure of the frozen historical Behrend target. -/
theorem exactRoot_proof : Root :=
  root_of_exactAssembly exactAssembly_proof

/-- Direct binding of the checked root to the statement-phase canonical name. -/
theorem behrendConstructionTarget_proof :
    Stage1Instances.THM_M_0957.BehrendConstructionTarget :=
  exactRoot_proof

assert_no_sorry dimensionControl_proof
assert_no_sorry rpowNormalization_proof
assert_no_sorry proxyRpowIdentity_proof
assert_no_sorry ambientFit_proof
assert_no_sorry linearCeiling_proof
assert_no_sorry reciprocalBalancedCore_proof
assert_no_sorry reciprocalDimensionLoss_proof
assert_no_sorry radixNonzero_proof
assert_no_sorry radixFloor_proof
assert_no_sorry quantitativeConstruction_installed
assert_no_sorry indexMonotonicity_installed
assert_no_sorry proxySlackAbsorption_proof
assert_no_sorry linearIncrementAbsorption_proof
assert_no_sorry dimensionSlack_proof
assert_no_sorry logDimensionLoss_proof
assert_no_sorry parameterAdmissibility_proof
assert_no_sorry proxyLogLower_proof
assert_no_sorry linearDimensionLoss_proof
assert_no_sorry subleadingLoss_proof
assert_no_sorry optimalExponentBridge_proof
assert_no_sorry proxyAsymptotic_proof
assert_no_sorry ratioAsymptotic_proof
assert_no_sorry sharpEstimate_proof
assert_no_sorry sharpParameter_proof
assert_no_sorry exactAssembly_proof
assert_no_sorry exactRoot_proof
assert_no_sorry behrendConstructionTarget_proof

#print sorries dimensionControl_proof
#print sorries rpowNormalization_proof
#print sorries proxyRpowIdentity_proof
#print sorries ambientFit_proof
#print sorries linearCeiling_proof
#print sorries reciprocalBalancedCore_proof
#print sorries reciprocalDimensionLoss_proof
#print sorries radixNonzero_proof
#print sorries radixFloor_proof
#print sorries quantitativeConstruction_installed
#print sorries indexMonotonicity_installed
#print sorries proxySlackAbsorption_proof
#print sorries linearIncrementAbsorption_proof
#print sorries dimensionSlack_proof
#print sorries logDimensionLoss_proof
#print sorries parameterAdmissibility_proof
#print sorries proxyLogLower_proof
#print sorries linearDimensionLoss_proof
#print sorries subleadingLoss_proof
#print sorries optimalExponentBridge_proof
#print sorries proxyAsymptotic_proof
#print sorries ratioAsymptotic_proof
#print sorries sharpEstimate_proof
#print sorries sharpParameter_proof
#print sorries exactAssembly_proof
#print sorries exactRoot_proof
#print sorries behrendConstructionTarget_proof

#print axioms dimensionControl_proof
#print axioms rpowNormalization_proof
#print axioms proxyRpowIdentity_proof
#print axioms ambientFit_proof
#print axioms linearCeiling_proof
#print axioms reciprocalBalancedCore_proof
#print axioms reciprocalDimensionLoss_proof
#print axioms radixNonzero_proof
#print axioms radixFloor_proof
#print axioms quantitativeConstruction_installed
#print axioms indexMonotonicity_installed
#print axioms proxySlackAbsorption_proof
#print axioms linearIncrementAbsorption_proof
#print axioms dimensionSlack_proof
#print axioms logDimensionLoss_proof
#print axioms parameterAdmissibility_proof
#print axioms proxyLogLower_proof
#print axioms linearDimensionLoss_proof
#print axioms subleadingLoss_proof
#print axioms optimalExponentBridge_proof
#print axioms proxyAsymptotic_proof
#print axioms ratioAsymptotic_proof
#print axioms sharpEstimate_proof
#print axioms sharpParameter_proof
#print axioms exactAssembly_proof
#print axioms exactRoot_proof
#print axioms behrendConstructionTarget_proof

end Stage1Instances.THM_M_0957_ObligationTree
