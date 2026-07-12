import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# THM-M-1014 independent validation probe

This module deliberately does not import the local statement or proof modules. It independently
reconstructs the exact continuous-mapping root from the pinned mathlib declaration.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1014.Validation

universe u v w

/-- Independently written exact-type kernel probe for the frozen continuous-mapping root. -/
theorem independentContinuousMappingTheorem :
    forall (alpha : Type u) (beta : Type v)
      [TopologicalSpace alpha] [MeasurableSpace alpha] [OpensMeasurableSpace alpha]
      [TopologicalSpace beta] [MeasurableSpace beta] [BorelSpace beta]
      (iota : Type w) (L : Filter iota)
      (mu_n : iota -> ProbabilityMeasure alpha) (mu : ProbabilityMeasure alpha)
      (f : alpha -> beta) (hf : Continuous f),
      Tendsto mu_n L (nhds mu) ->
      Tendsto
        (fun n => ProbabilityMeasure.map (mu_n n) hf.measurable.aemeasurable)
        L (nhds (ProbabilityMeasure.map mu hf.measurable.aemeasurable)) := by
  intro alpha beta _ _ _ _ _ _ iota L mu_n mu f hf hlim
  exact ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous mu_n mu hlim hf

#check ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous
#check independentContinuousMappingTheorem
#print axioms ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous
#print axioms independentContinuousMappingTheorem

end Stage1Instances.THM_M_1014.Validation
