import Mathlib.MeasureTheory.Measure.LevyConvergence
import Mathlib.MeasureTheory.Measure.Portmanteau
import Statement

/-!
# THM-M-1018 proof-phase lemmas

This module implements checked endpoint sublemmas from the frozen Levy
inversion architecture. The sharp Dirichlet limit and its composition into
the canonical root remain open.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1018.Proof

/-- The two endpoint hypotheses make the frontier of `(a,b]` null. -/
theorem frontier_Ioc_null
    (mu : Measure Real) [IsProbabilityMeasure mu] {a b : Real}
    (hab : a < b) (ha : mu {a} = 0) (hb : mu {b} = 0) :
    mu (frontier (Set.Ioc a b)) = 0 := by
  rw [frontier_Ioc hab]
  rw [pair_comm]
  simpa using (measure_union_null ha hb)

/-- Portmanteau specialized to the exact half-open interval in the root. -/
theorem tendsto_Ioc_mass_of_tendsto
    {iota : Type*} {l : Filter iota}
    (mu : Measure Real) [IsProbabilityMeasure mu]
    (mus : iota -> ProbabilityMeasure Real)
    (hmu : Tendsto mus l (nhds (show ProbabilityMeasure Real from ⟨mu, inferInstance⟩)))
    {a b : Real} (hab : a < b) (ha : mu {a} = 0) (hb : mu {b} = 0) :
    Tendsto (fun i => ((mus i : Measure Real) (Set.Ioc a b))) l
      (nhds (mu (Set.Ioc a b))) := by
  exact ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto'
    hmu (frontier_Ioc_null mu hab ha hb)

/-- Endpoint-null conversion from the closed interval to the frozen
half-open interval. -/
theorem measureReal_Icc_eq_Ioc
    (mu : Measure Real) [IsProbabilityMeasure mu] {a b : Real}
    (ha : mu {a} = 0) :
    mu.real (Set.Icc a b) = mu.real (Set.Ioc a b) := by
  rw [← Set.Icc_diff_left]
  symm
  exact measureReal_diff_null ((measureReal_eq_zero_iff).2 ha)

/-- Endpoint-null conversion from the open interval to the frozen half-open
interval. -/
theorem measureReal_Ioo_eq_Ioc
    (mu : Measure Real) [IsProbabilityMeasure mu] {a b : Real}
    (hb : mu {b} = 0) :
    mu.real (Set.Ioo a b) = mu.real (Set.Ioc a b) := by
  rw [← Set.Ioc_diff_right]
  exact measureReal_diff_null ((measureReal_eq_zero_iff).2 hb)

/-- An exact weak-convergence construction supplies convergence of the
selected interval mass. -/
theorem interval_mass_of_weak_limit
    {iota : Type*} {l : Filter iota}
    (mu : Measure Real) [IsProbabilityMeasure mu]
    (mus : iota -> ProbabilityMeasure Real)
    (hmu : Tendsto mus l (nhds (show ProbabilityMeasure Real from ⟨mu, inferInstance⟩)))
    {a b : Real} (hab : a < b) (ha : mu {a} = 0) (hb : mu {b} = 0) :
    Tendsto (fun i => (((mus i : Measure Real) (Set.Ioc a b)).toReal : Complex)) l
      (nhds (((mu (Set.Ioc a b)).toReal : Real) : Complex)) := by
  exact (Complex.continuous_ofReal.continuousAt.tendsto.comp
    ((ENNReal.tendsto_toReal (by finiteness)).comp
      (tendsto_Ioc_mass_of_tendsto mu mus hmu hab ha hb)))

#print axioms frontier_Ioc_null
#print axioms tendsto_Ioc_mass_of_tendsto
#print axioms measureReal_Icc_eq_Ioc
#print axioms measureReal_Ioo_eq_Ioc
#print axioms interval_mass_of_weak_limit

end Stage1Instances.THM_M_1018.Proof
