import Statement

/-!
# THM-M-1070 conditional obligation composition

This module checks the child-to-parent composition selected by the frozen architecture. Each
substantive Levy-process clause remains an explicit premise; this is not an existence theorem,
regularization theorem, or proof that an arbitrary process satisfies the predicate.
-/

open Filter MeasureTheory
open scoped NNReal Topology

namespace Stage1Instances.THM_M_1070

open ProbabilityTheory

/-- The exact clause package consumed by the canonical predicate. -/
def LevyProcessComponents {Omega : Type*} [MeasurableSpace Omega] (P : Measure Omega)
    (X : NNReal -> Omega -> Real) : Prop :=
  IsProbabilityMeasure P /\
  (forall t, AEMeasurable (X t) P) /\
  X 0 =ᵐ[P] 0 /\
  HasIndepIncrements X P /\
  (forall s t, IdentDistrib (X (s + t) - X s) (X t) P P) /\
  forall t, TendstoInMeasure P X (nhds t) (X t)

/-- Checked transport from all registered semantic children to the exact canonical target. -/
theorem isLevyProcess_of_components {Omega : Type*} [MeasurableSpace Omega]
    (P : Measure Omega) (X : NNReal -> Omega -> Real)
    (h : LevyProcessComponents P X) : IsLevyProcess P X := by
  exact h

/-- Reverse transport prevents the component package from silently strengthening the target. -/
theorem components_of_isLevyProcess {Omega : Type*} [MeasurableSpace Omega]
    (P : Measure Omega) (X : NNReal -> Omega -> Real)
    (h : IsLevyProcess P X) : LevyProcessComponents P X := by
  exact h

theorem isLevyProcess_iff_components {Omega : Type*} [MeasurableSpace Omega]
    (P : Measure Omega) (X : NNReal -> Omega -> Real) :
    IsLevyProcess P X <-> LevyProcessComponents P X := by
  rfl

#check isLevyProcess_of_components
#check components_of_isLevyProcess
#print axioms isLevyProcess_of_components
#print axioms isLevyProcess_iff_components

end Stage1Instances.THM_M_1070
