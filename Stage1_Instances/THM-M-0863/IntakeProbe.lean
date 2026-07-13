import Mathlib.Combinatorics.SimpleGraph.Connectivity.Subgraph

/-!
# THM-M-0863 discovery-only intake probe

These checks authenticate pinned finite-simple-graph APIs adjacent to a future encoding of
Whitney's ear-construction theorem. They do not define 2-vertex-connectivity or an ear
decomposition, select the canonical target, or prove the theorem.
-/

#check SimpleGraph.Preconnected
#check SimpleGraph.Connected
#check SimpleGraph.Preconnected.exists_isPath
#check SimpleGraph.Walk.IsPath
#check SimpleGraph.Walk.IsCycle
#check SimpleGraph.Walk.toSubgraph
#check SimpleGraph.Walk.connected_induce_support
#check SimpleGraph.Subgraph.induce
#check SimpleGraph.Subgraph.deleteVerts
