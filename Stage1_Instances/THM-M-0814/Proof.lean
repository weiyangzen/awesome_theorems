import ObligationTree
import Mathlib.Data.Finsupp.Order
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0814 partial proof execution

This module proves weak duality for the exact frozen chain-flow representation and gives the
no-chain boundary body.  The frozen universal maximum-flow-attainment and equal-cut interfaces
remain explicit premises; no checked case split connects the boundary body to the exact root here.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0814_Obligations

open Stage1Instances.THM_M_0814
universe uV uE

/-- Every feasible chain flow has value at most that of every disconnecting arc set.

For each supported chain, choose one cut arc met by that chain.  Its component value is at most
the sum of that same value over all cut arcs used by the chain.  Commuting the two finite sums turns
the resulting expression into the sum of cut-arc loads, which feasibility bounds by capacity.
The argument deliberately permits a chain to cross the cut more than once.
-/
theorem weakDuality_proof : WeakDuality.{uV, uE} := by
  intro V E _ _ G source sink capacity flow cut feasible disconnecting
  classical
  change flow.sum (fun _ value => value) <= cut.sum capacity
  calc
    flow.sum (fun _ value => value)
        <= flow.sum (fun chain value =>
          cut.sum fun arc => if arc ∈ Finset.univ.image chain.edge then value else 0) := by
      apply Finsupp.sum_le_sum
      intro chain _
      obtain ⟨i, hi⟩ := disconnecting.2 chain
      have hmem : chain.edge i ∈ cut := hi
      calc
        flow chain = if chain.edge i ∈ Finset.univ.image chain.edge then flow chain else 0 := by
          simp
        _ <= cut.sum (fun arc =>
            if arc ∈ Finset.univ.image chain.edge then flow chain else 0) := by
          have hnonneg : forall arc : E, arc ∈ cut ->
              (0 : NNReal) <=
                if arc ∈ Finset.univ.image chain.edge then flow chain else 0 := by
            intro arc _
            positivity
          exact Finset.single_le_sum hnonneg hmem
    _ = cut.sum (fun arc => arcLoad flow arc) := by
      rw [Finsupp.sum_finsetSum_comm]
      apply Finset.sum_congr rfl
      intro _ _
      rfl
    _ <= cut.sum capacity := by
      apply Finset.sum_le_sum
      intro arc harc
      exact feasible arc (disconnecting.1 arc harc)

/-- Exact witnesses for the frozen boundary branch with no source-to-sink chain.

Every flow is the zero `Finsupp`, the empty arc set disconnects vacuously, and both values are zero.
This theorem adds no terminal, positivity, or path-existence assumption to the canonical root.
-/
theorem noChain_case
    (V : Type uV) (E : Type uE) [Fintype V] [Fintype E]
    (G : Graph V E) (source sink : V) (capacity : E -> NNReal)
    (noChain : ¬ Nonempty (Chain G source sink)) :
    exists flow : Flow G source sink, exists disconnectingSet : Finset E,
      IsFeasible capacity flow /\
      IsDisconnecting G source sink disconnectingSet /\
      (forall other : Flow G source sink,
        IsFeasible capacity other -> flowValue other <= flowValue flow) /\
      (forall other : Finset E,
        IsDisconnecting G source sink other ->
          cutValue capacity disconnectingSet <= cutValue capacity other) /\
      flowValue flow = cutValue capacity disconnectingSet := by
  classical
  letI : IsEmpty (Chain G source sink) := ⟨fun chain => noChain ⟨chain⟩⟩
  refine ⟨0, ∅, ?_, ?_, ?_, ?_, ?_⟩
  · intro arc _
    simp [arcLoad]
  · constructor
    · simp
    · exact fun chain => isEmptyElim chain
  · intro other _
    rw [Subsingleton.elim other 0]
  · intro other _
    simp [cutValue]
  · simp [flowValue, cutValue]

/-- Local weak duality discharges one child of the exact conditional cut-certificate interface. -/
theorem cutCertificate_of_equalCut
    (equalCut : EqualCutForMaximalFlow.{uV, uE}) :
    CutCertificateForMaximalFlow.{uV, uE} :=
  cutCertificate_compose weakDuality_proof equalCut

/-- After this proof phase, the exact root needs only attainment and the source equal-cut product. -/
theorem root_of_maximalFlowAttainment_and_equalCut
    (maximumExists : MaximalFlowAttainment.{uV, uE})
    (equalCut : EqualCutForMaximalFlow.{uV, uE}) :
    MaxFlowMinCutTarget.{uV, uE} :=
  compose_root maximumExists (cutCertificate_of_equalCut equalCut)

assert_no_sorry weakDuality_proof
assert_no_sorry noChain_case
assert_no_sorry cutCertificate_of_equalCut
assert_no_sorry root_of_maximalFlowAttainment_and_equalCut

#print sorries weakDuality_proof noChain_case cutCertificate_of_equalCut
  root_of_maximalFlowAttainment_and_equalCut
#print axioms weakDuality_proof
#print axioms noChain_case
#print axioms cutCertificate_of_equalCut
#print axioms root_of_maximalFlowAttainment_and_equalCut

end Stage1Instances.THM_M_0814_Obligations
