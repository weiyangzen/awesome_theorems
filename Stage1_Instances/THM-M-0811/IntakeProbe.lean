import Mathlib.Combinatorics.SimpleGraph.Trails

/-!
# THM-M-0811 discovery-only intake probe

These checks authenticate pinned Eulerian-trail definitions and necessary degree consequences.
The imported module explicitly leaves the converse existence direction as TODO. This file neither
freezes a canonical target nor proves the catalog's unspecified iff.
-/

#check SimpleGraph.Walk.IsEulerian
#check SimpleGraph.Walk.IsEulerian.isTrail
#check SimpleGraph.Walk.isEulerian_iff
#check SimpleGraph.Walk.IsTrail.isEulerian_iff
#check SimpleGraph.Walk.IsEulerian.even_degree_iff
#check SimpleGraph.Walk.IsEulerian.card_odd_degree
