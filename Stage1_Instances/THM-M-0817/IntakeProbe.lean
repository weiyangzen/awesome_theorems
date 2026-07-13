import Mathlib.Combinatorics.SimpleGraph.Clique

/-!
# THM-M-0817 discovery-only intake probe

These checks authenticate pinned simple-graph vocabulary for cliques, independent sets, exact
finite cardinalities, and graph complement. They do not select a finite or infinite Ramsey
variant, identify a terminal Ramsey declaration, freeze a canonical target, or prove THM-M-0817.
-/

#check SimpleGraph.IsClique
#check SimpleGraph.IsNClique
#check SimpleGraph.IsIndepSet
#check SimpleGraph.IsNIndepSet
#check SimpleGraph.isClique_compl
#check SimpleGraph.isIndepSet_compl
#check SimpleGraph.isNClique_compl
#check SimpleGraph.isNIndepSet_compl
