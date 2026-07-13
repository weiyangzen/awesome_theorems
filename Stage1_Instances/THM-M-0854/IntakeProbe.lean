import Mathlib.Combinatorics.SimpleGraph.Hamiltonian

/-!
# THM-M-0854 discovery-only intake probe

These checks authenticate adjacent APIs in pinned mathlib. They do not select or prove an Ore
statement and do not import the divergent external Bondy-Chvatal branch.
-/

#check SimpleGraph
#check SimpleGraph.irrefl
#check SimpleGraph.degree
#check SimpleGraph.degree_lt_card_verts
#check SimpleGraph.Walk.IsHamiltonianCycle
#check SimpleGraph.IsHamiltonian
#check SimpleGraph.IsHamiltonian.mono
#check SimpleGraph.IsHamiltonian.connected
#check SimpleGraph.not_isHamiltonian_of_card_eq_two
#check SimpleGraph.top_adj
