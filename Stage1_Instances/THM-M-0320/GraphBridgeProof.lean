import ObligationTree

/-!
# THM-M-0320 graph-bridge proof

This module checks the upper-hemicontinuity-to-closed-graph obligation against
the frozen interfaces in `ObligationTree`. The closed-graph Kakutani core
remains outside the pinned dependency closure, so this module deliberately
does not declare the root theorem.
-/

namespace Stage1Instances.THM_M_0320

open Filter Set

/-- Upper hemicontinuity on the closed domain, together with closed values,
makes the ambient correspondence graph closed. -/
theorem upperHemicontinuityClosedGraphBridge :
    UpperHemicontinuityClosedGraphBridge := by
  intro n K F hK hF hupper
  apply IsSeqClosed.isClosed
  intro u p hu hp
  have hx_tendsto : Tendsto (fun i => (u i).1) atTop (nhds p.1) :=
    (continuous_fst.tendsto p).comp hp
  have hy_tendsto : Tendsto (fun i => (u i).2) atTop (nhds p.2) :=
    (continuous_snd.tendsto p).comp hp
  have hx_mem : p.1 ∈ K :=
    hK.mem_of_tendsto hx_tendsto (Eventually.of_forall fun i => (hu i).1)
  have hsubtype_tendsto :
      Tendsto (fun i => (⟨(u i).1, (hu i).1⟩ : K)) atTop (nhds ⟨p.1, hx_mem⟩) :=
    tendsto_subtype_rng.mpr hx_tendsto
  have hupper_restrict : UpperHemicontinuous (K.restrict F) :=
    upperHemicontinuousOn_iff_restrict.mpr hupper
  refine ⟨hx_mem, ?_⟩
  exact (hupper_restrict.upperHemicontinuousAt ⟨p.1, hx_mem⟩).mem_of_tendsto
    (hF p.1 hx_mem) hsubtype_tendsto
    (Frequently.of_forall fun i => (hu i).2) hy_tendsto

#print axioms upperHemicontinuityClosedGraphBridge

end Stage1Instances.THM_M_0320
