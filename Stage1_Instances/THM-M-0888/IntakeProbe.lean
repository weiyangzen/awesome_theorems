import Mathlib.Combinatorics.SimpleGraph.LapMatrix
import Mathlib.Combinatorics.SimpleGraph.Connectivity.EdgeConnectivity

/-!
Discovery-only API checks for a later source-frozen graph Cheeger inequality.

These are adjacent finite-graph, cut, and combinatorial-Laplacian interfaces.
They neither select a Cheeger constant or spectral gap nor state or prove the target.
-/

#check SimpleGraph
#check SimpleGraph.edgeFinset
#check SimpleGraph.neighborFinset
#check SimpleGraph.degree
#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.adjMatrix
#check SimpleGraph.lapMatrix
#check SimpleGraph.lapMatrix_toLinearMap₂'
#check SimpleGraph.posSemidef_lapMatrix
#check SimpleGraph.card_connectedComponent_eq_finrank_ker_toLin'_lapMatrix
#check SimpleGraph.IsEdgeConnected
