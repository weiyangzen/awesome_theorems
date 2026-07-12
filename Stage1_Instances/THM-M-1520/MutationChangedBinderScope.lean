import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

import «Stage1_Instances».«THM-M-1520».Statement

open MeasureTheory

namespace Stage1.THM_M_1520

def SingleTimeOnly : Prop :=
  forall (n : Nat) (H : PhaseSpace n -> Real) (Phi : Real -> PhaseSpace n -> PhaseSpace n)
      (t : Real),
    ContDiff Real 2 H ->
    (forall z, ContDiff Real 1 (fun u => Phi u z)) ->
    (forall u z, HasDerivAt (fun s => Phi s z) (hamiltonianVectorField H (Phi u z)) u) ->
    (forall z, Phi 0 z = z) ->
    (forall s u z, Phi (s + u) z = Phi s (Phi u z)) ->
    MeasurePreserving (Phi t) volume volume

example : SingleTimeOnly = LiouvilleStatement := rfl

end Stage1.THM_M_1520
