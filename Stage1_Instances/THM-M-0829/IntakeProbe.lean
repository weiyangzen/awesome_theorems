import Mathlib.Combinatorics.Quiver.Path.Weight
import Mathlib.Combinatorics.SimpleGraph.Metric
import Mathlib.Combinatorics.SimpleGraph.Walks.Counting

/-!
# THM-M-0829 discovery-only intake probe

These checks authenticate generic pinned directed-path, additive-weight, undirected shortest-walk,
and finite bounded-walk APIs adjacent to a possible future model. They do not define a capacitated
network, feasible flow, residual graph, level graph, blocking flow, maximum-flow theorem,
complexity bound, canonical target, or proof of the Dinic algorithm.
-/

#check Quiver.Path
#check Quiver.Path.length
#check Quiver.Path.addWeight
#check Quiver.Path.addWeight_comp
#check SimpleGraph.Walk
#check SimpleGraph.edist
#check SimpleGraph.Reachable.exists_walk_length_eq_edist
#check SimpleGraph.Walk.isPath_of_length_eq_dist
#check SimpleGraph.finsetWalkLengthLT
#check SimpleGraph.fintypeSetWalkLengthLT
