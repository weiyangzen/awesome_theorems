import Mathlib
import Statement

/-!
# THM-M-1246 regularized sharp estimate

This module proves the pointwise, integrability, and integral estimates that
turn a regularized integration-by-parts lower bound into the sharp Hardy
constant. The remaining proof modules supply that lower bound and remove the
regularization.
-/

noncomputable section

open MeasureTheory
open scoped RealInnerProductSpace

namespace Stage1Instances.THM_M_1246.Proof

open Stage1Instances.THM_M_1246

theorem young_sharp {a b lam : Real} (hlam : 0 < lam) :
    2 * a * b <= lam / 2 * a ^ 2 + 2 / lam * b ^ 2 := by
  have hs : 0 <= (lam * a - 2 * b) ^ 2 := sq_nonneg _
  field_simp
  nlinarith

theorem young_sharp_abs {a b lam : Real} (hlam : 0 < lam) :
    |2 * a * b| <= lam / 2 * a ^ 2 + 2 / lam * b ^ 2 := by
  have hs : 0 <= (lam * |a| - 2 * |b|) ^ 2 := sq_nonneg _
  rw [abs_mul, abs_mul]
  norm_num
  field_simp
  nlinarith [abs_nonneg a, abs_nonneg b, sq_abs a, sq_abs b]

theorem rearrange_sharp {A J lam : Real} (hlam : 0 < lam)
    (h : lam * A <= lam / 2 * A + 2 / lam * J) :
    A <= (2 / lam) ^ 2 * J := by
  field_simp at h ⊢
  nlinarith

theorem operator_radial_bound {n : Nat} (u : Space n -> Real) (x : Space n) :
    |fderiv Real u x x| <= ‖fderiv Real u x‖ * ‖x‖ := by
  simpa only [Real.norm_eq_abs] using (ContinuousLinearMap.le_opNorm (fderiv Real u x) x)

theorem regularized_pair_bound {n : Nat} (u : Space n -> Real)
    (eps : Real) (heps : 0 < eps) (x : Space n) :
    |2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))| <=
      2 * (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) * ‖fderiv Real u x‖ := by
  have hD : 0 < ‖x‖ ^ 2 + eps := by positivity
  rw [abs_mul, abs_mul, abs_div, abs_of_pos hD]
  norm_num
  have hrad := operator_radial_bound u x
  calc
    2 * |u x| * (|fderiv Real u x x| / (‖x‖ ^ 2 + eps))
        <= 2 * |u x| * (‖fderiv Real u x‖ * ‖x‖) / (‖x‖ ^ 2 + eps) := by
      rw [mul_div_assoc]
      gcongr
    _ = 2 * (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) * ‖fderiv Real u x‖ := by ring

