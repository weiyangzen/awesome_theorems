import LocalEncoding
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.MeasureTheory.Function.Jacobian
import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0612 dimension-two branch

This module proves the radius-squared obstruction when the coordinate index is
`Fin 1`. It is a genuine special-case proof, but it does not prove the
higher-dimensional branch or the canonical root.
-/

noncomputable section

open scoped BigOperators

open MeasureTheory

namespace Stage1.THM_M_0612

/-- A linear map preserving the standard two-dimensional symplectic form has determinant one. -/
theorem symplectic_det_dimTwo
    (A : PhaseSpace (Fin 1) →L[ℝ] PhaseSpace (Fin 1))
    (h : ∀ v w, standardForm (A v) (A w) = standardForm v w) :
    A.det = 1 := by
  change LinearMap.det A.toLinearMap = 1
  rw [← LinearMap.det_toMatrix (Pi.basisFun ℝ (Fin 1 ⊕ Fin 1))]
  let e : (Fin 1 ⊕ Fin 1) ≃ Fin 2 := finSumFinEquiv
  rw [← Matrix.det_reindex_self e]
  rw [Matrix.det_fin_two]
  have he0 : e.symm (0 : Fin 2) = Sum.inl 0 := by
    exact finSumFinEquiv_symm_apply_castAdd 0
  have he1 : e.symm (1 : Fin 2) = Sum.inr 0 := by
    exact finSumFinEquiv_symm_last
  simp only [Matrix.reindex_apply, Matrix.submatrix_apply]
  rw [he0, he1]
  have hh := h (Pi.single (Sum.inl 0) 1) (Pi.single (Sum.inr 0) 1)
  simpa [standardForm, LinearMap.toMatrix_apply, Pi.basisFun, Pi.single_apply,
    Finset.sum_ite_irrel, mul_comm] using hh

/-- A symplectic embedding of a two-dimensional ball preserves its volume. -/
theorem image_volume_eq_dimTwo
    {r : ℝ} {f : PhaseSpace (Fin 1) → PhaseSpace (Fin 1)}
    (hf : IsSymplecticEmbeddingOnBall r f) :
    volume (Set.image f (@ball (Fin 1) _ r)) = volume (@ball (Fin 1) _ r) := by
  rw [← MeasureTheory.lintegral_abs_det_fderiv_eq_addHaar_image
    volume (isOpen_ball r).measurableSet]
  · calc
      (∫⁻ x in @ball (Fin 1) _ r,
          ENNReal.ofReal |(fderiv ℝ f x).det| ∂volume) =
          ∫⁻ _x in @ball (Fin 1) _ r, (1 : ENNReal) ∂volume := by
            apply MeasureTheory.setLIntegral_congr_fun (isOpen_ball r).measurableSet
            intro x hx
            dsimp only
            rw [symplectic_det_dimTwo (fderiv ℝ f x) (hf.2.2 x hx)]
            norm_num
      _ = volume (@ball (Fin 1) _ r) := MeasureTheory.setLIntegral_one _
  · intro x hx
    exact (hasFDerivAt_of_contDiffOn_ball hf.1 hx).hasFDerivWithinAt
  · exact hf.2.1

/-- The coordinate ball in real dimension two has volume `pi * r^2`. -/
theorem volume_ball_dimTwo (r : ℝ) (hr : 0 < r) :
    volume (@ball (Fin 1) _ r) = ENNReal.ofReal r ^ 2 * ENNReal.ofReal Real.pi := by
  have h :=
    MeasureTheory.volume_sum_rpow_lt (Fin 1 ⊕ Fin 1) (p := (2 : ℝ)) (by norm_num) r
  rw [show @ball (Fin 1) _ r =
      {x : (Fin 1 ⊕ Fin 1) → ℝ | (∑ i, |x i| ^ (2 : ℝ)) ^ (1 / (2 : ℝ)) < r} by
    ext x
    simp only [ball, normSq, Set.mem_setOf_eq]
    rw [show (1 / (2 : ℝ)) = (2 : ℝ)⁻¹ by norm_num]
    conv_rhs => rw [← show (1 / (2 : ℝ)) = (2 : ℝ)⁻¹ by norm_num]
    rw [← Real.sqrt_eq_rpow]
    change (∑ i, x i ^ 2) < r ^ 2 ↔
      Real.sqrt (∑ i, |x i| ^ (2 : ℝ)) < r
    rw [Real.sqrt_lt' hr]
    simp [sq_abs]]
  rw [h]
  rw [show Fintype.card (Fin 1 ⊕ Fin 1) = 2 by decide]
  norm_num
  rw [show (3 / 2 : ℝ) = 1 / 2 + 1 by norm_num]
  rw [Real.Gamma_add_one (by norm_num : (1 / 2 : ℝ) ≠ 0)]
  rw [Real.Gamma_one_half_eq]
  have halg : (2 * ((1 / 2 : ℝ) * Real.sqrt Real.pi)) ^ 2 = Real.pi := by
    rw [show (2 : ℝ) * (1 / 2 * Real.sqrt Real.pi) = Real.sqrt Real.pi by ring]
    exact Real.sq_sqrt Real.pi_pos.le
  rw [halg]

/-- The squared-radius obstruction for the complete `Fin 1` branch. -/
theorem dimTwo_radiusSquaredObstruction
    (r R : ℝ) (hr : 0 < r) (hR : 0 < R)
    (f : PhaseSpace (Fin 1) → PhaseSpace (Fin 1))
    (hf : IsSymplecticEmbeddingOnBall r f)
    (hmaps : Set.MapsTo f (ball r) (cylinder 0 R)) :
    r ^ 2 ≤ R ^ 2 := by
  have hsubset : Set.image f (@ball (Fin 1) _ r) ⊆ @ball (Fin 1) _ R := by
    rintro _ ⟨x, hx, rfl⟩
    simpa [ball, cylinder, normSq] using hmaps hx
  have hvol : volume (Set.image f (@ball (Fin 1) _ r)) ≤
      volume (@ball (Fin 1) _ R) := measure_mono hsubset
  rw [image_volume_eq_dimTwo hf, volume_ball_dimTwo r hr,
    volume_ball_dimTwo R hR] at hvol
  have hpi : ENNReal.ofReal Real.pi ≠ 0 :=
    ENNReal.ofReal_ne_zero_iff.mpr Real.pi_pos
  apply (ENNReal.ofReal_le_ofReal_iff (sq_nonneg R)).mp
  rw [ENNReal.ofReal_pow hr.le, ENNReal.ofReal_pow hR.le]
  exact (ENNReal.mul_le_mul_iff_left hpi ENNReal.ofReal_ne_top).mp hvol

assert_no_sorry symplectic_det_dimTwo
assert_no_sorry image_volume_eq_dimTwo
assert_no_sorry volume_ball_dimTwo
assert_no_sorry dimTwo_radiusSquaredObstruction

#print sorries symplectic_det_dimTwo
#print sorries image_volume_eq_dimTwo
#print sorries volume_ball_dimTwo
#print sorries dimTwo_radiusSquaredObstruction

#print axioms symplectic_det_dimTwo
#print axioms image_volume_eq_dimTwo
#print axioms volume_ball_dimTwo
#print axioms dimTwo_radiusSquaredObstruction

end Stage1.THM_M_0612
