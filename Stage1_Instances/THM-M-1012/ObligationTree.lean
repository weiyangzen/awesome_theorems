import Mathlib.MeasureTheory.Measure.LevyConvergence

/-!
# THM-M-1012 obligation composition harness

This module checks the typed interfaces used by the frozen obligation graph.  Its
theorems only compose explicitly supplied child proofs; they do not claim that
the child obligations have been discharged in this phase.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology RealInnerProductSpace

namespace Stage1Instances.THM_M_1012.ObligationTree

universe u

abbrev RootTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E),
      Tendsto mu atTop (nhds mu0) <->
        forall t : E,
          Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
            (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))

abbrev ForwardTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E),
      Tendsto mu atTop (nhds mu0) ->
        forall t : E,
          Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
            (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))

abbrev ReverseTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E),
      (forall t : E,
        Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
          (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))) ->
      Tendsto mu atTop (nhds mu0)

abbrev TightnessTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E),
      (forall t : E,
        Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
          (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))) ->
      IsTightMeasureSet {((mu n : ProbabilityMeasure E) : Measure E) | n}

abbrev WeakFromTightTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E),
      (forall t : E,
        Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
          (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))) ->
      IsTightMeasureSet {((mu n : ProbabilityMeasure E) : Measure E) | n} ->
      Tendsto mu atTop (nhds mu0)

/-- Reverse implication composed from the two exact reverse-direction children. -/
theorem reverse_of_tightness_and_separation
    (tightness : TightnessTarget.{u}) (weakFromTight : WeakFromTightTarget.{u}) :
    ReverseTarget.{u} := by
  intro E _ _ _ _ _ mu mu0 hchar
  exact weakFromTight E mu mu0 hchar (tightness E mu mu0 hchar)

/-- Exact root composition from both directions of the equivalence. -/
theorem root_of_directions (forward : ForwardTarget.{u}) (reverse : ReverseTarget.{u}) :
    RootTarget.{u} := by
  intro E _ _ _ _ _ mu mu0
  exact Iff.intro (forward E mu mu0) (reverse E mu mu0)

#check reverse_of_tightness_and_separation
#check root_of_directions
#print axioms reverse_of_tightness_and_separation
#print axioms root_of_directions

end Stage1Instances.THM_M_1012.ObligationTree
