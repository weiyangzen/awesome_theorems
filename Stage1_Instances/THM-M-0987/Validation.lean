import Statement

/-!
# THM-M-0987 independent validation probe

This module independently transcribes the frozen target and applies the pinned
mathlib theorem without importing the repository proof module. It is a
same-workspace validation probe, not a distinct-runner attestation.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Finset
open scoped Real Topology

namespace Stage1Instances.THM_M_0987.Validation

universe uOmega uOmega'

/-- Independent exact-type replay of the selected real-valued i.i.d. CLT. -/
theorem independentlyReconstructedTarget :
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
          atTop Y (fun _ : Nat => P) P' := by
  intro Omega Omega' _ _ P P' _ _ X Y hY hL2 hIndep hIdent
  exact ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
    hY hL2 hIndep hIdent

/-- The independent transcription is definitionally the frozen target. -/
theorem independentTarget_iff_frozenTarget :
    (CentralLimitTheoremTarget.{uOmega, uOmega'}) <->
      (forall (Omega : Type uOmega) (Omega' : Type uOmega')
        [MeasurableSpace Omega] [MeasurableSpace Omega']
        (P : Measure Omega) (P' : Measure Omega')
        [IsProbabilityMeasure P] [IsProbabilityMeasure P']
        (X : Nat -> Omega -> Real) (Y : Omega' -> Real),
          HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' ->
          MemLp (X 0) 2 P -> iIndepFun X P ->
          (forall i : Nat, IdentDistrib (X i) (X 0) P P) ->
          TendstoInDistribution
            (fun (n : Nat) omega =>
              (Real.sqrt (n : Real))⁻¹ *
                ((∑ k ∈ Finset.range n, X k omega) - (n : Real) * P[X 0]))
            atTop Y (fun _ : Nat => P) P') := by
  rfl

#print axioms independentlyReconstructedTarget
#print axioms independentTarget_iff_frozenTarget
#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub

end Stage1Instances.THM_M_0987.Validation
