import Mathlib.Combinatorics.Digraph.Basic
import Mathlib.Combinatorics.Quiver.Path.Weight

/-!
# THM-M-0826 discovery-only intake probe

These declarations are generic directed-graph, dependent-path, and additive path-weight
infrastructure that a future source-selected Bellman-Ford model might use. They do not define
relaxation, shortest distance, negative-cycle handling, Bellman-Ford execution, or a correctness,
termination, path-reconstruction, detection, or complexity theorem.
-/

#check Digraph
#check Digraph.Adj
#check Quiver.Path
#check Quiver.Path.length
#check Quiver.Path.addWeight
#check Quiver.Path.addWeight_nil
#check Quiver.Path.addWeight_cons
#check Quiver.Path.addWeight_comp
#check Quiver.Path.addWeightOfEPs
#check Quiver.Path.addWeightOfEPs_comp

#print axioms Quiver.Path.addWeight_cons
#print axioms Quiver.Path.addWeight_comp
