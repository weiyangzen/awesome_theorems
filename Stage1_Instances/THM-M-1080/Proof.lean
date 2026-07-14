import Mathlib.Probability.Moments.SubGaussian
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Series

/-!
# THM-M-1080 proof bodies

This module proves the arbitrary-measurable-space bounded-increment form directly. It derives a
conditional Hoeffding bound from the martingale conditional-mean law, iterates the exponential
moment estimate, applies Chernoff's inequality, and includes all zero-boundary cases.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1080.Proof

universe u

def squaredBoundSum (c : Nat -> NNReal) (n : Nat) : Real :=
  ∑ k ∈ Finset.range n, (c (k + 1) : Real) ^ 2

def PositiveThresholdPackage : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal),
      Martingale X G mu ->
      forall n : Nat,
        (forall k, k < n -> ∀ᵐ omega ∂mu,
          |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
        forall t : Real, 0 < t ->
          mu.real {omega | t <= X n omega - X 0 omega} <=
            Real.exp (-(t ^ 2) / (2 * squaredBoundSum c n))

/-- The exponential lies below the secant through the symmetric endpoints `-a` and `a`. -/
theorem exp_secant_bound (a x lambda : Real) (ha : 0 < a) (hx : |x| <= a) :
    Real.exp (lambda * x) <=
      Real.cosh (lambda * a) + (x / a) * Real.sinh (lambda * a) := by
  have hxa : |x / a| <= 1 := by
    rw [abs_div, abs_of_pos ha]
    exact (div_le_one ha).2 hx
  convert Real.exp_mul_le_cosh_add_mul_sinh hxa (lambda * a) using 1 <;> field_simp <;> ring

/-- The martingale increments telescope to the endpoint difference. -/
theorem sum_increment_eq_sub (X : Nat -> Omega -> Real) (n : Nat) (omega : Omega) :
    (∑ k ∈ Finset.range n, (X (k + 1) omega - X k omega)) = X n omega - X 0 omega := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Finset.sum_range_succ, ih]
      ring

