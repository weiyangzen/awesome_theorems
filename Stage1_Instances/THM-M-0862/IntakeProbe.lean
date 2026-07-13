import Mathlib.Combinatorics.SimpleGraph.Connectivity.EdgeConnectivity
import Mathlib.Combinatorics.SimpleGraph.Maps

/-!
# THM-M-0862 discovery-only intake probe

These checks authenticate adjacent path, reachability, induced-graph, and edge-connectivity APIs in
the pinned mathlib snapshot. They do not select a Menger variant, define vertex connectivity or a
vertex separator, construct a path packing, establish source identity, or credit a proof body.
-/

#check SimpleGraph.Path
#check SimpleGraph.Walk.IsPath
#check SimpleGraph.Reachable
#check SimpleGraph.Reachable.exists_isPath
#check SimpleGraph.induce
#check SimpleGraph.IsEdgeReachable
#check SimpleGraph.IsEdgeConnected
#check SimpleGraph.Walk.IsPath.disjoint_support_of_append
