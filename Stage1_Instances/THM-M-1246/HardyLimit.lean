import Statement
import Mathlib.Analysis.SpecialFunctions.Integrability.Basic
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm
import Mathlib.MeasureTheory.Function.LpSpace.Indicator
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-!
# THM-M-1246 singular-integrability and limit package

This module proves that the inverse-square density in the frozen Hardy target
is integrable in dimension at least three. It also removes the positive radial
regularization by dominated convergence and records integrability of the
regularized divergence density used by integration by parts.
-/

noncomputable section

open MeasureTheory Set Filter
open scoped Topology ENNReal

namespace Stage1Instances.THM_M_1246.Proof

open Stage1Instances.THM_M_1246

private def radialMajorant (C R : Real) (r : Real) : Real :=
  if r ∈ Ioc 0 R then C / r ^ 2 else 0

private lemma radial_mul (n : Nat) (hn : 3 <= n) (C R y : Real) (hy : y ∈ Ioi 0) :
    y ^ (n - 1) * radialMajorant C R y =
      if y ∈ Ioc 0 R then C * y ^ (n - 3) else 0 := by
  simp only [radialMajorant]
  split_ifs
  · have hy0 : y ≠ 0 := ne_of_gt hy
    have hpow : n - 1 = (n - 3) + 2 := by omega
    rw [hpow, pow_add, pow_two, div_eq_mul_inv]
    field_simp
  · simp

private lemma radialMajorant_integrableOn (n : Nat) (hn : 3 <= n) (C R : Real) :
    IntegrableOn (fun y : Real => y ^ (n - 1) * radialMajorant C R y) (Ioi 0) := by
  let p : Real -> Real := fun y => C * y ^ (n - 3)
  have hp : IntegrableOn p (Ioc 0 R) := by
    apply IntegrableOn.mono_set
      ((continuous_const.mul (continuous_id.pow _)).continuousOn.integrableOn_compact isCompact_Icc)
    exact Ioc_subset_Icc_self
  have hi : Integrable (Set.indicator (Ioc 0 R) p) :=
    hp.integrable_indicator measurableSet_Ioc
  have hall : (fun y : Real => y ^ (n - 1) * radialMajorant C R y) =
      Set.indicator (Ioc 0 R) p := by
    funext y
    by_cases hy : y ∈ Ioi (0 : Real)
    · rw [radial_mul n hn C R y hy]
      simp [p, Set.indicator]
    · have hy0 : ¬ 0 < y := by simpa using hy
      simp [radialMajorant, Set.indicator, hy0]
  rw [hall]
  exact hi.integrableOn

private lemma radialMajorant_integrable (n : Nat) (hn : 3 <= n) (C R : Real) :
    Integrable (fun x : Space n => radialMajorant C R ‖x‖) := by
  haveI : Nontrivial (Space n) := by
    have hpi : Nontrivial (Fin n -> Real) :=
      @Pi.nontrivial_at (Fin n) (fun _ => Real) (⟨0, by omega⟩ : Fin n)
        inferInstance inferInstance
    exact @WithLp.instNontrivial 2 (Fin n -> Real) hpi
  rw [MeasureTheory.integrable_fun_norm_addHaar]
  simpa [Space] using radialMajorant_integrableOn n hn C R

/-- A continuous compactly supported function has integrable inverse-square
density in every Euclidean dimension at least three. -/
lemma weighted_integrable (n : Nat) (hn : 3 <= n) (u : Space n -> Real)
    (hu : Continuous u) (hcu : HasCompactSupport u) :
    Integrable (fun x => |u x| ^ 2 / ‖x‖ ^ 2) := by
  let N : Real := lpNorm u ⊤ volume
  have hmem : MemLp u ⊤ := hu.memLp_of_hasCompactSupport hcu
  obtain ⟨R, hR⟩ := hcu.isCompact.isBounded.subset_closedBall (0 : Space n)
  apply (radialMajorant_integrable n hn (N ^ 2) R).mono'
  · exact ((hu.abs.aestronglyMeasurable.pow 2).div₀
      ((continuous_norm.pow 2).aestronglyMeasurable))
  · filter_upwards [ae_le_lpNorm_exponent_top hmem] with x hx
    by_cases hx0 : x = 0
    · subst x
      simp [radialMajorant]
    by_cases hxK : x ∈ tsupport u
    · have hxR : ‖x‖ <= R := by
        simpa [Metric.mem_closedBall, dist_eq_norm] using hR hxK
      have hxpos : 0 < ‖x‖ := norm_pos_iff.mpr hx0
      have huN : |u x| <= N := by simpa [N, Real.norm_eq_abs] using hx
      have huN2 : |u x| ^ 2 <= N ^ 2 := by nlinarith [abs_nonneg (u x)]
      rw [Real.norm_eq_abs, abs_of_nonneg (div_nonneg (sq_nonneg _) (sq_nonneg _))]
      rw [radialMajorant, if_pos (show ‖x‖ ∈ Ioc 0 R from ⟨hxpos, hxR⟩)]
      exact div_le_div_of_nonneg_right huN2 (sq_nonneg _)
    · have hux : u x = 0 := image_eq_zero_of_notMem_tsupport hxK
      rw [hux]
      simp only [abs_zero, zero_pow (by omega : (2 : Nat) ≠ 0), zero_div, Real.norm_eq_abs,
        abs_zero]
      simp only [radialMajorant]
      split_ifs
      · exact div_nonneg (sq_nonneg N) (sq_nonneg ‖x‖)
      · exact le_rfl

