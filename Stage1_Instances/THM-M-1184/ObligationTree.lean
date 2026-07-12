import Statement

/-!
# THM-M-1184 conditional obligation composition

This module checks the final composition interface of the frozen architecture.
The two inequality packages remain explicit premises; no duality proof is
asserted here.
-/

noncomputable section

open MeasureTheory Set

namespace Stage1Instances.THM_M_1184

universe u v

/-- The weak-duality half, uniformly over the exact canonical context. -/
def WeakDualityPackage : Prop :=
  forall (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
    (c : X × Y -> Real), Continuous c ->
      sSup (range (DualValue mu nu c)) <=
        sInf (range (PrimalValue (mu := mu) (nu := nu) c))

/-- The strong-duality half, uniformly over the exact canonical context. -/
def ReverseDualityPackage : Prop :=
  forall (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
    (c : X × Y -> Real), Continuous c ->
      sInf (range (PrimalValue (mu := mu) (nu := nu) c)) <=
        sSup (range (DualValue mu nu c))

/-- Checked conditional composition into the exact canonical root. -/
theorem root_of_duality_packages
    (weak : WeakDualityPackage.{u, v})
    (reverse : ReverseDualityPackage.{u, v}) :
    KantorovichDualityTarget.{u, v} := by
  intro X Y _ _ _ _ _ _ _ _ mu nu c hc
  exact le_antisymm (reverse X Y mu nu c hc) (weak X Y mu nu c hc)

#print axioms root_of_duality_packages

end Stage1Instances.THM_M_1184
