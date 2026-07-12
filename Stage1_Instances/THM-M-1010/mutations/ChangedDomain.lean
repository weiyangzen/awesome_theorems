import «Stage1_Instances».«THM-M-1010».Statement

open MeasureTheory

universe u

namespace Stage1Instances.THM_M_1010.Mutations

def RealOnly : Prop := Target Real

-- Expected failure: the all-Polish-spaces target is not definitionally the Real-only mutation.
example : (forall (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S], Target S) <-> RealOnly := Iff.rfl

end Stage1Instances.THM_M_1010.Mutations
