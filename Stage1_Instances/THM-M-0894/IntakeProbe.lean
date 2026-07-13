import Mathlib.Combinatorics.SimpleGraph.Diam
import Mathlib.Combinatorics.SimpleGraph.StronglyRegular

/-!
# THM-M-0894 discovery-only intake probe

These checks authenticate adjacent pinned graph metric, neighborhood, regularity, and strongly
regular APIs. They do not define distance-regularity, select a canonical theorem, identify
intersection numbers or an intersection array, compile a source transport, or supply proof credit.
-/

#check SimpleGraph
#check SimpleGraph.edist
#check SimpleGraph.dist
#check SimpleGraph.ediam
#check SimpleGraph.diam
#check SimpleGraph.neighborFinset
#check SimpleGraph.commonNeighbors
#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.IsSRGWith
#check SimpleGraph.IsSRGWith.regular
#check SimpleGraph.IsSRGWith.param_eq

#print axioms SimpleGraph.connected_iff_diam_ne_zero
#print axioms SimpleGraph.IsSRGWith.param_eq
