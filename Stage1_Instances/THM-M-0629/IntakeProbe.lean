import Mathlib.Topology.Compactification.OnePoint.Basic

/-!
# THM-M-0629 discovery-only intake probe

These commands authenticate the pinned one-point-extension carrier, canonical embedding,
compactness, separation, density, and uniqueness interfaces. They do not choose the catalog's
exact compactification bundle, establish source-statement identity, or prove this target.
-/

#check OnePoint
#check OnePoint.infty
#check OnePoint.compl_range_coe
#check OnePoint.isOpenEmbedding_coe
#check OnePoint.denseRange_coe
#check OnePoint.isDenseEmbedding_coe
#check OnePoint.equivOfIsEmbeddingOfRangeEq

example (X : Type*) [TopologicalSpace X] : CompactSpace (OnePoint X) := inferInstance

example (X : Type*) [TopologicalSpace X] [WeaklyLocallyCompactSpace X] [T2Space X] :
    T4Space (OnePoint X) := inferInstance

#print axioms OnePoint.compl_range_coe
#print axioms OnePoint.isOpenEmbedding_coe
#print axioms OnePoint.denseRange_coe
#print axioms OnePoint.equivOfIsEmbeddingOfRangeEq
