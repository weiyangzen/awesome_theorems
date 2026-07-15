import CocycleBridge
import Mathlib.Analysis.SpecificLimits.Basic

open Filter Function MeasureTheory
open scoped Matrix.Norms.L2Operator

noncomputable section

universe u v

namespace Stage1Instances.THM_M_1056

variable {Omega : Type u}
variable {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
variable [FiniteDimensional Real E]

theorem coord_norm_upper (x : E) :
    ‖coordEquiv (E := E) x‖ ≤
      ‖(coordEquiv (E := E)).toContinuousLinearMap‖ * ‖x‖ :=
  (coordEquiv (E := E)).toContinuousLinearMap.le_opNorm x

theorem coord_norm_lower (x : E) :
    ‖x‖ ≤ ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖ *
      ‖coordEquiv (E := E) x‖ := by
  conv_lhs => rw [← (coordEquiv (E := E)).symm_apply_apply x]
  exact (coordEquiv (E := E)).symm.toContinuousLinearMap.le_opNorm _

theorem norm_pos_of_equiv_apply {x : E} (hx : x ≠ 0) :
    0 < ‖coordEquiv (E := E) x‖ := norm_pos_iff.mpr (by
      intro hzero
      apply hx
      apply (coordEquiv (E := E)).injective
      simpa using hzero)

theorem norm_pos_of_cocycleVector
    (T : Omega -> Omega) (A : Omega -> E ≃L[Real] E)
    (n : Nat) (omega : Omega) {x : E} (hx : x ≠ 0) :
    0 < ‖bridgeCocycleVector T A n omega x‖ := by
  induction n generalizing omega x with
  | zero => simpa [bridgeCocycleVector] using (norm_pos_iff.mpr hx)
  | succ n ih =>
      rw [cocycleVector_succ_base]
      exact ih (omega := T omega) (by
        intro hzero
        apply hx
        apply (A omega).injective
        simpa using hzero)

theorem log_coord_norm_sub_log_norm_upper
    (x : E) (hx : x ≠ 0) :
    Real.log ‖coordEquiv (E := E) x‖ - Real.log ‖x‖ ≤
      Real.log ‖(coordEquiv (E := E)).toContinuousLinearMap‖ := by
  have hxpos : 0 < ‖x‖ := norm_pos_iff.mpr hx
  have hcxpos := norm_pos_of_equiv_apply (E := E) hx
  have hle := coord_norm_upper (E := E) x
  by_cases htriv : Subsingleton E
  · exact False.elim (hx (Subsingleton.elim x 0))
  · letI : Nontrivial E := not_subsingleton_iff_nontrivial.mp htriv
    have hepos := (coordEquiv (E := E)).norm_pos
    have hlog := Real.log_le_log hcxpos hle
    rw [Real.log_mul hepos.ne' hxpos.ne'] at hlog
    linarith

theorem log_coord_norm_sub_log_norm_lower
    (x : E) (hx : x ≠ 0) :
    -Real.log ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖ ≤
      Real.log ‖coordEquiv (E := E) x‖ - Real.log ‖x‖ := by
  have hxpos : 0 < ‖x‖ := norm_pos_iff.mpr hx
  have hcxpos := norm_pos_of_equiv_apply (E := E) hx
  have hle := coord_norm_lower (E := E) x
  by_cases htriv : Subsingleton E
  · exact False.elim (hx (Subsingleton.elim x 0))
  · letI : Nontrivial E := not_subsingleton_iff_nontrivial.mp htriv
    have hespos := (coordEquiv (E := E)).norm_symm_pos
    have hlog := Real.log_le_log hxpos hle
    rw [Real.log_mul hespos.ne' hcxpos.ne'] at hlog
    linarith

theorem tendsto_growth_coordinate_iff
    (T : Omega -> Omega) (A : Omega -> E ≃L[Real] E)
    (omega : Omega) (x : E) (hx : x ≠ 0) (lambda : Real) :
    Tendsto
        (fun n : Nat => (n : Real)⁻¹ *
          Real.log ‖Matrix.toEuclideanCLM (𝕜 := Real)
            (matrixCocycle (matrixGenerator A) T n omega)
            (coordEquiv (E := E) x)‖)
        atTop (nhds lambda) <->
      Tendsto
        (fun n : Nat => Real.log ‖bridgeCocycleVector T A n omega x‖ / n)
        atTop (nhds lambda) := by
  have hpoint : forall n : Nat,
      Matrix.toEuclideanCLM (𝕜 := Real)
          (matrixCocycle (matrixGenerator A) T n omega)
          (coordEquiv (E := E) x) =
        coordEquiv (E := E) (bridgeCocycleVector T A n omega x) :=
    fun n => matrixCocycle_generator_apply T A n omega x
  let f : Nat -> Real := fun n =>
    (n : Real)⁻¹ * Real.log ‖coordEquiv (E := E) (bridgeCocycleVector T A n omega x)‖
  let g : Nat -> Real := fun n =>
    (n : Real)⁻¹ * Real.log ‖bridgeCocycleVector T A n omega x‖
  have hdiff : Tendsto (fun n => f n - g n) atTop (nhds 0) := by
    have hbound : forall n,
        |f n - g n| ≤
          max (|Real.log ‖(coordEquiv (E := E)).toContinuousLinearMap‖|)
            (|Real.log ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖|) / n := by
      intro n
      by_cases hn : n = 0
      · simp [hn, f, g]
      · have hxiter : bridgeCocycleVector T A n omega x ≠ 0 :=
          norm_ne_zero_iff.mp (norm_pos_of_cocycleVector T A n omega hx).ne'
        have hu := log_coord_norm_sub_log_norm_upper
          (E := E) (bridgeCocycleVector T A n omega x) hxiter
        have hl := log_coord_norm_sub_log_norm_lower
          (E := E) (bridgeCocycleVector T A n omega x) hxiter
        have hnpos : 0 < (n : Real) := by exact_mod_cast (Nat.pos_of_ne_zero hn)
        dsimp [f, g]
        have hfactor :
            (n : Real)⁻¹ * Real.log ‖coordEquiv (E := E) (bridgeCocycleVector T A n omega x)‖ -
                (n : Real)⁻¹ * Real.log ‖bridgeCocycleVector T A n omega x‖ =
              (n : Real)⁻¹ *
                (Real.log ‖coordEquiv (E := E) (bridgeCocycleVector T A n omega x)‖ -
                  Real.log ‖bridgeCocycleVector T A n omega x‖) := by ring
        rw [hfactor]
        rw [abs_mul, abs_inv, abs_of_pos hnpos]
        rw [div_eq_inv_mul]
        change (n : Real)⁻¹ *
            |Real.log ‖coordEquiv (E := E) (bridgeCocycleVector T A n omega x)‖ -
              Real.log ‖bridgeCocycleVector T A n omega x‖| ≤
          (n : Real)⁻¹ *
            max (|Real.log ‖(coordEquiv (E := E)).toContinuousLinearMap‖|)
              (|Real.log ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖|)
        apply mul_le_mul_of_nonneg_left _ (inv_nonneg.mpr hnpos.le)
        rw [abs_le]
        constructor
        · calc
            -max (|Real.log ‖(coordEquiv (E := E)).toContinuousLinearMap‖|)
                (|Real.log ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖|) ≤
                -|Real.log ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖| :=
              neg_le_neg (le_max_right _ _)
            _ ≤ -Real.log ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖ :=
              neg_le_neg (le_abs_self _)
            _ ≤ _ := hl
        · exact le_trans hu (le_trans (le_abs_self _) (le_max_left _ _))
    have hzero : Tendsto
        (fun n : Nat =>
          max (|Real.log ‖(coordEquiv (E := E)).toContinuousLinearMap‖|)
            (|Real.log ‖(coordEquiv (E := E)).symm.toContinuousLinearMap‖|) / n)
        atTop (nhds 0) := tendsto_const_div_atTop_nhds_zero_nat _
    rw [tendsto_zero_iff_abs_tendsto_zero]
    exact squeeze_zero' (Eventually.of_forall fun n => abs_nonneg (f n - g n))
      (Eventually.of_forall hbound) hzero
  constructor
  · intro hf
    have hff : Tendsto f atTop (nhds lambda) := by
      simpa only [f, hpoint] using hf
    have hg : Tendsto g atTop (nhds lambda) := by
      have := hdiff.const_sub lambda
      have : Tendsto (fun n => f n - (f n - g n)) atTop (nhds (lambda - 0)) :=
        hff.sub hdiff
      simpa only [sub_sub_cancel, sub_zero] using this
    simpa only [g, div_eq_inv_mul] using hg
  · intro hg
    have hgg : Tendsto g atTop (nhds lambda) := by
      simpa only [g, div_eq_inv_mul] using hg
    have hf : Tendsto f atTop (nhds lambda) := by
      have := hdiff.add hgg
      simpa only [sub_add_cancel, zero_add] using this
    simpa only [f, hpoint] using hf

end Stage1Instances.THM_M_1056