/-- Positive denominator regularizations converge to the singular density
integral. The value at the origin is discarded through the singleton-null
property of Euclidean volume. -/
lemma regularized_integral_tendsto (n : Nat) (hn : 3 <= n) (u : Space n -> Real)
    (hu : Continuous u) (hcu : HasCompactSupport u) :
    Tendsto (fun k : Nat => ∫ x, |u x| ^ 2 / (‖x‖ ^ 2 + 1 / ((k : Real) + 1))) atTop
      (nhds (∫ x, |u x| ^ 2 / ‖x‖ ^ 2)) := by
  haveI : Nontrivial (Space n) := by
    have hpi : Nontrivial (Fin n -> Real) :=
      @Pi.nontrivial_at (Fin n) (fun _ => Real) (⟨0, by omega⟩ : Fin n)
        inferInstance inferInstance
    exact @WithLp.instNontrivial 2 (Fin n -> Real) hpi
  have hae : ∀ᵐ x : Space n, x ≠ 0 := by
    rw [ae_iff]
    simpa using (measure_singleton (0 : Space n) : volume ({0} : Set (Space n)) = 0)
  let f : Space n -> Real := fun x => |u x| ^ 2 / ‖x‖ ^ 2
  apply tendsto_integral_filter_of_dominated_convergence f
  · exact Filter.Eventually.of_forall fun k =>
      ((hu.abs.aestronglyMeasurable.pow 2).div₀
        (((continuous_norm.pow 2).add continuous_const).aestronglyMeasurable))
  · exact Filter.Eventually.of_forall fun k => by
      filter_upwards [hae] with x hx
      rw [Real.norm_eq_abs, abs_of_nonneg (div_nonneg (sq_nonneg _) (add_nonneg
        (sq_nonneg _) (by positivity)))]
      exact div_le_div_of_nonneg_left (sq_nonneg _) (sq_pos_of_pos (norm_pos_iff.mpr hx))
        (le_add_of_nonneg_right (by positivity))
  · exact weighted_integrable n hn u hu hcu
  · filter_upwards [hae] with x hx
    have hx0 : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero _ (norm_ne_zero_iff.mpr hx)
    have hden : Tendsto (fun k : Nat => ‖x‖ ^ 2 + 1 / ((k : Real) + 1)) atTop
        (nhds (‖x‖ ^ 2)) := by
      convert tendsto_const_nhds.add
        (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := Real)) using 1 <;> simp
    exact tendsto_const_nhds.div hden hx0

/-- The regularized divergence density multiplied by a compactly supported
continuous square is integrable. -/
lemma regularized_divergence_integrable {n : Nat} (u : Space n -> Real)
    (hu : Continuous u) (huc : HasCompactSupport u)
    (eps : Real) (heps : 0 < eps) :
    Integrable (fun x => u x ^ 2 *
      ((n : Real) / (‖x‖ ^ 2 + eps) -
        2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps)^2)) := by
  have hdiv : Continuous (fun x : Space n =>
      ((n : Real) / (‖x‖ ^ 2 + eps) -
        2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps)^2)) := by
    have hden : Continuous (fun x : Space n => ‖x‖ ^ 2 + eps) :=
      (continuous_norm.pow 2).add continuous_const
    exact (continuous_const.div hden (by intro x; positivity)).sub
      ((continuous_const.mul (continuous_norm.pow 2)).div (hden.pow 2)
        (by intro x; positivity))
  exact (hu.pow 2).mul hdiv |>.integrable_of_hasCompactSupport
    (by simpa only [pow_two] using huc.mul_right.mul_right)

end Stage1Instances.THM_M_1246.Proof
