import «Stage1_Instances».«THM-M-1010».Statement

open MeasureTheory

universe u

-- Expected failure: without BorelSpace, the weak-convergence target is not available.
#check fun (S : Type u) [TopologicalSpace S] [MeasurableSpace S] [PolishSpace S] =>
  Stage1Instances.THM_M_1010.Target S
