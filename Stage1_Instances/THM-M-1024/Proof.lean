import Statement

/-!
# THM-M-1024 proof execution

This module implements the compensated-integrability part of the first analytic
leaf in the frozen proof architecture: the closed-unit-ball compensated integrand
in `levyExponent` is Bochner integrable against every locally valid Levy measure.
It deliberately makes no claim that the whole leaf or the forward, converse, or
uniqueness packages are complete.
-/

namespace Stage1Instances.THM_M_1024

open MeasureTheory Set
open scoped ENNReal

/-- The closed-unit-ball compensated integrand used by `levyExponent`. -/
noncomputable def compensatedIntegrand {d : Nat} (u x : Space d) : Complex :=
  Complex.exp (Complex.I * ((@inner Real _ _ u x : Real) : Complex)) - 1
    - Complex.I * ((@inner Real _ _ u x : Real) : Complex) * if ‖x‖ ≤ 1 then 1 else 0

@[simp]
theorem compensatedIntegrand_zero_right {d : Nat} (u : Space d) :
    compensatedIntegrand u 0 = 0 := by
  simp [compensatedIntegrand]

/-- The frozen compensated integrand is measurable in its jump variable. -/
theorem measurable_compensatedIntegrand {d : Nat} (u : Space d) :
    Measurable (compensatedIntegrand u) := by
  unfold compensatedIntegrand
  apply Measurable.sub
  · exact (((measurable_const.mul (by fun_prop)).cexp).sub measurable_const)
  · exact (measurable_const.mul (by fun_prop)).mul
      (measurable_const.ite (isClosed_le continuous_norm continuous_const).measurableSet
        measurable_const)

/-- Outside the closed unit ball, the compensation vanishes and the norm is at
most two. -/
theorem norm_compensatedIntegrand_le_two {d : Nat} (u x : Space d) (hx : 1 < ‖x‖) :
    ‖compensatedIntegrand u x‖ ≤ 2 := by
  simp only [compensatedIntegrand, not_le.mpr hx, if_false, mul_zero, sub_zero]
  calc
    ‖Complex.exp (Complex.I * ((@inner Real _ _ u x : Real) : Complex)) - 1‖
        ≤ ‖Complex.exp (Complex.I * ((@inner Real _ _ u x : Real) : Complex))‖ +
            ‖(1 : Complex)‖ := norm_sub_le _ _
    _ = 1 + 1 := by
      rw [show Complex.I * ((@inner Real _ _ u x : Real) : Complex) =
          ((@inner Real _ _ u x : Real) : Complex) * Complex.I by ring,
        Complex.norm_exp_ofReal_mul_I, norm_one]
    _ = 2 := by norm_num

