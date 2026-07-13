import Mathlib.Combinatorics.SimpleGraph.Connectivity.EdgeConnectivity
import Mathlib.Combinatorics.SimpleGraph.Finite

/-!
# THM-M-0832 discovery-only intake probe

These checks authenticate pinned finite simple-graph, edge, neighborhood, degree, and unweighted
edge-connectivity interfaces. They do not define weighted cuts, graph contraction, maximum-adjacency
search, or the Stoer-Wagner algorithm, and they prove no target theorem.
-/

#check SimpleGraph
#check SimpleGraph.edgeSet
#check SimpleGraph.edgeFinset
#check SimpleGraph.neighborSet
#check SimpleGraph.neighborFinset
#check SimpleGraph.degree
#check SimpleGraph.IsEdgeReachable
#check SimpleGraph.IsEdgeConnected
#check SimpleGraph.isEdgeConnected_one
