import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.EdgeLabeling
import Mathlib.Combinatorics.SimpleGraph.LineGraph

/-!
# THM-M-0905 discovery-only intake probe

These checks authenticate generic pinned ordinary-coloring, bipartite, edge-labeling, and line-graph
APIs adjacent to a possible future statement. They do not model a multigraph with parallel-edge
identity, lists of allowed colors, proper list edge coloring, edge-choosability, a canonical target,
or Galvin's proof.
-/

#check SimpleGraph.Coloring
#check SimpleGraph.Colorable
#check SimpleGraph.IsBipartite
#check SimpleGraph.IsBipartiteWith
#check SimpleGraph.EdgeLabeling
#check SimpleGraph.EdgeLabeling.labelGraph
#check SimpleGraph.lineGraph
#check SimpleGraph.lineGraph_adj_iff_exists
