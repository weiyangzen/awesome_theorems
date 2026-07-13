import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Combinatorics.Digraph.Basic
import Mathlib.Combinatorics.Quiver.Path.Weight
import Mathlib.Data.List.MinMax

/-!
# THM-M-0878 discovery-only intake probe

These checks authenticate pinned directed-graph, additive path-weight, finite-sum, and finite-list
minimization APIs. They do not define a capacitated network, feasible flow, residual network, cost
objective, optimizer, algorithm, canonical target, or proof of any minimum-cost-flow result.
-/

#check Digraph
#check Digraph.Adj
#check Quiver.Path
#check Quiver.Path.addWeight
#check Quiver.Path.addWeight_comp
#check Finset.sum
#check List.argmin
#check List.argmin_mem
#check List.le_of_mem_argmin
