import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.Hall
import Mathlib.Combinatorics.SimpleGraph.Matching
import Mathlib.Combinatorics.SimpleGraph.VertexCover

/-! Discovery-only API checks for a later exact Konig theorem statement. -/

#check SimpleGraph.IsBipartite
#check SimpleGraph.IsBipartiteWith
#check SimpleGraph.Subgraph.IsMatching
#check SimpleGraph.IsVertexCover
#check SimpleGraph.vertexCoverNum
#check SimpleGraph.vertexCoverNum_exists
#check SimpleGraph.Subgraph.IsMatching.toEdge
#check SimpleGraph.Subgraph.IsMatching.toEdge.surjective
#check SimpleGraph.exists_isMatching_of_forall_ncard_le
