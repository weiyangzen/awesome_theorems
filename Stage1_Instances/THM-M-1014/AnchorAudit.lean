import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# THM-M-1014 pinned anchor audit

This module checks the exact probability-measure anchor found in the pinned
mathlib revision. It is evidence for the anchor-audit node; later nodes retain
their own proof, composition, and release gates.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1014.AnchorAudit

universe u v w

/-- An independently elaborated copy of the frozen continuous-mapping target. -/
def AuditedStatementShape : Prop :=
  forall (alpha : Type u) (beta : Type v)
    [TopologicalSpace alpha] [MeasurableSpace alpha] [OpensMeasurableSpace alpha]
    [TopologicalSpace beta] [MeasurableSpace beta] [BorelSpace beta]
    (iota : Type w) (L : Filter iota)
    (mu_n : iota -> ProbabilityMeasure alpha) (mu : ProbabilityMeasure alpha)
    (f : alpha -> beta) (hf : Continuous f),
    Tendsto mu_n L (nhds mu) ->
    Tendsto
      (fun n => ProbabilityMeasure.map (mu_n n) hf.measurable.aemeasurable)
      L (nhds (ProbabilityMeasure.map mu hf.measurable.aemeasurable))

#check ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous
#check ProbabilityMeasure.continuous_map
#check ProbabilityMeasure.tendsto_iff_forall_lintegral_tendsto
#check FiniteMeasure.tendsto_map_of_tendsto_of_continuous

/-- The pinned mathlib theorem has the exact strength of the frozen target. -/
theorem exactTarget_from_pinned_mathlib : AuditedStatementShape.{u, v, w} := by
  intro alpha beta _ _ _ _ _ _ iota L mu_n mu f hf hlim
  exact ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous mu_n mu hlim hf

end Stage1Instances.THM_M_1014.AnchorAudit

#print axioms Stage1Instances.THM_M_1014.AnchorAudit.exactTarget_from_pinned_mathlib
