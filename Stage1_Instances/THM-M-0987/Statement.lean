import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-0987: exact one-dimensional i.i.d. central limit statement

This module freezes the statement boundary only. It deliberately does not prove
the target or give proof credit to the historical Stage1 wrapper.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Finset
open scoped Real Topology

namespace Stage1Instances.THM_M_0987

universe uOmega uOmega'

/-- The exact one-dimensional real-valued i.i.d. CLT branch selected from the
theorem-family wording at intake. The limiting variance is allowed to be zero. -/
def CentralLimitTheoremTarget : Prop :=
  forall (Omega : Type uOmega) (Omega' : Type uOmega')
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat -> Omega -> Real) (Y : Omega' -> Real),
      HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' ->
      MemLp (X 0) 2 P ->
      iIndepFun X P ->
      (forall i : Nat, IdentDistrib (X i) (X 0) P P) ->
      TendstoInDistribution
        (fun (n : Nat) omega =>
          (Real.sqrt (n : Real))⁻¹ *
            ((∑ k ∈ Finset.range n, X k omega) - (n : Real) * P[X 0]))
        atTop Y (fun _ : Nat => P) P'

/-- A local transcription of the type of the pinned mathlib declaration. -/
def PinnedMathlibSourceShape : Prop :=
  forall (Omega : Type uOmega) (Omega' : Type uOmega')
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat -> Omega -> Real) (Y : Omega' -> Real),
      HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' ->
      MemLp (X 0) 2 P ->
      iIndepFun X P ->
      (forall i : Nat, IdentDistrib (X i) (X 0) P P) ->
      TendstoInDistribution
        (fun (n : Nat) omega =>
          (Real.sqrt (n : Real))⁻¹ *
            ((∑ k ∈ Finset.range n, X k omega) - (n : Real) * P[X 0]))
        atTop Y (fun _ : Nat => P) P'

/-- The canonical target is definitionally the locally transcribed pinned type. -/
theorem target_iff_pinnedMathlibSourceShape :
    CentralLimitTheoremTarget.{uOmega, uOmega'} <->
      PinnedMathlibSourceShape.{uOmega, uOmega'} := by
  rfl

-- Separately elaborated structural mutations; none is credited as equivalent.
def mutationRemovedIndependence : Prop :=
  forall (Omega : Type uOmega) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (X : Nat -> Omega -> Real), MemLp (X 0) 2 P -> True

def mutationChangedDomainToNatural : Prop :=
  forall (Omega : Type uOmega) [MeasurableSpace Omega]
    (_X : Nat -> Omega -> Nat), True

def mutationChangedBinderScope : Prop :=
  forall (Omega : Type uOmega) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (X : Nat -> Omega -> Real),
      exists _Y : Omega -> Real, MemLp (X 0) 2 P -> True

def mutationExcludedZeroVariance : Prop :=
  forall (Omega : Type uOmega) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (X : Nat -> Omega -> Real), variance (X 0) P != 0 -> True

/-- The finite sum at the `n = 0` boundary is zero; the target does not discard it. -/
theorem centeredSum_zero {Omega : Type uOmega} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Omega -> Real) (omega : Omega) :
    (∑ k ∈ Finset.range 0, X k omega) - (0 : Real) * P[X 0] = 0 := by
  simp

end Stage1Instances.THM_M_0987

#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub

set_option pp.explicit true in
#print Stage1Instances.THM_M_0987.CentralLimitTheoremTarget
