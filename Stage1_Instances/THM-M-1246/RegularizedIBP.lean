import Mathlib
import Statement

/-!
# Regularized integration by parts for THM-M-1246

This module proves the coordinate divergence formula for the regularized radial
field `x / (‖x‖ ^ 2 + eps)` and sums its integration-by-parts identities.
-/

set_option maxHeartbeats 1000000

noncomputable section

open MeasureTheory
open scoped RealInnerProductSpace
open Stage1Instances.THM_M_1246

namespace Stage1Instances.THM_M_1246.Proof

theorem regularized_coord_fderiv {n : Nat} (eps : Real) (i : Fin n) (x : Space n)
    (hD : ‖x‖ ^ 2 + eps ≠ 0) :
    fderiv Real (fun x : Space n => x i / (‖x‖ ^ 2 + eps)) x
      (EuclideanSpace.basisFun (Fin n) Real i)
      = 1 / (‖x‖ ^ 2 + eps) - 2 * (x i)^2 / (‖x‖ ^ 2 + eps)^2 := by
  let D : Real := ‖x‖ ^ 2 + eps
  have hnum : HasFDerivAt (fun y : Space n => y i)
      ((PiLp.proj 2 (fun _ : Fin n => Real) i) : Space n →L[Real] Real) x :=
    PiLp.hasFDerivAt_apply (p := 2) x i
  have hden : HasFDerivAt (fun y : Space n => ‖y‖ ^ 2 + eps)
      (2 • innerSL Real x) x :=
    (hasStrictFDerivAt_norm_sq x).hasFDerivAt.add_const eps
  have hinv : HasFDerivAt (fun y : Space n => (‖y‖ ^ 2 + eps)⁻¹)
      ((ContinuousLinearMap.toSpanSingleton Real (-(D ^ 2)⁻¹)).comp
        (2 • innerSL Real x)) x := by
    convert (hasFDerivAt_inv hD).comp x hden using 1
  have hquot := hnum.mul hinv
  change fderiv Real ((fun y : Space n => y i) *
      fun y : Space n => (‖y‖ ^ 2 + eps)⁻¹) x
      (EuclideanSpace.basisFun (Fin n) Real i) = _
  rw [hquot.fderiv]
  have hinner : inner Real x (EuclideanSpace.basisFun (Fin n) Real i) = x i :=
    EuclideanSpace.inner_basisFun_real (Fin n) x i
  simp only [ContinuousLinearMap.add_apply, ContinuousLinearMap.smul_apply,
    ContinuousLinearMap.comp_apply, ContinuousLinearMap.toSpanSingleton_apply,
    PiLp.proj_apply, smul_eq_mul]
  rw [innerSL_apply_apply]
  rw [hinner]
  simp [D, div_eq_mul_inv]
  field_simp
  ring

theorem regularized_divergence {n : Nat} (eps : Real) (x : Space n)
    (hD : ‖x‖ ^ 2 + eps ≠ 0) :
    (∑ i : Fin n, fderiv Real (fun y : Space n => y i / (‖y‖ ^ 2 + eps)) x
      (EuclideanSpace.basisFun (Fin n) Real i))
      = (n : Real) / (‖x‖ ^ 2 + eps)
          - 2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps)^2 := by
  calc
    _ = ∑ i : Fin n,
        (1 / (‖x‖ ^ 2 + eps) - 2 * (x i)^2 / (‖x‖ ^ 2 + eps)^2) := by
      apply Finset.sum_congr rfl
      intro i hi
      exact regularized_coord_fderiv eps i x hD
    _ = (n : Real) / (‖x‖ ^ 2 + eps)
          - 2 * (∑ i : Fin n, (x i)^2) / (‖x‖ ^ 2 + eps)^2 := by
      simp only [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
        Fintype.card_fin, nsmul_eq_mul]
      rw [← Finset.sum_div, ← Finset.mul_sum]
      ring
    _ = _ := by rw [← EuclideanSpace.real_norm_sq_eq x]

