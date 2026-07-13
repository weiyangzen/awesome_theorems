import Mathlib.Combinatorics.SimpleGraph.Finite

/-!
# THM-M-0875 discovery-only intake probe

These checks authenticate pinned finite-simple-graph, graph-isomorphism, neighborhood, and degree
interfaces adjacent to possible Weisfeiler-Leman encodings. They do not define a refinement
algorithm, select a source proposition, or prove any correctness, completeness, stabilization, or
complexity claim for THM-M-0875.
-/

#check SimpleGraph
#check SimpleGraph.Iso
#check SimpleGraph.Iso.mapNeighborSet
#check SimpleGraph.Iso.card_eq
#check SimpleGraph.Iso.degree_eq
#check SimpleGraph.neighborSet
#check SimpleGraph.neighborFinset
#check SimpleGraph.degree
#check SimpleGraph.card_neighborFinset_eq_degree
#check Finset.filter
#check Fintype.card

#print axioms SimpleGraph.Iso.degree_eq
#print axioms SimpleGraph.Iso.card_eq
