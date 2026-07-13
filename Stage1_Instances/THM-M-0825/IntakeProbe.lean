import Mathlib.Combinatorics.Quiver.Arborescence
import Mathlib.Combinatorics.Quiver.Path.Weight
import Mathlib.Combinatorics.SimpleGraph.Metric

/-!
# THM-M-0825 discovery-only intake probe

These checks authenticate pinned unweighted graph-distance, additive path-weight, and shortest-path
interfaces adjacent to a future source-selected Dijkstra correctness theorem. They do not define or
execute Dijkstra's algorithm, select a canonical target, or supply proof credit.
-/

#check SimpleGraph.edist
#check SimpleGraph.edist_eq_sInf
#check SimpleGraph.Reachable.exists_walk_length_eq_edist
#check SimpleGraph.edist_le
#check SimpleGraph.reachable_of_edist_ne_top
#check SimpleGraph.dist
#check SimpleGraph.dist_eq_sInf
#check SimpleGraph.dist_le
#check Quiver.Path.addWeight
#check Quiver.Path.addWeightOfEPs
#check Quiver.Path.addWeight_comp
#check Quiver.Path.addWeight_cons
#check Quiver.Path.addWeightOfEPs_comp
#check Quiver.shortestPath
#check Quiver.shortest_path_spec