/-- Conditional Hoeffding bound for one martingale increment, without a standard-Borel premise. -/
theorem condExp_exp_increment_le
    (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal) (hMart : Martingale X G mu) (k : Nat)
    (hBound : ∀ᵐ omega ∂mu,
      |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) (lambda : Real) :
    ∀ᵐ omega ∂mu,
      (mu[fun omega => Real.exp (lambda * (X (k + 1) omega - X k omega)) | G k]) omega <=
        Real.exp ((c (k + 1) : Real) ^ 2 * lambda ^ 2 / 2) := by
  let Y : Omega -> Real := fun omega => X (k + 1) omega - X k omega
  have hY_int : Integrable Y mu := (hMart.integrable (k + 1)).sub (hMart.integrable k)
  have hY_meas : AEMeasurable Y mu := hY_int.aestronglyMeasurable.aemeasurable
  have hY_mem : ∀ᵐ omega ∂mu,
      Y omega ∈ Set.Icc (-(c (k + 1) : Real)) (c (k + 1) : Real) := by
    filter_upwards [hBound] with omega hb
    simpa [Y, abs_le] using hb
  have hExp_int : Integrable (fun omega => Real.exp (lambda * Y omega)) mu :=
    ProbabilityTheory.integrable_exp_mul_of_mem_Icc
      (μ := mu) (a := -(c (k + 1) : Real)) (b := (c (k + 1) : Real))
        (t := lambda) hY_meas hY_mem
  have hCenter : (mu[Y | G k]) =ᵐ[mu] 0 := by
    calc
      (mu[Y | G k]) =ᵐ[mu] (mu[X (k + 1) | G k]) - (mu[X k | G k]) :=
        condExp_sub (hMart.integrable (k + 1)) (hMart.integrable k) (G k)
      _ =ᵐ[mu] X k - X k :=
        (hMart.condExp_ae_eq (Nat.le_succ k)).sub (hMart.condExp_ae_eq (le_refl k))
      _ =ᵐ[mu] 0 := by simp
  let C := Real.cosh (lambda * (c (k + 1) : Real))
  let r := Real.sinh (lambda * (c (k + 1) : Real)) / (c (k + 1) : Real)
  have hPoint : ∀ᵐ omega ∂mu,
      Real.exp (lambda * Y omega) <=
        C + r * Y omega := by
    by_cases hc : c (k + 1) = 0
    · filter_upwards [hY_mem, hCenter] with omega hy hzero
      have hy0 : Y omega = 0 := by simpa [hc] using hy
      simp [C, r, hc, hy0]
    · have hcpos : 0 < (c (k + 1) : Real) := NNReal.coe_pos.mpr (pos_iff_ne_zero.mpr hc)
      filter_upwards [hY_mem] with omega hy
      convert exp_secant_bound (c (k + 1) : Real) (Y omega) lambda hcpos
        ((abs_le).2 hy) using 1 <;> simp only [C, r] <;> ring
  have hRhs_int : Integrable
      (fun omega => C + r * Y omega) mu :=
    (integrable_const C).add (hY_int.const_mul r)
  have hCond := condExp_mono (m := G k) hExp_int hRhs_int hPoint
  have hRewrite :
      (mu[fun omega => C + r * Y omega | G k]) =ᵐ[mu]
      fun omega => C + r * (mu[Y | G k]) omega := by
    calc
      _ =ᵐ[mu] (mu[fun _ => C | G k]) + (mu[r • Y | G k]) :=
        condExp_add (integrable_const _) (hY_int.const_mul _) (G k)
      _ =ᵐ[mu] (fun _ => C) + r • (mu[Y | G k]) := by
        filter_upwards [condExp_smul r Y (G k)] with omega hsmul
        simp only [condExp_const (G.le k), Pi.add_apply, Pi.smul_apply, smul_eq_mul]
        exact congrArg (fun z => C + z) hsmul
      _ = _ := by rfl
  filter_upwards [hCond, hRewrite, hCenter] with omega hle heq hzero
  simp only [Pi.zero_apply] at hzero
  rw [heq, hzero, mul_zero, add_zero] at hle
  exact hle.trans <| by
    dsimp only [C]
    convert Real.cosh_le_exp_half_sq (lambda * (c (k + 1) : Real)) using 1 <;> ring

/-- The endpoint exponential is integrable under the finite family of increment bounds. -/
theorem exp_endpoint_integrable
    (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal) (hMart : Martingale X G mu) (n : Nat)
    (hBound : forall k, k < n -> ∀ᵐ omega ∂mu,
      |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) (lambda : Real) :
    Integrable (fun omega => Real.exp (lambda * (X n omega - X 0 omega))) mu := by
  have hmeas : AEMeasurable (fun omega => X n omega - X 0 omega) mu :=
    ((hMart.integrable n).sub (hMart.integrable 0)).aestronglyMeasurable.aemeasurable
  have hsumBound : ∀ᵐ omega ∂mu,
      |X n omega - X 0 omega| <= ∑ k ∈ Finset.range n, (c (k + 1) : Real) := by
    have hall : ∀ᵐ omega ∂mu, ∀ k, k < n ->
        |X (k + 1) omega - X k omega| <= (c (k + 1) : Real) :=
      ae_all_iff.2 fun k => ae_all_iff.2 fun hk => hBound k hk
    filter_upwards [hall] with omega hb
    rw [← sum_increment_eq_sub X n omega]
    exact (Finset.abs_sum_le_sum_abs _ _).trans
      (Finset.sum_le_sum fun k hk => hb k (Finset.mem_range.1 hk))
  apply ProbabilityTheory.integrable_exp_mul_of_mem_Icc
    (μ := mu) (a := -(∑ k ∈ Finset.range n, (c (k + 1) : Real)))
      (b := ∑ k ∈ Finset.range n, (c (k + 1) : Real)) (t := lambda) hmeas
  filter_upwards [hsumBound] with omega hb
  exact (abs_le).1 hb

