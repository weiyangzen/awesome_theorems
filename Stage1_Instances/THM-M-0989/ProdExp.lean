/-
Copyright (c) 2025 Patrick Rubin-Delanchy. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Patrick Rubin-Delanchy
-/
import Mathlib.Analysis.SpecialFunctions.Complex.LogBounds
import Mathlib.Order.Filter.AtTopBot.Basic

/-!
# Product-to-exponential limit for nonempty triangular rows

This file adapts `Clt.ProdExp` from `patrickrd/CLT-lindeberg` at commit
`82249ccfc05c0d97b86f33fce2582f0bf4ff9c06` to rows indexed by
`Fin (n + 1)`, matching the frozen `THM-M-0989` array interface. The source
snapshot used for the adaptation has SHA-256
`6068339f52c68388a0ce45dfd30b4801de1aab5421ef98e1fc19a81cba05851c`.

If `a : (n : Nat) -> Fin (n + 1) -> Complex` satisfies
* `sum k, a n k -> L`, and
* `sum k, norm (a n k) ^ 2 -> 0`,

then `prod k, (1 + a n k) -> exp L`.
-/

noncomputable section

open Filter Complex Finset
open scoped Topology

namespace Stage1Instances.THM_M_0989.ProductLimit

variable {a : (n : Nat) -> Fin (n + 1) -> Complex}

/-- For `norm z <= 1 / 2`, the logarithm remainder is at most `norm z ^ 2`. -/
private lemma norm_log_one_add_sub_self_le_sq {z : Complex} (hz : ‖z‖ <= 1 / 2) :
    ‖log (1 + z) - z‖ <= ‖z‖ ^ 2 := by
  have hz1 : ‖z‖ < 1 := lt_of_le_of_lt hz (by norm_num)
  calc
    ‖log (1 + z) - z‖
        <= ‖z‖ ^ 2 * (1 - ‖z‖)⁻¹ / 2 := norm_log_one_add_sub_self_le hz1
    _ <= ‖z‖ ^ 2 * 2 / 2 := by
      gcongr
      rw [inv_le_comm₀ (by linarith) (by norm_num)]
      linarith
    _ = ‖z‖ ^ 2 := by ring

/-- Vanishing sums of squared norms make every entry eventually small. -/
private lemma eventually_norm_le_of_sum_sq_tendsto
    (hsq : Tendsto (fun n => ∑ k : Fin (n + 1), ‖a n k‖ ^ 2) atTop (nhds 0)) :
    ∀ᶠ n in atTop, forall k : Fin (n + 1), ‖a n k‖ <= 1 / 2 := by
  rw [Metric.tendsto_nhds] at hsq
  have h14 := hsq (1 / 4) (by positivity)
  simp only [Real.dist_eq, sub_zero] at h14
  filter_upwards [h14] with n hn k
  have hle : ‖a n k‖ ^ 2 <= ∑ j : Fin (n + 1), ‖a n j‖ ^ 2 :=
    Finset.single_le_sum (f := fun j => ‖a n j‖ ^ 2)
      (fun _ _ => by positivity) (mem_univ k)
  have habs : |∑ j : Fin (n + 1), ‖a n j‖ ^ 2| =
      ∑ j : Fin (n + 1), ‖a n j‖ ^ 2 :=
    abs_of_nonneg (sum_nonneg fun _ _ => by positivity)
  have hsq_small : ‖a n k‖ ^ 2 < 1 / 4 := lt_of_le_of_lt hle (habs ▸ hn)
  nlinarith [sq_nonneg ‖a n k‖, norm_nonneg (a n k)]

