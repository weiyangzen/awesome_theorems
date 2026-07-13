/-
Copyright (c) 2025. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Linear

/-!
# Bounds on the exponential Taylor remainder

Pointwise bounds on `exp z - 1 - z - z²/2` used in the Lindeberg CLT.

This file adapts `Clt/CharFunBound.lean` from `patrickrd/CLT-lindeberg` at
commit `82249ccfc05c0d97b86f33fce2582f0bf4ff9c06` (upstream file SHA-256
`2c04f861f5c5faf0622f6c39157420f67f4e41d2f5a3b8acc8282461897143e1`).
The adaptation adds a target-specific namespace, removes stale commented
code, reformats the source, and adds axiom probes; the mathematical proof
bodies follow the upstream Apache-2.0 source.
-/

noncomputable section

open Complex Finset MeasureTheory intervalIntegral

namespace Stage1Instances.THM_M_0989.CharFunBound

private lemma norm_ofReal_mul_I (y : ℝ) : ‖(↑y * I : ℂ)‖ = |y| := by
  simp [Complex.norm_real, Real.norm_eq_abs]

/-- Third-order Taylor bound: for `‖z‖ ≤ 1`,
`‖exp z - 1 - z - z²/2‖ ≤ ‖z‖³`. -/
lemma norm_cexp_sub_taylor_two_le {z : ℂ} (hz : ‖z‖ ≤ 1) :
    ‖exp z - 1 - z - z ^ 2 / 2‖ ≤ ‖z‖ ^ 3 := by
  have h : ‖exp z - 1 - z - z ^ 2 / 2‖
      = ‖exp z - ∑ m ∈ range 3, z ^ m / m.factorial‖ := by
    congr 1
    simp [sum_range_succ, Nat.factorial]
    ring
  rw [h]
  calc ‖exp z - ∑ m ∈ range 3, z ^ m / m.factorial‖
      ≤ ‖z‖ ^ 3 * ((Nat.succ 3 : ℝ) * (Nat.factorial 3 * (3 : ℕ) : ℝ)⁻¹) :=
        exp_bound hz (by decide)
    _ ≤ ‖z‖ ^ 3 * 1 := by gcongr; norm_num [Nat.factorial]
    _ = ‖z‖ ^ 3 := mul_one _

/-- Second-order bound for purely imaginary arguments: for `|y| ≤ 1`,
`‖exp(iy) - 1 - iy‖ ≤ y²`. -/
lemma norm_cexp_mul_I_sub_one_sub_le_sq {y : ℝ} (hy : |y| ≤ 1) :
    ‖exp (↑y * I) - 1 - ↑y * I‖ ≤ y ^ 2 := by
  have h1 : ‖(↑y * I : ℂ)‖ ≤ 1 := by rw [norm_ofReal_mul_I]; exact hy
  calc ‖exp (↑y * I) - 1 - ↑y * I‖
      ≤ ‖(↑y * I : ℂ)‖ ^ 2 := norm_exp_sub_one_sub_id_le h1
    _ = y ^ 2 := by rw [norm_ofReal_mul_I]; simp [sq_abs]

/-- Third-order bound for purely imaginary arguments: for `|y| ≤ 1`,
`‖exp(iy) - 1 - iy + y²/2‖ ≤ |y|³`. -/
lemma norm_cexp_mul_I_sub_taylor_two_le {y : ℝ} (hy : |y| ≤ 1) :
    ‖exp (↑y * I) - 1 - ↑y * I + ((y ^ 2 / 2 : ℝ) : ℂ)‖ ≤ |y| ^ 3 := by
  have hz : ‖(↑y * I : ℂ)‖ ≤ 1 := by rw [norm_ofReal_mul_I]; exact hy
  have key : ((y ^ 2 / 2 : ℝ) : ℂ) = -((↑y * I) ^ 2 / 2) := by
    push_cast
    simp [mul_pow, I_sq]
    ring
  rw [key, ← sub_eq_add_neg]
  calc ‖exp (↑y * I) - 1 - ↑y * I - (↑y * I) ^ 2 / 2‖
      ≤ ‖(↑y * I : ℂ)‖ ^ 3 := norm_cexp_sub_taylor_two_le hz
    _ = |y| ^ 3 := by rw [norm_ofReal_mul_I]

/-- Crude global bound on the purely imaginary second-order remainder. -/
lemma norm_cexp_mul_I_sub_taylor_two_le_crude (y : ℝ) :
    ‖exp (↑y * I) - 1 - ↑y * I + ((y ^ 2 / 2 : ℝ) : ℂ)‖
      ≤ 2 + |y| + y ^ 2 / 2 := by
  have h1 : ‖exp (↑y * I) - 1 - ↑y * I‖ ≤ 2 + |y| := by
    have h_sub1 : ‖exp (↑y * I) - 1‖ ≤ 2 := by
      calc ‖exp (↑y * I) - 1‖
          ≤ ‖exp (↑y * I)‖ + ‖(1 : ℂ)‖ := norm_sub_le _ _
        _ = 2 := by
            rw [norm_exp_ofReal_mul_I]
            have : ‖(1 : ℂ)‖ = 1 := norm_one
            linarith
    calc ‖exp (↑y * I) - 1 - ↑y * I‖
        ≤ ‖exp (↑y * I) - 1‖ + ‖(↑y * I : ℂ)‖ := norm_sub_le _ _
      _ ≤ 2 + |y| := by linarith [norm_ofReal_mul_I y]
  have h2 : ‖((y ^ 2 / 2 : ℝ) : ℂ)‖ = y ^ 2 / 2 := by
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg (by positivity)]
  linarith [norm_add_le (exp (↑y * I) - 1 - ↑y * I) ((y ^ 2 / 2 : ℝ) : ℂ)]

