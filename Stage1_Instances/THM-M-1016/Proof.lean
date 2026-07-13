import Statement
import ObligationTree
import Mathlib.MeasureTheory.Measure.TightNormed
import Mathlib.Analysis.Calculus.FDeriv.Basic

/-!
# THM-M-1016 proof phase

This module proves the frozen finite-dimensional delta method. Weak convergence makes the
normalized laws uniformly tight. Divergence of the positive scaling then forces concentration at
the expansion point, and the Frechet little-o estimate makes the uniformly scaled remainder
negligible in measure. The frozen conditional composition supplies the final Slutsky step.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1016.Proof

open Stage1Instances.THM_M_1016

universe u v w

/-- The laws of a distributionally convergent normalized sequence form a tight family. -/
theorem normalizedLawsTight
    (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    (Y : Nat -> Omega -> E) (Z : Omega' -> E)
    (hY : TendstoInDistribution Y atTop Z (fun _ => mu) mu') :
    IsTightMeasureSet (Set.range (fun n => mu.map (Y n))) := by
  let laws : Nat -> ProbabilityMeasure E := fun n =>
    ⟨mu.map (Y n), Measure.isProbabilityMeasure_map (hY.forall_aemeasurable n)⟩
  let lawZ : ProbabilityMeasure E :=
    ⟨mu'.map Z, Measure.isProbabilityMeasure_map hY.aemeasurable_limit⟩
  have hlaws : Tendsto laws atTop (nhds lawZ) := hY.tendsto
  have hcompact : IsCompact (Set.insert lawZ (Set.range laws)) :=
    hlaws.isCompact_insert_range
  have hclosure : IsCompact (closure (Set.range laws)) :=
    hcompact.closure_of_subset (by
      intro p hp
      exact Set.mem_insert_iff.mpr (Or.inr hp))
  have htight : IsTightMeasureSet
      {((p : ProbabilityMeasure E) : Measure E) | p ∈ Set.range laws} :=
    isTightMeasureSet_of_isCompact_closure hclosure
  convert htight using 1
  ext nu
  simp only [Set.mem_range, Set.mem_setOf_eq]
  constructor
  · rintro ⟨n, rfl⟩
    exact ⟨laws n, ⟨n, rfl⟩, rfl⟩
  · rintro ⟨p, ⟨n, rfl⟩, rfl⟩
    exact ⟨n, rfl⟩

/-- Uniform norm-tail control for every member of the normalized sequence. -/
theorem normalizedTail
    (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    (Y : Nat -> Omega -> E) (Z : Omega' -> E)
    (hY : TendstoInDistribution Y atTop Z (fun _ => mu) mu') :
    Tendsto (fun R : Real => ⨆ n, mu {omega | R < ‖Y n omega‖}) atTop (nhds 0) := by
  have htight := normalizedLawsTight Omega Omega' mu mu' E Y Z hY
  have htail := tendsto_measure_norm_gt_of_isTightMeasureSet htight
  refine htail.congr' (Filter.Eventually.of_forall fun R => ?_)
  simp only [iSup_range]
  apply iSup_congr
  intro n
  rw [Measure.map_apply_of_aemeasurable (hY.forall_aemeasurable n)
    (measurableSet_lt (measurable_const : Measurable fun _ : E => R) measurable_norm)]
  rfl

/-- A divergent positive scaling and tight normalized laws force `X n -> theta` in measure. -/
theorem inputConvergesInMeasure
    (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    (X : Nat -> Omega -> E) (Z : Omega' -> E) (theta : E)
    (r : Nat -> Real) (hr_pos : forall n, 0 < r n) (hr_inf : Tendsto r atTop atTop)
    (hX : TendstoInDistribution
      (fun n omega => r n • (X n omega - theta)) atTop Z (fun _ => mu) mu') :
    TendstoInMeasure mu X atTop (fun _ => theta) := by
  let Y : Nat -> Omega -> E := fun n omega => r n • (X n omega - theta)
  have htail := normalizedTail Omega Omega' mu mu' E Y Z hX
  rw [tendstoInMeasure_iff_norm]
  intro epsilon hepsilon
  apply ENNReal.tendsto_atTop_zero.mpr
  intro eta heta
  obtain ⟨R, hRtail⟩ := (htail.eventually_lt_const heta).exists
  have hr_event : ∀ᶠ n in atTop, R / epsilon < r n :=
    hr_inf (eventually_gt_atTop (R / epsilon))
  exact Filter.eventually_atTop.1 <| hr_event.mono fun n hn => by
    calc
      mu {omega | (epsilon : Real) ≤ ‖X n omega - theta‖}
          ≤ mu {omega | R < ‖Y n omega‖} := by
            apply measure_mono
            intro omega homega
            dsimp only [Y]
            change R < ‖r n • (X n omega - theta)‖
            rw [norm_smul, Real.norm_eq_abs, abs_of_pos (hr_pos n)]
            have hmul : R < r n * epsilon := (div_lt_iff₀ hepsilon).mp hn
            exact hmul.trans_le (mul_le_mul_of_nonneg_left homega (hr_pos n).le)
      _ ≤ ⨆ k, mu {omega | R < ‖Y k omega‖} :=
        le_iSup (fun k => mu {omega | R < ‖Y k omega‖}) n
      _ ≤ eta := hRtail.le

/-- The scaled Frechet remainder tends to zero in measure. -/
theorem scaledRemainderTendstoInMeasure
    (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w) (F : Type*)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup F] [NormedSpace Real F] [FiniteDimensional Real F]
    [MeasurableSpace F] [BorelSpace F]
    (X : Nat -> Omega -> E) (Z : Omega' -> E) (theta : E)
    (r : Nat -> Real) (hr_pos : forall n, 0 < r n) (hr_inf : Tendsto r atTop atTop)
    (g : E -> F) (g' : E →L[Real] F) (_hg_meas : Measurable g)
    (hg_diff : HasFDerivAt g g' theta)
    (hX : TendstoInDistribution
      (fun n omega => r n • (X n omega - theta)) atTop Z (fun _ => mu) mu') :
    TendstoInMeasure mu
      (fun n omega =>
        r n • (g (X n omega) - g theta) - g' (r n • (X n omega - theta)))
      atTop 0 := by
  rw [tendstoInMeasure_iff_norm]
  intro epsilon hepsilon
  let Y : Nat -> Omega -> E := fun n omega => r n • (X n omega - theta)
  let rem : E -> F := fun x => g x - g theta - g' (x - theta)
  have htail : Tendsto (fun R : Real => ⨆ n, mu {omega | R < ‖Y n omega‖}) atTop (nhds 0) :=
    normalizedTail Omega Omega' mu mu' E Y Z hX
  have hconc : TendstoInMeasure mu X atTop (fun _ => theta) :=
    inputConvergesInMeasure Omega Omega' mu mu' E X Z theta r hr_pos hr_inf hX
  apply ENNReal.tendsto_atTop_zero.mpr
  intro eta heta
  have heta2 : (0 : ENNReal) < eta / 2 := ENNReal.div_pos heta.ne' (by norm_num)
  obtain ⟨R, hRtail, hRpos⟩ :=
    ((htail.eventually_lt_const heta2).and (eventually_gt_atTop (0 : Real))).exists
  let c : Real := epsilon / (R + 1)
  have hc : 0 < c := div_pos hepsilon (by positivity)
  have hsmall : ∀ᶠ x in nhds theta, ‖rem x‖ ≤ c * ‖x - theta‖ := by
    simpa [rem] using hg_diff.isLittleO.bound hc
  rcases Metric.eventually_nhds_iff.1 hsmall with ⟨delta, hdelta, hbound⟩
  have hbad := tendstoInMeasure_iff_norm.mp hconc delta hdelta
  have hbad_event : ∀ᶠ n in atTop, mu {omega | delta ≤ ‖X n omega - theta‖} < eta / 2 :=
    hbad.eventually_lt_const heta2
  exact Filter.eventually_atTop.1 <| hbad_event.mono fun n hn => by
   calc
    mu {omega | (epsilon : Real) ≤
        ‖(r n • (g (X n omega) - g theta) - g' (r n • (X n omega - theta))) - 0‖}
        ≤ mu ({omega | delta ≤ ‖X n omega - theta‖} ∪
            {omega | R < ‖Y n omega‖}) := by
          apply measure_mono
          intro omega homega
          simp only [sub_zero] at homega
          by_contra hnot
          simp only [Set.mem_union, Set.mem_setOf_eq, not_or, not_le, not_lt] at hnot
          have hxball : X n omega ∈ Metric.ball theta delta := by
            simpa [Metric.mem_ball, dist_eq_norm] using hnot.1
          have hrem := hbound hxball
          have hYle : ‖Y n omega‖ ≤ R := hnot.2
          have hrewrite :
              r n • (g (X n omega) - g theta) - g' (r n • (X n omega - theta)) =
                r n • rem (X n omega) := by
            dsimp only [rem]
            rw [map_smul]
            module
          change epsilon ≤
            ‖r n • (g (X n omega) - g theta) - g' (r n • (X n omega - theta))‖ at homega
          rw [hrewrite, norm_smul, Real.norm_eq_abs, abs_of_pos (hr_pos n)] at homega
          have hnormY : ‖Y n omega‖ = r n * ‖X n omega - theta‖ := by
            dsimp only [Y]
            rw [norm_smul, Real.norm_eq_abs, abs_of_pos (hr_pos n)]
          have hprod : r n * ‖rem (X n omega)‖ ≤ c * ‖Y n omega‖ := by
            rw [hnormY]
            nlinarith [hrem, (hr_pos n).le]
          have hcR : c * ‖Y n omega‖ < epsilon := by
            calc
              c * ‖Y n omega‖ ≤ c * R := mul_le_mul_of_nonneg_left hYle hc.le
              _ < epsilon := by
                dsimp only [c]
                rw [div_mul_eq_mul_div, div_lt_iff₀ (by linarith [hRpos])]
                nlinarith [hRpos]
          exact (not_lt_of_ge homega) (hprod.trans_lt hcR)
    _ ≤ mu {omega | delta ≤ ‖X n omega - theta‖} + mu {omega | R < ‖Y n omega‖} :=
      measure_union_le _ _
    _ ≤ eta / 2 + (⨆ k, mu {omega | R < ‖Y k omega‖}) := by
      gcongr
      exact le_iSup (fun k => mu {omega | R < ‖Y k omega‖}) n
    _ ≤ eta := by
      calc
        eta / 2 + (⨆ k, mu {omega | R < ‖Y k omega‖}) ≤ eta / 2 + eta / 2 :=
          add_le_add_right hRtail.le _
        _ = eta := ENNReal.add_halves eta

/-- Measurability of the normalized input recovers measurability of every transformed statistic. -/
theorem transformedAEMeasurable
    (Omega : Type u)
    [MeasurableSpace Omega]
    (mu : Measure Omega)
    (E : Type w) (F : Type*)
    [NormedAddCommGroup E] [NormedSpace Real E]
    [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup F] [NormedSpace Real F]
    [MeasurableSpace F] [BorelSpace F]
    (X : Nat -> Omega -> E) (theta : E) (r : Nat -> Real)
    (hr_pos : forall n, 0 < r n)
    (g : E -> F) (hg_meas : Measurable g)
    (hXmeas : forall n, AEMeasurable (fun omega => r n • (X n omega - theta)) mu) :
    forall n, AEMeasurable (fun omega => r n • (g (X n omega) - g theta)) mu := by
  intro n
  have hr_ne : r n ≠ 0 := (hr_pos n).ne'
  have hXn : AEMeasurable (X n) mu := by
    have hscaled := hXmeas n
    have hrecover : X n = fun omega => (r n)⁻¹ •
        (r n • (X n omega - theta)) + theta := by
      funext omega
      rw [inv_smul_smul₀ hr_ne]
      simp
    rw [hrecover]
    fun_prop
  fun_prop

/-- Exact proof of the unchanged statement, assembled through the frozen conditional theorem. -/
theorem deltaMethod
    (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w) (F : Type*)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup F] [NormedSpace Real F] [FiniteDimensional Real F]
    [MeasurableSpace F] [BorelSpace F]
    (X : Nat -> Omega -> E) (Z : Omega' -> E) (theta : E)
    (r : Nat -> Real) (hr_pos : forall n, 0 < r n) (hr_inf : Tendsto r atTop atTop)
    (g : E -> F) (g' : E →L[Real] F) (hg_meas : Measurable g)
    (hg_diff : HasFDerivAt g g' theta)
    (hX : TendstoInDistribution
      (fun n omega => r n • (X n omega - theta)) atTop Z (fun _ => mu) mu') :
    TendstoInDistribution
      (fun n omega => r n • (g (X n omega) - g theta)) atTop
      (fun omega => g' (Z omega)) (fun _ => mu) mu' := by
  apply deltaMethod_of_remainder Omega Omega' mu mu' E F X Z theta r hr_pos hr_inf g g'
    hg_meas hg_diff hX
  · exact scaledRemainderTendstoInMeasure Omega Omega' mu mu' E F X Z theta r
      hr_pos hr_inf g g' hg_meas hg_diff hX
  · exact transformedAEMeasurable Omega mu E F X theta r hr_pos g hg_meas
      hX.forall_aemeasurable

/-- Placeholder-free proof of the exact proposition frozen in `Statement.lean`. -/
theorem statementProof : StatementShape.{u, v, w} := by
  intro Omega Omega' _ _ mu mu' _ _ E F _ _ _ _ _ _ _ _ _ _ X Z theta r hr_pos hr_inf
    g g' hg_meas hg_diff hX
  exact deltaMethod Omega Omega' mu mu' E F X Z theta r hr_pos hr_inf g g' hg_meas hg_diff hX

#print axioms normalizedLawsTight
#print axioms normalizedTail
#print axioms inputConvergesInMeasure
#print axioms scaledRemainderTendstoInMeasure
#print axioms transformedAEMeasurable
#print axioms deltaMethod
#print axioms statementProof

end Stage1Instances.THM_M_1016.Proof
