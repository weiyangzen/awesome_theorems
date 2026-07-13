import Mathlib.Combinatorics.SimpleGraph.DeleteEdges
import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Combinatorics.SimpleGraph.Subgraph
import Mathlib.Order.WellQuasiOrder

/-!
# THM-M-0868 discovery-only intake probe

These checks authenticate pinned graph-deletion, isomorphism, induced-graph, and generic WQO
interfaces adjacent to a future graph-minor encoding. They do not define edge contraction or a
graph-minor relation, select the canonical target, or prove the Graph Minor Theorem.
-/

#check SimpleGraph
#check SimpleGraph.deleteEdges
#check SimpleGraph.Subgraph.deleteVerts
#check SimpleGraph.Iso
#check SimpleGraph.induce
#check WellQuasiOrdered
