import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# THM-M-1014 canonical statement

This module freezes the everywhere-continuous pushforward form of the continuous mapping theorem.
It declares proposition-valued statement and mutation probes; it does not prove the proposition.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1014

universe u v w

/-- Weak convergence of probability measures is preserved by pushforward along a continuous map. -/
def StatementShape : Prop :=
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

/-- Mutation: replace continuity by measurability, which does not preserve weak convergence. -/
def MutationMeasurableOnly : Prop :=
  forall (alpha : Type u) (beta : Type v)
    [TopologicalSpace alpha] [MeasurableSpace alpha] [OpensMeasurableSpace alpha]
    [TopologicalSpace beta] [MeasurableSpace beta] [BorelSpace beta]
    (iota : Type w) (L : Filter iota)
    (mu_n : iota -> ProbabilityMeasure alpha) (mu : ProbabilityMeasure alpha)
    (f : alpha -> beta) (hf : Measurable f),
    Tendsto mu_n L (nhds mu) ->
    Tendsto (fun n => ProbabilityMeasure.map (mu_n n) hf.aemeasurable)
      L (nhds (ProbabilityMeasure.map mu hf.aemeasurable))

/-- Mutation: reverse the weak-convergence premise. -/
def MutationReversedPremise : Prop :=
  forall (alpha : Type u) (beta : Type v)
    [TopologicalSpace alpha] [MeasurableSpace alpha] [OpensMeasurableSpace alpha]
    [TopologicalSpace beta] [MeasurableSpace beta] [BorelSpace beta]
    (iota : Type w) (L : Filter iota) (n0 : iota)
    (mu_n : iota -> ProbabilityMeasure alpha) (mu : ProbabilityMeasure alpha)
    (f : alpha -> beta) (hf : Continuous f),
    Tendsto (fun _ => mu) L (nhds (mu_n n0)) ->
    Tendsto
      (fun n => ProbabilityMeasure.map (mu_n n) hf.measurable.aemeasurable)
      L (nhds (ProbabilityMeasure.map mu hf.measurable.aemeasurable))

/-- Mutation: use an unrelated constant limiting pushforward. -/
def MutationConstantLimit : Prop :=
  forall (alpha : Type u) (beta : Type v)
    [TopologicalSpace alpha] [MeasurableSpace alpha] [OpensMeasurableSpace alpha]
    [TopologicalSpace beta] [MeasurableSpace beta] [BorelSpace beta]
    (iota : Type w) (L : Filter iota)
    (mu_n : iota -> ProbabilityMeasure alpha) (mu rho : ProbabilityMeasure alpha)
    (f : alpha -> beta) (hf : Continuous f),
    Tendsto mu_n L (nhds mu) ->
    Tendsto
      (fun n => ProbabilityMeasure.map (mu_n n) hf.measurable.aemeasurable)
      L (nhds (ProbabilityMeasure.map rho hf.measurable.aemeasurable))

#check StatementShape
#print StatementShape
#print MutationMeasurableOnly
#print MutationReversedPremise
#print MutationConstantLimit

end Stage1Instances.THM_M_1014
