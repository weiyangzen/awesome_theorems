import «Stage1_Instances».«THM-M-1083».Vendor.BrownianMotion.Continuity.KolmogorovChentsov
import «Stage1_Instances».«THM-M-1083».Statement

/-!
# THM-M-1083 proof

The terminal Kolmogorov--Chentsov engine is vendored from an immutable BrownianMotion revision.
This module proves the interval covering-number specialization and checks the exact canonical root.
-/

noncomputable section

open MeasureTheory Set Metric
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1083.Proof

universe u

abbrev TimeInterval (T : ℝ) := Set.Icc (0 : ℝ) T
abbrev RealProcess (T : ℝ) (Ω : Type u) := TimeInterval T → Ω → ℝ

/-- The canonical interval has metric covering dimension one. -/
theorem timeInterval_hasBoundedCoveringNumber {T : ℝ} (hT : 0 < T) :
    HasBoundedCoveringNumber (Set.univ : Set (TimeInterval T))
      ((3 : ℝ≥0∞) * ENNReal.ofReal T) 1 := by
  let R : ℝ≥0 := ⟨T, hT.le⟩
  have h_iso : Isometry ((↑) : TimeInterval T → ℝ) := fun _ _ => rfl
  have h_image : ((↑) : TimeInterval T → ℝ) '' Set.univ = Set.Icc 0 T := by
    ext x
    simp only [Set.mem_image, Set.mem_univ, true_and, Set.mem_Icc]
    refine ⟨?_, ?_⟩
    · rintro ⟨y, -, rfl⟩
      exact y.2
    · intro hx
      exact ⟨⟨x, hx⟩, by simp⟩
  have h_diam : Metric.ediam (Set.univ : Set (TimeInterval T)) = ENNReal.ofReal T := by
    rw [← h_iso.ediam_image, h_image, Real.ediam_Icc]
    simp
  constructor
  · rw [h_diam]
    exact ENNReal.ofReal_lt_top
  intro eps heps
  rw [← h_iso.coveringNumber_image' h_iso.injective.injOn, h_image]
  rw [h_diam] at heps
  have hsubset : Set.Icc (0 : ℝ) T ⊆ Metric.closedEBall (T / 2) (R / 2) := by
    intro x hx
    simp only [Metric.mem_closedEBall, edist_dist, Real.dist_eq]
    refine ENNReal.ofReal_le_of_le_toReal ?_
    rw [ENNReal.toReal_div, ENNReal.coe_toReal, ENNReal.toReal_ofNat]
    change |x - T / 2| ≤ T / 2
    exact abs_le.mpr ⟨by linarith [hx.1], by linarith [hx.2]⟩
  calc
    (coveringNumber eps (Set.Icc (0 : ℝ) T) : ℝ≥0∞)
      ≤ coveringNumber (eps / 2) (Metric.closedEBall (T / 2) (R / 2)) := by
        gcongr
        exact coveringNumber_subset_le hsubset
    _ ≤ 3 * (R / 2 : ℝ≥0) / (eps / 2 : ℝ≥0) := by
      have h := coveringNumber_closedBall_le_three_mul (r := R / 2) (ε := eps / 2)
        (x := T / 2) ?_ ?_
      · simp only [ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, ENNReal.coe_div,
          ENNReal.coe_ofNat, Module.finrank_self, pow_one] at h
        rwa [ENNReal.coe_div (by simp), ENNReal.coe_div (by simp)]
      · exact ne_of_gt (by simpa [R] using hT)
      · gcongr
        simpa [ENNReal.ofReal_eq_coe_nnreal hT.le, R] using heps
    _ = 3 * R / eps := by
      conv_lhs => rw [mul_div_assoc]
      conv_rhs => rw [mul_div_assoc]
      congr 1
      simp only [ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, ENNReal.coe_div,
        ENNReal.coe_ofNat]
      simp_rw [div_eq_mul_inv]
      rw [ENNReal.mul_inv (by simp) (by simp), inv_inv, mul_assoc, mul_comm _ (2 : ℝ≥0∞),
        ← mul_assoc _ (2 : ℝ≥0∞), ENNReal.inv_mul_cancel (by simp) (by simp), one_mul]
    _ = (3 : ℝ≥0∞) * R * (eps : ℝ≥0∞)⁻¹ ^ (1 : ℝ) := by
      rw [div_eq_mul_inv, ENNReal.rpow_one]
    _ = (3 : ℝ≥0∞) * ENNReal.ofReal T * (eps : ℝ≥0∞)⁻¹ ^ (1 : ℝ) := by
      rw [ENNReal.ofReal_eq_coe_nnreal hT.le]

/-- The canonical hypotheses form mathlib's Kolmogorov-process substrate. -/
theorem isKolmogorovProcess_of_increment
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω)
    {T alpha beta : ℝ} {C : ℝ≥0} {X : RealProcess T Ω}
    (halpha : 0 < alpha) (hbeta : 0 < beta)
    (hmeas : ∀ t, Measurable (X t))
    (hmoment : ∀ s t,
      ∫⁻ ω, edist (X s ω) (X t ω) ^ alpha ∂P ≤
        (C : ℝ≥0∞) * edist s t ^ (1 + beta)) :
    ProbabilityTheory.IsKolmogorovProcess X P alpha (1 + beta) C := by
  exact ProbabilityTheory.IsKolmogorovProcess.mk_of_secondCountableTopology
    hmeas hmoment halpha (by linarith)

/-- The premise-free proof of the exact frozen proposition. -/
theorem kolmogorovContinuity : Stage1Instances.THM_M_1083.KolmogorovContinuity.{u} := by
  intro Ω _ P _ T alpha beta C X hT halpha hbeta hmeas hmoment
  have hX : ProbabilityTheory.IsKolmogorovProcess X P alpha (1 + beta) C :=
    ProbabilityTheory.IsKolmogorovProcess.mk_of_secondCountableTopology
      hmeas hmoment halpha (by linarith)
  obtain ⟨Y, _hYmeas, hYeq, hYholder⟩ :=
    ProbabilityTheory.exists_modification_holder
      (p := alpha) (q := 1 + beta) (d := (1 : ℝ))
      (timeInterval_hasBoundedCoveringNumber hT) isOpen_univ
      hX.IsAEKolmogorovProcess
      (by
        exact ENNReal.mul_ne_top (by norm_num)
          ENNReal.ofReal_ne_top)
      (by norm_num) (by linarith)
  refine ⟨Y, ?_, ?_⟩
  · intro t
    exact (hYeq t (Set.mem_univ t)).symm
  · intro gamma hgamma hgamma_lt
    filter_upwards [] with omega
    obtain ⟨K, hK⟩ := hYholder gamma hgamma (by simpa using hgamma_lt) omega
    exact ⟨K, holderOnWith_univ.mp hK⟩

/-- Direct exact-type bridge to the public canonical statement declaration. -/
theorem canonicalProof : Stage1Instances.THM_M_1083.Statement.{u} := by
  exact kolmogorovContinuity

#print axioms timeInterval_hasBoundedCoveringNumber
#print axioms isKolmogorovProcess_of_increment
#print axioms kolmogorovContinuity
#print axioms canonicalProof

end Stage1Instances.THM_M_1083.Proof
