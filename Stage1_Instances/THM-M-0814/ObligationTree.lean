import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0814 obligation composition harness

This module fixes exact interfaces for the two terminal mathematical products of the frozen
architecture.  Both products remain explicit premises.  The checked terms below validate only
child-to-parent composition; they do not prove max-flow/min-cut or close either child.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0814_Obligations

open Stage1Instances.THM_M_0814

universe uV uE

/-- A feasible flow whose value dominates every other feasible flow in the same network. -/
def IsMaximumFlow {V : Type uV} {E : Type uE}
    {G : Graph V E} {source sink : V} (capacity : E -> NNReal)
    (flow : Flow G source sink) : Prop :=
  IsFeasible capacity flow /\
    forall other : Flow G source sink,
      IsFeasible capacity other -> flowValue other <= flowValue flow

/-- The architecture's first exact terminal interface: maximum-flow attainment. -/
def MaximalFlowAttainment : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal),
      HasTerminals G source sink ->
      HasPositiveCapacities G capacity ->
        exists flow : Flow G source sink, IsMaximumFlow capacity flow

/-- Weak duality in the exact chain-flow/disconnecting-set representation. -/
def WeakDuality : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal)
    (flow : Flow G source sink) (cut : Finset E),
      IsFeasible capacity flow ->
      IsDisconnecting G source sink cut ->
        flowValue flow <= cutValue capacity cut

/-- The source proof's three lemmas produce a disconnecting set having the same value as any
selected maximal flow.  The universal minimum comparison is deliberately not hidden here. -/
def EqualCutForMaximalFlow : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal),
      HasTerminals G source sink ->
      HasPositiveCapacities G capacity ->
      forall flow : Flow G source sink,
        IsMaximumFlow capacity flow ->
          exists cut : Finset E,
            IsDisconnecting G source sink cut /\
              flowValue flow = cutValue capacity cut

/-- The second exact terminal interface: an equal cut for a maximal flow, strengthened to the
minimum-cut comparison by weak duality. -/
def CutCertificateForMaximalFlow : Prop :=
  forall (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal),
      HasTerminals G source sink ->
      HasPositiveCapacities G capacity ->
      forall flow : Flow G source sink,
        IsMaximumFlow capacity flow ->
          exists cut : Finset E,
            IsDisconnecting G source sink cut /\
            (forall other : Finset E,
              IsDisconnecting G source sink other ->
                cutValue capacity cut <= cutValue capacity other) /\
            flowValue flow = cutValue capacity cut

/-- Exact composition of weak duality with the equal-cut product. -/
theorem cutCertificate_compose
    (weakDuality : WeakDuality.{uV, uE})
    (equalCut : EqualCutForMaximalFlow.{uV, uE}) :
    CutCertificateForMaximalFlow.{uV, uE} := by
  intro V E _ _ G source sink capacity terminals positive flow maximal
  obtain ⟨cut, disconnecting, value_eq⟩ :=
    equalCut V E G source sink capacity terminals positive flow maximal
  refine ⟨cut, disconnecting, ?_, value_eq⟩
  intro other other_disconnecting
  rw [← value_eq]
  exact weakDuality V E G source sink capacity flow other
    maximal.1 other_disconnecting

/-- Root composition certificate.  Both exact terminal children are named and consumed. -/
theorem compose_root
    (maximumExists : MaximalFlowAttainment.{uV, uE})
    (cutCertificate : CutCertificateForMaximalFlow.{uV, uE}) :
    MaxFlowMinCutTarget.{uV, uE} := by
  intro V E _ _ G source sink capacity terminals positive
  obtain ⟨flow, feasible, maximal⟩ :=
    maximumExists V E G source sink capacity terminals positive
  obtain ⟨cut, disconnecting, minimum, value_eq⟩ :=
    cutCertificate V E G source sink capacity terminals positive flow
      ⟨feasible, maximal⟩
  exact ⟨flow, cut, feasible, disconnecting, maximal, minimum, value_eq⟩

/-- The exact terminal assembly is not a second semantic theorem; this identity certificate binds
the terminal node to the canonical root without duplicate proof credit. -/
theorem root_of_terminal
    (terminal : MaxFlowMinCutTarget.{uV, uE}) :
    MaxFlowMinCutTarget.{uV, uE} :=
  terminal

#check MaximalFlowAttainment
#check WeakDuality
#check EqualCutForMaximalFlow
#check CutCertificateForMaximalFlow
#check cutCertificate_compose
#check compose_root
#check root_of_terminal

assert_no_sorry cutCertificate_compose
assert_no_sorry compose_root
assert_no_sorry root_of_terminal

#print sorries cutCertificate_compose compose_root root_of_terminal
#print axioms cutCertificate_compose
#print axioms compose_root
#print axioms root_of_terminal

end Stage1Instances.THM_M_0814_Obligations
