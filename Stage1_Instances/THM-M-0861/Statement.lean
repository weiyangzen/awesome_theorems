import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Data.Set.Card

/-!
# THM-M-0861: exact Konig edge-coloring statement

This module freezes the finite bipartite multigraph statement selected from
Konig's 1916 Satz C and the catalog's chromatic-index equality wording. Edge
identities are separate from vertices, so parallel edges remain distinct.
This is a statement artifact; it contains no proof of the coloring theorem.
-/

noncomputable section

open Set

namespace Stage1Instances.THM_M_0861

universe u v

/-- A fixed two-side assignment is compatible with every link of `G`. -/
def IsBipartiteWith {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (side : Vertex -> Bool) : Prop :=
  forall e x y, G.IsLink e x y -> side x ≠ side y

/-- The multigraph admits a bipartition. This condition also excludes loops. -/
def IsBipartite {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) : Prop :=
  exists side : Vertex -> Bool, IsBipartiteWith G side

/-- Bipartiteness rules out a link whose two ends are the same vertex. -/
theorem IsBipartite.noLoops {Vertex : Type u} {Edge : Type v}
    {G : Graph Vertex Edge} (hG : IsBipartite G) :
    forall e x, Not (G.IsLink e x x) := by
  obtain ⟨side, hside⟩ := hG
  intro e x hloop
  exact (hside e x x hloop) rfl

/-- Degree counts incident edge identities, hence counts parallel edges with
multiplicity. On the selected bipartite domain there are no loops. -/
def degree {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (x : Vertex) : Nat :=
  (G.incidenceSet x).ncard

/-- Maximum multiplicity-counted incidence degree over the actual finite
vertex set, with value zero when that set is empty. -/
def maxDegree {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) : Nat :=
  vertexFinite.toFinset.sup (degree G)

/-- `G` has a proper edge coloring with the palette `Fin colorCount`.
Only actual edges are colored. Distinct edge identities incident with a common
vertex receive different colors, including parallel edges with equal ends. -/
def EdgeColorable {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (colorCount : Nat) : Prop :=
  exists color : {e : Edge // e ∈ Graph.edgeSet G} -> Fin colorCount,
    forall e f : {e : Edge // e ∈ Graph.edgeSet G}, e ≠ f ->
      forall x : Vertex, G.Inc e.1 x -> G.Inc f.1 x -> color e ≠ color f

/-- A graph with no actual edges has the unique empty proper coloring with
zero colors. This fixes the zero-palette convention used by the root. -/
theorem edgeColorable_zero_of_edgeSet_eq_empty {Vertex : Type u} {Edge : Type v}
    {G : Graph Vertex Edge} (hE : G.edgeSet = ∅) : EdgeColorable G 0 := by
  let noActualEdge : {e : Edge // e ∈ G.edgeSet} -> Empty := fun e => by
    have : e.1 ∈ (∅ : Set Edge) := hE ▸ e.2
    exact this.elim
  refine ⟨fun e => Empty.elim (noActualEdge e), ?_⟩
  intro e
  exact Empty.elim (noActualEdge e)

/-- `colorCount` is the least palette size for a proper edge coloring. -/
def HasChromaticIndex {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (colorCount : Nat) : Prop :=
  EdgeColorable G colorCount /\
    forall k : Nat, EdgeColorable G k -> colorCount <= k

/-- The chromatic index of an edgeless graph is zero under the selected
least-palette definition. -/
theorem hasChromaticIndex_zero_of_edgeSet_eq_empty {Vertex : Type u} {Edge : Type v}
    {G : Graph Vertex Edge} (hE : G.edgeSet = ∅) : HasChromaticIndex G 0 :=
  ⟨edgeColorable_zero_of_edgeSet_eq_empty hE, fun k _ => Nat.zero_le k⟩

/-- Konig's edge-coloring theorem for finite bipartite multigraphs: the least
number of colors in a proper edge coloring is the maximum incidence degree. -/
def KonigEdgeColoringTarget : Prop :=
  forall {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) (_edgeFinite : G.edgeSet.Finite),
    IsBipartite G -> HasChromaticIndex G (maxDegree G vertexFinite)

/-- Source-shaped expansion: Satz C gives the first conjunct at `Delta`, and
the elementary maximum-degree lower bound is the second conjunct. -/
def ExpandedTarget : Prop :=
  forall {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) (_edgeFinite : G.edgeSet.Finite),
    IsBipartite G ->
      EdgeColorable G (maxDegree G vertexFinite) /\
        forall k : Nat, EdgeColorable G k -> maxDegree G vertexFinite <= k

/-- Checked definitional transport between the least-palette and expanded forms. -/
theorem konigEdgeColoringTarget_iff_expandedTarget :
    KonigEdgeColoringTarget.{u, v} <-> ExpandedTarget.{u, v} :=
  Iff.rfl

-- Structural mutations. Each elaborates but changes the selected proposition.

/-- Removed-hypothesis mutation: bipartiteness is omitted. -/
def mutationRemovedBipartiteHypothesis : Prop :=
  forall {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) (_edgeFinite : G.edgeSet.Finite),
    HasChromaticIndex G (maxDegree G vertexFinite)

/-- Changed-domain mutation: only finite ambient carrier types are admitted,
rather than arbitrary carriers with finite actual vertex and edge sets. -/
def mutationFiniteAmbientDomains : Prop :=
  forall {Vertex : Type u} {Edge : Type v} [Fintype Vertex] [Fintype Edge]
    (G : Graph Vertex Edge), IsBipartite G ->
      HasChromaticIndex G (Finset.univ.sup (degree G))

/-- Changed-scope mutation: one bipartition is chosen before the graph. -/
def mutationGlobalBipartitionScope : Prop :=
  forall {Vertex : Type u} {Edge : Type v}, exists side : Vertex -> Bool,
    forall (G : Graph Vertex Edge) (vertexFinite : G.vertexSet.Finite)
      (_edgeFinite : G.edgeSet.Finite),
      IsBipartiteWith G side -> HasChromaticIndex G (maxDegree G vertexFinite)

/-- Boundary mutation: finite bipartite multigraphs of maximum degree zero are
excluded, removing the empty and edgeless cases. -/
def mutationPositiveMaximumDegreeOnly : Prop :=
  forall {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) (_edgeFinite : G.edgeSet.Finite),
    IsBipartite G -> 0 < maxDegree G vertexFinite ->
      HasChromaticIndex G (maxDegree G vertexFinite)

#check_failure
  (rfl : KonigEdgeColoringTarget.{u, v} = mutationRemovedBipartiteHypothesis.{u, v})
#check_failure
  (rfl : KonigEdgeColoringTarget.{u, v} = mutationFiniteAmbientDomains.{u, v})
#check_failure
  (rfl : KonigEdgeColoringTarget.{u, v} = mutationGlobalBipartitionScope.{u, v})
#check_failure
  (rfl : KonigEdgeColoringTarget.{u, v} = mutationPositiveMaximumDegreeOnly.{u, v})

#print axioms Stage1Instances.THM_M_0861.IsBipartite.noLoops
#print axioms Stage1Instances.THM_M_0861.edgeColorable_zero_of_edgeSet_eq_empty
#print axioms Stage1Instances.THM_M_0861.hasChromaticIndex_zero_of_edgeSet_eq_empty
#print axioms Stage1Instances.THM_M_0861.konigEdgeColoringTarget_iff_expandedTarget

end Stage1Instances.THM_M_0861

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0861.KonigEdgeColoringTarget
