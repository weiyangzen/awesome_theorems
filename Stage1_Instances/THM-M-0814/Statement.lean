import Mathlib.Algebra.BigOperators.Finsupp.Basic
import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Data.NNReal.Defs

/-!
# THM-M-0814: source-exact max-flow min-cut statement

This module formalizes the finite undirected, path-decomposed network used in Ford and
Fulkerson's 1956 Theorem 1. It states the theorem but contains no proof of it.
-/

namespace Stage1Instances.THM_M_0814

universe uV uE

/-- A non-self-intersecting source-to-sink chain in an undirected multigraph.

The arrays list `length + 1` distinct vertices and `length` distinct arcs; each listed arc links
its two consecutive vertices. Requiring positive length encodes the source/sink distinction used
in the source theorem.
-/
structure Chain {V : Type uV} {E : Type uE} (G : Graph V E) (source sink : V) where
  length : Nat
  positive : 0 < length
  /-- The source's ordered vertices, including both endpoints. -/
  vertex : Fin (length + 1) -> V
  /-- The source's ordered arcs. -/
  edge : Fin length -> E
  /-- A chain does not repeat a vertex. -/
  vertex_injective : Function.Injective vertex
  /-- A chain does not repeat an arc. -/
  edge_injective : Function.Injective edge
  /-- The first vertex is the distinguished source. -/
  starts : vertex 0 = source
  /-- The last vertex is the distinguished sink. -/
  ends : vertex (Fin.last length) = sink
  /-- Each listed arc joins its consecutive listed vertices. -/
  links : forall i : Fin length,
    G.IsLink (edge i) (vertex (Fin.castSucc i)) (vertex i.succ)

/-- A finite collection of nonnegative chain-flow values.

`Finsupp` preserves the paper's collection semantics: only finitely many chains have nonzero
weight, while repeated copies are immaterial because their weights combine additively.
-/
abbrev Flow {V : Type uV} {E : Type uE} (G : Graph V E) (source sink : V) :=
  Chain G source sink →₀ NNReal

/-- The source and sink are distinct vertices of the graph. -/
def HasTerminals {V : Type uV} {E : Type uE}
    (G : Graph V E) (source sink : V) : Prop :=
  source ∈ G.vertexSet /\ sink ∈ G.vertexSet /\ source ≠ sink

/-- Every graph arc has the strictly positive capacity required by the 1956 source. -/
def HasPositiveCapacities {V : Type uV} {E : Type uE}
    (G : Graph V E) (capacity : E -> NNReal) : Prop :=
  forall arc : E, arc ∈ G.edgeSet -> 0 < capacity arc

/-- The total amount of a path-decomposed flow using an arc. -/
noncomputable def arcLoad {V : Type uV} {E : Type uE}
    {G : Graph V E} {source sink : V} (flow : Flow G source sink) (arc : E) : NNReal :=
  by
    classical
    exact flow.sum fun chain value =>
      if arc ∈ Finset.univ.image chain.edge then value else 0

/-- The value of a path-decomposed flow is the sum of its component values. -/
noncomputable def flowValue {V : Type uV} {E : Type uE}
    {G : Graph V E} {source sink : V} (flow : Flow G source sink) : NNReal :=
  flow.sum fun _ value => value

/-- A flow is feasible when the load on every graph arc is bounded by its capacity. -/
noncomputable def IsFeasible {V : Type uV} {E : Type uE}
    {G : Graph V E} {source sink : V} (capacity : E -> NNReal)
    (flow : Flow G source sink) : Prop :=
  forall arc : E, arc ∈ G.edgeSet -> arcLoad flow arc <= capacity arc

/-- A disconnecting set consists of graph arcs and meets every source-to-sink chain. -/
noncomputable def IsDisconnecting {V : Type uV} {E : Type uE}
    (G : Graph V E) (source sink : V) (cut : Finset E) : Prop :=
  (forall arc : E, arc ∈ cut -> arc ∈ G.edgeSet) /\
  forall chain : Chain G source sink, exists i : Fin chain.length, chain.edge i ∈ cut

/-- The value of a disconnecting set is the sum of its arc capacities. -/
noncomputable def cutValue {E : Type uE} (capacity : E -> NNReal) (cut : Finset E) : NNReal :=
  cut.sum capacity

/-- Ford-Fulkerson's 1956 minimal-cut theorem, in its original finite undirected chain-flow form.

