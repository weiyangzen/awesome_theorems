import Mathlib.Combinatorics.SimpleGraph.Bipartite

/-!
# THM-M-0865 discovery-only intake probe

These commands authenticate pinned simple-graph, isomorphism, subgraph-copy, complete-graph, and
complete-bipartite-graph vocabulary adjacent to a possible Kuratowski statement. The parameterized
schema does not define planarity or topological-minor containment, select the canonical target, or
provide proof credit.
-/

namespace Stage1Instances.THM_M_0865

#check SimpleGraph
#check SimpleGraph.Iso
#check SimpleGraph.Copy
#check SimpleGraph.IsContained
#check SimpleGraph.completeGraph
#check completeBipartiteGraph
#check SimpleGraph.completeBipartiteGraph_isContained_iff

universe u

def KuratowskiShape
    (Planar : {V : Type u} -> SimpleGraph V -> Prop)
    (IsTopologicalMinor : {X : Type} -> {Y : Type u} ->
      SimpleGraph X -> SimpleGraph Y -> Prop) : Prop :=
  forall (V : Type u) (G : SimpleGraph V),
    Planar G <->
      (Not (IsTopologicalMinor (SimpleGraph.completeGraph (Fin 5)) G) ∧
       Not (IsTopologicalMinor (completeBipartiteGraph (Fin 3) (Fin 3)) G))

#check KuratowskiShape

end Stage1Instances.THM_M_0865
