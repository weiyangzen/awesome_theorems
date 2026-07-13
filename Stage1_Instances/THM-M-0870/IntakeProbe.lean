import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Data.Set.Card

/-!
# THM-M-0870 discovery-only intake probe

These checks authenticate pinned simple-graph, tree, induced-graph, and finite-set-cardinality
interfaces adjacent to possible encodings of tree decompositions. They do not define a tree
decomposition or treewidth, select a canonical proposition, or transfer proof credit from mathlib.
-/

namespace Stage1Instances.THM_M_0870

#check SimpleGraph
#check SimpleGraph.Adj
#check SimpleGraph.IsTree
#check SimpleGraph.induce
#check SimpleGraph.Iso.isTree_iff
#check SimpleGraph.Connected.exists_isTree_le
#check Set.ncard
#check Set.ncard_eq_toFinset_card

#print axioms SimpleGraph.Iso.isTree_iff
#print axioms SimpleGraph.Connected.exists_isTree_le

end Stage1Instances.THM_M_0870
