import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Data.Finset.Max

/-!
# THM-M-0814 discovery-only intake probe

These checks authenticate pinned undirected multigraph incidence and finite aggregation APIs. They
do not define a capacitated network, a feasible flow, a cut, or a canonical target, and they do not
prove the max-flow min-cut theorem.
-/

#check Graph
#check Graph.IsLink
#check Graph.Inc
#check Graph.banana
#check Finset.sum
#check Finset.max'
