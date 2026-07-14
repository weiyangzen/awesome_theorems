import Proof
import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1007 same-worker differential validation

This module rechecks the proof phase's exact sufficiency declaration at the
frozen obligation type and also reconstructs that direction from explicit
large-jump transport and centered-series premises. The bounded independent-
series necessity direction remains absent, so this module does not prove the
canonical biconditional root. The explicit-premise reconstruction is a same-
worker differential probe, not distinct-runner independent verification.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1007.Validation

universe u

/-- Exact-type probe for the proof phase's closed sufficiency direction. -/
theorem exactSufficiencyTypeProbe :
    Stage1Instances.THM_M_1007.ObligationTree.Sufficiency.{u} :=
  Stage1Instances.THM_M_1007.Proof.obligationTree_sufficiency

/-- Differential composition of the two implications needed by the exact
three-series sufficiency direction. Both mathematical engines remain explicit
premises, which prevents this validation probe from manufacturing root proof
credit. -/
theorem sufficiencyFromExplicitBridges
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real) (hc : 0 < c)
    (hX : forall n, Measurable (X n)) (hIndep : iIndepFun X mu)
    (largeJumpTransport :
      Summable (fun n => mu.real {omega | c < |X n omega|}) ->
        (∀ᵐ omega ∂mu,
          Stage1Instances.THM_M_1007.SeriesConverges
            (fun n => Stage1Instances.THM_M_1007.truncate c (X n) omega)) ->
        ∀ᵐ omega ∂mu,
          Stage1Instances.THM_M_1007.SeriesConverges (fun n => X n omega))
    (centeredSeries :
      (forall n, Measurable (X n)) -> iIndepFun X mu -> 0 < c ->
        Stage1Instances.THM_M_1007.SeriesConverges (fun n =>
          integral mu (Stage1Instances.THM_M_1007.truncate c (X n))) ->
        Summable (fun n =>
          variance (Stage1Instances.THM_M_1007.truncate c (X n)) mu) ->
        ∀ᵐ omega ∂mu,
          Stage1Instances.THM_M_1007.SeriesConverges
            (fun n => Stage1Instances.THM_M_1007.truncate c (X n) omega))
    (conditions :
      Summable (fun n => mu.real {omega | c < |X n omega|}) /\
      Stage1Instances.THM_M_1007.SeriesConverges (fun n =>
        integral mu (Stage1Instances.THM_M_1007.truncate c (X n))) /\
      Summable (fun n =>
        variance (Stage1Instances.THM_M_1007.truncate c (X n)) mu)) :
    ∀ᵐ omega ∂mu,
      Stage1Instances.THM_M_1007.SeriesConverges (fun n => X n omega) := by
  obtain ⟨hjump, hmean, hvar⟩ := conditions
  exact largeJumpTransport hjump (centeredSeries hX hIndep hc hmean hvar)

assert_no_sorry Stage1Instances.THM_M_1007.Proof.obligationTree_sufficiency
assert_no_sorry exactSufficiencyTypeProbe
assert_no_sorry sufficiencyFromExplicitBridges
#print sorries Stage1Instances.THM_M_1007.Proof.obligationTree_sufficiency
#print sorries exactSufficiencyTypeProbe
#print sorries sufficiencyFromExplicitBridges
#print axioms Stage1Instances.THM_M_1007.Proof.obligationTree_sufficiency
#print axioms exactSufficiencyTypeProbe
#print axioms sufficiencyFromExplicitBridges

end Stage1Instances.THM_M_1007.Validation
