import Statement

/-!
# THM-M-1009 independent validation probe

This module deliberately does not import `Proof.lean` or `ObligationTree.lean`.
It reconstructs the final analytic assembly from independently supplied
interfaces, so validation can check the frozen root without calling the local
root theorem.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

universe u

namespace Stage1Instances.THM_M_1009.Validation

open Stage1Instances.THM_M_1009

/-- Independent composition of the tail bound and tail-measure convergence.
The two premises expose the substantive proof interfaces instead of importing
the proof-phase implementation. -/
theorem independentRootFromInterfaces
    (tailBound : forall (Omega : Type u) [MeasurableSpace Omega]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (A : Nat -> Set Omega),
        (forall n : Nat, MeasurableSet (A n)) ->
          Tendsto (partialEventMass mu A) atTop atTop ->
            forall m : Nat,
              Filter.limsup (eventMassRatio mu A) atTop <=
                mu.real (⋃ k : Nat, A (m + k)))
    (tailLimit : forall (Omega : Type u) [MeasurableSpace Omega]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (A : Nat -> Set Omega),
        (forall n : Nat, MeasurableSet (A n)) ->
          Tendsto (fun m => mu.real (⋃ k : Nat, A (m + k))) atTop
            (nhds (mu.real (limsup A atTop)))) :
    ErdosRenyiLowerBoundTarget.{u} := by
  intro Omega _ mu _ A hA hdiv
  exact ge_of_tendsto' (tailLimit Omega mu A hA) (tailBound Omega mu A hA hdiv)

/-- Exact-type probe for the canonical frozen target. -/
theorem exactTargetProbe
    (h : ErdosRenyiLowerBoundTarget.{u}) : ErdosRenyiLowerBoundTarget.{u} := h

#check independentRootFromInterfaces
#check (exactTargetProbe :
  ErdosRenyiLowerBoundTarget.{u} -> ErdosRenyiLowerBoundTarget.{u})
#print axioms independentRootFromInterfaces
#print axioms exactTargetProbe

end Stage1Instances.THM_M_1009.Validation
