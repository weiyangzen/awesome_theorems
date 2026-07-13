import Mathlib.Combinatorics.SimpleGraph.Coloring
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.LineGraph

/-!
# THM-M-0859 discovery-only intake probe

These checks authenticate pinned finite-simple-graph APIs adjacent to a future Vizing-theorem
encoding. They do not choose the multigraph or simple theorem, freeze a canonical target, or prove
Vizing's theorem.
-/

#check SimpleGraph.edgeSet
#check SimpleGraph.lineGraph
#check SimpleGraph.lineGraph_adj_iff_exists
#check SimpleGraph.Coloring
#check SimpleGraph.Colorable
#check SimpleGraph.maxDegree
#check SimpleGraph.degree_le_maxDegree

section ProspectiveSimpleEncoding

variable {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]

#check (show Prop from G.lineGraph.Colorable (G.maxDegree + 1))

end ProspectiveSimpleEncoding
