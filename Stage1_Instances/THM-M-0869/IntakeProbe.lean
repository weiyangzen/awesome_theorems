import Mathlib.Combinatorics.SimpleGraph.Copy

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0869 catalog topic.

The interfaces distinguish ordinary copy containment, freeness, and induced containment. They do
not select a graph class, an obstruction family, a minor relation, or a characterization theorem.
-/

#check SimpleGraph.IsContained
#check SimpleGraph.Free
#check SimpleGraph.IsIndContained
#check SimpleGraph.IsContained.trans
#check SimpleGraph.IsIndContained.trans
#check SimpleGraph.isContained_iff_exists_iso_subgraph
#check SimpleGraph.isIndContained_iff_exists_iso_subgraph
