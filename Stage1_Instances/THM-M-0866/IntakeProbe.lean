import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.Copy

/-!
# THM-M-0866 discovery-only intake probe

These commands authenticate pinned finite-simple-graph and subgraph-copy APIs adjacent to a future
Wagner-theorem encoding. They do not define graph minors or planarity, choose a canonical target,
or prove Wagner's theorem.
-/

namespace Stage1Instances.THM_M_0866

#check SimpleGraph
#check SimpleGraph.completeGraph
#check completeBipartiteGraph
#check SimpleGraph.Copy
#check SimpleGraph.IsContained
#check SimpleGraph.IsIndContained
#check SimpleGraph.induce

end Stage1Instances.THM_M_0866