private lemma hasDerivAt_ofReal_mul_I (t : ℝ) :
    HasDerivAt (fun s : ℝ ↦ (↑s : ℂ) * I) I t := by
  have h := ((hasDerivAt_id (t : ℂ)).const_mul I).comp_ofReal
  simp only [mul_comm I, one_mul, id] at h
  exact h

private lemma hasDerivAt_cexp_sub (t : ℝ) :
    HasDerivAt (fun s : ℝ ↦ cexp (↑s * I) - 1 - ↑s * I)
      (I * (cexp (↑t * I) - 1)) t := by
  have h1 : HasDerivAt (fun s : ℝ => cexp (↑s * I)) (cexp (↑t * I) * I) t :=
    (hasDerivAt_exp _).comp t (hasDerivAt_ofReal_mul_I t)
  have h2 : HasDerivAt (fun _s : ℝ => (1 : ℂ)) 0 t := hasDerivAt_const t 1
  have h3 : HasDerivAt (fun s : ℝ => ↑s * I) I t := hasDerivAt_ofReal_mul_I t
  exact ((h1.sub h2).sub h3).congr_of_eventuallyEq
    (Filter.Eventually.of_forall fun s => by simp [Pi.sub_apply, mul_comm]) |>.congr_deriv
    (by ring)

private lemma ftc_cexp (y : ℝ) :
    ∫ t in (0 : ℝ)..y, I * (cexp (↑t * I) - 1) = cexp (↑y * I) - 1 - ↑y * I := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
    (fun t _ ↦ hasDerivAt_cexp_sub t) (by apply Continuous.intervalIntegrable; fun_prop)]
  simp

private lemma integral_id_Icc {y : ℝ} :
    ∫ t in (0 : ℝ)..y, t = y ^ 2 / 2 := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
    (fun t _ ↦ by
      have h := (hasDerivAt_pow 2 t).div_const (2 : ℝ)
      simp at h
      exact h)
    (by exact continuous_id.intervalIntegrable _ _)]
  simp

/-- Sharp global quadratic bound for the first-order purely imaginary
remainder.  Unlike the local Taylor bounds, this holds for every `y : ℝ`. -/
lemma norm_cexp_mul_I_sub_one_sub_le_half_sq (y : ℝ) :
    ‖cexp (↑y * I) - 1 - ↑y * I‖ ≤ y ^ 2 / 2 := by
  rw [← ftc_cexp]
  have hbound : ∀ t : ℝ, ‖I * (cexp (↑t * I) - 1)‖ ≤ |t| := by
    intro t
    rw [norm_mul, Complex.norm_I, one_mul, mul_comm (↑t : ℂ) I]
    exact_mod_cast Real.norm_exp_I_mul_ofReal_sub_one_le
  have hint : IntervalIntegrable (fun t => (|t| : ℝ)) MeasureTheory.volume 0 y :=
    Continuous.intervalIntegrable (by fun_prop) _ _
  calc ‖∫ t in (0 : ℝ)..y, I * (cexp (↑t * I) - 1)‖
      ≤ |∫ t in (0 : ℝ)..y, abs t| :=
        intervalIntegral.norm_integral_le_abs_of_norm_le
          (Filter.Eventually.of_forall fun t => hbound t) hint
    _ = y ^ 2 / 2 := by
        rcases le_or_gt 0 y with hy | hy
        · have h : ∫ t in (0 : ℝ)..y, abs t = ∫ t in (0 : ℝ)..y, t :=
            intervalIntegral.integral_congr (fun t ht => by
              simp only [Set.uIcc_of_le hy] at ht
              exact abs_of_nonneg ht.1)
          rw [h, integral_id_Icc, abs_of_nonneg (by positivity)]
        · have h : ∫ t in (0 : ℝ)..y, abs t = ∫ t in (0 : ℝ)..y, -t :=
            intervalIntegral.integral_congr (fun t ht => by
              simp only [Set.uIcc_of_ge hy.le] at ht
              exact abs_of_nonpos ht.2)
          rw [h, intervalIntegral.integral_neg, intervalIntegral.integral_symm, neg_neg]
          rw [show (fun x : ℝ => x) = id from rfl,
            intervalIntegral.integral_eq_sub_of_hasDerivAt
            (fun t _ => by
              have h := (hasDerivAt_pow 2 t).div_const (2 : ℝ)
              simp at h
              exact h)
            (continuous_id.intervalIntegrable _ _)]
          simp
          positivity

#print axioms norm_cexp_sub_taylor_two_le
#print axioms norm_cexp_mul_I_sub_one_sub_le_sq
#print axioms norm_cexp_mul_I_sub_taylor_two_le
#print axioms norm_cexp_mul_I_sub_taylor_two_le_crude
#print axioms norm_cexp_mul_I_sub_one_sub_le_half_sq

end Stage1Instances.THM_M_0989.CharFunBound
