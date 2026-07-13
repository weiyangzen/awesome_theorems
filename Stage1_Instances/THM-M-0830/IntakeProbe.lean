import Mathlib.Combinatorics.Digraph.Basic
import Mathlib.Combinatorics.Quiver.Path.Weight
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# THM-M-0830 discovery-only intake probe

These checks authenticate pinned directed-graph, path, weight, and finite-sum substrate. They do
not define a flow network, preflow, residual graph, push/relabel state machine, FIFO implementation,
maximum-flow correctness theorem, or complexity bound.
-/

#check Digraph
#check Digraph.Adj
#check Quiver.Path
#check Quiver.Path.length
#check Quiver.Path.addWeight
#check Finset.sum
