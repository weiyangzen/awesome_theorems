import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs

/-!
# THM-M-0851 discovery-only intake probe

These checks authenticate adjacent pinned random-graph and connectivity interfaces. They do not
select a graph model or state a connectivity-threshold theorem.
-/

#check SimpleGraph.binomialRandom
#check SimpleGraph.binomialRandom_zero
#check SimpleGraph.binomialRandom_one
#check SimpleGraph.Preconnected
#check SimpleGraph.Connected
#check SimpleGraph.connected_bot_iff
#check SimpleGraph.connected_top_iff

#print axioms SimpleGraph.connected_bot_iff
#print axioms SimpleGraph.connected_top_iff