theorem regularized_coord_ibp {n : Nat} (u : Space n → Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u)
    (eps : Real) (heps : 0 < eps) (i : Fin n) :
    (∫ x, u x ^ 2 * fderiv Real
        (fun y : Space n => y i / (‖y‖ ^ 2 + eps)) x
        (EuclideanSpace.basisFun (Fin n) Real i))
      = - ∫ x, fderiv Real (fun y : Space n => u y ^ 2) x
          (EuclideanSpace.basisFun (Fin n) Real i) *
          (x i / (‖x‖ ^ 2 + eps)) := by
  let v : Space n := EuclideanSpace.basisFun (Fin n) Real i
  let f : Space n → Real := fun x => u x ^ 2
  let g : Space n → Real := fun x => x i / (‖x‖ ^ 2 + eps)
  have hden_ne : ∀ x : Space n, ‖x‖ ^ 2 + eps ≠ 0 := by
    intro x
    positivity
  have hf : ContDiff Real ⊤ f := by
    dsimp [f]
    fun_prop
  have hg : ContDiff Real ⊤ g := by
    dsimp [g]
    exact (contDiff_piLp_apply (p := (2 : ENNReal))).div
      ((contDiff_norm_sq Real).add contDiff_const) hden_ne
  have hfc : HasCompactSupport f := by
    dsimp [f]
    simpa only [pow_two] using huc.mul_right
  have hf'g : Integrable (fun x ↦ fderiv Real f x v * g x) :=
    ((hf.continuous_fderiv (by simp)).clm_apply continuous_const).mul hg.continuous
      |>.integrable_of_hasCompactSupport (hfc.fderiv_apply Real v).mul_right
  have hfg' : Integrable (fun x ↦ f x * fderiv Real g x v) :=
    hf.continuous.mul ((hg.continuous_fderiv (by simp)).clm_apply continuous_const)
      |>.integrable_of_hasCompactSupport hfc.mul_right
  have hfg : Integrable (fun x ↦ f x * g x) :=
    hf.continuous.mul hg.continuous |>.integrable_of_hasCompactSupport hfc.mul_right
  have hibp := integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable
    (f := f) (g := g) (v := v) hf'g hfg' hfg
    (fun x hx => hf.differentiable (by simp) x)
    (fun x hx => hg.differentiable (by simp) x)
  simpa [f, g, v] using hibp