/-- Finite iteration of the one-step conditional Hoeffding estimate. -/
theorem exp_increment_sum_integral_le
    (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal) (hMart : Martingale X G mu) (n : Nat)
    (hBound : forall k, k < n -> ∀ᵐ omega ∂mu,
      |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) (lambda : Real) :
    mu[fun omega => Real.exp (lambda * (X n omega - X 0 omega))] <=
      Real.exp (lambda ^ 2 * squaredBoundSum c n / 2) := by
  induction n with
  | zero => simp [squaredBoundSum]
  | succ n ih =>
      have hbn := hBound n (Nat.lt_succ_self n)
      have hprev : forall k, k < n -> ∀ᵐ omega ∂mu,
          |X (k + 1) omega - X k omega| <= (c (k + 1) : Real) :=
        fun k hk => hBound k (hk.trans (Nat.lt_succ_self n))
      specialize ih hprev
      let S : Omega -> Real := fun omega => X n omega - X 0 omega
      let Y : Omega -> Real := fun omega => X (n + 1) omega - X n omega
      have hS_meas : StronglyMeasurable[G n] S :=
        (hMart.stronglyMeasurable n).sub
          ((hMart.stronglyMeasurable 0).mono (G.mono (Nat.zero_le n)))
      have hS_bdd : ∀ᵐ omega ∂mu,
          |S omega| <= ∑ k ∈ Finset.range n, (c (k + 1) : Real) := by
        have hall : ∀ k ∈ Finset.range n, ∀ᵐ omega ∂mu,
            |X (k + 1) omega - X k omega| <= (c (k + 1) : Real) := by
          intro k hk
          exact hprev k (Finset.mem_range.mp hk)
        rw [← Finset.eventually_all] at hall
        filter_upwards [hall] with omega hall
        rw [show S omega = ∑ k ∈ Finset.range n,
            (X (k + 1) omega - X k omega) by
          simpa [S] using (sum_increment_eq_sub X n omega).symm]
        exact (Finset.abs_sum_le_sum_abs _ _).trans
          (Finset.sum_le_sum fun k hk => hall k hk)
      have hExpS_int : Integrable (fun omega => Real.exp (lambda * S omega)) mu := by
        apply ProbabilityTheory.integrable_exp_mul_of_mem_Icc
          (μ := mu) (a := -(∑ k ∈ Finset.range n, (c (k + 1) : Real)))
            (b := ∑ k ∈ Finset.range n, (c (k + 1) : Real)) (t := lambda)
              (hS_meas.mono (G.le n)).aemeasurable
        filter_upwards [hS_bdd] with omega hb
        exact (abs_le.mp hb)
      have hYexp_int : Integrable (fun omega => Real.exp (lambda * Y omega)) mu := by
        apply ProbabilityTheory.integrable_exp_mul_of_mem_Icc
          (μ := mu) (a := -(c (n + 1) : Real)) (b := (c (n + 1) : Real))
            (t := lambda)
          ((hMart.integrable (n + 1)).sub
            (hMart.integrable n)).aestronglyMeasurable.aemeasurable
        filter_upwards [hbn] with omega hb
        exact (abs_le).1 (by simpa [Y] using hb)
      have hProd_int : Integrable
          (fun omega => Real.exp (lambda * S omega) * Real.exp (lambda * Y omega)) mu := by
        have hProdBdd : ∀ᵐ omega ∂mu,
            |Real.exp (lambda * S omega) * Real.exp (lambda * Y omega)| <=
              Real.exp (|lambda| *
                ((∑ k ∈ Finset.range n, (c (k + 1) : Real)) + (c (n + 1) : Real))) := by
          filter_upwards [hS_bdd, hbn] with omega hs hy
          rw [abs_mul, abs_of_pos (Real.exp_pos _), abs_of_pos (Real.exp_pos _), ← Real.exp_add]
          apply Real.exp_le_exp.mpr
          calc
            lambda * S omega + lambda * Y omega
                <= |lambda * S omega| + |lambda * Y omega| :=
              add_le_add (le_abs_self _) (le_abs_self _)
            _ = |lambda| * |S omega| + |lambda| * |Y omega| := by simp [abs_mul]
            _ <= |lambda| * (∑ k ∈ Finset.range n, (c (k + 1) : Real)) +
                  |lambda| * (c (n + 1) : Real) := by gcongr
            _ = _ := by ring
        exact Integrable.mono' (integrable_const _) (hExpS_int.1.mul hYexp_int.1) hProdBdd
      calc
        mu[fun omega => Real.exp (lambda * (X (n + 1) omega - X 0 omega))]
            = mu[fun omega => Real.exp (lambda * S omega) * Real.exp (lambda * Y omega)] := by
              congr 1 with omega
              change Real.exp (lambda * (X (n + 1) omega - X 0 omega)) =
                Real.exp (lambda * S omega) * Real.exp (lambda * Y omega)
              rw [← Real.exp_add]
              congr 1
              simp only [S, Y]
              ring
        _ = mu[mu[fun omega => Real.exp (lambda * S omega) *
              Real.exp (lambda * Y omega) | G n]] := by
              rw [integral_condExp (G.le n)]
        _ = mu[fun omega => Real.exp (lambda * S omega) *
              (mu[fun omega => Real.exp (lambda * Y omega) | G n]) omega] := by
              apply integral_congr_ae
              exact condExp_mul_of_stronglyMeasurable_left
                (Real.continuous_exp.comp_stronglyMeasurable
                  (hS_meas.const_mul lambda)) hProd_int hYexp_int
        _ <= mu[fun omega => Real.exp (lambda * S omega) *
              Real.exp ((c (n + 1) : Real) ^ 2 * lambda ^ 2 / 2)] := by
              apply integral_mono_ae
              · exact integrable_condExp.congr
                  (condExp_mul_of_stronglyMeasurable_left
                    (Real.continuous_exp.comp_stronglyMeasurable
                      (hS_meas.const_mul lambda)) hProd_int hYexp_int)
              · fun_prop
              · have hone := condExp_exp_increment_le Omega mu G X c hMart n hbn lambda
                filter_upwards [hone] with omega hone
                exact mul_le_mul_of_nonneg_left hone (Real.exp_pos _).le
        _ = mu[fun omega => Real.exp (lambda * S omega)] *
              Real.exp ((c (n + 1) : Real) ^ 2 * lambda ^ 2 / 2) := by
              rw [integral_mul_const]
        _ <= Real.exp (lambda ^ 2 * squaredBoundSum c n / 2) *
              Real.exp ((c (n + 1) : Real) ^ 2 * lambda ^ 2 / 2) := by gcongr
        _ = Real.exp (lambda ^ 2 * squaredBoundSum c (n + 1) / 2) := by
              rw [← Real.exp_add]
              simp [squaredBoundSum, Finset.sum_range_succ]
              ring

