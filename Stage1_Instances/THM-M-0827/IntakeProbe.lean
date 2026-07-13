import Mathlib.Combinatorics.Digraph.Basic
import Mathlib.Combinatorics.Quiver.Path.Weight
import Mathlib.Combinatorics.SimpleGraph.Metric

/-!
# THM-M-0827 discovery-only intake probe

These checks authenticate pinned directed-graph, additive path-weight, and unweighted graph-distance
interfaces adjacent to a future source-selected Floyd-Warshall theorem. They do not define or run
Floyd-Warshall, select a canonical target, or supply correctness or complexity proof credit.
-/

#check Digraph
#check Digraph.Adj
#check Quiver.Path
#check Quiver.Path.length
#check Quiver.Path.addWeight
#check Quiver.Path.addWeight_nil
#check Quiver.Path.addWeight_cons
#check Quiver.Path.addWeight_comp
#check SimpleGraph.edist
#check SimpleGraph.edist_eq_sInf
#check SimpleGraph.Reachable.exists_walk_length_eq_edist
#check SimpleGraph.edist_le
#check SimpleGraph.dist
#check SimpleGraph.dist_eq_sInf
#check SimpleGraph.dist_le
