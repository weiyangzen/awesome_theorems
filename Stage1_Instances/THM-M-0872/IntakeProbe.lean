import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Computability.TuringMachine.Computable

/-!
# THM-M-0872 discovery-only intake probe

These checks authenticate pinned finite-simple-graph, graph-tree, and machine-time interfaces that
could support a future Bodlaender statement. They do not define tree decompositions or treewidth,
choose a canonical theorem, implement an algorithm, or prove correctness or linear time.
-/

#check SimpleGraph
#check SimpleGraph.Adj
#check SimpleGraph.IsAcyclic
#check SimpleGraph.IsTree
#check SimpleGraph.isTree_iff_existsUnique_path
#check Turing.FinTM2
#check Turing.TM2OutputsInTime
#check Turing.TM2ComputableInTime
#check StateTransition.EvalsToInTime

#print axioms SimpleGraph.isTree_iff_existsUnique_path