/-- The log-sum approximation error is bounded by the sum of squared norms. -/
private lemma norm_sum_log_sub_sum_le
    {n : Nat} (h : forall k : Fin (n + 1), ‖a n k‖ <= 1 / 2) :
    ‖∑ k : Fin (n + 1), log (1 + a n k) - ∑ k : Fin (n + 1), a n k‖ <=
      ∑ k : Fin (n + 1), ‖a n k‖ ^ 2 := by
  rw [← sum_sub_distrib]
  calc
    ‖∑ k, (log (1 + a n k) - a n k)‖
        <= ∑ k, ‖log (1 + a n k) - a n k‖ := norm_sum_le _ _
    _ <= ∑ k, ‖a n k‖ ^ 2 :=
      sum_le_sum fun k _ => norm_log_one_add_sub_self_le_sq (h k)

/-- Exponentiating the sum of logs recovers the product when no factor is zero. -/
private lemma exp_sum_log_eq_prod
    {n : Nat} (h : forall k : Fin (n + 1), ‖a n k‖ < 1) :
    exp (∑ k : Fin (n + 1), log (1 + a n k)) =
      ∏ k : Fin (n + 1), (1 + a n k) := by
  rw [exp_sum]
  congr 1 with k
  apply exp_log
  have hk : ‖a n k‖ < 1 := h k
  have hnorm : ‖(1 : Complex) + a n k‖ >= 1 - ‖a n k‖ := by
    have hbound := norm_sub_norm_le (1 : Complex) (-(a n k))
    simp [norm_neg] at hbound
    linarith
  intro hzero
  simp [hzero] at hnorm
  linarith

/--
If the row sums converge to `L` and the row sums of squared norms vanish, then
the products of `1 + a n k` converge to `Complex.exp L`.

This is the `Fin (n + 1)` product-limit bridge used by the frozen triangular
array in `THM-M-0989`.
-/
theorem tendsto_row_prod_one_add_of_sum_norm_sq
    {L : Complex}
    (hsum : Tendsto (fun n => ∑ k : Fin (n + 1), a n k) atTop (nhds L))
    (hsq : Tendsto (fun n => ∑ k : Fin (n + 1), ‖a n k‖ ^ 2) atTop (nhds 0)) :
    Tendsto (fun n => ∏ k : Fin (n + 1), (1 + a n k)) atTop (nhds (exp L)) := by
  have hlog : Tendsto (fun n => ∑ k : Fin (n + 1), log (1 + a n k))
      atTop (nhds L) := by
    have hdiff : Tendsto
        (fun n => ∑ k : Fin (n + 1), log (1 + a n k) -
          ∑ k : Fin (n + 1), a n k)
        atTop (nhds 0) := by
      rw [Metric.tendsto_nhds]
      intro epsilon hepsilon
      have hev := eventually_norm_le_of_sum_sq_tendsto hsq
      rw [Metric.tendsto_nhds] at hsq
      have hsq_epsilon := hsq epsilon hepsilon
      simp only [Real.dist_eq, sub_zero] at hsq_epsilon
      filter_upwards [hev, hsq_epsilon] with n hn hsmall
      rw [dist_eq_norm, sub_zero]
      calc
        ‖∑ k : Fin (n + 1), log (1 + a n k) - ∑ k : Fin (n + 1), a n k‖
            <= ∑ k : Fin (n + 1), ‖a n k‖ ^ 2 := norm_sum_log_sub_sum_le hn
        _ <= |∑ k : Fin (n + 1), ‖a n k‖ ^ 2| := le_abs_self _
        _ < epsilon := hsmall
    have hadd := hdiff.add hsum
    simp only [zero_add] at hadd
    exact hadd.congr (fun n => by ring)
  have hexp : Tendsto
      (fun n => exp (∑ k : Fin (n + 1), log (1 + a n k)))
      atTop (nhds (exp L)) :=
    (continuous_exp.tendsto _).comp hlog
  refine hexp.congr' ?_
  have hev := eventually_norm_le_of_sum_sq_tendsto hsq
  filter_upwards [hev] with n hn
  exact exp_sum_log_eq_prod (fun k => lt_of_le_of_lt (hn k) (by norm_num))

#print axioms tendsto_row_prod_one_add_of_sum_norm_sq

end Stage1Instances.THM_M_0989.ProductLimit
