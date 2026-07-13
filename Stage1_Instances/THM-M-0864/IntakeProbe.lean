import Mathlib.Combinatorics.SimpleGraph.Circulant
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Subgraph
import Mathlib.Combinatorics.SimpleGraph.Operations

/-!
# THM-M-0864 discovery-only intake probe

These checks authenticate pinned ordinary-connectivity, vertex-deletion, cycle-graph, isomorphism,
and local graph-operation APIs adjacent to a future Tutte wheel theorem encoding. They do not
define 3-vertex-connectivity, a wheel, edge contraction, minimal 3-connectivity, a decomposition
sequence, or a canonical target, and they credit no proof body for THM-M-0864.
-/

#check SimpleGraph.Connected
#check SimpleGraph.Subgraph.deleteVerts
#check SimpleGraph.cycleGraph
#check SimpleGraph.cycleGraph.cycle
#check SimpleGraph.Iso
#check SimpleGraph.replaceVertex
#check SimpleGraph.edge
#check SimpleGraph.Subgraph.deleteEdges
