import Statement

/-!
# THM-M-1013: proof of the frozen Cramer-Wold target

The forward implication is the continuous mapping theorem.  For the reverse
implication, convergence of the projection along `t` gives convergence of its
characteristic function at frequency one; the projection identity turns this
into pointwise convergence of the vector characteristic functions, to which
the pinned Levy convergence theorem applies.
-/

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1013.Proof

noncomputable section

open Stage1Instances.THM_M_1013

/-- The characteristic function of a scalar projection at frequency one is
the vector characteristic function at the projection coefficient. -/
lemma projection_charFun_one_measure {d : Nat} (mu : Measure (Vector d))
    (t : Vector d) :
    charFun (mu.map (projection t)) 1 = charFun mu t := by
  rw [charFun_apply_real, charFun_apply]
  rw [integral_map ((continuous_projection t).aemeasurable) (by fun_prop)]
  simp [projection]

/-- Frozen forward branch, supplied by the pinned continuous mapping theorem. -/
theorem forward {d : Nat} {mu : Nat -> ProbabilityMeasure (Vector d)}
    {mu0 : ProbabilityMeasure (Vector d)}
    (h : Tendsto mu atTop (nhds mu0)) :
    forall t : Vector d,
      Tendsto
        (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
        atTop
        (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable))) := by
  intro t
  exact ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous
    mu mu0 h (continuous_projection t)

/-- Frozen reverse branch, obtained from the pinned characteristic-function
criterion after checking the scalar/vector projection identity locally. -/
theorem reverse {d : Nat} {mu : Nat -> ProbabilityMeasure (Vector d)}
    {mu0 : ProbabilityMeasure (Vector d)}
    (h : forall t : Vector d,
      Tendsto
        (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
        atTop
        (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable)))) :
    Tendsto mu atTop (nhds mu0) := by
  apply ProbabilityMeasure.tendsto_iff_tendsto_charFun.mpr
  intro t
  have hchar := (ProbabilityMeasure.tendsto_iff_tendsto_charFun.mp (h t)) 1
  simpa only [ProbabilityMeasure.toMeasure_map, projection_charFun_one_measure]
    using hchar

/-- Exact proof of the canonical proposition frozen in `Statement.lean`. -/
theorem cramerWold : StatementShape := by
  intro d mu mu0
  exact ⟨forward, reverse⟩

#print axioms projection_charFun_one_measure
#print axioms forward
#print axioms reverse
#print axioms cramerWold

end

end Stage1Instances.THM_M_1013.Proof
