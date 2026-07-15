import Statement

/-!
# THM-M-1070 proof execution

This module implements the exact conjunction assembly frozen by the obligation tree. It does not
assert that an arbitrary process is a Levy process: each substantive process clause remains an
explicit premise because the canonical target is a predicate with no particular process data.
-/

open Filter MeasureTheory Set
open scoped BigOperators NNReal Topology

namespace Stage1Instances.THM_M_1070

open ProbabilityTheory

/-- A family of constant random variables is jointly independent under a probability measure. -/
private theorem iIndepFun_const {I Omega E : Type*} [MeasurableSpace Omega]
    [MeasurableSpace E] (P : Measure Omega) (hP : IsProbabilityMeasure P) (c : I -> E) :
    iIndepFun (fun i (_ : Omega) => c i) P := by
  letI : IsProbabilityMeasure P := hP
  rw [iIndepFun_iff]
  intro S f hf
  have htriv : forall i, i ∈ S -> f i = ∅ ∨ f i = Set.univ := by
    intro i hi
    have hm := hf i hi
    rw [MeasurableSpace.comap_const (c i)] at hm
    exact MeasurableSpace.measurableSet_bot_iff.mp hm
  by_cases hempty : exists i, i ∈ S ∧ f i = ∅
  · obtain ⟨i, hi, hfi⟩ := hempty
    have hinter : (⋂ j ∈ S, f j) = ∅ := by
      rw [Set.eq_empty_iff_forall_notMem]
      intro x hx
      have hxi : x ∈ f i := Set.mem_iInter₂.mp hx i hi
      simp [hfi] at hxi
    rw [hinter, measure_empty]
    exact (Finset.prod_eq_zero hi (by simp [hfi])).symm
  · have hnot : forall i, i ∈ S -> f i ≠ ∅ := by
      intro i hi hfi
      exact hempty ⟨i, hi, hfi⟩
    have hfuniv : forall i, i ∈ S -> f i = Set.univ := by
      intro i hi
      rcases htriv i hi with hi0 | hiU
      · exact (hnot i hi hi0).elim
      · exact hiU
    have hinter : (⋂ j ∈ S, f j) = Set.univ := by
      rw [Set.eq_univ_iff_forall]
      intro x
      rw [Set.mem_iInter₂]
      intro j hj
      simp [hfuniv j hj]
    rw [hinter, measure_univ]
    have hprod : ∏ j ∈ S, P (f j) = 1 := by
      apply Finset.prod_eq_one
      intro j hj
      simp [hfuniv j hj]
    exact hprod.symm

/-- Placeholder-free child-to-parent composition for the six clauses of the frozen predicate. -/
theorem isLevyProcess_of_clauses {Omega : Type*} [MeasurableSpace Omega]
    (P : Measure Omega) (X : NNReal -> Omega -> Real)
    (hP : IsProbabilityMeasure P)
    (hmeasurable : forall t, AEMeasurable (X t) P)
    (hzero : X 0 =ᵐ[P] 0)
    (hindependent : HasIndepIncrements X P)
    (hstationary : forall s t, IdentDistrib (X (s + t) - X s) (X t) P P)
    (hcontinuous : forall t, TendstoInMeasure P X (nhds t) (X t)) :
    IsLevyProcess P X := by
  exact ⟨hP, hmeasurable, hzero, hindependent, hstationary, hcontinuous⟩

/-- Exact elimination back to the six registered children; this checks that assembly neither
strengthens nor weakens the frozen predicate. -/
theorem clauses_of_isLevyProcess {Omega : Type*} [MeasurableSpace Omega]
    (P : Measure Omega) (X : NNReal -> Omega -> Real)
    (h : IsLevyProcess P X) :
    IsProbabilityMeasure P /\
      (forall t, AEMeasurable (X t) P) /\
      X 0 =ᵐ[P] 0 /\
      HasIndepIncrements X P /\
      (forall s t, IdentDistrib (X (s + t) - X s) (X t) P P) /\
      forall t, TendstoInMeasure P X (nhds t) (X t) := by
  exact h

/-- The zero process is a concrete Levy process on every supplied probability space. This is an
unregistered existence witness; it does not close the frozen arbitrary-`P`, arbitrary-`X` root. -/
theorem isLevyProcess_zero {Omega : Type*} [MeasurableSpace Omega]
    (P : Measure Omega) (hP : IsProbabilityMeasure P) :
    IsLevyProcess P (fun (_ : NNReal) (_ : Omega) => (0 : Real)) := by
  let X : NNReal -> Omega -> Real := fun _ _ => 0
  refine ⟨hP, ?_, ?_, ?_, ?_, ?_⟩
  · intro t
    exact aemeasurable_const
  · exact Filter.Eventually.of_forall (fun _ => rfl)
  · intro n t ht
    convert iIndepFun_const P hP (fun (_ : Fin n) => (0 : Real)) with i omega
    simp
  · intro s t
    simpa using (IdentDistrib.refl (μ := P) (f := fun (_ : Omega) => (0 : Real))
      aemeasurable_const)
  · intro t eps heps
    change Tendsto (fun _ : NNReal => P {omega | eps ≤ edist (0 : Real) 0})
      (nhds t) (nhds 0)
    have hset : {omega : Omega | eps ≤ edist (0 : Real) 0} = ∅ := by
      ext omega
      simp [not_le.mpr heps]
    rw [hset]
    simp only [measure_empty]
    exact (tendsto_const_nhds : Tendsto (fun _ : NNReal => (0 : ENNReal))
      (nhds t) (nhds 0))

/-- The zero measure gives a checked countermodel to any attempted theorem claiming that the
frozen predicate holds for arbitrary `P` and `X`. This is blocker evidence, not a replacement for
the open semantic clauses. -/
theorem zeroMeasure_not_isLevyProcess {Omega : Type*} [MeasurableSpace Omega]
    (X : NNReal -> Omega -> Real) : Not (IsLevyProcess (0 : Measure Omega) X) := by
  intro h
  have hone : (0 : Measure Omega) Set.univ = 1 := h.1.measure_univ
  have hzero : (0 : Measure Omega) Set.univ = 0 := rfl
  exact zero_ne_one (hzero.symm.trans hone)

#print axioms isLevyProcess_of_clauses
#print axioms clauses_of_isLevyProcess
#print axioms isLevyProcess_zero
#print axioms zeroMeasure_not_isLevyProcess

end Stage1Instances.THM_M_1070
