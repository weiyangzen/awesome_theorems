import Mathlib.Combinatorics.SimpleGraph.Coloring
import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Combinatorics.SimpleGraph.Paths

/-!
# THM-M-0840 discovery-only intake probe

These checks authenticate pinned finite-simple-graph APIs adjacent to a future strong perfect graph
encoding. They do not define perfect or Berge graphs, select the canonical target, or prove the
strong perfect graph theorem.
-/

#check SimpleGraph.induce
#check SimpleGraph.compl_adj
#check SimpleGraph.Walk.IsCycle
#check SimpleGraph.Walk.IsCycle.three_le_length
#check SimpleGraph.chromaticNumber
#check SimpleGraph.cliqueNum
#check SimpleGraph.cliqueNum_le_chromaticNumber