There is a maximal feasible flow and a minimum disconnecting set, and their values agree.
-/
def MaxFlowMinCutTarget : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal),
      HasTerminals G source sink ->
      HasPositiveCapacities G capacity ->
        exists flow : Flow G source sink, exists disconnectingSet : Finset E,
          IsFeasible capacity flow /\
          IsDisconnecting G source sink disconnectingSet /\
          (forall other : Flow G source sink,
            IsFeasible capacity other -> flowValue other <= flowValue flow) /\
          (forall other : Finset E,
            IsDisconnecting G source sink other ->
              cutValue capacity disconnectingSet <= cutValue capacity other) /\
          flowValue flow = cutValue capacity disconnectingSet

/-- A source-shaped spelling of the canonical target with its premises sequenced explicitly. -/
def ExpandedTarget : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal),
      HasTerminals G source sink ->
      HasPositiveCapacities G capacity ->
        exists flow : Flow G source sink, exists disconnectingSet : Finset E,
          IsFeasible capacity flow /\
          IsDisconnecting G source sink disconnectingSet /\
          (forall other : Flow G source sink,
            IsFeasible capacity other -> flowValue other <= flowValue flow) /\
          (forall other : Finset E,
            IsDisconnecting G source sink other ->
              cutValue capacity disconnectingSet <= cutValue capacity other) /\
          flowValue flow = cutValue capacity disconnectingSet

/-- Checked direct respelling of the canonical proposition. -/
theorem maxFlowMinCutTarget_iff_expanded :
    MaxFlowMinCutTarget.{uV, uE} <-> ExpandedTarget.{uV, uE} :=
  Iff.rfl

/-! Structural mutations used only by the statement-identity checker. -/

/-- Removed-hypothesis mutation: positive capacities are no longer required. -/
def mutationRemovedPositiveCapacity : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal),
      HasTerminals G source sink ->
        exists flow : Flow G source sink, exists disconnectingSet : Finset E,
          IsFeasible capacity flow /\
          IsDisconnecting G source sink disconnectingSet /\
          (forall other : Flow G source sink,
            IsFeasible capacity other -> flowValue other <= flowValue flow) /\
          (forall other : Finset E,
            IsDisconnecting G source sink other ->
              cutValue capacity disconnectingSet <= cutValue capacity other) /\
          flowValue flow = cutValue capacity disconnectingSet

/-- Changed-domain mutation: capacities and component values use natural numbers. -/
def mutationNaturalCapacityDomain : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> Nat),
      HasTerminals G source sink ->
      (forall arc : E, arc ∈ G.edgeSet -> 0 < capacity arc) ->
        exists disconnectingSet : Finset E, IsDisconnecting G source sink disconnectingSet

/-- Changed-scope mutation: one network is existential rather than every network being universal. -/
def mutationExistentialNetwork : Prop :=
  exists V : Type uV, exists E : Type uE, exists G : Graph V E,
    exists source sink : V, HasTerminals G source sink

/-- Boundary mutation: networks with no source-to-sink chain are excluded. -/
def mutationRequiresSourceSinkChain : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal),
      HasTerminals G source sink ->
      Nonempty (Chain G source sink) ->
      HasPositiveCapacities G capacity ->
        exists flow : Flow G source sink, exists disconnectingSet : Finset E,
          IsFeasible capacity flow /\
          IsDisconnecting G source sink disconnectingSet /\
          (forall other : Flow G source sink,
            IsFeasible capacity other -> flowValue other <= flowValue flow) /\
          (forall other : Finset E,
            IsDisconnecting G source sink other ->
              cutValue capacity disconnectingSet <= cutValue capacity other) /\
          flowValue flow = cutValue capacity disconnectingSet

#check_failure
  (rfl : MaxFlowMinCutTarget.{uV, uE} = mutationRemovedPositiveCapacity.{uV, uE})
#check_failure
  (rfl : MaxFlowMinCutTarget.{uV, uE} = mutationNaturalCapacityDomain.{uV, uE})
#check_failure
  (rfl : MaxFlowMinCutTarget.{uV, uE} = mutationExistentialNetwork.{uV, uE})
#check_failure
  (rfl : MaxFlowMinCutTarget.{uV, uE} = mutationRequiresSourceSinkChain.{uV, uE})

#print axioms maxFlowMinCutTarget_iff_expanded

end Stage1Instances.THM_M_0814

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0814.MaxFlowMinCutTarget
