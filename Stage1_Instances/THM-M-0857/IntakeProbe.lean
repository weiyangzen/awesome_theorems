import Mathlib.Combinatorics.SimpleGraph.Connectivity.EdgeConnectivity
import Mathlib.Combinatorics.SimpleGraph.Tutte

/-!
# THM-M-0857 discovery-only intake probe

These checks authenticate pinned simple-graph interfaces relevant to Petersen's theorem. They do
not freeze a simple-graph specialization of the historical multigraph statement, prove the
cubic-bridgeless reduction, or supply proof credit.
-/

#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.IsBridge
#check SimpleGraph.isBridge_iff
#check SimpleGraph.isBridge_iff_mem_and_forall_cycle_notMem
#check SimpleGraph.IsEdgeConnected
#check SimpleGraph.isEdgeConnected_two
#check SimpleGraph.Subgraph.IsPerfectMatching
#check SimpleGraph.Subgraph.isPerfectMatching_iff
#check SimpleGraph.IsTutteViolator
#check SimpleGraph.tutte
