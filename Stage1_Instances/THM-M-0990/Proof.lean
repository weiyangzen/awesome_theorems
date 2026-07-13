import «Stage1_Instances».«THM-M-0990».Normalization
import «Stage1_Instances».«THM-M-0990».GeneralizedLindeberg

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory
open scoped BigOperators ProbabilityTheory Real Topology

namespace Stage1Instances.THM_M_0990

universe u v

theorem sq_le_rpow_mul_final {epsilon delta z : Real}
    (hepsilon : 0 < epsilon) (hdelta : 0 < delta)
    (hz : epsilon < |z|) :
    z ^ 2 <= epsilon ^ (-delta) * |z| ^ (2 + delta) := by
  have hp : epsilon ^ delta <= |z| ^ delta :=
    Real.rpow_le_rpow hepsilon.le hz.le hdelta.le
  have hepow : 0 < epsilon ^ delta := Real.rpow_pos_of_pos hepsilon delta
  have hzabs : 0 < |z| := hepsilon.trans hz
  rw [Real.rpow_add hzabs 2 delta, Real.rpow_two]
  have hmul : |z| ^ 2 * epsilon ^ delta <= |z| ^ 2 * |z| ^ delta :=
    mul_le_mul_of_nonneg_left hp (sq_nonneg |z|)
  rw [Real.rpow_neg hepsilon.le]
  apply (le_inv_mul_iff₀' hepow).2
  simpa only [sq_abs] using hmul

theorem truncatedSecondMoment_scaled_le_final
    {Omega : Type*} [MeasurableSpace Omega]
    {P : Measure Omega} {W : Omega -> Real} {scale epsilon delta : Real}
    (hscale : 0 < scale) (hepsilon : 0 < epsilon) (hdelta : 0 < delta)
    (hWmeas : AEMeasurable W P)
    (hWsq : Integrable (fun omega => W omega ^ 2) P)
    (hmoment : Integrable (fun omega => |W omega| ^ (2 + delta)) P) :
    THM_M_0989.truncatedSecondMoment P (fun omega => scale⁻¹ * W omega) epsilon <=
      epsilon ^ (-delta) * (scale ^ (2 + delta))⁻¹ *
        ∫ omega, |W omega| ^ (2 + delta) ∂P := by
  let Z : Omega -> Real := fun omega => scale⁻¹ * W omega
  have hZmeas : AEMeasurable Z P := aemeasurable_const.mul hWmeas
  have hZsq : Integrable (fun omega => Z omega ^ 2) P := by
    convert hWsq.const_mul (scale⁻¹ ^ 2) using 1 <;> funext omega <;>
      simp only [Z] <;> ring
  have hZtrunc : Integrable (fun omega => Z omega ^ 2 *
      if epsilon < ‖Z omega‖ then 1 else 0) P := by
    let s : Set Omega := {omega | epsilon < ‖Z omega‖}
    have hs : NullMeasurableSet s P :=
      nullMeasurableSet_lt aemeasurable_const hZmeas.norm
    have hind : s.indicator (fun omega => Z omega ^ 2) =
        fun omega => Z omega ^ 2 * if epsilon < ‖Z omega‖ then 1 else 0 := by
      funext omega
      by_cases h : omega ∈ s <;> simp [Set.indicator, s, h]
    rw [← hind]
    exact hZsq.indicator₀ hs
  have hZmoment : Integrable (fun omega => |Z omega| ^ (2 + delta)) P := by
    convert hmoment.const_mul ((scale ^ (2 + delta))⁻¹) using 1
    funext omega
    simp only [Z]
    rw [abs_mul, abs_inv, abs_of_pos hscale,
      Real.mul_rpow (by positivity) (abs_nonneg _), Real.inv_rpow hscale.le]
  unfold THM_M_0989.truncatedSecondMoment
  change (∫ omega, Z omega ^ 2 *
      (if epsilon < ‖Z omega‖ then 1 else 0) ∂P) <= _
  calc
    _ <= ∫ omega, epsilon ^ (-delta) * |Z omega| ^ (2 + delta) ∂P := by
      refine integral_mono hZtrunc (hZmoment.const_mul _) fun omega => ?_
      by_cases hlarge : epsilon < ‖Z omega‖
      · rw [if_pos hlarge, mul_one]
        exact sq_le_rpow_mul_final hepsilon hdelta
          (by simpa [Real.norm_eq_abs] using hlarge)
      · rw [if_neg hlarge, mul_zero]
        positivity
    _ = epsilon ^ (-delta) * ∫ omega, |Z omega| ^ (2 + delta) ∂P := by
      rw [integral_const_mul]
    _ = epsilon ^ (-delta) * ((scale ^ (2 + delta))⁻¹ *
        ∫ omega, |W omega| ^ (2 + delta) ∂P) := by
      congr 1
      rw [← integral_const_mul]
      congr 1
      funext omega
      simp only [Z]
      rw [abs_mul, abs_inv, abs_of_pos hscale,
        Real.mul_rpow (by positivity) (abs_nonneg _), Real.inv_rpow hscale.le]
    _ = _ := by ring

theorem sum_truncatedSecondMoment_normalized_le_final
    {Omega : Type*} [MeasurableSpace Omega]
    {P : Measure Omega} [IsProbabilityMeasure P]
    (X : Nat -> Nat -> Omega -> Real) (delta epsilon : Real)
    (hepsilon : 0 < epsilon) (hdelta : 0 < delta)
    (hMeas : ∀ n k, Measurable (X n k))
    (hLp : ∀ n k, MemLp (X n k) 2 P)
    (hMoment : ∀ n k, Integrable
      (fun omega => |centered P X n k omega| ^ (2 + delta)) P)
    (n : Nat) (hvar : 0 < rowVarianceSum P X n) :
    (∑ k : Fin n, THM_M_0989.truncatedSecondMoment P
      (normalizedIncrement P X n k) epsilon) <=
      epsilon ^ (-delta) * lyapunovRatio P X delta n := by
  have hscale : 0 < rowScale P X n := Real.sqrt_pos.2 hvar
  calc
    _ <= ∑ k : Fin n,
        epsilon ^ (-delta) * (rowScale P X n ^ (2 + delta))⁻¹ *
          ∫ omega, |centered P X n k.val omega| ^ (2 + delta) ∂P := by
      exact Finset.sum_le_sum fun k _ =>
        truncatedSecondMoment_scaled_le_final hscale hepsilon hdelta
          (centered_measurable P X hMeas n k.val).aemeasurable
          (centered_memLp X hLp n k.val).integrable_sq
          (hMoment n k.val)
    _ = epsilon ^ (-delta) *
        ((rowScale P X n ^ (2 + delta))⁻¹ *
          ∑ k : Fin n, ∫ omega,
            |centered P X n k.val omega| ^ (2 + delta) ∂P) := by
      rw [← Finset.mul_sum]
      ring
    _ = epsilon ^ (-delta) * lyapunovRatio P X delta n := by
      congr 1
      unfold lyapunovRatio
      congr 1
      rw [Finset.sum_fin_eq_sum_range]
      exact Finset.sum_congr rfl fun k hk => by
        rw [dif_pos (Finset.mem_range.1 hk)]
        rfl

theorem normalizedRowSum_measurable_final
    {Omega : Type*} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (hMeas : ∀ n k, Measurable (X n k)) (n : Nat) :
    Measurable (normalizedRowSum P X n) := by
  unfold normalizedRowSum
  exact measurable_const.mul (Finset.measurable_fun_sum (Finset.range n)
    (fun k _ => centered_measurable P X hMeas n k))

theorem lyapunovCentralLimit_exact : StatementShape.{u, v} := by
  intro Omega _ Omega' _ P P' _ _ X Y delta hY hdelta hMeas hInd hLp
    hMoment hVar hLyap
  let A : EventuallyNormalizedTriangularArray Omega := {
    probabilityMeasure := P
    isProbabilityMeasure := inferInstance
    increment := normalizedIncrement P X
    rowIndependent := fun n => normalizedIncrement_independent X hInd n
    rowAEMeasurable := fun n k =>
      (normalizedIncrement_memLp X hLp n k).aemeasurable
    rowIntegrable := fun n k =>
      (normalizedIncrement_memLp X hLp n k).integrable (by norm_num)
    rowSquareIntegrable := fun n k =>
      (normalizedIncrement_memLp X hLp n k).integrable_sq
    rowCentered := fun n k => normalizedIncrement_integral_eq_zero X hLp n k
    rowVarianceNormalized := by
      filter_upwards [hVar] with n hn
      exact normalizedIncrement_variance_sum X hMeas n hn
    lindebergCondition := by
      intro epsilon hepsilon
      have hupper : Tendsto
          (fun n => epsilon ^ (-delta) * lyapunovRatio P X delta n)
          atTop (nhds 0) := by
        simpa using tendsto_const_nhds.mul hLyap
      refine squeeze_zero' ?_ ?_ hupper
      · exact Eventually.of_forall fun n => Finset.sum_nonneg fun k _ =>
          THM_M_0989.truncatedSecondMoment_nonneg P
            (normalizedIncrement P X n k) epsilon
      · filter_upwards [hVar] with n hn
        exact sum_truncatedSecondMoment_normalized_le_final X delta epsilon
          hepsilon hdelta hMeas hLp hMoment n hn }
  have hCLT := eventualLindebergFeller_exact A
  refine {
    forall_aemeasurable := fun n =>
      (normalizedRowSum_measurable_final P X hMeas n).aemeasurable
    aemeasurable_limit := hY.aemeasurable
    tendsto := ?_ }
  have ht := hCLT.tendsto
  convert ht using 2 with n
  · apply Subtype.ext
    apply Measure.map_congr
    exact Filter.Eventually.of_forall fun omega => by
      simpa only [A, eventualRowSum] using
        (congrFun (normalizedIncrement_sum P X n) omega).symm
  · apply Subtype.ext
    simpa [Measure.map_id] using hY.map_eq

#print axioms lyapunovCentralLimit_exact
#print axioms sq_le_rpow_mul_final
#print axioms truncatedSecondMoment_scaled_le_final
#print axioms sum_truncatedSecondMoment_normalized_le_final
#print axioms normalizedRowSum_measurable_final

end Stage1Instances.THM_M_0990
