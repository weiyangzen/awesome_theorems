import Statement

/-!
# THM-M-1070 proof execution

This module implements the exact conjunction assembly frozen by the obligation tree. It does not
assert that an arbitrary process is a Levy process: each substantive process clause remains an
explicit premise because the canonical target is a predicate with no particular process data.
-/

open Filter MeasureTheory
open scoped NNReal Topology

namespace Stage1Instances.THM_M_1070

open ProbabilityTheory

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

#print axioms isLevyProcess_of_clauses
#print axioms clauses_of_isLevyProcess

end Stage1Instances.THM_M_1070