/-- Pointwise domination by the Levy-measure weight.  The constant depends on
the fixed frequency `u`, while the dominating function is exactly the one in
`IsLevyMeasure`. -/
theorem norm_compensatedIntegrand_le {d : Nat} (u x : Space d) :
    ‖compensatedIntegrand u x‖ ≤ (2 + 3 * ‖u‖ ^ 2) * min 1 (‖x‖ ^ 2) := by
  by_cases hx : ‖x‖ ≤ 1
  · have hmin : min (1 : Real) (‖x‖ ^ 2) = ‖x‖ ^ 2 :=
      min_eq_right (pow_le_one₀ (norm_nonneg x) hx)
    rw [hmin]
    simp only [compensatedIntegrand, hx, if_true, mul_one]
    set z : Complex :=
      Complex.I * ((@inner Real _ _ u x : Real) : Complex) with hz_def
    have hz_eq : z = ((@inner Real _ _ u x : Real) : Complex) * Complex.I := by
      rw [hz_def]
      ring
    have hz_norm : ‖z‖ = |@inner Real _ _ u x| := by
      rw [hz_eq, norm_mul, Complex.norm_real, Complex.norm_I, mul_one,
        Real.norm_eq_abs]
    have hinner : |@inner Real _ _ u x| ≤ ‖u‖ * ‖x‖ := abs_real_inner_le_norm u x
    by_cases hz_small : ‖z‖ ≤ 1
    · calc
        ‖Complex.exp z - 1 - z‖ ≤ ‖z‖ ^ 2 :=
          Complex.norm_exp_sub_one_sub_id_le hz_small
        _ ≤ (‖u‖ * ‖x‖) ^ 2 := by
          gcongr
          rw [hz_norm]
          exact hinner
        _ = ‖u‖ ^ 2 * ‖x‖ ^ 2 := by ring
        _ ≤ (2 + 3 * ‖u‖ ^ 2) * ‖x‖ ^ 2 := by
          nlinarith [sq_nonneg ‖u‖, sq_nonneg ‖x‖]
    · have hz_large : 1 < ‖z‖ := lt_of_not_ge hz_small
      have hz_exp : ‖Complex.exp z‖ = 1 := by
        rw [hz_eq, Complex.norm_exp_ofReal_mul_I]
      have htri : ‖Complex.exp z - 1 - z‖ ≤ 2 + ‖z‖ := by
        calc
          ‖Complex.exp z - 1 - z‖ ≤ ‖Complex.exp z - 1‖ + ‖z‖ := norm_sub_le _ _
          _ ≤ (‖Complex.exp z‖ + ‖(1 : Complex)‖) + ‖z‖ := by
            gcongr
            exact norm_sub_le _ _
          _ = 2 + ‖z‖ := by rw [hz_exp, norm_one]; ring
      have hz_sq : 2 + ‖z‖ ≤ 3 * ‖z‖ ^ 2 := by nlinarith [sq_nonneg ‖z‖]
      calc
        ‖Complex.exp z - 1 - z‖ ≤ 2 + ‖z‖ := htri
        _ ≤ 3 * ‖z‖ ^ 2 := hz_sq
        _ ≤ 3 * (‖u‖ * ‖x‖) ^ 2 := by
          gcongr
          rw [hz_norm]
          exact hinner
        _ = 3 * ‖u‖ ^ 2 * ‖x‖ ^ 2 := by ring
        _ ≤ (2 + 3 * ‖u‖ ^ 2) * ‖x‖ ^ 2 := by
          nlinarith [sq_nonneg ‖x‖]
  · have hx_large : 1 < ‖x‖ := lt_of_not_ge hx
    have hmin : min (1 : Real) (‖x‖ ^ 2) = 1 :=
      min_eq_left (one_le_pow₀ hx_large.le)
    rw [hmin]
    calc
      ‖compensatedIntegrand u x‖ ≤ 2 := norm_compensatedIntegrand_le_two u x hx_large
      _ ≤ (2 + 3 * ‖u‖ ^ 2) * 1 := by nlinarith [sq_nonneg ‖u‖]

/-- The analytic obligation needed for the jump term of `levyExponent`. -/
theorem integrable_compensatedIntegrand {d : Nat} {nu : Measure (Space d)}
    (hnu : IsLevyMeasure nu) (u : Space d) :
    Integrable (compensatedIntegrand u) nu := by
  refine (hnu.2.const_mul (2 + 3 * ‖u‖ ^ 2)).mono'
    (measurable_compensatedIntegrand u).aestronglyMeasurable ?_
  filter_upwards [] with x
  simpa only [norm_mul, Real.norm_eq_abs, abs_of_nonneg (by positivity :
      0 ≤ 2 + 3 * ‖u‖ ^ 2)] using norm_compensatedIntegrand_le u x

/-- The jump integral occurring syntactically in `levyExponent` is
well-defined as a Bochner integral for every valid triplet. -/
theorem integrable_levyExponent_jump {d : Nat} {data : LevyTriplet d}
    (hdata : IsLevyMeasure data.jumps) (u : Space d) :
    Integrable
      (fun x : Space d =>
        Complex.exp (Complex.I * ((@inner Real _ _ u x : Real) : Complex)) - 1
          - Complex.I * ((@inner Real _ _ u x : Real) : Complex) *
            if ‖x‖ ≤ 1 then 1 else 0)
      data.jumps := by
  simpa only [compensatedIntegrand] using integrable_compensatedIntegrand hdata u

set_option pp.universes true in
#check integrable_compensatedIntegrand

#print axioms integrable_compensatedIntegrand

#print axioms integrable_levyExponent_jump

end Stage1Instances.THM_M_1024
