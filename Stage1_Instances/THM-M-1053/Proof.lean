import ObligationTree

/-!
# THM-M-1053 proof-phase consistency check

The frozen `ErgodicLimitIdentificationPackage` is stronger than the required
ergodic identification: it asserts that *every* integrable invariant `g` is
the integral of an unrelated integrable `f`.  The theorem below gives a
kernel-checked counterexample on the one-point probability space.  Therefore
that frozen child obligation cannot receive a proof body as stated.
-/

open Function MeasureTheory

namespace Stage1.THM_M_1053

/-- The identity map on a one-point probability space is ergodic. -/
private theorem ergodic_id_punit :
    Ergodic (id : PUnit -> PUnit) (Measure.dirac PUnit.unit) := by
  refine ⟨MeasurePreserving.id _, ?_⟩
  constructor
  intro s _hs _hinv
  rw [Filter.eventuallyConst_set', ae_dirac_eq]
  by_cases h : PUnit.unit ∈ s
  · refine Or.inr ?_
    rw [Filter.EventuallyEq, Filter.eventually_pure]
    apply propext
    exact iff_true_intro h
  · refine Or.inl ?_
    rw [Filter.EventuallyEq, Filter.eventually_pure]
    apply propext
    exact iff_false_intro h

/-- Formal obstruction to closing the frozen identification package. -/
theorem not_ergodicLimitIdentificationPackage :
    ¬ ErgodicLimitIdentificationPackage.{0} := by
  intro identify
  let mu : Measure PUnit := Measure.dirac PUnit.unit
  haveI : IsProbabilityMeasure mu := inferInstance
  have h := identify PUnit inferInstance mu inferInstance id
    (MeasurePreserving.id mu) (fun _ => 0) (fun _ => 1)
    (by fun_prop) (by fun_prop) (by simp) ergodic_id_punit
  simpa [mu, ae_dirac_eq] using h

#print axioms not_ergodicLimitIdentificationPackage

end Stage1.THM_M_1053
