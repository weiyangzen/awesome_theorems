import Statement

/-!
# THM-M-0861 obligation-tree composition harness

This module checks only the exact child-to-parent shape selected by the frozen
obligation registry.  The upper- and lower-bound packages are explicit
hypotheses: no proof of either package is asserted here.
-/

noncomputable section

open Set

namespace Stage1Instances.THM_M_0861_Obligations

universe u v

open Stage1Instances.THM_M_0861

/-- The source-facing fixed-palette premise used by Satz C. -/
def DegreeBound {Vertex : Type u} {Edge : Type v}
    (G : Graph Vertex Edge) (colorCount : Nat) : Prop :=
  forall x, x ∈ G.vertexSet -> degree G x <= colorCount

/-- Source-strengthened upper-bound package.  This is an open proof interface,
not a declaration of König's theorem. -/
def BoundedSatzCTarget : Prop :=
  forall {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (_vertexFinite : G.vertexSet.Finite) (_edgeFinite : G.edgeSet.Finite)
    (colorCount : Nat),
    IsBipartite G -> DegreeBound G colorCount -> EdgeColorable G colorCount

/-- Exact upper conjunct of `ExpandedTarget`. -/
def UpperBoundTarget : Prop :=
  forall {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) (_edgeFinite : G.edgeSet.Finite),
    IsBipartite G -> EdgeColorable G (maxDegree G vertexFinite)

/-- Exact elementary lower conjunct of `ExpandedTarget`. -/
def LowerBoundTarget : Prop :=
  forall {Vertex : Type u} {Edge : Type v} (G : Graph Vertex Edge)
    (vertexFinite : G.vertexSet.Finite) (_edgeFinite : G.edgeSet.Finite),
    IsBipartite G ->
      forall k : Nat, EdgeColorable G k -> maxDegree G vertexFinite <= k

/-- Exact checked relationship owned by the statement-transport obligation. -/
def RootTransportTarget : Prop :=
  KonigEdgeColoringTarget.{u, v} <-> ExpandedTarget.{u, v}

/-- The exact pair of proof packages consumed by root composition. -/
def AssemblyTarget : Prop :=
  UpperBoundTarget.{u, v} /\ LowerBoundTarget.{u, v}

/-- Conditional child-to-assembly certificate. Both child packages are used. -/
theorem assembly_of_upper_and_lower
    (upper : UpperBoundTarget.{u, v})
    (lower : LowerBoundTarget.{u, v}) : AssemblyTarget.{u, v} :=
  ⟨upper, lower⟩

/-- Checked expansion of the bundled packages at the exact statement binders. -/
theorem expanded_of_assembly
    (assembly : AssemblyTarget.{u, v}) : ExpandedTarget.{u, v} := by
  intro Vertex Edge G vertexFinite edgeFinite hBipartite
  exact ⟨assembly.1 G vertexFinite edgeFinite hBipartite,
    assembly.2 G vertexFinite edgeFinite hBipartite⟩

/-- Local wrapper exposing the statement phase's exact checked Iff. -/
theorem checked_root_transport : RootTransportTarget.{u, v} :=
  konigEdgeColoringTarget_iff_expandedTarget

/-- Checked assembly-to-root certificate. Both typed children are explicit. -/
theorem root_of_assembly
    (transport : RootTransportTarget.{u, v})
    (assembly : AssemblyTarget.{u, v}) : KonigEdgeColoringTarget.{u, v} :=
  transport.mpr (expanded_of_assembly assembly)

/-- Combined conditional root harness.  This theorem is useful for detecting
unused or mismatched child packages; it does not inhabit either child. -/
theorem root_of_upper_and_lower
    (upper : UpperBoundTarget.{u, v})
    (lower : LowerBoundTarget.{u, v}) : KonigEdgeColoringTarget.{u, v} :=
  root_of_assembly checked_root_transport (assembly_of_upper_and_lower upper lower)

#check DegreeBound
#check BoundedSatzCTarget
#check UpperBoundTarget
#check LowerBoundTarget
#check RootTransportTarget
#check AssemblyTarget
#check assembly_of_upper_and_lower
#check expanded_of_assembly
#check checked_root_transport
#check root_of_assembly
#check root_of_upper_and_lower

#print axioms assembly_of_upper_and_lower
#print axioms expanded_of_assembly
#print axioms checked_root_transport
#print axioms root_of_assembly
#print axioms root_of_upper_and_lower

end Stage1Instances.THM_M_0861_Obligations
