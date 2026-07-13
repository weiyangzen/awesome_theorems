import Mathlib.Algebra.BigOperators.Finsupp.Basic
import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Data.NNReal.Defs
import Mathlib.Topology.Order.Compact

/-!
# THM-M-0814 anchor-audit probes

This module elaborates a parameterized copy of the frozen proposition's binder/conclusion shape
and checks the closest pinned mathlib substrate. No pinned dependency declares a network-flow
theorem, so this file adds no proof of the target. The immutable external Atlas candidate is
intentionally not imported: it is outside the local dependency closure, has a materially different
directed-flow statement, and its license and trust boundaries require separate review.
-/

namespace Stage1Instances.THM_M_0814_AnchorAudit

universe uV uE

/-- Parameterized shape probe for the statement gate's canonical proposition.

`Statement.lean` is separately re-elaborated and fingerprinted by the checker. This definition is
not credited as a checked equality or transport to that declaration. -/
def ExactTarget
    (HasTerminals : forall {V : Type uV} {E : Type uE}, Graph V E -> V -> V -> Prop)
    (HasPositiveCapacities :
      forall {V : Type uV} {E : Type uE}, Graph V E -> (E -> NNReal) -> Prop)
    (Flow : forall {V : Type uV} {E : Type uE}, Graph V E -> V -> V -> Type (max uV uE))
    (IsFeasible : forall {V : Type uV} {E : Type uE} {G : Graph V E}
      {source sink : V}, (E -> NNReal) -> Flow G source sink -> Prop)
    (IsDisconnecting : forall {V : Type uV} {E : Type uE},
      Graph V E -> V -> V -> Finset E -> Prop)
    (flowValue : forall {V : Type uV} {E : Type uE} {G : Graph V E}
      {source sink : V}, Flow G source sink -> NNReal)
    (cutValue : forall {E : Type uE}, (E -> NNReal) -> Finset E -> NNReal) : Prop :=
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

#check Graph
#check Graph.IsLink
#check Graph.Inc
#check Graph.IsLink.edge_mem
#check Finsupp.sum
#check Finset.sum
#check NNReal
#check Real.toNNReal
#check Real.coe_toNNReal
#check IsCompact.exists_isMinOn
#check IsCompact.exists_isMaxOn

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0814_AnchorAudit
