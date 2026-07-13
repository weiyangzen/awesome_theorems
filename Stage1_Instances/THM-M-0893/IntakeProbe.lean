import Mathlib.Combinatorics.SimpleGraph.Diam
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Maps

/-!
# THM-M-0893 discovery-only intake probe

These checks authenticate pinned graph interfaces adjacent to a possible Bannai-Ito encoding.
They do not define distance-regularity, select the finiteness/diameter target, enumerate graph
isomorphism classes, or supply proof credit.
-/

#check SimpleGraph
#check SimpleGraph.Connected
#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.dist
#check SimpleGraph.edist
#check SimpleGraph.diam
#check SimpleGraph.connected_iff_diam_ne_zero
#check SimpleGraph.Iso
