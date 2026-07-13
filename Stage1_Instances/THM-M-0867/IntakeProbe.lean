import Mathlib.Order.WellQuasiOrder
import Mathlib.Combinatorics.SimpleGraph.DeleteEdges
import Mathlib.Combinatorics.SimpleGraph.Maps

/-!
# THM-M-0867 discovery-only intake probe

These checks authenticate adjacent pinned WQO and finite simple-graph interfaces. They do not
define graph minors, select the source statement, establish a source transport, or prove the
Robertson-Seymour theorem.
-/

#check WellQuasiOrdered
#check wellQuasiOrdered_iff_exists_monotone_subseq
#check SimpleGraph
#check SimpleGraph.Iso
#check SimpleGraph.induce
#check SimpleGraph.deleteEdges
#check SimpleGraph.map
