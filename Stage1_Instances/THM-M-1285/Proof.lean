import Statement

/-!
# THM-M-1285 proof-lane lemmas

This module implements the frozen rational-level, centered-ball route. It
constructs a measurable radial decreasing profile, proves exact positive
strict-superlevel volumes, and closes the exact canonical target.
-/

namespace Stage1Instances.THM_M_1285

open MeasureTheory
open scoped ENNReal

/-- A function obtained by applying a profile to the norm is radial. -/
theorem isRadial_profile {n : Nat} (profile : ℝ → ENNReal) :
    IsRadial (fun x : Euclidean n => profile ‖x‖) := by
  intro x y hxy
  exact congrArg profile hxy

/-- An antitone profile gives a radially nonincreasing function. -/
theorem isRadiallyNonincreasing_profile {n : Nat} (profile : ℝ → ENNReal)
    (hprofile : Antitone profile) :
    IsRadiallyNonincreasing (fun x : Euclidean n => profile ‖x‖) := by
  intro x y hxy
  exact hprofile hxy

/-- A measurable profile gives a measurable radial candidate. -/
theorem measurable_profile {n : Nat} (profile : ℝ → ENNReal)
    (hprofile : Measurable profile) :
    Measurable (fun x : Euclidean n => profile ‖x‖) := by
  exact hprofile.comp measurable_norm

/-- Volume of a positive strict superlevel of `f`. -/
noncomputable def distribution {n : Nat} (f : Euclidean n → ENNReal)
    (t : ENNReal) : ENNReal :=
  volume {x | t < f x}

/-- The strict-superlevel distribution decreases with the threshold. -/
theorem distribution_antitone {n : Nat} (f : Euclidean n → ENNReal) :
    Antitone (distribution f) := by
  intro t u htu
  exact measure_mono fun x hx => htu.trans_lt hx

/-- Every strict superlevel is the union of its rationally higher strict
superlevels. -/
theorem iUnion_strictSuperlevel_gt {n : Nat} (f : Euclidean n → ENNReal)
    (t : ENNReal) :
    (⋃ q : ℚ, ⋃ (_ : 0 ≤ q ∧ t < Real.toNNReal q),
        {x | (Real.toNNReal q : ENNReal) < f x}) = {x | t < f x} := by
  ext x
  simp only [Set.mem_iUnion, Set.mem_setOf_eq]
  constructor
  · rintro ⟨q, ⟨hq0, htq⟩, hqfx⟩
    exact htq.trans hqfx
  · intro htfx
    rcases ENNReal.lt_iff_exists_rat_btwn.mp htfx with ⟨q, hq0, htq, hqfx⟩
    exact ⟨q, ⟨⟨hq0, htq⟩, hqfx⟩⟩

