import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

import «Stage1_Instances».«THM-M-1520».Statement

open MeasureTheory

namespace Stage1.THM_M_1520

def PositiveDimensionOnly : Prop :=
  forall (n : Nat), 0 < n -> forall (H : PhaseSpace n -> Real)
      (Phi : Real -> PhaseSpace n -> PhaseSpace n),
    ContDiff Real 2 H ->
    (forall z, ContDiff Real 1 (fun t => Phi t z)) ->
    (forall t z, HasDerivAt (fun s => Phi s z) (hamiltonianVectorField H (Phi t z)) t) ->
    (forall z, Phi 0 z = z) ->
    (forall s t z, Phi (s + t) z = Phi s (Phi t z)) ->
    forall t, MeasurePreserving (Phi t) volume volume

example : PositiveDimensionOnly = LiouvilleStatement := rfl

end Stage1.THM_M_1520
