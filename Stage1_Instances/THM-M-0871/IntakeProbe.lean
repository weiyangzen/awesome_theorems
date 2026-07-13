import Mathlib.ModelTheory.Graph
import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Combinatorics.SimpleGraph.Maps

/-!
# THM-M-0871 discovery-only intake probe

These checks authenticate pinned first-order graph, simple-tree, and graph-isomorphism interfaces
adjacent to a future Courcelle encoding. They do not define monadic second-order or counting logic,
a tree decomposition, treewidth, a model checker, a complexity bound, or THM-M-0871.
-/

#check FirstOrder.Language.graph
#check SimpleGraph.structure
#check FirstOrder.Language.Theory.simpleGraph
#check FirstOrder.Language.simpleGraphOfStructure
#check FirstOrder.Language.structure_simpleGraphOfStructure
#check SimpleGraph.IsTree
#check SimpleGraph.Iso

#print axioms FirstOrder.Language.structure_simpleGraphOfStructure
#print axioms SimpleGraph.Iso.isTree_iff
