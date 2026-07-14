import Statement

/-!
# THM-M-1067 proof-phase boundary audit

The frozen time measure is the pushforward of all real Lebesgue measure by `Real.toNNReal`.
Consequently it has an infinite atom at zero. The checked bodies below show that this makes the
frozen occupation identity impossible for every candidate local-time field under every Wiener
measure. This is a statement blocker, not a proof of Brownian local-time existence.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal Topology

namespace Stage1Instances.THM_M_1067

/-- The negative half-line is collapsed to zero, giving the frozen time measure an infinite atom. -/
theorem nonnegativeLebesgue_singleton_zero :
    nonnegativeLebesgue ({0} : Set ℝ≥0) = ∞ := by
  rw [nonnegativeLebesgue,
    Measure.map_apply measurable_real_toNNReal (measurableSet_singleton (0 : ℝ≥0))]
  have hpre : Real.toNNReal ⁻¹' ({0} : Set ℝ≥0) = Set.Iic 0 := by
    ext x
    simp [Real.toNNReal_eq_zero]
  rw [hpre, Real.volume_Iic]

private def zeroIndicator : ℝ → ℝ≥0∞ :=
  Set.indicator ({0} : Set ℝ) (fun _ => 1)

private theorem measurable_zeroIndicator : Measurable zeroIndicator := by
  exact measurable_const.indicator (measurableSet_singleton (0 : ℝ))

/-- At time zero, the frozen time integral is infinite while the spatial singleton integral is
zero, independently of the proposed field. -/
theorem occupation_at_zero_false
    (w : BrownianPath) (L : BrownianPath → ℝ≥0 → ℝ → ℝ≥0) :
    ¬ ((∫⁻ s in Set.Icc (0 : ℝ≥0) 0,
          zeroIndicator (w.1 s) ∂nonnegativeLebesgue) =
        ∫⁻ x : ℝ, zeroIndicator x * (L w 0 x : ℝ≥0∞)) := by
  have hlhs : (∫⁻ s in Set.Icc (0 : ℝ≥0) 0,
      zeroIndicator (w.1 s) ∂nonnegativeLebesgue) = ∞ := by
    rw [Set.Icc_self, lintegral_singleton]
    simp [zeroIndicator, w.property, nonnegativeLebesgue_singleton_zero]
  have hrhs : (∫⁻ x : ℝ, zeroIndicator x * (L w 0 x : ℝ≥0∞)) = 0 := by
    have hfun : (fun x : ℝ => zeroIndicator x * (L w 0 x : ℝ≥0∞)) =
        ({0} : Set ℝ).indicator (fun x => (L w 0 x : ℝ≥0∞)) := by
      funext x
      by_cases hx : x = 0
      · subst x
        simp [zeroIndicator]
      · simp [zeroIndicator, hx]
    rw [hfun, lintegral_indicator (measurableSet_singleton (0 : ℝ))]
    simp
  rw [hlhs, hrhs]
  exact ENNReal.top_ne_zero

/-- No field can satisfy the frozen local-time predicate for a Wiener measure. -/
theorem no_local_time_of_wiener
    {W : Measure BrownianPath} (hW : IsWienerMeasure W)
    (L : BrownianPath → ℝ≥0 → ℝ → ℝ≥0) :
    ¬ IsBrownianLocalTime W L := by
  intro hL
  letI : IsProbabilityMeasure W := hW.1
  obtain ⟨w, _hcont, hocc⟩ := hL.2.exists
  exact occupation_at_zero_false w L (hocc 0 zeroIndicator measurable_zeroIndicator)

/-- The exact frozen target is equivalent to nonexistence of its own Wiener measures, rather than
to Brownian local-time existence. -/
theorem target_iff_no_wiener_measure :
    BrownianLocalTimeTarget ↔ ¬ ∃ W : Measure BrownianPath, IsWienerMeasure W := by
  constructor
  · intro hTarget ⟨W, hW⟩
    obtain ⟨L, hL⟩ := hTarget W hW
    exact no_local_time_of_wiener hW L hL
  · intro hNoW W hW
    exact (hNoW ⟨W, hW⟩).elim

#check nonnegativeLebesgue_singleton_zero
#check occupation_at_zero_false
#check no_local_time_of_wiener
#check target_iff_no_wiener_measure

#print axioms nonnegativeLebesgue_singleton_zero
#print axioms occupation_at_zero_false
#print axioms no_local_time_of_wiener
#print axioms target_iff_no_wiener_measure

end Stage1Instances.THM_M_1067
