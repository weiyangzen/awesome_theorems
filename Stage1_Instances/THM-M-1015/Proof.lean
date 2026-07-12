import Statement

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped Topology ProbabilityTheory

namespace Stage1Instances.THM_M_1015.Proof

open Stage1Instances.THM_M_1015

universe u v w

variable {iota : Type u} {Omega : Type v} {OmegaL : Type w}
  [MeasurableSpace Omega] [MeasurableSpace OmegaL]
  (mu : Measure Omega) [IsProbabilityMeasure mu]
  (muL : Measure OmegaL) [IsProbabilityMeasure muL]
  (l : Filter iota) [l.IsCountablyGenerated]
  (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real)

/-- Inversion preserves convergence in measure when the constant limit is nonzero. -/
theorem tendstoInMeasure_inv_const (hc : c ≠ 0)
    (hY : TendstoInMeasure mu Y l (fun _ : Omega => c)) :
    TendstoInMeasure mu (fun n omega => (Y n omega)⁻¹) l (fun _ : Omega => c⁻¹) := by
  rw [tendstoInMeasure_iff_dist] at hY ⊢
  intro epsilon hepsilon
  have h_event : ∀ᶠ y in nhds c, dist y⁻¹ c⁻¹ < epsilon :=
    (continuousAt_inv₀ hc) (Metric.ball_mem_nhds c⁻¹ hepsilon)
  rcases Metric.mem_nhds_iff.1 h_event with ⟨delta, hdelta, hball⟩
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds
    (hY delta hdelta) (fun _ => zero_le _) ?_
  intro n
  apply measure_mono
  intro omega homega
  by_contra hnot
  have hy : Y n omega ∈ Metric.ball c delta := by
    simpa [Metric.mem_ball, not_le] using hnot
  have hlt : dist (Y n omega)⁻¹ c⁻¹ < epsilon := hball hy
  exact (not_lt_of_ge homega) hlt

/-- Exact four-branch real Slutsky package, including division for a nonzero constant. -/
theorem slutsky_real
    (hXZ : TendstoInDistribution X l Z (fun _ : iota => mu) muL)
    (hY : TendstoInMeasure mu Y l (fun _ : Omega => c))
    (hYmeas : forall n, AEMeasurable (Y n) mu) :
    SlutskyConclusions mu muL l X Y Z c := by
  refine ⟨hXZ.prodMk_of_tendstoInMeasure_const X Y Z hY hYmeas,
    hXZ.add_of_tendstoInMeasure_const hY hYmeas, ?_, ?_⟩
  · exact hXZ.continuous_comp_prodMk_of_tendstoInMeasure_const
      (g := fun p : Real × Real => p.1 * p.2) (by fun_prop) hY hYmeas
  · intro hc
    have hc' : c ≠ 0 := by simpa using hc
    have hInv := tendstoInMeasure_inv_const mu l Y c hc' hY
    have hInvMeas : forall n, AEMeasurable (fun omega => (Y n omega)⁻¹) mu :=
      fun n => (measurable_inv.aemeasurable.comp_aemeasurable (hYmeas n))
    simpa [div_eq_mul_inv] using
      hXZ.continuous_comp_prodMk_of_tendstoInMeasure_const
        (g := fun p : Real × Real => p.1 * p.2) (by fun_prop) hInv hInvMeas

/-- Unconditional closure of the exact frozen proposition. -/
theorem statement_proof : Stage1Instances.THM_M_1015.Statement.{u, v, w} := by
  intro iota Omega OmegaL _ _ mu _ muL _ l _ X Y Z c hXZ hY hYmeas
  exact slutsky_real mu muL l X Y Z c hXZ hY hYmeas

#print axioms tendstoInMeasure_inv_const
#print axioms slutsky_real
#print axioms statement_proof

end Stage1Instances.THM_M_1015.Proof
