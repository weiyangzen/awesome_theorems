import Mathlib.Topology.Metrizable.Basic
import Mathlib.Topology.Separation.Regular

/-!
# THM-M-0625 discovery-only intake probe

These checks authenticate the pinned APIs for regularity, ordinary normality,
pairwise-disjoint indexed families, and metrizability. They do not define
collectionwise normality or a Moore/developable space, select a canonical target,
or prove a Bing metrization theorem.
-/

#check RegularSpace
#check NormalSpace
#check normal_separation
#check Set.PairwiseDisjoint
#check TopologicalSpace.PseudoMetrizableSpace
#check TopologicalSpace.MetrizableSpace
