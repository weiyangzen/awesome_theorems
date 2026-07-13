import Mathlib.Combinatorics.SimpleGraph.Tutte

/-!
# THM-M-0856 discovery-only intake probe

These checks authenticate the exact pinned mathlib interfaces adjacent to the catalog's Tutte
theorem wording. They do not select a canonical source edition, complete the statement phase,
audit the terminal proof body, or prove any rev-5.6 node.
-/

#check SimpleGraph.IsTutteViolator
#check SimpleGraph.Subgraph.IsPerfectMatching
#check @SimpleGraph.tutte
#print axioms SimpleGraph.tutte
