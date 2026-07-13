import ProofLemmas
import «ObligationTree»
import Mathlib.Util.AssertNoSorry

noncomputable section

namespace Stage1Instances.THM_M_1553

open ProofLemmas

theorem logarithmic_bilinear_identity (tau : Stage1Instances.THM_M_1553.Field) (h : ContDiff ℝ 5 tau)
    (positive : ∀ z, 0 < tau z)
    (bilinear : SatisfiesKdVBilinearEquation tau) :
    ∀ z, mixedDerivative 4 0 (fun w => Real.log (tau w)) z +
      6 * (mixedDerivative 2 0 (fun w => Real.log (tau w)) z) ^ 2 +
      mixedDerivative 1 1 (fun w => Real.log (tau w)) z = 0 := by
  let L : Stage1Instances.THM_M_1553.Field := fun w => Real.log (tau w)
  have hL : ContDiff ℝ 5 L := log_contDiff tau h positive
  intro z
  have htau : tau z = Real.exp (L z) := Real.exp_log (positive z) |>.symm
  have h10 : mixedDerivative 1 0 tau z =
      mixedDerivative 1 0 (fun w => Real.exp (L w)) z := by
    exact congrFun (tau_mixedDerivative_of_log tau positive 1 0) z
  have h20 : mixedDerivative 2 0 tau z =
      mixedDerivative 2 0 (fun w => Real.exp (L w)) z := by
    exact congrFun (tau_mixedDerivative_of_log tau positive 2 0) z
  have h30 : mixedDerivative 3 0 tau z =
      mixedDerivative 3 0 (fun w => Real.exp (L w)) z := by
    exact congrFun (tau_mixedDerivative_of_log tau positive 3 0) z
  have h40 : mixedDerivative 4 0 tau z =
      mixedDerivative 4 0 (fun w => Real.exp (L w)) z := by
    exact congrFun (tau_mixedDerivative_of_log tau positive 4 0) z
  have h01 : mixedDerivative 0 1 tau z =
      mixedDerivative 0 1 (fun w => Real.exp (L w)) z := by
    exact congrFun (tau_mixedDerivative_of_log tau positive 0 1) z
  have h11 : mixedDerivative 1 1 tau z =
      mixedDerivative 1 1 (fun w => Real.exp (L w)) z := by
    exact congrFun (tau_mixedDerivative_of_log tau positive 1 1) z
  have he10 := congrFun (exp_mixed_one_zero L (hL.of_le (by norm_num))) z
  have he20 := congrFun (exp_mixed_two_zero L (hL.of_le (by norm_num))) z
  have he30 := congrFun (exp_mixed_three_zero L (hL.of_le (by norm_num))) z
  have he40 := congrFun (exp_mixed_four_zero L (hL.of_le (by norm_num))) z
  have he01 := congrFun (exp_mixed_zero_one L (hL.of_le (by norm_num))) z
  have he11 := congrFun (exp_mixed_one_one L (hL.of_le (by norm_num))) z
  have hb := bilinear z
  rw [hirotaD_four_zero, hirotaD_one_one] at hb
  rw [htau, h10, h20, h30, h40, h01, h11,
      he10, he20, he30, he40, he01, he11] at hb
  have hexp : Real.exp (L z) ≠ 0 := Real.exp_ne_zero _
  apply (mul_left_cancel₀ (pow_ne_zero 2 hexp) :
      Real.exp (L z) ^ 2 * _ = Real.exp (L z) ^ 2 * _ → _)
  nlinarith

theorem logDerivativeBridge (tau : Stage1Instances.THM_M_1553.Field) : LogDerivativeBridge tau := by
  intro h positive bilinear z
  let L : Stage1Instances.THM_M_1553.Field := fun w => Real.log (tau w)
  have hL : ContDiff ℝ 5 L := log_contDiff tau h positive
  have hcore_point := logarithmic_bilinear_identity tau h positive bilinear
  have hcore :
      (fun w => mixedDerivative 4 0 L w +
        6 * (mixedDerivative 2 0 L w) ^ 2 + mixedDerivative 1 1 L w) =
      (fun _ : ℝ × ℝ => 0) := by
    funext w
    exact hcore_point w
  have hx := congrArg partialX hcore
  have hL4 : ContDiff ℝ 1 (mixedDerivative 4 0 L) := by
    exact mixedDerivative_contDiff 4 0 1 L (by simpa using hL)
  have hL2 : ContDiff ℝ 1 (mixedDerivative 2 0 L) := by
    apply mixedDerivative_contDiff 2 0 1 L
    exact hL.of_le (by norm_num)
  have hL11 : ContDiff ℝ 1 (mixedDerivative 1 1 L) := by
    apply mixedDerivative_contDiff 1 1 1 L
    exact hL.of_le (by norm_num)
  rw [partialX_add
        (fun w => mixedDerivative 4 0 L w +
          6 * (mixedDerivative 2 0 L w) ^ 2)
        (mixedDerivative 1 1 L)
        (hL4.add (contDiff_const.mul (hL2.pow 2))) hL11,
      partialX_add (mixedDerivative 4 0 L)
        (fun w => 6 * (mixedDerivative 2 0 L w) ^ 2)
        hL4 (contDiff_const.mul (hL2.pow 2)),
      partialX_const_mul 6 (fun w => (mixedDerivative 2 0 L w) ^ 2),
      partialX_pow_two (mixedDerivative 2 0 L) hL2,
      partialX_mixedDerivative 4 0 L,
      partialX_mixedDerivative 2 0 L,
      partialX_mixedDerivative 1 1 L] at hx
  have hxz := congrFun hx z
  simp [partialX] at hxz
  have hT : partialT (mixedDerivative 2 0 L) = mixedDerivative 2 1 L := by
    apply partialT_mixedDerivative 2 0 L
    exact hL.of_le (by norm_num)
  change kdvResidual (tauTransform tau) z = 0
  rw [show tauTransform tau = fun w => 2 * mixedDerivative 2 0 L w by
    funext w
    rfl]
  unfold kdvResidual
  rw [partialT_const_mul, partialX_const_mul,
      iterate_partialX_const_mul, hT]
  have h25 := congrFun (partialX_mixedDerivative 2 0 L) z
  have hiter : partialX (partialX (partialX (mixedDerivative 2 0 L))) z =
      mixedDerivative 5 0 L z := by
    rw [partialX_mixedDerivative 2 0 L,
      partialX_mixedDerivative 3 0 L,
      partialX_mixedDerivative 4 0 L]
  change partialX (mixedDerivative 2 0 L) z = mixedDerivative 3 0 L z at h25
  simp [iterate, Function.comp_def]
  rw [h25, hiter]
  nlinarith

theorem hirotaKdVTarget_proof : HirotaKdVTarget := by
  exact hirotaKdVTarget_of_logDerivativeBridge logDerivativeBridge

assert_no_sorry logarithmic_bilinear_identity
assert_no_sorry logDerivativeBridge
assert_no_sorry hirotaKdVTarget_proof

#print sorries logarithmic_bilinear_identity
#print sorries logDerivativeBridge
#print sorries hirotaKdVTarget_proof

#print axioms logarithmic_bilinear_identity
#print axioms logDerivativeBridge
#print axioms hirotaKdVTarget_proof

end Stage1Instances.THM_M_1553
