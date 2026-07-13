import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.EdgeLabeling
import Mathlib.Combinatorics.SimpleGraph.LineGraph

/-!
# THM-M-0861 discovery-only intake probe

These checks authenticate the pinned multigraph incidence representation and adjacent simple-graph
APIs for bipartiteness, line-graph coloring, maximum degree, and arbitrary edge labels. They do not
define the required multigraph bipartiteness, degree, proper edge coloring, or chromatic index, and
they neither select nor prove König's edge-coloring theorem.
-/

#check Graph
#check Graph.IsLink
#check Graph.Inc
#check Graph.incidenceSet
#check SimpleGraph.IsBipartite
#check SimpleGraph.IsBipartiteWith
#check SimpleGraph.lineGraph
#check SimpleGraph.lineGraph_adj_iff_exists
#check SimpleGraph.Coloring
#check SimpleGraph.Colorable
#check SimpleGraph.chromaticNumber
#check SimpleGraph.maxDegree
#check SimpleGraph.degree_le_maxDegree
#check SimpleGraph.EdgeLabeling

#print axioms SimpleGraph.lineGraph_adj_iff_exists
#print axioms SimpleGraph.degree_le_maxDegree