/-- The distribution at a threshold is the supremum of its values at
rationally higher thresholds. -/
theorem distribution_iSup_rat_gt {n : Nat} (f : Euclidean n → ENNReal)
    (t : ENNReal) :
    distribution f t =
      ⨆ q : ℚ, ⨆ (_ : 0 ≤ q ∧ t < Real.toNNReal q),
        distribution f (Real.toNNReal q) := by
  let s : {q : ℚ // 0 ≤ q ∧ t < Real.toNNReal q} → Set (Euclidean n) :=
    fun q => {x | (Real.toNNReal q.1 : ENNReal) < f x}
  have hdir : Directed (· ⊆ ·) s := by
    intro a b
    by_cases hab : a.1 ≤ b.1
    · refine ⟨a, Set.Subset.rfl, ?_⟩
      intro x hx
      exact (ENNReal.coe_le_coe.mpr
        (Real.toNNReal_mono (Rat.cast_le.mpr hab))).trans_lt hx
    · have hba : b.1 ≤ a.1 := le_of_not_ge hab
      refine ⟨b, ?_, Set.Subset.rfl⟩
      intro x hx
      exact (ENNReal.coe_le_coe.mpr
        (Real.toNNReal_mono (Rat.cast_le.mpr hba))).trans_lt hx
  rw [distribution, ← iUnion_strictSuperlevel_gt f t]
  change volume (⋃ q : ℚ, ⋃ (hq : 0 ≤ q ∧ t < Real.toNNReal q),
    s ⟨q, hq⟩) = _
  rw [← Set.iUnion_subtype (fun q : ℚ => 0 ≤ q ∧ t < Real.toNNReal q) s]
  rw [hdir.measure_iUnion]
  rw [iSup_subtype']
  rfl

/-- Radius of the centered Euclidean ball with prescribed finite volume. -/
noncomputable def radiusForVolume {n : Nat} (_hn : 0 < n) (a : ENNReal) : ℝ :=
  if _ha : a = 0 then 0 else
    (a.toReal / (volume (Metric.ball (0 : Euclidean n) 1)).toReal) ^ (n : ℝ)⁻¹

/-- The selected radius realizes every finite `ENNReal` volume exactly. -/
theorem volume_ball_radiusForVolume {n : Nat} (hn : 0 < n) (a : ENNReal)
    (ha : a ≠ ∞) :
    volume (Metric.ball (0 : Euclidean n) (radiusForVolume hn a)) = a := by
  by_cases ha0 : a = 0
  · simp [radiusForVolume, ha0]
  have hV0 : volume (Metric.ball (0 : Euclidean n) 1) ≠ 0 :=
    ne_of_gt (Metric.measure_ball_pos volume (0 : Euclidean n) zero_lt_one)
  have hVtop : volume (Metric.ball (0 : Euclidean n) 1) ≠ ∞ := measure_ball_ne_top
  have hapos : 0 < a.toReal := ENNReal.toReal_pos ha0 ha
  have hVpos : 0 < (volume (Metric.ball (0 : Euclidean n) 1)).toReal :=
    ENNReal.toReal_pos hV0 hVtop
  have hratio : 0 ≤ a.toReal / (volume (Metric.ball (0 : Euclidean n) 1)).toReal :=
    (div_pos hapos hVpos).le
  have hn0 : n ≠ 0 := Nat.ne_of_gt hn
  let i : Fin n := ⟨0, hn⟩
  letI : Nonempty (Fin n) := ⟨i⟩
  letI : Nontrivial (Euclidean n) := inferInstance
  rw [radiusForVolume, dif_neg ha0]
  rw [Measure.addHaar_ball volume 0 (Real.rpow_nonneg hratio _)]
  rw [finrank_euclideanSpace]
  simp only [Fintype.card_fin]
  rw [Real.rpow_inv_natCast_pow hratio hn0]
  rw [ENNReal.ofReal_div_of_pos hVpos]
  rw [ENNReal.ofReal_toReal ha, ENNReal.ofReal_toReal hVtop]
  exact ENNReal.div_mul_cancel hV0 hVtop

/-- The centered-ball radius is nonnegative. -/
theorem radiusForVolume_nonneg {n : Nat} (hn : 0 < n) (a : ENNReal) :
    0 ≤ radiusForVolume hn a := by
  simp only [radiusForVolume]
  split_ifs
  · exact le_rfl
  · positivity

/-- Larger finite target volumes receive no smaller centered-ball radius. -/
theorem radiusForVolume_mono {n : Nat} (hn : 0 < n) {a b : ENNReal}
    (hbtop : b ≠ ∞) (hab : a ≤ b) :
    radiusForVolume hn a ≤ radiusForVolume hn b := by
  by_cases ha : a = 0
  · simpa [radiusForVolume, ha] using radiusForVolume_nonneg hn b
  have hb : b ≠ 0 := fun hb => ha (le_antisymm (hb ▸ hab) (zero_le _))
  simp only [radiusForVolume, dif_neg ha, dif_neg hb]
  apply Real.rpow_le_rpow
  · positivity
  · apply div_le_div_of_nonneg_right
    · exact ENNReal.toReal_mono hbtop hab
    · exact ENNReal.toReal_nonneg
  · positivity

/-- Countable rational profile associated to a radial radius selector. -/
noncomputable def starProfile {n : Nat} (radius : ENNReal → ℝ)
    (f : Euclidean n → ENNReal) (r : ℝ) : ENNReal :=
  ⨆ q : ℚ, if _hq : 0 ≤ q ∧ r < radius (distribution f (Real.toNNReal q)) then
    (Real.toNNReal q : ENNReal) else 0

/-- The countable rational profile is measurable in its radius argument. -/
theorem starProfile_measurable {n : Nat} (radius : ENNReal → ℝ)
    (f : Euclidean n → ENNReal) :
    Measurable (starProfile radius f) := by
  apply Measurable.iSup
  intro q
  apply Measurable.ite
  · by_cases hq : 0 ≤ q
    · simpa only [hq, true_and] using
        measurableSet_lt (measurable_id : Measurable (fun r : ℝ => r))
          (measurable_const : Measurable
            (fun _ : ℝ => radius (distribution f (Real.toNNReal q))))
    · simp [hq]
  · exact measurable_const
  · exact measurable_const

/-- The countable rational profile decreases with the radius argument. -/
theorem starProfile_antitone {n : Nat} (radius : ENNReal → ℝ)
    (f : Euclidean n → ENNReal) :
    Antitone (starProfile radius f) := by
  intro r s hrs
  apply iSup_mono
  intro q
  split_ifs with hs hr
  · exact le_rfl
  · simp only [nonpos_iff_eq_zero]
    by_contra hq0
    exact hr ⟨hs.1, hrs.trans_lt hs.2⟩
  · exact zero_le _
  · exact le_rfl

/-- A strict superlevel of the rational profile is the union of the
corresponding centered balls. -/
theorem strictSuperlevel_starProfile {n : Nat} (radius : ENNReal → ℝ)
    (f : Euclidean n → ENNReal) (t : ENNReal) :
    {x | t < starProfile radius f ‖x‖} =
      ⋃ q : ℚ, ⋃ (_ : 0 ≤ q ∧ t < Real.toNNReal q),
        Metric.ball (0 : Euclidean n)
          (radius (distribution f (Real.toNNReal q))) := by
  ext x
  simp only [Set.mem_setOf_eq, Set.mem_iUnion, starProfile, lt_iSup_iff]
  constructor
  · rintro ⟨q, hq⟩
    by_cases hcond :
        0 ≤ q ∧ ‖x‖ < radius (distribution f (Real.toNNReal q))
    · rw [dif_pos hcond] at hq
      refine ⟨q, ⟨⟨hcond.1, hq⟩, ?_⟩⟩
      simpa [Metric.mem_ball, dist_zero_right] using hcond.2
    · rw [dif_neg hcond] at hq
      exact (not_lt_of_ge (zero_le t) hq).elim
  · rintro ⟨q, ⟨⟨hq0, htq⟩, hxball⟩⟩
    refine ⟨q, ?_⟩
    rw [dif_pos]
    · exact htq
    · refine ⟨hq0, ?_⟩
      simpa [Metric.mem_ball, dist_zero_right] using hxball

/-- Positive strict superlevels of the rational profile have exactly the
prescribed distribution. -/
theorem measure_strictSuperlevel_starProfile {n : Nat}
    (radius : ENNReal → ℝ) (f : Euclidean n → ENNReal)
    (hfinite : ∀ t : ENNReal, 0 < t → distribution f t ≠ ∞)
    (hradius_mono : ∀ {a b : ENNReal}, a ≤ b → b ≠ ∞ → radius a ≤ radius b)
    (hradius_volume : ∀ a : ENNReal, a ≠ ∞ →
      volume (Metric.ball (0 : Euclidean n) (radius a)) = a)
    (t : ENNReal) (ht : 0 < t) :
    volume {x : Euclidean n | t < starProfile radius f ‖x‖} =
      distribution f t := by
  rw [strictSuperlevel_starProfile radius f t]
  let s : {q : ℚ // 0 ≤ q ∧ t < Real.toNNReal q} → Set (Euclidean n) :=
    fun q => Metric.ball 0 (radius (distribution f (Real.toNNReal q.1)))
  have hpos (q : {q : ℚ // 0 ≤ q ∧ t < Real.toNNReal q}) :
      0 < (Real.toNNReal q.1 : ENNReal) := ht.trans q.2.2
  have hdir : Directed (· ⊆ ·) s := by
    intro a b
    by_cases hab : a.1 ≤ b.1
    · refine ⟨a, Set.Subset.rfl, ?_⟩
      apply Metric.ball_subset_ball
      apply hradius_mono
      · apply distribution_antitone
        exact ENNReal.coe_le_coe.mpr
          (Real.toNNReal_mono (Rat.cast_le.mpr hab))
      · exact hfinite _ (hpos a)
    · have hba : b.1 ≤ a.1 := le_of_not_ge hab
      refine ⟨b, ?_, Set.Subset.rfl⟩
      apply Metric.ball_subset_ball
      apply hradius_mono
      · apply distribution_antitone
        exact ENNReal.coe_le_coe.mpr
          (Real.toNNReal_mono (Rat.cast_le.mpr hba))
      · exact hfinite _ (hpos b)
  change volume (⋃ q : ℚ, ⋃ (hq : 0 ≤ q ∧ t < Real.toNNReal q),
    s ⟨q, hq⟩) = _
  rw [← Set.iUnion_subtype (fun q : ℚ => 0 ≤ q ∧ t < Real.toNNReal q) s]
  rw [hdir.measure_iUnion]
  calc
    (⨆ q : {q : ℚ // 0 ≤ q ∧ t < Real.toNNReal q}, volume (s q)) =
        ⨆ q : {q : ℚ // 0 ≤ q ∧ t < Real.toNNReal q},
          distribution f (Real.toNNReal q.1) := by
      apply iSup_congr
      intro q
      exact hradius_volume _ (hfinite _ (hpos q))
    _ = ⨆ q : ℚ, ⨆ (_ : 0 ≤ q ∧ t < Real.toNNReal q),
        distribution f (Real.toNNReal q) := by
      rw [iSup_subtype']
    _ = distribution f t := (distribution_iSup_rat_gt f t).symm

/-- Placeholder-free closure of the exact frozen Schwarz rearrangement root
by the rational-level centered-ball construction. -/
theorem schwarzRearrangementTarget_proof : SchwarzRearrangementTarget := by
  intro n hn f _hf hfinite
  let radius : ENNReal → ℝ := radiusForVolume hn
  let fstar : Euclidean n → ENNReal :=
    fun x => starProfile radius f ‖x‖
  refine ⟨fstar, ?_, ?_, ?_, ?_⟩
  · exact measurable_profile (starProfile radius f)
      (starProfile_measurable radius f)
  · exact isRadial_profile (starProfile radius f)
  · exact isRadiallyNonincreasing_profile (starProfile radius f)
      (starProfile_antitone radius f)
  · intro t ht
    change volume {x : Euclidean n | t < starProfile radius f ‖x‖} = _
    rw [measure_strictSuperlevel_starProfile radius f]
    · rfl
    · intro u hu
      exact hfinite u hu
    · intro a b hab hbtop
      exact radiusForVolume_mono hn hbtop hab
    · intro a hatop
      exact volume_ball_radiusForVolume hn a hatop
    · exact ht

#print axioms isRadial_profile
#print axioms isRadiallyNonincreasing_profile
#print axioms measurable_profile
#print axioms distribution_antitone
#print axioms iUnion_strictSuperlevel_gt
#print axioms distribution_iSup_rat_gt
#print axioms volume_ball_radiusForVolume
#print axioms radiusForVolume_mono
#print axioms starProfile_measurable
#print axioms starProfile_antitone
#print axioms strictSuperlevel_starProfile
#print axioms measure_strictSuperlevel_starProfile
#print axioms schwarzRearrangementTarget_proof

end Stage1Instances.THM_M_1285
