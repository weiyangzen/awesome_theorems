import Mathlib.Combinatorics.Graph.Subgraph
import Mathlib.Combinatorics.SimpleGraph.EdgeLabeling

/-!
# THM-M-0860 discovery-only intake probe

These checks authenticate pinned multigraph-incidence and adjacent simple-graph interfaces. They do
not define a proper multigraph edge colouring or chromatic index, select Shannon's exact statement,
or prove any form of Shannon's theorem.
-/

#check Graph
#check Graph.IsLink
#check Graph.Inc
#check Graph.IsLoopAt
#check Graph.IsNonloopAt
#check Graph.Adj
#check Graph.IsSubgraph
#check SimpleGraph.EdgeLabeling
#check SimpleGraph.degree
#check SimpleGraph.maxDegree
