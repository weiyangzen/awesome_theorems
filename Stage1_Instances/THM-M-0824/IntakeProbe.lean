import Mathlib.Combinatorics.SimpleGraph.Acyclic

/-!
# THM-M-0824 discovery-only intake probe

These checks authenticate pinned finite-simple-graph, spanning-subgraph, and tree interfaces
adjacent to possible formulations of Prim's algorithm. They do not define edge weights, Prim's
iteration, a tie policy, an output tree, minimum total weight, or a correctness theorem.
-/

#check SimpleGraph
#check SimpleGraph.Subgraph.IsSpanning
#check SimpleGraph.IsTree
#check SimpleGraph.edgeFinset
#check SimpleGraph.Connected.exists_isTree_le
#check SimpleGraph.IsTree.card_edgeFinset

#print axioms SimpleGraph.Connected.exists_isTree_le
#print axioms SimpleGraph.IsTree.card_edgeFinset