theorem regularized_summed_ibp {n : Nat} (u : Space n → Real)
    (hu : ContDiff Real ⊤ u) (huc : HasCompactSupport u)
    (eps : Real) (heps : 0 < eps) :
    (∫ x, u x ^ 2 *
        ((n : Real) / (‖x‖ ^ 2 + eps)
          - 2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps)^2))
      = - ∫ x, 2 * u x *
          (fderiv Real u x x / (‖x‖ ^ 2 + eps)) := by
  let e : Fin n → Space n := fun i => EuclideanSpace.basisFun (Fin n) Real i
  let D : Space n → Real := fun x => ‖x‖ ^ 2 + eps
  have hD : ∀ x : Space n, D x ≠ 0 := by
    intro x
    dsimp [D]
    positivity
  have hleft_int : ∀ i : Fin n, Integrable (fun x => u x ^ 2 *
      fderiv Real (fun y : Space n => y i / D y) x (e i)) := by
    intro i
    have hu2 : ContDiff Real ⊤ (fun x : Space n => u x ^ 2) := by
      fun_prop
    have hg : ContDiff Real ⊤ (fun y : Space n => y i / D y) := by
      dsimp [D]
      exact (contDiff_piLp_apply (p := (2 : ENNReal))).div
        ((contDiff_norm_sq Real).add contDiff_const) (by intro x; positivity)
    exact hu2.continuous.mul
      ((hg.continuous_fderiv (by simp)).clm_apply continuous_const)
      |>.integrable_of_hasCompactSupport
        (by simpa only [pow_two] using huc.mul_right.mul_right)
  calc
    _ = ∫ x, ∑ i : Fin n, u x ^ 2 *
          fderiv Real (fun y : Space n => y i / D y) x (e i) := by
      apply integral_congr_ae
      filter_upwards [] with x
      rw [← Finset.mul_sum]
      exact congrArg (u x ^ 2 * ·) (regularized_divergence eps x (hD x)).symm
    _ = ∑ i : Fin n, ∫ x, u x ^ 2 *
          fderiv Real (fun y : Space n => y i / D y) x (e i) := by
      exact integral_finset_sum Finset.univ (fun i _ => hleft_int i)
    _ = ∑ i : Fin n, (- ∫ x,
          fderiv Real (fun y : Space n => u y ^ 2) x (e i) *
            (x i / D x)) := by
      apply Finset.sum_congr rfl
      intro i hi
      simpa [D, e] using regularized_coord_ibp u hu huc eps heps i
    _ = - ∫ x, 2 * u x *
          (fderiv Real u x x / D x) := by
      have hright_int : ∀ i : Fin n, Integrable (fun x : Space n =>
          -(fderiv Real (fun y : Space n => u y ^ 2) x (e i) *
            (x i / D x))) := by
        intro i
        have hu2 : ContDiff Real ⊤ (fun x : Space n => u x ^ 2) := by
          fun_prop
        let du2 : Space n → Real := fun x =>
          fderiv Real (fun y : Space n => u y ^ 2) x (e i)
        let gi : Space n → Real := fun x => x i / D x
        have hdu2 : Continuous du2 := by
          dsimp [du2]
          exact (hu2.continuous_fderiv (by simp)).clm_apply continuous_const
        have hg : ContDiff Real ⊤ (fun x : Space n => x i / D x) := by
          dsimp [D]
          exact (contDiff_piLp_apply (p := (2 : ENNReal))).div
            ((contDiff_norm_sq Real).add contDiff_const) (by intro x; positivity)
        have hdu2c : HasCompactSupport du2 := by
          dsimp [du2]
          apply HasCompactSupport.fderiv_apply (𝕜 := Real)
          simpa only [pow_two] using huc.mul_right
        have hcont : Continuous (fun x : Space n => -(du2 x * gi x)) :=
          (hdu2.mul hg.continuous).neg
        have hcomp : HasCompactSupport (fun x : Space n => -(du2 x * gi x)) :=
          hdu2c.mul_right.neg
        exact hcont.integrable_of_hasCompactSupport hcomp
      calc
        _ = ∑ i : Fin n, ∫ x, -(fderiv Real (fun y : Space n => u y ^ 2) x (e i) *
              (x i / D x)) := by simp only [integral_neg, Finset.sum_neg_distrib]
        _ = ∫ x, ∑ i : Fin n, -(fderiv Real (fun y : Space n => u y ^ 2) x (e i) *
              (x i / D x)) :=
          (integral_finset_sum Finset.univ (fun i _ => hright_int i)).symm
        _ = _ := by
          rw [← integral_neg]
          apply integral_congr_ae
          filter_upwards [] with x
          rw [Finset.sum_neg_distrib]
          apply congrArg Neg.neg
          have hdu : DifferentiableAt Real u x := hu.differentiable (by simp) x
          have hpow := (hdu.hasFDerivAt.pow 2).fderiv
          rw [hpow]
          simp only [Nat.reduceSubDiff, pow_one, nsmul_eq_mul,
            ContinuousLinearMap.smul_apply, smul_eq_mul]
          simp_rw [mul_div]
          rw [← Finset.sum_div]
          apply congrArg (fun z : Real => z / D x)
          calc
            _ = 2 * u x * (∑ i : Fin n, fderiv Real u x (e i) * x i) := by
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro i hi
              ring
            _ = 2 * u x * fderiv Real u x x := by
              congr 1
              calc
                _ = fderiv Real u x (∑ i : Fin n, x i • e i) := by
                  rw [map_sum]
                  apply Finset.sum_congr rfl
                  intro i hi
                  rw [map_smul, smul_eq_mul]
                  ring
                _ = _ := by
                  rw [(show (∑ i : Fin n, x i • e i) = x by
                    simpa [e, EuclideanSpace.basisFun_repr] using
                      (EuclideanSpace.basisFun (Fin n) Real).sum_repr x)]

end Stage1Instances.THM_M_1246.Proof
