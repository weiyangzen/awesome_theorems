import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Combinatorics.Hall.Basic
import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.Coloring
import Mathlib.Combinatorics.SimpleGraph.EdgeLabeling
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Hall
import Mathlib.Combinatorics.SimpleGraph.LineGraph
import Mathlib.Data.Set.Card

/-!
# THM-M-0861 immutable anchor probe

This module repeats the frozen finite-bipartite-multigraph target and checks the
closest pinned mathlib interfaces. It deliberately declares no inhabitant of
`ExactTarget`: none of the inspected declarations is Konig's edge-coloring
theorem for multigraphs.
-/

noncomputable section

open Set

namespace Stage1Instances.THM_M_0861_AnchorAudit

universe u v

def IsBipartiteWith {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (side : Vertex -> Bool) : Prop :=
  forall e x y, G.IsLink e x y -> side x ≠ side y

def IsBipartite {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) : Prop :=
  exists side : Vertex -> Bool, IsBipartiteWith G side

def degree {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (x : Vertex) : Nat :=
  (G.incidenceSet x).ncard

def maxDegree {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) : Nat :=
  vertexFinite.toFinset.sup (degree G)

def EdgeColorable {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (colorCount : Nat) : Prop :=
  exists color : {e : Edge // e ∈ Graph.edgeSet G} -> Fin colorCount,
    forall e f : {e : Edge // e ∈ Graph.edgeSet G}, e ≠ f ->
      forall x : Vertex, G.Inc e.1 x -> G.Inc f.1 x -> color e ≠ color f

def HasChromaticIndex {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (colorCount : Nat) : Prop :=
  EdgeColorable G colorCount /\
    forall k : Nat, EdgeColorable G k -> colorCount <= k

/-- Literal copy of the statement-phase proposition. -/
def ExactTarget : Prop :=
  forall {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) (_edgeFinite : G.edgeSet.Finite),
    IsBipartite G -> HasChromaticIndex G (maxDegree G vertexFinite)

-- Multigraph representation and incidence substrate.
#check Graph
#check Graph.IsLink
#check Graph.Inc
#check Graph.incidenceSet

-- Simple-graph-only coloring and line-graph substrate.
#check SimpleGraph.IsBipartiteWith
#check SimpleGraph.IsBipartite
#check SimpleGraph.EdgeLabeling
#check SimpleGraph.lineGraph
#check SimpleGraph.Coloring
#check SimpleGraph.chromaticNumber
#check SimpleGraph.maxDegree

-- Hall/matching results are proof-bearing but do not state edge coloring.
#check SimpleGraph.exists_isMatching_of_forall_ncard_le
#check SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le
#check Finset.all_card_le_biUnion_card_iff_exists_injective

-- The strongest adjacent pinned theorems are not inhabitants of the root.
#check_failure (SimpleGraph.lineGraph_adj_iff_exists : ExactTarget.{u, v})
#check_failure
  (SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le : ExactTarget.{u, v})

#print sorries SimpleGraph.lineGraph_adj_iff_exists
#print sorries SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le
#print sorries Finset.all_card_le_biUnion_card_iff_exists_injective
#print axioms SimpleGraph.lineGraph_adj_iff_exists
#print axioms SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le
#print axioms Finset.all_card_le_biUnion_card_iff_exists_injective

end Stage1Instances.THM_M_0861_AnchorAudit

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0861_AnchorAudit.ExactTarget
