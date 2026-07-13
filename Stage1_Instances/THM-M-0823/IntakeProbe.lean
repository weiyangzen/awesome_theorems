import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Combinatorics.SimpleGraph.Subgraph

/-!
# THM-M-0823 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for forests, trees, spanning subgraphs, edge
sets, and unweighted spanning-tree existence. They do not define weights or Kruskal's algorithm,
select a canonical target, or prove minimum-spanning-tree correctness.
-/

#check SimpleGraph.IsAcyclic
#check SimpleGraph.IsTree
#check SimpleGraph.Subgraph.IsSpanning
#check SimpleGraph.Subgraph.edgeSet
#check SimpleGraph.Subgraph.spanningCoe
#check SimpleGraph.Connected.exists_isTree_le