theorem regularized_pair_young {n : Nat} (u : Space n -> Real)
    (eps lam : Real) (heps : 0 < eps) (hlam : 0 < lam) (x : Space n) :
    |2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))| <=
      lam / 2 * (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2 +
        2 / lam * ‖fderiv Real u x‖ ^ 2 := by
  exact (regularized_pair_bound u eps heps x).trans (young_sharp hlam)

theorem abs_integral_pair_le_young {α : Type*} [MeasurableSpace α]
    (μ : Measure α) (a b : α -> Real) (lam : Real) (hlam : 0 < lam)
    (ha : Integrable (fun x => a x ^ 2) μ)
    (hb : Integrable (fun x => b x ^ 2) μ)
    (hab : Integrable (fun x => 2 * a x * b x) μ) :
    |∫ x, 2 * a x * b x ∂μ| <=
      lam / 2 * (∫ x, a x ^ 2 ∂μ) + 2 / lam * (∫ x, b x ^ 2 ∂μ) := by
  calc
    |∫ x, 2 * a x * b x ∂μ| <= ∫ x, |2 * a x * b x| ∂μ :=
      abs_integral_le_integral_abs
    _ <= ∫ x, (lam / 2 * a x ^ 2 + 2 / lam * b x ^ 2) ∂μ := by
      apply integral_mono hab.norm (ha.const_mul _ |>.add (hb.const_mul _))
      intro x
      exact young_sharp_abs hlam
    _ = lam / 2 * (∫ x, a x ^ 2 ∂μ) + 2 / lam * (∫ x, b x ^ 2 ∂μ) := by
      rw [integral_add (ha.const_mul _) (hb.const_mul _), integral_const_mul,
        integral_const_mul]

theorem abs_integral_regularized_pair_le_young {n : Nat} (u : Space n -> Real)
    (eps lam : Real) (heps : 0 < eps) (hlam : 0 < lam)
    (hw : Integrable (fun x => (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2))
    (hdu : Integrable (fun x => ‖fderiv Real u x‖ ^ 2))
    (hpair : Integrable (fun x =>
      2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps)))) :
    |∫ x, 2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))| <=
      lam / 2 * (∫ x, (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2) +
        2 / lam * (∫ x, ‖fderiv Real u x‖ ^ 2) := by
  calc
    |∫ x, 2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))|
        <= ∫ x, |2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))| :=
      abs_integral_le_integral_abs
    _ <= ∫ x, (lam / 2 * (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2 +
        2 / lam * ‖fderiv Real u x‖ ^ 2) := by
      apply integral_mono hpair.norm (hw.const_mul _ |>.add (hdu.const_mul _))
      exact fun x => regularized_pair_young u eps lam heps hlam x
    _ = lam / 2 * (∫ x, (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2) +
        2 / lam * (∫ x, ‖fderiv Real u x‖ ^ 2) := by
      rw [integral_add (hw.const_mul _) (hdu.const_mul _), integral_const_mul,
        integral_const_mul]

theorem sharp_bound_of_ibp_and_young {A I J lam : Real} (hlam : 0 < lam)
    (hibp : lam * A <= |I|)
    (hyoung : |I| <= lam / 2 * A + 2 / lam * J) :
    A <= (2 / lam) ^ 2 * J :=
  rearrange_sharp hlam (hibp.trans hyoung)

theorem regularized_weight_sq_le {n : Nat} (u : Space n -> Real)
    (eps : Real) (heps : 0 < eps) (x : Space n) :
    (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2 <=
      |u x| ^ 2 / (‖x‖ ^ 2 + eps) := by
  have hD : 0 < ‖x‖ ^ 2 + eps := by positivity
  have hnorm : ‖x‖ ^ 2 <= ‖x‖ ^ 2 + eps := by linarith
  rw [div_pow]
  calc
    (|u x| * ‖x‖) ^ 2 / (‖x‖ ^ 2 + eps) ^ 2 =
        |u x| ^ 2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps) ^ 2 := by ring
    _ <= |u x| ^ 2 * (‖x‖ ^ 2 + eps) / (‖x‖ ^ 2 + eps) ^ 2 := by
      gcongr
    _ = |u x| ^ 2 / (‖x‖ ^ 2 + eps) := by
      field_simp [ne_of_gt hD]

theorem divergence_regularized_lower {n : Nat} (eps : Real) (heps : 0 < eps)
    (x : Space n) :
    ((n : Real) - 2) / (‖x‖ ^ 2 + eps) <=
      (n : Real) / (‖x‖ ^ 2 + eps) -
        2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps) ^ 2 := by
  have hD : 0 < ‖x‖ ^ 2 + eps := by positivity
  field_simp [ne_of_gt hD]
  nlinarith

theorem fderiv_norm_sq_integrable {n : Nat} (u : Space n -> Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u) :
    Integrable (fun x => ‖fderiv Real u x‖ ^ 2) := by
  have hcont : Continuous (fun x : Space n => ‖fderiv Real u x‖ ^ 2) :=
    (hu.continuous_fderiv (by simp)).norm.pow 2
  have hcfd : HasCompactSupport (fun x : Space n => ‖fderiv Real u x‖) :=
    (huc.fderiv (𝕜 := Real)).norm
  have hc : HasCompactSupport (fun x : Space n => ‖fderiv Real u x‖ ^ 2) := by
    simpa only [pow_two] using hcfd.mul_right
  exact hcont.integrable_of_hasCompactSupport hc

theorem regularized_weight_sq_integrable {n : Nat} (u : Space n -> Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u)
    (eps : Real) (heps : 0 < eps) :
    Integrable (fun x => (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2) := by
  have hcont : Continuous (fun x : Space n =>
      (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2) := by
    apply Continuous.pow
    apply Continuous.div
    · exact hu.continuous.abs.mul continuous_norm
    · fun_prop
    · intro x
      positivity
  have hc1 : HasCompactSupport (fun x : Space n => |u x| * ‖x‖) := huc.abs.mul_right
  have hc2 : HasCompactSupport (fun x : Space n =>
      |u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) := by
    simpa only [div_eq_mul_inv] using hc1.mul_right
  have hc : HasCompactSupport (fun x : Space n =>
      (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2) := by
    simpa only [pow_two] using hc2.mul_right
  exact hcont.integrable_of_hasCompactSupport hc

theorem regularized_density_integrable {n : Nat} (u : Space n -> Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u)
    (eps : Real) (heps : 0 < eps) :
    Integrable (fun x => |u x| ^ 2 / (‖x‖ ^ 2 + eps)) := by
  have hcont : Continuous (fun x : Space n => |u x| ^ 2 / (‖x‖ ^ 2 + eps)) := by
    apply Continuous.div
    · exact hu.continuous.abs.pow 2
    · fun_prop
    · intro x
      positivity
  have hc0 : HasCompactSupport (fun x : Space n => |u x| ^ 2) := by
    simpa only [pow_two] using huc.abs.mul_right
  have hc : HasCompactSupport (fun x : Space n => |u x| ^ 2 / (‖x‖ ^ 2 + eps)) := by
    simpa only [div_eq_mul_inv] using hc0.mul_right
  exact hcont.integrable_of_hasCompactSupport hc

theorem regularized_pair_integrable {n : Nat} (u : Space n -> Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u)
    (eps : Real) (heps : 0 < eps) :
    Integrable (fun x => 2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))) := by
  have hcont : Continuous (fun x : Space n =>
      2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))) := by
    apply Continuous.mul
    · exact continuous_const.mul hu.continuous
    · apply Continuous.div
      · exact (hu.continuous_fderiv (by simp)).clm_apply continuous_id
      · fun_prop
      · intro x
        positivity
  have hc0 : HasCompactSupport (fun x : Space n =>
      u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))) := huc.mul_right
  have hc : HasCompactSupport (fun x : Space n =>
      2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))) := by
    simpa only [mul_assoc] using hc0.mul_left
  exact hcont.integrable_of_hasCompactSupport hc

