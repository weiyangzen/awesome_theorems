import Statement

/-!
# THM-M-1015 independent validation probe

This module checks the exact frozen four-branch target without importing `Proof.lean` or
`ObligationTree.lean`. The quotient argument is reconstructed independently in this module.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped Topology ProbabilityTheory

namespace Stage1Instances.THM_M_1015.Validation

open Stage1Instances.THM_M_1015

universe u v w

variable {iota : Type u} {Omega : Type v} {OmegaL : Type w}
  [MeasurableSpace Omega] [MeasurableSpace OmegaL]
  (mu : Measure Omega) [IsProbabilityMeasure mu]
  (muL : Measure OmegaL) [IsProbabilityMeasure muL]
  (l : Filter iota) [l.IsCountablyGenerated]
  (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real)

private theorem inv_const
    (hc : c ≠ 0)
    (hY : TendstoInMeasure mu Y l (fun _ : Omega => c)) :
    TendstoInMeasure mu (fun n omega => (Y n omega)⁻¹) l (fun _ : Omega => c⁻¹) := by
  rw [tendstoInMeasure_iff_dist] at hY ⊢
  intro epsilon hepsilon
  have hnear : ∀ᶠ y in nhds c, dist y⁻¹ c⁻¹ < epsilon :=
    (continuousAt_inv₀ hc) (Metric.ball_mem_nhds c⁻¹ hepsilon)
  rcases Metric.mem_nhds_iff.1 hnear with ⟨delta, hdelta, hball⟩
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds
    (hY delta hdelta) (fun _ => zero_le _) ?_
  intro n
  apply measure_mono
  intro omega hbad
  by_contra hnot
  have hy : Y n omega ∈ Metric.ball c delta := by
    simpa [Metric.mem_ball, not_le] using hnot
  have hlt : dist (Y n omega)⁻¹ c⁻¹ < epsilon := hball hy
  exact (not_lt_of_ge hbad) hlt

/-- Independently reconstructed proof of the exact imported target. -/
theorem independent_root : Stage1Instances.THM_M_1015.Statement.{u, v, w} := by
  intro iota Omega OmegaL _ _ mu _ muL _ l _ X Y Z c hXZ hY hYmeas
  refine ⟨hXZ.prodMk_of_tendstoInMeasure_const X Y Z hY hYmeas,
    hXZ.add_of_tendstoInMeasure_const hY hYmeas, ?_, ?_⟩
  · exact hXZ.continuous_comp_prodMk_of_tendstoInMeasure_const
      (g := fun p : Real × Real => p.1 * p.2) (by fun_prop) hY hYmeas
  · intro hc
    have hc' : c ≠ 0 := by simpa using hc
    have hInv := inv_const mu l Y c hc' hY
    have hInvMeas : forall n, AEMeasurable (fun omega => (Y n omega)⁻¹) mu :=
      fun n => measurable_inv.aemeasurable.comp_aemeasurable (hYmeas n)
    simpa [div_eq_mul_inv] using
      hXZ.continuous_comp_prodMk_of_tendstoInMeasure_const
        (g := fun p : Real × Real => p.1 * p.2) (by fun_prop) hInv hInvMeas

#print axioms independent_root

end Stage1Instances.THM_M_1015.Validation
