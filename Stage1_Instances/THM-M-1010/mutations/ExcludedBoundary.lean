import «Stage1_Instances».«THM-M-1010».Statement

open MeasureTheory

universe u

namespace Stage1Instances.THM_M_1010.Mutations

def ExcludingConstantCase
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] : Prop :=
  forall (muSeq : Nat -> ProbabilityMeasure S) (mu : ProbabilityMeasure S),
    Not (muSeq 0 = mu) ->
    WeakConvergence muSeq mu -> Nonempty (Representation S muSeq mu)

-- Expected failure: adding a disequality excludes constant sequences from the root.
example (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] :
    Target S <-> ExcludingConstantCase S := Iff.rfl

end Stage1Instances.THM_M_1010.Mutations