/-- The positive-threshold terminal package, including the zero squared-bound branch. -/
theorem positiveThreshold
    (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal) (hMart : Martingale X G mu) (n : Nat)
    (hBound : forall k, k < n -> ∀ᵐ omega ∂mu,
      |X (k + 1) omega - X k omega| <= (c (k + 1) : Real))
    (t : Real) (ht : 0 < t) :
    mu.real {omega | t <= X n omega - X 0 omega} <=
      Real.exp (-(t ^ 2) / (2 * squaredBoundSum c n)) := by
  let S := squaredBoundSum c n
  have hS : 0 <= S := Finset.sum_nonneg fun _ _ => sq_nonneg _
  by_cases hS0 : S = 0
  · have hc0 : ∀ k, k < n -> c (k + 1) = 0 := by
      intro k hk
      have hterm : (c (k + 1) : Real) ^ 2 = 0 := by
        have hle : (c (k + 1) : Real) ^ 2 <= S := by
          dsimp only [S, squaredBoundSum]
          exact Finset.single_le_sum (fun j _ => sq_nonneg ((c (j + 1) : Real)))
            (Finset.mem_range.2 hk)
        nlinarith
      exact NNReal.coe_eq_zero.mp (sq_eq_zero_iff.mp hterm)
    have hdiff0 : ∀ᵐ omega ∂mu, X n omega - X 0 omega = 0 := by
      have hall : ∀ᵐ omega ∂mu, ∀ k, k < n ->
          X (k + 1) omega - X k omega = 0 :=
        ae_all_iff.2 fun k => ae_all_iff.2 fun hk => by
          filter_upwards [hBound k hk] with omega hb
          have hzero : |X (k + 1) omega - X k omega| <= 0 := by
            simpa [hc0 k hk] using hb
          exact abs_eq_zero.mp (le_antisymm hzero (abs_nonneg _))
      filter_upwards [hall] with omega hall
      rw [← sum_increment_eq_sub X n omega]
      exact Finset.sum_eq_zero fun k hk => hall k (Finset.mem_range.1 hk)
    have hevent : {omega | t <= X n omega - X 0 omega} =ᵐ[mu] (∅ : Set Omega) := by
      filter_upwards [hdiff0] with omega hzero
      apply propext
      change (t <= X n omega - X 0 omega) ↔ False
      rw [hzero]
      exact iff_false_intro (not_le_of_gt ht)
    rw [measureReal_congr hevent, measureReal_empty]
    positivity
  · have hSpos : 0 < S := lt_of_le_of_ne hS (Ne.symm hS0)
    let lambda := t / S
    have hlambda : 0 <= lambda := div_nonneg ht.le hS
    have hInt := exp_endpoint_integrable Omega mu G X c hMart n hBound lambda
    calc
      mu.real {omega | t <= X n omega - X 0 omega}
          <= Real.exp (-lambda * t) *
              mu[fun omega => Real.exp (lambda * (X n omega - X 0 omega))] :=
        ProbabilityTheory.measure_ge_le_exp_mul_mgf t hlambda hInt
      _ <= Real.exp (-lambda * t) * Real.exp (lambda ^ 2 * S / 2) := by
        gcongr
        exact exp_increment_sum_integral_le Omega mu G X c hMart n hBound lambda
      _ = Real.exp (-(t ^ 2) / (2 * S)) := by
        rw [← Real.exp_add]
        congr 1
        dsimp only [lambda]
        field_simp
        ring

