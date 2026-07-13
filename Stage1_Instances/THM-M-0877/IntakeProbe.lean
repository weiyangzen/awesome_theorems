import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Combinatorics.Digraph.Basic
import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Data.Finset.Max

/-!
# THM-M-0877 discovery-only intake probe

These checks authenticate pinned undirected and directed graph substrate plus finite aggregation.
They do not define capacities, feasible flows, conservation, cuts, or a canonical target, and they
do not prove any max-flow/min-cut result.
-/

#check Graph
#check Graph.IsLink
#check Graph.Inc
#check Digraph
#check Finset.sum
#check Finset.max'
