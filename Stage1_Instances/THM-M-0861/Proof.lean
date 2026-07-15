import ObligationTree

/-!
# THM-M-0861 proof-phase bodies

This module proves the elementary maximum-degree bound and the exact lower
conjunct of Konig's edge-coloring target.  It deliberately does not postulate
the still-open fixed-palette Satz C upper bound.
-/

noncomputable section

namespace Stage1Instances.THM_M_0861_Proof

universe u v

open Stage1Instances.THM_M_0861
open Stage1Instances.THM_M_0861_Obligations

/-- Every actual vertex has incidence degree at most the finite maximum. -/
theorem degree_le_maxDegree {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (vertexFinite : G.vertexSet.Finite) :
    DegreeBound G (maxDegree G vertexFinite) := by
  intro x hx
  exact Finset.le_sup (vertexFinite.mem_toFinset.mpr hx)

/-- Incidence at a vertex is a finite set whenever the actual edge set is. -/
theorem incidenceSet_finite {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (edgeFinite : G.edgeSet.Finite) (x : Vertex) :
    (G.incidenceSet x).Finite :=
  edgeFinite.subset (G.incidenceSet_subset_edgeSet x)

/-- Restriction of a proper edge coloring to one incidence subtype is
injective. -/
theorem incidentColor_injective {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) {k : Nat}
    (color : {e : Edge // e ∈ G.edgeSet} -> Fin k)
    (proper : forall e f : {e : Edge // e ∈ G.edgeSet}, e ≠ f ->
      forall x : Vertex, G.Inc e.1 x -> G.Inc f.1 x -> color e ≠ color f)
    (x : Vertex) :
    Function.Injective (fun e : G.incidenceSet x =>
      color ⟨e.1, G.incidenceSet_subset_edgeSet x e.2⟩) := by
  intro e f sameColor
  apply Subtype.ext
  by_contra differentEdges
  have differentActualEdges :
      (⟨e.1, G.incidenceSet_subset_edgeSet x e.2⟩ :
        {e : Edge // e ∈ G.edgeSet}) ≠
      ⟨f.1, G.incidenceSet_subset_edgeSet x f.2⟩ := by
    intro sameActualEdge
    exact differentEdges (congrArg
      (fun z : {e : Edge // e ∈ G.edgeSet} => z.1) sameActualEdge)
  exact (proper _ _ differentActualEdges x e.2 f.2) sameColor

/-- Pointwise degree bounds compose through the frozen finite supremum. -/
theorem maxDegree_le_of_degree_le {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (vertexFinite : G.vertexSet.Finite) (k : Nat)
    (degree_le : forall x, x ∈ G.vertexSet -> degree G x <= k) :
    maxDegree G vertexFinite <= k := by
  apply Finset.sup_le
  intro x hx
  exact degree_le x (vertexFinite.mem_toFinset.mp hx)

/-- A proper coloring is injective on the edges incident with a fixed vertex.
Consequently every palette has at least the maximum incidence degree. -/
theorem lowerBound : LowerBoundTarget.{u, v} := by
  intro Vertex Edge G vertexFinite edgeFinite _hBipartite k hColorable
  obtain ⟨color, hproper⟩ := hColorable
  apply maxDegree_le_of_degree_le G vertexFinite k
  intro x _hx
  letI : Fintype (G.incidenceSet x) :=
    (incidenceSet_finite G edgeFinite x).fintype
  change Nat.card (G.incidenceSet x) <= k
  simpa only [Nat.card_fin] using Nat.card_le_card_of_injective _
    (incidentColor_injective G color hproper x)

/-- A finite set whose cardinality is at most `k` embeds into `Fin k`. -/
noncomputable def edgePaletteEmbedding {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (edgeFinite : G.edgeSet.Finite) (k : Nat)
    (edgeCount_le : G.edgeSet.ncard <= k) :
    {e : Edge // e ∈ G.edgeSet} ↪ Fin k := by
  letI : Fintype {e : Edge // e ∈ G.edgeSet} := edgeFinite.fintype
  apply (Function.Embedding.nonempty_of_card_le _).some
  rw [Fintype.card_fin]
  rw [<- Nat.card_eq_fintype_card, Nat.card_coe_set_eq]
  exact edgeCount_le

/-- If the palette is at least as large as the whole actual edge set, an
arbitrary injection of edge identities into colors is automatically proper. -/
theorem edgeColorable_of_edge_ncard_le {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (edgeFinite : G.edgeSet.Finite) (k : Nat)
    (edgeCount_le : G.edgeSet.ncard <= k) : EdgeColorable G k := by
  let embedding := edgePaletteEmbedding G edgeFinite k edgeCount_le
  refine ⟨embedding, ?_⟩
  intro e f differentEdges _x _he _hf
  exact embedding.injective.ne differentEdges

/-- Instantiating a proof of the source-strengthened fixed-palette theorem at
the maximum degree closes the exact upper conjunct.  The premise remains
visible and receives no proof credit here. -/
theorem upperBound_of_boundedSatzC
    (satzC : BoundedSatzCTarget.{u, v}) : UpperBoundTarget.{u, v} := by
  intro Vertex Edge G vertexFinite edgeFinite hBipartite
  exact satzC G vertexFinite edgeFinite (maxDegree G vertexFinite)
    hBipartite (degree_le_maxDegree G vertexFinite)

/-- Exact conditional root composition with only Satz C left explicit. -/
theorem konigEdgeColoring_of_boundedSatzC
    (satzC : BoundedSatzCTarget.{u, v}) : KonigEdgeColoringTarget.{u, v} :=
  root_of_upper_and_lower (upperBound_of_boundedSatzC satzC) lowerBound

#check degree_le_maxDegree
#check incidenceSet_finite
#check incidentColor_injective
#check maxDegree_le_of_degree_le
#check lowerBound
#check edgePaletteEmbedding
#check edgeColorable_of_edge_ncard_le
#check upperBound_of_boundedSatzC
#check konigEdgeColoring_of_boundedSatzC

#print axioms degree_le_maxDegree
#print axioms incidenceSet_finite
#print axioms incidentColor_injective
#print axioms maxDegree_le_of_degree_le
#print axioms lowerBound
#print axioms edgePaletteEmbedding
#print axioms edgeColorable_of_edge_ncard_le
#print axioms upperBound_of_boundedSatzC
#print axioms konigEdgeColoring_of_boundedSatzC

end Stage1Instances.THM_M_0861_Proof