theorem regularized_weight_integral_le_density {n : Nat} (u : Space n -> Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u)
    (eps : Real) (heps : 0 < eps) :
    (∫ x, (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2) <=
      ∫ x, |u x| ^ 2 / (‖x‖ ^ 2 + eps) := by
  apply integral_mono
    (regularized_weight_sq_integrable u hu huc eps heps)
    (regularized_density_integrable u hu huc eps heps)
  exact fun x => regularized_weight_sq_le u eps heps x

theorem abs_integral_regularized_pair_le_density {n : Nat} (u : Space n -> Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u)
    (eps lam : Real) (heps : 0 < eps) (hlam : 0 < lam) :
    |∫ x, 2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))| <=
      lam / 2 * (∫ x, |u x| ^ 2 / (‖x‖ ^ 2 + eps)) +
        2 / lam * (∫ x, ‖fderiv Real u x‖ ^ 2) := by
  have hw := regularized_weight_sq_integrable u hu huc eps heps
  have hdu := fderiv_norm_sq_integrable u hu huc
  have hp := regularized_pair_integrable u hu huc eps heps
  have hy := abs_integral_regularized_pair_le_young u eps lam heps hlam hw hdu hp
  have hwd := regularized_weight_integral_le_density u hu huc eps heps
  calc
    |∫ x, 2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))|
        <= lam / 2 * (∫ x, (|u x| * ‖x‖ / (‖x‖ ^ 2 + eps)) ^ 2) +
          2 / lam * (∫ x, ‖fderiv Real u x‖ ^ 2) := hy
    _ <= lam / 2 * (∫ x, |u x| ^ 2 / (‖x‖ ^ 2 + eps)) +
          2 / lam * (∫ x, ‖fderiv Real u x‖ ^ 2) := by
      gcongr

theorem regularized_sharp_from_ibp_lower {n : Nat} (u : Space n -> Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u)
    (eps lam : Real) (heps : 0 < eps) (hlam : 0 < lam)
    (hibpLower : lam * (∫ x, |u x| ^ 2 / (‖x‖ ^ 2 + eps)) <=
      |∫ x, 2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))|) :
    (∫ x, |u x| ^ 2 / (‖x‖ ^ 2 + eps)) <=
      (2 / lam) ^ 2 * ∫ x, ‖fderiv Real u x‖ ^ 2 := by
  exact sharp_bound_of_ibp_and_young hlam hibpLower
    (abs_integral_regularized_pair_le_density u hu huc eps lam heps hlam)

theorem integral_mul_divergence_lower {n : Nat} (u : Space n -> Real)
    (eps : Real) (heps : 0 < eps)
    (hleft : Integrable (fun x =>
      ((n : Real) - 2) * (|u x| ^ 2 / (‖x‖ ^ 2 + eps))))
    (hright : Integrable (fun x => |u x| ^ 2 *
      ((n : Real) / (‖x‖ ^ 2 + eps) -
        2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps) ^ 2))) :
    ((n : Real) - 2) * (∫ x, |u x| ^ 2 / (‖x‖ ^ 2 + eps)) <=
      ∫ x, |u x| ^ 2 *
        ((n : Real) / (‖x‖ ^ 2 + eps) -
          2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps) ^ 2) := by
  rw [← integral_const_mul]
  apply integral_mono hleft hright
  intro x
  change ((n : Real) - 2) * (|u x| ^ 2 / (‖x‖ ^ 2 + eps)) <=
    |u x| ^ 2 * ((n : Real) / (‖x‖ ^ 2 + eps) -
      2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps) ^ 2)
  convert mul_le_mul_of_nonneg_left
    (divergence_regularized_lower eps heps x) (sq_nonneg |u x|) using 1 <;> ring

end Stage1Instances.THM_M_1246.Proof
