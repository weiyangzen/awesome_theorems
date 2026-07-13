import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.Topology.Algebra.Module.LinearPMap

/-!
# THM-M-0277 discovery-only intake probe

These commands authenticate direct pinned closed-graph interfaces and the total/partial-domain
distinction. They do not select the catalogue's exact statement, establish a source-to-Lean
transport, or prove the target.
-/

#check LinearMap.graph
#check LinearMap.continuous_of_isClosed_graph
#check LinearMap.continuous_of_seq_closed_graph
#check ContinuousLinearMap.ofIsClosedGraph
#check ContinuousLinearMap.ofSeqClosedGraph
#check LinearPMap.graph
#check LinearPMap.IsClosed

#print axioms LinearMap.continuous_of_isClosed_graph
#print axioms LinearMap.continuous_of_seq_closed_graph
