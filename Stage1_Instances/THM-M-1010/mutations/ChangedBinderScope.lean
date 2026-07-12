import «Stage1_Instances».«THM-M-1010».Statement

open Filter MeasureTheory Topology

universe u

namespace Stage1Instances.THM_M_1010.Mutations

def OneLimitForAllSequences
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] : Prop :=
  exists mu : ProbabilityMeasure S,
    forall muSeq : Nat -> ProbabilityMeasure S,
      WeakConvergence muSeq mu -> Nonempty (Representation S muSeq mu)

-- Expected failure: moving the limit law outside existential scope changes the proposition.
example (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] :
    Target S <-> OneLimitForAllSequences S := Iff.rfl

end Stage1Instances.THM_M_1010.Mutations