/-- The included `t = 0` branch follows solely from the probability-measure bound. -/
theorem zeroThreshold
    (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal) (hMart : Martingale X G mu) (n : Nat)
    (hBound : forall k, k < n -> ∀ᵐ omega ∂mu,
      |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) :
    mu.real {omega | (0 : Real) <= X n omega - X 0 omega} <=
      Real.exp (-((0 : Real) ^ 2) / (2 * squaredBoundSum c n)) := by
  simpa using (measureReal_le_one : mu.real {omega | (0 : Real) <= X n omega - X 0 omega} <= 1)

/-- The exact frozen target, assembled from the proved positive and zero threshold branches. -/
theorem azumaUpperTail :
    forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
      [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
      (c : Nat -> NNReal),
        Martingale X G mu ->
        forall n : Nat,
          (forall k, k < n -> ∀ᵐ omega ∂mu,
            |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
          forall t : Real, 0 <= t ->
            mu.real {omega | t <= X n omega - X 0 omega} <=
              Real.exp (-(t ^ 2) / (2 * squaredBoundSum c n)) := by
  intro Omega mOmega mu hmu G X c hMart n hBound t ht
  rcases ht.eq_or_lt with rfl | ht
  · exact zeroThreshold Omega mu G X c hMart n hBound
  · exact positiveThreshold Omega mu G X c hMart n hBound t ht

#print axioms sum_increment_eq_sub
#print axioms exp_secant_bound
#print axioms condExp_exp_increment_le
#print axioms exp_endpoint_integrable
#print axioms exp_increment_sum_integral_le
#print axioms positiveThreshold
#print axioms zeroThreshold
#print axioms azumaUpperTail

end Stage1Instances.THM_M_1080.Proof
